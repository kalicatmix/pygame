#!/usr/bin/env python
'''
author:kalicat
date:2018/6/30
description:
simple game of tank
'''
import pygame
import pygame.gfxdraw
import sys,time,threading,random
die = False
SCORE=0
thread=None
STARTGAME=False
eX=random.randint(10,450)
eY=random.randint(10,450)
def main():
    global thread,STARTGAME,eX,eY
    #variables
    X=0
    Y=0
    STEP=0
    STATUS=False
    STATUSX=False
    PLAY=True
    # functions
    def drawBackground():
        SCOREX = FONTX.render("score:" + str(SCORE), True, (50, 25, 127))
        STEPX = FONTX.render("step:" + str(STEP), True, (50, 25, 127))
        DISPLAY.blit(STEPX, (400, 30))
        DISPLAY.blit(SCOREX, (400, 0))
    def drawSHOT():
        DISPLAY.fill(pygame.Color(255, 255, 255))
        drawBackground()
    #display init
    pygame.init()
    DISPLAY=pygame.display.set_mode((500,500),0,32)
    pygame.display.set_caption("game")
    pygame.display.set_icon(pygame.image.load("./source/game.png"))
    #music load
    pygame.mixer.music.load("./source/river.mp3")
    pygame.mixer.music.play(-1,0.0)
    #image load
    IMG=pygame.image.load("./source/background.jpg")
    BACKGROUND=pygame.transform.scale(IMG,(500,500))
    DISPLAY.blit(BACKGROUND,(0,0))
    PLAYER=pygame.image.load("./source/player1.gif")
    PLAYER_UP=pygame.transform.rotate(PLAYER,90)
    SHOT=pygame.image.load("./source/shot.gif")
    SHOT_R=pygame.transform.rotate(SHOT,90)
    #font load
    FONT=pygame.font.Font("./source/simfang.ttf",50)
    START=FONT.render("START GAME",True,(0,255,127))
    Control=FONT.render("CONTROL",True,(0,255,127))
    ROW=FONT.render(("->Left&&&Right<-"),True,(0,255,127))
    DISPLAY.blit(START,(130,50))
    DISPLAY.blit(Control,(150,150))
    DISPLAY.blit(ROW,(60,200))
    STARTGAME=False
    FONTX = pygame.font.Font("./source/simfang.ttf", 20)
    def getXY():
        return random.randint(10,400)
    def getWay():
        return random.randint(0,3)
    def drawEnimies():
        DISPLAY.fill(pygame.Color(255,255,255))
        DISPLAY.blit(BACKGROUND,(0,0))
        drawBackground()
        if STATUS:
            DISPLAY.blit(PLAYER_UP,(X,Y))
        else:
            DISPLAY.blit(PLAYER,(X,Y))
        global eX,eY
        if eX<0 or eX>500 or eY<0 or eY>500:
            if getWay()==0:
                eX = 0
                eY = 0
                return 0
            if getWay()==1:
                eX=400
                eY=0
                return 0
            if getWay()==2:
                eX=0
                eY=400
                return 0
            if getWay()==3:
                eX=400
                eY=400
                return 0
        if getWay()==0:
            eX+=10
            DISPLAY.blit(PLAYER, (eX, eY))
            pygame.display.update()
            return 0
        if getWay()==1:
            eY+=10
            DISPLAY.blit(PLAYER_UP, (eX, eY))
            pygame.display.update()
            return 0
        if getWay()==2:
            eX-=10
            DISPLAY.blit(PLAYER, (eX, eY))
            pygame.display.update()
            return 0
        if getWay()==3:
            eY-=10
            DISPLAY.blit(PLAYER_UP, (eX, eY))
            pygame.display.update()
            return 0
    def make_enimies():
       while True:
           global die,SCORE,eX,eY
           if not die:
               drawEnimies()
               pygame.time.wait(100)
           else:
               die=False
               SCORE +=1
               DISPLAY.fill(pygame.Color(255,255,255))
               drawBackground()
               DISPLAY.blit(pygame.image.load("./source/explosion.gif"), (eX, eY))
               pygame.display.update()
               eX=getXY()
               eY=getXY()
               pygame.time.wait(50)
    #start enimies thread
    thread = pygame.threads.Thread(target=make_enimies)
    while True:
      drawBackground()
      event=pygame.event.wait()
      if event.type==pygame.MOUSEBUTTONDOWN and not STARTGAME:
          if(event.pos[0] in range(130,300) and event.pos[1] in range(0,100)):
              pygame.mixer.Sound("./source/boom.wav").play()
              DISPLAY.fill(pygame.Color(255,255,255))
              DISPLAY.blit(BACKGROUND,(0,0))
              STARTGAME=True
              pygame.mixer.music.stop()
              DISPLAY.blit(PLAYER,(X,Y))
              thread.start()
              STARTGAME=True
      if STARTGAME and (event.type == pygame.KEYUP):
      #default
          DISPLAY.fill(pygame.Color(255,255,255))
          DISPLAY.blit(BACKGROUND,(0,0))
          key=event.key
          if key==pygame.K_a:
              pygame.mixer.Sound("./source/boom.wav").play()
              if STATUS:
                  DISPLAY.blit(PLAYER_UP,(X,Y))
              else:
                  DISPLAY.blit(PLAYER,(X,Y))
              x = X
              y = Y
              while PLAY:
                  global die
                  if x<-10 or x > 500 or y <-10 or y > 500:
                      PLAY = False
                  else:
                      if(x in range(eX-40,eX+40) and y in range(eY-40,eY+40)):
                          die=True
                      if STATUS:
                          if STATUSX:
                              y -= 10
                          else:
                              y +=10
                          drawSHOT()
                          DISPLAY.blit(BACKGROUND,(0,0))
                          DISPLAY.blit(PLAYER_UP,(X,Y))
                          DISPLAY.blit(SHOT, (X, y))
                          pygame.display.update()
                          pygame.time.wait(10)
                      else:
                          if STATUSX:
                              x -=10
                          else:
                              x +=10
                          drawSHOT()
                          DISPLAY.blit(BACKGROUND,(0,0))
                          DISPLAY.blit(PLAYER,(X,Y))
                          DISPLAY.blit(SHOT_R, (x, Y))
                          pygame.display.update()
                          pygame.time.wait(10)
              PLAY=True
              continue
          if key==pygame.K_UP:
              STEP+=1
              Y-=10
              DISPLAY.blit(PLAYER_UP, (X, Y))
              STATUS=True
              STATUSX=True
              continue
          if key==pygame.K_DOWN:
              STEP += 1
              Y+=10
              DISPLAY.blit(PLAYER_UP, (X, Y))
              STATUS=True
              STATUSX=False
              continue
          if key==pygame.K_LEFT:
              STEP += 1
              X-=10
              DISPLAY.blit(PLAYER, (X, Y))
              STATUS=False
              STATUSX=True
              continue
          if key==pygame.K_RIGHT:
              STEP += 1
              X+=10
              DISPLAY.blit(PLAYER, (X, Y))
              STATUS=False
              STATUSX=False
              continue
          DISPLAY.blit(PLAYER,(X,Y))
      if(event.type==pygame.QUIT):
        pygame.mixer.music.stop()
        pygame.time.wait(1000)
        pygame.quit()
        sys.exit(1)
      pygame.display.update()

if __name__=="__main__":
    main()