# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 09:03:04 2024

@author: Brooklyn
"""

import pygame, random, simpleGE

class Taco(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("taco1.png")
        self.setSize(100, 100)
        self.reset()
    
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(1, 8)
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
        
class Hotdog(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("hotdog1.png")
        self.setSize(100,100)
        self.reset()
        
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        self.dy = random.randint(1, 8)
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()


class Cart(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("tacocart2.png")
        self.setSize(150, 150)
        self.position = (285, 395)
        self.moveSpeed = 10
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
        
class lblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text= "Score 0"
        self.center = (100,30)
        
class lblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time Left: 10"
        self.center =(500,30)
        self.counter = 0
        self.text = "0"
        self.timer = simpleGE.Timer()
        
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.background.fill((18, 22, 41))
        self.setImage("tacobckgrnd.PNG")
        
        self.sndTaco = simpleGE.Sound("crunch.wav")
        self.sndHotdog = simpleGE.Sound ("error1.wav")
       
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.score = 0
        
        self.cart = Cart(self)
        self.taco = []
        for i in range(20):
            self.taco.append(Taco(self))
            
        self.cart = Cart(self)
        self.hotdog = []
        for i in range(5):
            self.hotdog.append(Hotdog(self))
        
        self.lblScore = lblScore()
        self.lblTime = lblTime()
        
        self.sprites = [self.cart, self.taco, self.hotdog,  self.lblScore,  self.lblTime]
        
        
    
    def process(self):
        for Taco in self.taco:
            if self.cart.collidesWith(Taco):
                self.sndTaco.play()
                Taco.reset()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
            self.lblTime.text = f" Time Left: {self.timer.getTimeLeft():.2f}"
            if self.timer.getTimeLeft() < 0:
                self.stop()
                
        for Hotdog in self.hotdog:
            if self.cart.collidesWith(Hotdog):
                self.sndHotdog.play()
                Hotdog.reset()
                self.score -= 1
               # self.timer.getTimeLeft -= 1
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() <= 0:
            print(f" Final Score: {self.score}")
            self.stop
                
class Instruction(simpleGE.Scene):
    def __init__(self, score = 0):
        super().__init__()
        self.setImage("tacobckgrnd.png")
        self.status= "Quit"
        self.score = score 
        
        self.Instruction = simpleGE.MultiLabel() 
        self.Instruction.textLines = [
            " I don't why...",
            " But there's tacos falling out of the sky.",
            " To retrieve them all",
            " Avoid the HOTDOGS !",
            " What a foody start",
            " Please help me restock my taco cart.",
            " Press left or right keys to move the cart."
            ]
        
        self.Instruction.center = (320,240)
        self.Instruction.size = (400,250)
        self.lblScore = simpleGE.Label()
        self.lblScore.center = (320,50)
        self.lblScore.size = (400,30)
        self.lblScore.text = f" Previous Score: {self.score} "
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.center = (100,450)
        self.btnPlay.text = "Play (up)"
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.center = (540, 450)
        self.btnQuit.text = "Quit (down)"
        self.sprites = [self.lblScore, self.Instruction, self.btnPlay , self.btnQuit]
        
    def process(self):
        if self.btnPlay.clicked:
            self.status= "play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.status ="quit"
            self.stop()
            
        if self.isKeyPressed(pygame.K_UP):
            self.status ="play"
            self.stop()
            
        if self.isKeyPressed(pygame.K_DOWN):
            self.status = "quit"
            self.stop()
            
            
        
def main():
    pygame.display.set_caption("Cinco de Taco!")
    
    keepGoing = True 
    score = 0 
    while keepGoing:
        instruction = Instruction(score)
        instruction.start()
        print(instruction.status)
        
        if instruction.status == "play": 
            game = Game()
            game.start()
            score = game.score
            
        else:
            keepGoing = False 
        
        # if instruction.status == "quit":
        #     game = Game()
        #     game.stop()
            
        # else: 
        #     keepGoing = False 
        


if __name__ == "__main__":
    main()