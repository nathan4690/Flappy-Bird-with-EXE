"""
Flappy bird remake
Made by Nhan (nathan)

-----------------------
This is my second ever long project(more than 500 lines of code) that have tkinter included.
A version of Flappy Bird, have fun!

-----------------------
NOTES:
- You can click any keyboard button or click your mouse in the game window to make the bird flap.
- Medals are calculated with score like the following:
  + Score > 29: Gold
  + 30 > Score > 19: Silver
  + 20 > Score > 9: Bronze
  + 10 > Score: No medal
- Best score is compared with the all best score in the leaderboard.
- If you don't type your name in the ask dialog or exit it, the default name will be 'Anonymous'.
"""

import pygame,tkinter
from random import randint
from PIL import Image
from math import ceil, floor
from tkinter import ttk

pygame.init()
screen_width = 300
screen_height = 500
RESOURCESPATH = "Resources/"
ENDPATH = "-removebg-preview.png"

# Init resources
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy bird")
screen.fill((255,255,255))

pipePic = pygame.image.load(RESOURCESPATH + "pipe.png")
pipeSize = (Image.open(RESOURCESPATH+"pipe.png").width,Image.open(RESOURCESPATH+"pipe.png").height)

ratio = Image.open(RESOURCESPATH+"ground.png").width // 450
groundPic = pygame.image.load(RESOURCESPATH + "ground.png")
groundSize = (Image.open(RESOURCESPATH+"ground.png").width // ratio,Image.open(RESOURCESPATH+"ground.png").height // ratio)
groundPic = pygame.transform.scale(groundPic,(960 // ratio,90 // ratio))

ratio2 = Image.open(RESOURCESPATH+"sky.png").height / (500-(ceil(groundSize[1])))
skyPic = pygame.image.load(RESOURCESPATH + "sky.png")
skySize = (Image.open(RESOURCESPATH+"sky.png").width / ratio2,Image.open(RESOURCESPATH+"sky.png").height /  ratio2)
skyPic = pygame.transform.scale(skyPic,(ceil(skySize[0])+3,ceil(skySize[1])+3))

ratio3 = Image.open(RESOURCESPATH+"sky.png").width / 20
scorepics = []
for x in range(10):
    scorepic = pygame.image.load(RESOURCESPATH+str(x)+".png")
    scoresizey = Image.open(RESOURCESPATH+str(x)+".png").height -20
    scorepic = pygame.transform.scale(scorepic,(20,scoresizey))
    scorepics.append(scorepic)

scorepicsend = []
for x in range(10):
    scorepicend = pygame.image.load(RESOURCESPATH+str(x)+".png")
    scoreendsizey = Image.open(RESOURCESPATH+str(x)+".png").height -30
    scorepicend = pygame.transform.scale(scorepicend,(14,scoreendsizey))
    scorepicsend.append(scorepicend)

textpics = []
textsize = ([250,75],[500,250])
texts = ["FlappyBirdStartText.png","gameOverText"+ENDPATH]
for y in range(2):
    ratio4 = Image.open(RESOURCESPATH+texts[y]).width // 100
    textpic = pygame.image.load(RESOURCESPATH+texts[y])
    textpic = pygame.transform.scale(textpic,(textsize[y][0],textsize[y][1]))
    textpics.append(textpic)

buttonpics = []
buttonsName = ["StartButton"+ENDPATH,"leaderboard-button"+ENDPATH]
ratio5 = [Image.open(RESOURCESPATH+"StartButton"+ENDPATH).width // 100,Image.open(RESOURCESPATH+"leaderboard-button"+ENDPATH).width // 100]
for x in range(2):
    buttonpic = pygame.image.load(RESOURCESPATH+buttonsName[x])
    buttonsize = Image.open(RESOURCESPATH+buttonsName[x]).height // ratio5[x]
    buttonpic = pygame.transform.scale(buttonpic,(100,buttonsize))
    buttonpics.append(buttonpic)

tutorialPic = pygame.image.load(RESOURCESPATH+"tutorial-click"+ENDPATH)
tutorialPic = pygame.transform.scale(tutorialPic,(110,80))

endBoardSize = (288,352)
endBoardPic = pygame.image.load(RESOURCESPATH+"endboard"+ENDPATH)
endBoardPic = pygame.transform.scale(endBoardPic,endBoardSize)

medalpics = []
medalsName = ["bronze"+ENDPATH,"silver"+ENDPATH,"gold"+ENDPATH]
rat6  = 50
ratio6 = [Image.open(RESOURCESPATH+medalsName[0]).width / rat6,Image.open(RESOURCESPATH+medalsName[1]).width / rat6,Image.open(RESOURCESPATH+medalsName[2]).width / rat6]
ratio6 = list(map(ceil,ratio6))
for x in range(3):
    medalpic = pygame.image.load(RESOURCESPATH+medalsName[x])
    medalsize = Image.open(RESOURCESPATH+medalsName[x]).height
    medalpic = pygame.transform.scale(medalpic,(rat6,rat6))
    medalpics.append(medalpic)

class Bird():
    def __init__(self,x,y) -> None: 
        self.reset(x, y)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.rotdir = 0
        self.predir = 180
        self.dir = 180
        self.yvel = 0
        self.mod = 30
        self.birdPic = pygame.image.load(RESOURCESPATH + "bird" + ENDPATH)
        self.birdPic = pygame.transform.scale(self.birdPic,(42,24))
        self.rotatedimg = self.birdPic
        self.rect = pygame.Rect(self.x,self.y,self.mod+3,self.mod-3)

    def draw(self):
        self.dir = 180 + (self.yvel * 2)
        self.rotdir = 0
        while not (self.rotdir == self.dir - 180):
            if self.rotdir <= self.dir - 180: 
                self.rotdir += 1
            else: 
                self.rotdir -= 1

        self.rotatedimg = pygame.transform.rotate(self.birdPic,self.rotdir)
        self.rect.topleft = (self.x+5,self.y)
        screen.blit(self.rotatedimg,(self.x,self.y))
    
    def physics(self):
        self.yvel -= 1
        self.y -= self.yvel

    def flap(self): 
        self.yvel = 10
        self.predir = self.dir + 1

class Pipe():
    def __init__(self,x,y):
        self.reset(x, y)

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.rect1 = pygame.Rect(0,0,int(pipeSize[0]),int(pipeSize[1]) - 200)
        self.rect2 = pygame.Rect(0,0,int(pipeSize[0]),int(pipeSize[1]) - 200)
        self.rect1.center = int(pipeSize[0]) // 2,int(pipeSize[1]) // 2
        self.vel = 5
    
    def draw(self):
        self.rect1.center = (self.x + int(pipeSize[0]) // 2,self.y + int(pipeSize[1]) // 2 -310)
        self.rect2.center = (self.x + int(pipeSize[0]) // 2,self.y + int(pipeSize[1]) // 2 + 310)
        screen.blit(pipePic,(self.x,self.y))
        
    def move(self): self.x -= self.vel

class Ground():
    def __init__(self,x,y):
        self.reset(x, y)

    def draw(self):
        self.rect.topleft = (self.x,self.y)
        screen.blit(groundPic,[self.x,self.y])

    def move(self): self.x -= self.vel

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.vel = 5
        self.rect = pygame.Rect(0,0,int(groundSize[0]),int(groundSize[1]))

class Sky():
    def __init__(self,x,y):
        self.reset(x, y)

    def draw(self):
        self.rect.topleft = (self.x,self.y)
        screen.blit(skyPic,[self.x,self.y])

    def move(self): self.x -= self.vel

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.vel = 3
        self.rect = pygame.Rect(0,0,int(groundSize[0]),int(groundSize[1]))

class Score():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y 
        self.scorelen = len(str(score))

    def draw(self):
        self.scorelen = len(str(score))
        for x in range(self.scorelen):
            screen.blit(scorepics[int(str(score)[x])],(self.x - self.scorelen*25 // 2 + x*25,self.y))

class Text():
    def __init__(self,startx,starty,endx,endy):
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy

    def drawStart(self):
        screen.blit(textpics[0],(self.startx,self.starty))

    def drawEnd(self):
        screen.blit(textpics[1],(self.endx,self.endy))

class Button():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.buttonsizey = Image.open(RESOURCESPATH+buttonsName[0]).height // ratio5[0]
        self.rectStart = pygame.Rect(self.x,self.y,100,self.buttonsizey)
        self.buttonsizey = Image.open(RESOURCESPATH+buttonsName[1]).height // ratio5[1]
        self.rectLeader = pygame.Rect(self.x,self.y,100,self.buttonsizey)

    def draw(self):
        screen.blit(buttonpics[0],(self.x,self.y))
        screen.blit(buttonpics[1],(200 - self.x,self.y))
        self.rectStart.topleft = (self.x,self.y)
        self.rectLeader.topleft = (200-self.x,self.y)

class Tutorial():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(tutorialPic,(self.x,self.y))

class EndFac():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.score = "0"
        self.medal = 0

    def drawboard(self):
        screen.blit(endBoardPic,(self.x,self.y))

    def drawMedal(self,score):
        self.medal = floor(score / 10)
        if self.medal > 3:
            self.medal = 3

        if not self.medal == 0:
            screen.blit(medalpics[self.medal-1],(self.x+52,self.y+157))

    def drawScore(self,score):
        self.score = str(score)
        for i in range(-1,(len(self.score)*(-1))-1,-1):
            screen.blit(scorepicsend[int(self.score[i])],(self.x+220+(i+1)*15,self.y+155))
        
        with open(RESOURCESPATH+"leaderboard.txt") as showBest:
            b = showBest.readlines()[1]
        self.score = b.rstrip("\n")

        for i in range(-1,(len(self.score)*(-1))-1,-1):
            screen.blit(scorepicsend[int(self.score[i])],(self.x+220+(i+1)*15,self.y+200))

def showLeaderboard():
    leader = tkinter.Tk()
    leader.geometry("400x200")
    leader.title("Top 5 Flappy Bird Scores")
    leader.resizable(False,False)

    with open(RESOURCESPATH+"leaderboard.txt") as leaderin:
        leaders = [s.strip("\n") for s in leaderin.readlines()]
    
    leads = []
    if len(leaders) > 0:
        for lead in range(len(leaders)-1,-1,-2):
            leads.insert(0,((lead//2)+1,leaders[lead-1],leaders[lead]))

    columns = ("#1","#2","#3")
    leaderboard = ttk.Treeview(leader,columns=columns,show="headings")
    leaderboard.column("#1",width=100)
    leaderboard.column("#2",minwidth=200,width=200)
    leaderboard.column("#3",width=100)
    leaderboard.heading("#1",text="Ranking")
    leaderboard.heading("#2",text="Player")
    leaderboard.heading("#3",text="Score")
    
    for lead in leads:
        leaderboard.insert("",tkinter.END,values=lead)

    leaderboard.pack()
    leader.mainloop()

def setname(name):
    global myname
    myname = name.get()
    askforname.destroy()

# Define variables
pipestart = -250
pipeend = 0
flappy = Bird(50,200)
pygame.display.set_icon(flappy.birdPic)

pipe1 = Pipe(300,randint(pipestart,pipeend))
pipe2 = Pipe(300,randint(pipestart,pipeend))

ground1 = Ground(0,500-(int(groundSize[1])))
ground2 = Ground(300,ground1.y)
ground1move = True
ground2move = False

sky1 = Sky(0,0)
sky2 = Sky(300,0)
sky1move = True
sky2move = False

pipe1move = True
pipe2move = False

flappyText = Text(150-(textsize[0][0] // 2),100,150-(textsize[1][0] // 2),00)

tut = Tutorial(90,200)

flappyButtons = Button(25,300)

endFacility = EndFac(150 - endBoardSize[0]//2,50)
maxX = 51
minX = 49
global done,lose,score,startGame,added,startTut
startTut = False
score = 0
scoreMark = Score(150,50)
added = False
startGame = False
lose = False
done = False
flap = False
clock = pygame.time.Clock()

while not done:
    clock.tick(30)
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type in[pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN] and startGame:
            flap = True
        if (not startGame) and flappyButtons.rectStart.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            startTut = True
            added = False
        if (not startGame) and flappyButtons.rectLeader.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            showLeaderboard()
        if (not startGame) and startTut and event.type in [pygame.KEYDOWN,pygame.MOUSEBUTTONDOWN] and not(flappyButtons.rectStart.collidepoint(pygame.mouse.get_pos())):
            flap = True
            startTut = False
            startGame = True

    # The game starts here
    # Not yet split all of these codes to a function because of scopes
    # Game Over
    if startGame:
        if lose:
            startGame = False
            while lose:
                clock.tick(30)
                screen.fill((255,255,255))
                sky1.draw()
                sky2.draw()
                pipe1.draw()
                pipe2.draw()
                flappy.draw()
                ground1.draw()
                ground2.draw()
                flappyButtons.draw()
                flappyText.drawEnd()
                endFacility.drawboard()
                endFacility.drawMedal(score)
                endFacility.drawScore(score)
                if not (flappy.rect.colliderect(ground1.rect) == 1 or flappy.rect.colliderect(ground2.rect) == 1):
                    flappy.dir = 90
                    flappy.physics()

                if(flappy.rect.colliderect(ground1.rect) == 1 or flappy.rect.colliderect(ground2.rect) == 1):
                    clock.tick(60)
                    while (flappy.y >= 475-(int(groundSize[1]))):
                        flappy.y -= 1
                    clock.tick(30)
                    flappy.yvel = 0

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        lose = False

                    if (not startGame) and flappyButtons.rectStart.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                        startTut = True
                        pipe1.reset(300,randint(pipestart,pipeend))
                        pipe2.reset(450,randint(pipestart,pipeend))
                        lose = False
                        added = False

                    if (not startGame) and flappyButtons.rectLeader.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                        showLeaderboard()

                pygame.display.flip()
        
        #Sky moves
    if sky1move:
        sky1.draw()
        sky1.move()
        if sky1.x < 300 - (ceil(skySize[0])):
            sky2move = True
        if sky1.x < 0 - (ceil(skySize[0])):
            sky1.reset(300,0)
            sky1move = False
    if sky2move:
        sky2.draw()
        sky2.move()
        if sky2.x < 300 - (ceil(skySize[0])):
            sky1move = True
        if sky2.x < 0 - (ceil(skySize[0])):
            sky2.reset(300,0)
            sky2move = False

    # Pipe Moves 
    if startGame:
        if pipe1move:
            pipe1.draw()
            pipe1.move()
            if pipe1.x < 150:
                pipe2move = True
            if pipe1.x < 0:
                pipe1.reset(300,randint(pipestart,pipeend))
                pipe1move = False
            if pipe1.x < maxX and pipe1.x > minX:
                score += 1
        if pipe2move:
            pipe2.draw()
            pipe2.move()
            if pipe2.x < 150:
                pipe1move = True
            if pipe2.x < 0:
                pipe2.reset(300,randint(pipestart,pipeend))
                pipe2move = False
            if pipe2.x < maxX and pipe2.x > minX:
                score += 1
        
    # Ground moves
    if ground1move:
        ground1.draw()
        ground1.move()
        if ground1.x < -150:
            ground2move = True
        if ground1.x < -450:
            ground1.reset(300,500-(int(groundSize[1])))
            ground1move = False
    if ground2move:
        ground2.draw()
        ground2.move()
        if ground2.x < -150:
            ground1move = True
        if ground2.x < -450:
            ground2.reset(300,500-(int(groundSize[1])))
            ground2move = False
    
    # Flap. If endgame, save score to local storage
    if startGame:
        if flap:
            flappy.flap()
            flap = False
        for rec in [pipe1.rect1,pipe2.rect1,pipe1.rect2,pipe2.rect2,ground1.rect]:
            if flappy.rect.colliderect(rec):
                if not added:
                    global askforname
                    askforname = tkinter.Tk()
                    askforname.title("What's your name?")
                    name = tkinter.StringVar()
                    ent = tkinter.Entry(askforname,textvariable=name,width=50).pack()
                    sub = tkinter.Button(askforname,text="Submit",command=lambda:[setname(name)]).pack()
                    askforname.mainloop()
                    with open(RESOURCESPATH+"leaderboard.txt") as leaderin:
                        leaders = [s.strip("\n") for s in leaderin.readlines()]
                        
                    leads = []
                    leadname = []
                    leadnames = {}
                    for lead in range(len(leaders)-1,-1,-2):
                        if not int(leaders[lead]) in leadnames:
                            leadnames[int(leaders[lead])] = list([leaders[lead-1]])
                            # leadnames[int(leaders[lead])].append(leaders[lead-1])
                        else:
                            leadnames[int(leaders[lead])].append(leaders[lead-1])
                        leads.insert(0,int(leaders[lead]))
                    
                    try:
                        a = myname[:]
                    except NameError:
                        myname = "Anonymous"
                    
                    if myname == "": myname = "Anonymous"
                    if not score in leadnames:
                        leadnames[score] = [myname]
                        # leadnames[int(leaders[lead])].append(leaders[lead-1])
                    else:
                        leadnames[score].append(myname)

                    leads.append(score)
                    leads.sort(reverse=True)
                    if len(leads) > 5:
                        for _ in range(len(leads)-5):
                            del leads[-1]
                    for x in leads:
                        leadname.append(leadnames[x][0])
                        leadnames[x].pop(0)

                    with open(RESOURCESPATH+"leaderboard.txt","w") as leaderin:
                        for x in range(len(leads)):
                            leaderin.write(str(leadname[x])+"\n")
                            leaderin.write(str(leads[x])+"\n")
                added = True

                lose=True
        scoreMark.draw()
        flappy.draw()
        flappy.physics()
    
    #Draws start screen
    if not startGame and not startTut:
        flappyText.drawStart()
        flappyButtons.draw()
    
    #Start tutorial
    if startTut:
        score = 0
        flappy.reset(50,200)
        flappyButtons.rectStart.topleft = (-1000,-1000)
        flappyButtons.rectLeader.topleft = (-1000,-1000)
        flappy.draw()
        tut.draw()
    
    ground1.draw()
    pygame.display.flip()