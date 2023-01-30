from time import sleep
from os import system
from hashlib import sha256
import random
import serial
from win32 import win32api
from mss import base, mss
from PIL import ImageGrab, Image
import cv2
import numpy as np

arduino = serial.Serial('COM5', 128000)

GC = False
MM = True
VALORANT = False
RCS = True
TRIGGERBOT = True
MINECRAFT = False
S_HEIGHT, S_WIDTH  = ImageGrab.grab().size
GRABZONE           = 3
 
class AimBot:
    def __init__(self, fov=10):
        self.fov = fov
        self.sct = mss()
        self.screenshot = self.sct.monitors[1]
        self.screenshot['left'] = int((self.screenshot['width'] / 2) - (self.fov / 2))
        self.screenshot['top'] = int((self.screenshot['height'] / 2) - (self.fov / 2))
        self.screenshot['width'] = self.fov
        self.screenshot['height'] = self.fov
        self.center = self.fov / 2

        self.lower = np.array([140, 111, 160])
        self.upper = np.array([148, 154, 194])

        self.xspd = 0.8
        self.yspd = 0.8
        print("Ready !")

    def mousemove(self, x, y):
        if x < 0:
            x = x + 256
        if y < 0:
            y = y + 256

        pax = [int(x), int(y)]
        arduino.write(pax)

    def run(self):
                img = np.array(self.sct.grab(self.screenshot))
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, self.lower, self.upper)
                kernel = np.ones((3, 3), np.uint8)
                dilated = cv2.dilate(mask, kernel, iterations=5)
                thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                if len(contours) != 0:
                    M = cv2.moments(thresh)
                    point_to_aim = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    closestX = point_to_aim[0] + 2
                    closestY = point_to_aim[1] - 5

                    diff_x = int(closestX - self.center)
                    diff_y = int(closestY - self.center)

                    target_x = diff_x * self.xspd
                    target_y = diff_y * self.yspd

                    self.mousemove(target_x, target_y)

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
            sleep(0.04)
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
