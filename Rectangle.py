import pygame
from random import *


class Character:

    def __init__(self, location_x = 0, location_y = 0, color = [255, 255, 255], size_x = 10, size_y = 10, keys = [False, False, False, False], character = pygame.image.load("img/blue.png"), dead = False, deadticks = 0, speed = 0, car = False, invticks = 0, menu = False, traction = 6):
        self.location_x = location_x
        self.location_y = location_y
        self.color = color
        self.size_x = size_x
        self.size_y = size_y
        self.keys = keys
        self.dead = dead
        self.deadticks = deadticks
        self.speed = speed
        self.car = car
        self.invticks = invticks
        self.menu = menu
        self.traction = traction
        self.character = character
    
    def GetPosition(self):
        return [self.location_x, self.location_y]

    def UpdatePosition(self):
        keystates = self.keys
        if not self.car:
            if keystates[0] == True: self.GoToPosition(self.GetPosition()[0], self.GetPosition()[1] - self.speed)
            if keystates[2] == True: self.GoToPosition(self.GetPosition()[0], self.GetPosition()[1] + self.speed)
            if keystates[1] == True: self.GoToPosition(self.GetPosition()[0] - self.speed, self.GetPosition()[1])
            if keystates[3] == True: self.GoToPosition(self.GetPosition()[0] + self.speed, self.GetPosition()[1])
        else:
            if keystates[1] == True: self.GoToPosition(self.GetPosition()[0] - self.traction, self.GetPosition()[1])
            if keystates[3] == True: self.GoToPosition(self.GetPosition()[0] + self.traction, self.GetPosition()[1])
    def SetSpeed(self):
        surface = self.size_x * self.size_y
        fraction = 1 / surface
        self.speed = 3500 * fraction
    
    def GoToPosition(self, x, y):
        self.location_x = x
        self.location_y = y

    def SetColor(self, colrange):
        self.color = list(colrange)

    def GetColor(self):
        return self.color

    def GetRect(self):
        return [self.location_x, self.location_y, self.size_x, self.size_y]
    
    def SetSize(self, width, height):
        self.size_x = width
        self.size_y = height
    
    def DrawCharacter(self, screen):
        if not self.dead:
            pygame.draw.rect(screen, self.GetColor(), self.GetRect())
        else:
            if self.deadticks > 80:
                self.GoToPosition(randint(0, 500), randint(0, 500))
                self.dead = False
                self.deadticks = 0
            self.deadticks += 1

