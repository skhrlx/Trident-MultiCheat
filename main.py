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

arduino = serial.Serial('COM3', 128000)

BHOP = False #working smooth for CS:GO, and CS2, valve made the BHOP most difficult, so, it can help you...(You can edit the delay and the amount of scrolls to fit better for you)
RCS = True #i made it better, currently in the updated source, it is working smooth asf, writing the perfect recoil and legit, this old script just down your mouse...you can do better
TRIGGERBOT = True #slow
MINECRAFT = False #a good approach is use a usb host shield and arduino leonardo, I can use it as 40CPS (LEFT) and 550CPS (RIGHT) clicker, without getting banned by screenshare/ac since is only hardware and it will bypass everyone
AIMBOT = True #slow
FORTNITE = False # I coded an fortnite edit macro as well, but this source is VERY outdated. The macro performs good

S_HEIGHT, S_WIDTH  = ImageGrab.grab().size
GRABZONE           = 3

def bhop(): 
    pax = [int(1)]
    return arduino.write(pax)

def rcs():
    pax = [int(4)]
    return arduino.write(pax)

def shoot_kb(): 
    pax = [int(2)]
    return arduino.write(pax)

def right_ac(): 
    pax = [int(5)]
    return arduino.write(pax)

def down():
    pax = [int(6)]
    print("mouse down")
    return arduino.write(pax)

def up():
    pax = [int(7)]
    print("mouse up")
    return arduino.write(pax)

class FoundEnemy(Exception):
    pass

class AimBot:
    def __init__(self):
        self.lower = np.array([140, 111, 160])
        self.upper = np.array([148, 154, 194])

        self.xspd = 1.8 #1.3
        self.yspd = 0.3 #0.3
        print("Ready !")

    def mousemove(self, x, y):
        if x < 0:
            x = x + 256
        if y < 0:
            y = y + 256

        pax = [int(3), int(x), int(y)]
        arduino.write(pax)

    def grab(self):
        self.sct = mss()
        self.fov = 45 #37
        self.screenshot = self.sct.monitors[1]
        self.screenshot['left'] = int((self.screenshot['width'] / 2) - (self.fov / 2))
        self.screenshot['top'] = int((self.screenshot['height'] / 2) - (self.fov / 2))
        self.screenshot['width'] = self.fov
        self.screenshot['height'] = self.fov
        self.center = self.fov / 2
        with mss() as sct:
            return np.array(self.sct.grab(self.screenshot))

         
    def run(self):
        img = self.grab()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower, self.upper)
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=5)
        thresh = cv2.threshold(dilated, 60, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            M = cv2.moments(thresh)
            point_to_aim = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            closestX = point_to_aim[0] + 1.0 #+ 1
            closestY = point_to_aim[1] - 6.5 #- 5

            diff_x = int(closestX - self.center)
            diff_y = int(closestY - self.center)

            target_x = diff_x * self.xspd / 1.1
            target_y = diff_y * self.yspd / 1.1

            self.mousemove(target_x, target_y)

class TriggerBot:

    def __init__(self):
        print("Ready !")

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
    trigger = TriggerBot()
    aim = AimBot()
    while True:
        aim.run()
        if win32api.GetAsyncKeyState(0x01) and AIMBOT:
            aim.run(), rcs(), rcs()
        
        if win32api.GetAsyncKeyState(0x06) and AIMBOT:
            aim.run()

        if win32api.GetAsyncKeyState(0x20) and BHOP:
            bhop()
            #random_sleep = random.uniform(0.01, 0.015)
            #sleep(random_sleep)
            sleep(0.000001)
            continue
        
        if win32api.GetAsyncKeyState(0x01) and RCS:
            rcs()
            sleep(0.012)
            continue
        
        if win32api.GetAsyncKeyState(0x05) and TRIGGERBOT:
            trigger.scan()

        if win32api.GetAsyncKeyState(0x06) and MINECRAFT:
            shoot_kb()
            random_sleep = random.uniform(0.055, 0.075)
            sleep(random_sleep)

        if win32api.GetAsyncKeyState(0x05) and MINECRAFT:
            right_ac()
            random_sleep = random.uniform(0.055, 0.075)
            sleep(random_sleep)
