from time import sleep
from os import system
from hashlib import sha256
import random
import serial
from win32 import win32api
from mss import base, mss
from PIL import ImageGrab, Image
#import pygetwindow as gw

arduino = serial.Serial('COM5', 128000)

GC = False
MM = False
VALORANT = False
RCS = False
TRIGGERBOT = False
MINECRAFT = True
S_HEIGHT, S_WIDTH  = ImageGrab.grab().size
#S_HEIGHT = 768
#S_WIDTH = 1024 
GRABZONE           = 3
def gc_bhop(): 
    return arduino.write(b'l')
    
def mm_bhop():
    return arduino.write(b'o')

def rcs():
    return arduino.write(b'k')

    
def valorant_bhop():
    return arduino.write(b'i')

def shoot_kb(): 
    return arduino.write(b'j')

def left_ac(): 
    return arduino.write(b'm')

def right_ac(): 
    return arduino.write(b'n')

class FoundEnemy(Exception):
    pass


class TriggerBot:

    def color_check(self, red: int, green: int, blue: int) -> bool:
        if green >= 0xAA: return False
        if green >= 0x78: return abs(red - blue) <= 0x8 and red - green >= 0x32 and blue - green >= 0x32 and red >= 0x69 and blue >= 0x69
        
        return abs(red - blue) <= 0xD and red - green >= 0x3C and blue - green >= 0x3C and red >= 0x6E and blue >= 0x64


    def grab(self) -> Image:
        with mss() as sct:
            bbox     = (int(S_HEIGHT / 2 - GRABZONE), int(S_WIDTH / 2 - GRABZONE), int(S_HEIGHT / 2 + GRABZONE), int(S_WIDTH / 2 + GRABZONE))
            sct_img  = sct.grab(bbox)
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


    def scan(self) -> None:
        pmap        = self.grab()

        try:
            for x in range(0, GRABZONE * 2):
                for y in range(0, GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.color_check(r, g, b): raise FoundEnemy
        
        except FoundEnemy:
            shoot_kb()

if __name__ == "__main__":
    _hash = sha256(f'{random.random()}'.encode('utf-8')).hexdigest()
    print(_hash), system(f'title {_hash}'), sleep(0.5), system('@echo off'), system('cls')
    bot = TriggerBot()
    while True:
        
        if win32api.GetAsyncKeyState(0x20) and GC:
            gc_bhop()
            continue
        
        if win32api.GetAsyncKeyState(0x20) and MM:
            mm_bhop()
            sleep(0.005)
            continue
        
        if win32api.GetAsyncKeyState(0x20) and VALORANT:
            valorant_bhop()
            continue
        
        if win32api.GetAsyncKeyState(0x01) and RCS:
            rcs()
            sleep(0.01)
            continue
        
        if win32api.GetAsyncKeyState(0x06) and TRIGGERBOT:
            bot.scan()
            continue

        if win32api.GetAsyncKeyState(0x06) and MINECRAFT:
            left_ac()
            random_sleep = random.uniform(0.055, 0.075)
            sleep(random_sleep)
            continue

        if win32api.GetAsyncKeyState(0x05) and MINECRAFT:
            right_ac()
            sleep(0.01)
            continue

        sleep(0.0025)
