import pygame
import time
import random

pygame.init()

display_width=1280
display_height=720

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
brown=(165,42,42)

car_width=60

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Lets Race")
clock=pygame.time.Clock()

CarImg=pygame.image.load("Racecar.png")

def get_high_score():
    # Default high score
    high_score = 0

    # Try to read the high score from a file
    try:
        high_score_file = open("high_score.txt", "r")
        high_score = int(high_score_file.read())
        high_score_file.close()
        print("The high score is", high_score)
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")

    return high_score

def save_high_score(new_high_score):
    try:
        # Write the file to disk
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(new_high_score))
        high_score_file.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")

def things_dodged(count):
    high_score = get_high_score()
    font=pygame.font.SysFont(None,40)
    text=font.render("Score "+str(count),True,black)
    if count > high_score:
        save_high_score(count)
    highScore=font.render("High Score "+str(high_score),True,black)
    gameDisplay.blit(text,(20,20))
    gameDisplay.blit(highScore,(20,50))

def car1(x,y):
    gameDisplay.blit(CarImg,(x,y))

def car2(x,y):
    gameDisplay.blit(CarImg,(x,y))


def things(thingx,thingy,thingw,thingh,color):
    color=brown

    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

def text_objects(text,font):
    textSurface=font.render(text, True, red)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText=pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect=text_objects(text, largeText)
    TextRect.center=((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def crash1():
    message_display('PLayer 1 Crashed')

def crash2():
    message_display('PLayer 2 Crashed')

def crash3():
    message_display('Collision')

def game_loop():
    y_change=0
    y2_change=0

    x=(display_width*0.48/2)
    y=(display_height*0.79)

    x2=(display_width*0.48*1.5)
    y2=(display_height*0.79)

    x_change=0
    x2_change=0

    thing_startx=random.randrange(0,display_width)
    thing_starty=-600
    thing_speed=9
    thing_width=100
    thing_height=100

    dodged=0

    gameExit=False

    while not gameExit:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_a:
                    x_change=-8
                    y_change=0
                elif event.key==pygame.K_d:
                    x_change=8
                    y_change=0
                elif event.key==pygame.K_w:
                    x_change=0
                    y_change=-8
                elif event.key==pygame.K_s:
                    x_change=-0
                    y_change=8
                if event.key==pygame.K_LEFT:
                    x2_change=-8
                    y2_change=0
                elif event.key==pygame.K_RIGHT:
                    x2_change=8
                    y2_change=0
                elif event.key==pygame.K_UP:
                    x2_change=0
                    y2_change=-8
                elif event.key==pygame.K_DOWN:
                    x2_change=-0
                    y2_change=8

            if event.type==pygame.KEYUP:
                if event.key==pygame.K_d or event.key==pygame.K_a or event.key==pygame.K_s or event.key==pygame.K_w or event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT or event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    x_change=0
                    y_change=0
                    x2_change=0
                    y2_change=0

        x+=x_change
        if y+y_change>=display_height*0.79:
            y_change=0
        elif y+y_change<=0:
        	y_change=0
        y+=y_change

        x2+=x2_change
        if y2+y2_change>=display_height*0.79:
            y2_change=0
        elif y2+y2_change<=0:
        	y2_change=0
        y2+=y2_change

        gameDisplay.fill(white)

        #things(thingx,thingy,thingw,thingh,color)
        things(thing_startx,thing_starty,thing_width,thing_height,black)
        thing_starty+=thing_speed
        car1(x,y)
        car2(x2,y2)
        things_dodged(dodged)

        if x>display_width-car_width or x<0:
            crash1()
        if x2>display_width-car_width or x2<0:
            crash2()

        if thing_starty>display_height:
            thing_starty=0-thing_height
            thing_startx=random.randrange(0,display_width)
            dodged+=1
            if thing_speed<25:
                thing_speed+=0.5

        if ((x+car_width>x2 and x<x2+car_width) and (y-125<y2 and y>y2-125)):
            print('collide')
            crash3()

        if y<thing_starty+thing_height:
            print('y crossover')

            if ((x>thing_startx and x<thing_startx+thing_width) and (y>thing_starty and y<thing_starty+thing_height)) or ((x+car_width>thing_startx and x+car_width<thing_startx+thing_width) and (y>thing_starty and y<thing_starty+thing_height)):
                print('x1 crossover')
                crash1()

        if y2<thing_starty+thing_height:
            print('y2 crossover')

            if ((x2>thing_startx and x2<thing_startx+thing_width) and (y2>thing_starty and y2<thing_starty+thing_height)) or ((x2+car_width>thing_startx and x2+car_width<thing_startx+thing_width) and (y2>thing_starty and y2<thing_starty+thing_height)):
                print('x2 crossover')
                crash2()

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
