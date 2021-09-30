import os

print("Checking for required modules...")
try:
    import pygame
except:
    if not os.system("pip install pygame"):
        print("Python hasn't being installed or pip hasn't been added to PATH. Please try again")
        raise NotImplementedError()

if os.system("pip install pyinstaller"):
    print("Python hasn't being installed or pip hasn't been added to PATH. Please try again")
    raise NotImplementedError

print("Done")
print("Creating exe file...")

if not os.path.exists("dist\\mainFlap.exe") and not os.path.exists("mainFlap.txt") and not os.path.exists("mainFlap.exe"):
    if os.system("pyinstaller --onefile -w mainFlap.py"):
        print("An error occured with pyinstaller.")
        raise NotImplementedError

print("Copying EXE to main path...",end=" ")

if not os.path.exists("mainFlap.exe"):
    try:
        os.rename("dist\\mainFlap.exe","mainFlap.txt")
    except:
        pass
    os.rename("mainFlap.txt","mainFlap.exe")

print("Done")
print("Cleaning up...",end=" ")

try:
    os.remove("mainFlap.spec")
    os.remove("build\\")
    os.remove("dist\\")
except:
    print("Failed")
    print("Please consider to delete the following file and folder(s) by yourself:")
    delete = ["\\mainFlap.spec","\\build","\\dist"]
    for x in delete:
        if os.path.exists(os.path.abspath(os.path.dirname(__file__))+x):
            print(os.path.abspath(os.path.dirname(__file__)) + x)
else:
    print("Done")
input("Press Enter to run the flappy bird program...")
os.system("mainFlap.exe")
