##PistolFight (For smaller screens), multiplayer shooter game
##Copyright (C) 2019  Nathaniel Crosby
##
##This program is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program.  If not, see <https://www.gnu.org/licenses/>.
#print GNU terminal screen
print("Pistol Fight, Copyright (C) 2019 Nathaniel Crosby\nThis program comes with ABSOLUTELY NO WARRANTY\nThis is free software, and you are welcome to redistribute it\nunder certain conditions")
#import modules
import pygame, sys, os, time

#import all pygame libraries
from pygame.locals import *

#center the pygame window
os.environ['SDL_VIDEO_CENTERED'] = '1'

#the following is trivial and self-explanitory, but I'll explain what it does anyways.
#set window dimentions and FPS
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
FPS = 60
bullet1=False

#God this code is starting to look like the Soviet Union with all this red.
#Oh well, Mrs Tylor taught me to extentively comment my code.
#You know what's cool? The size I can take the IDLE window with my 4K monitor.

#set paths for resources
current_path = os.path.dirname(__file__)
resources_path = os.path.join(current_path, 'resources')
sprites_path = os.path.join(resources_path, 'sprites')
sounds_path = os.path.join(resources_path, 'sounds')

#set up pygame, icons, FPS, and the window surface..
pygame.init()
ICON = pygame.image.load(os.path.join(sprites_path, 'icon.png')) #has to be here so it can load before the video mode is set
pygame.display.set_icon(ICON)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32) #sets window mode
pygame.mixer.pre_init(44100, 16, 2, 4096) #starts pygame mixer
mainClock = pygame.time.Clock() #runs FPS
pygame.mouse.set_visible(False)

#load all necessary sprites/images
TITLESCREEN = pygame.image.load(os.path.join(sprites_path, 'title.png')).convert()
BULLET = pygame.image.load(os.path.join(sprites_path, 'bullet.png')).convert()
MAINUI = pygame.image.load(os.path.join(sprites_path, 'main.png')).convert()
ONE = pygame.image.load(os.path.join(sprites_path, 'one.png')).convert()
TWO = pygame.image.load(os.path.join(sprites_path, 'two.png')).convert()
THREE = pygame.image.load(os.path.join(sprites_path, 'three.png')).convert()
FOUR = pygame.image.load(os.path.join(sprites_path, 'four.png')).convert()
FIVE = pygame.image.load(os.path.join(sprites_path, 'five.png')).convert()
SIX = pygame.image.load(os.path.join(sprites_path, 'six.png')).convert()
SEVEN = pygame.image.load(os.path.join(sprites_path, 'seven.png')).convert()
EIGHT = pygame.image.load(os.path.join(sprites_path, 'eight.png')).convert()
NINE = pygame.image.load(os.path.join(sprites_path, 'nine.png')).convert()
P1WIN = pygame.image.load(os.path.join(sprites_path, 'p1win.png')).convert()
P2WIN = pygame.image.load(os.path.join(sprites_path, 'p2win.png')).convert()
PLAYER = pygame.image.load(os.path.join(sprites_path, 'player.png'))
BLINKER = pygame.image.load(os.path.join(sprites_path, 'blinker.png'))
#My god, for some reason only certain images would work when i tried to use '\sprites\image.png' for a directory, and
#that worked for some images, the rest would throw an exception. So I had to import os and add 2 variables for the
#directory to work on all images. God, I really hate Python.
#UPDATE: yeah i could use double backslashes but oh well, this code works fine. Thanks to Oskar for pointing it out.

#load all necessary sounds
gunshot = pygame.mixer.Sound(os.path.join(sounds_path, 'gunshot.wav'))
hit = pygame.mixer.Sound(os.path.join(sounds_path, 'hit.wav'))
#turns out pygame doesnt like anything above a 16-bit encoding for a wav file.
#also I had to put pygame.init() before this so it would actually load the wav files.
#thank god for audacity.

#set window title
pygame.display.set_caption('Pistol Fight')

#code stating both player's rectangle and move rate
playerRect = PLAYER.get_rect() #the player's rectangle
playerRect2 = PLAYER.get_rect() #player rectangle for player 2
PLAYERMOVERATE = 7.5

def main(): #def for the whole game
    #Player Score Variables
    P1SCORE = 0
    P2SCORE = 0

    #Bullet position lists
    P1BULLET=[]
    P2BULLET=[]
        
    #code to terminate the program
    def terminate():
        print ("Quitting...")
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    #Code that allows the player to move left, the appretices did this.
    moveLeft = moveRight = moveUp = moveDown = False
    moveLeft2 = moveRight2 = moveUp2 = moveDown2 = False

    #bind ESC and Close Button, title screen edition.
    def waitForPlayerToPressKey():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                       terminate()
                    return
            
    #define player boundaries
    def handle_player_movement(player, move_left, move_right, move_up, move_down):

        #Limits where player 1 can move
        if move_left and player.left > 0:
            player.move_ip(-1 * PLAYERMOVERATE, 0)
        elif move_right and player.right < 200:
            player.move_ip(PLAYERMOVERATE, 0)
        elif move_up and player.top > 50:
            player.move_ip(0, -1 * PLAYERMOVERATE)
        elif move_down and player.bottom < WINDOWHEIGHT:
            player.move_ip(0, PLAYERMOVERATE)
        return

    def handle_player2_movement(player, move_left2, move_right2, move_up2, move_down2):

        #limits where player 2 can move
        if move_left2 and player.left > 300:
            player.move_ip(-1 * PLAYERMOVERATE, 0)
        elif move_right2 and player.right < 500:
            player.move_ip(PLAYERMOVERATE, 0)
        elif move_up2 and player.top > 50:
            player.move_ip(0, -1 * PLAYERMOVERATE)
        elif move_down2 and player.bottom < WINDOWHEIGHT:
            player.move_ip(0, PLAYERMOVERATE)
    #a seperate def for player 2? wo-hoo.

    #display the title screen
    windowSurface.blit(TITLESCREEN, [0, 0])
    pygame.display.update()
    waitForPlayerToPressKey()

    #allow the players to move
    playerRect.topleft = (40, 80)
    playerRect2.topleft = (WINDOWWIDTH - 80, 80)

    #keybinds for main game.
    run = True
    clock = pygame.time.Clock()
    while run: #while, an iteration construct.

        #allow the game to accept keybinds in the main game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:

                #Bind ESC and Close Button, main game edition.
                if event.key == K_ESCAPE:
                    terminate()

                # Player 1
                if event.key == K_a:
                    moveLeft = True
                elif event.key == K_w:
                    moveUp = True
                elif event.key == K_s:
                    moveDown = True
                elif event.key == K_d:
                    moveRight = True
                elif event.key == K_LCTRL:
                    if P1BULLET==[]:
                        pygame.mixer.Sound.play(gunshot)
                        P1BULLET=[playerRect.left+20, playerRect.top+27]

                # Player 2
                if event.key == K_LEFT:
                    moveLeft2 = True
                elif event.key == K_UP:
                    moveUp2 = True
                elif event.key == K_DOWN:
                    moveDown2 = True
                elif event.key == K_RIGHT:
                    moveRight2 = True
                elif event.key == K_RCTRL:
                    if P2BULLET==[]:
                        pygame.mixer.Sound.play(gunshot)
                        P2BULLET=[playerRect2.left, playerRect2.top+27]
                    
            elif event.type == pygame.KEYUP:

                # Player 1
                if event.key == K_a:
                    moveLeft = False
                elif event.key == K_w:
                    moveUp = False
                elif event.key == K_s:
                    moveDown = False
                elif event.key == K_d:
                    moveRight = False

                # Player 2
                elif event.key == K_LEFT:
                    moveLeft2 = False
                elif event.key == K_UP:
                    moveUp2 = False
                elif event.key == K_DOWN:
                    moveDown2 = False
                elif event.key == K_RIGHT:
                    moveRight2 = False

        #allow the game to handle player movement.    
        handle_player_movement(playerRect, moveLeft, moveRight, moveUp, moveDown)
        handle_player2_movement(playerRect2, moveLeft2, moveRight2, moveUp2, moveDown2)

        #Render the main game interface.
        windowSurface.fill((0,0,0))
        windowSurface.blit(MAINUI, [0, 0]) #mainui is the yellow top bar, the black play area and the yellow fences seperating the two players.

        #Scoring System, Player 1
        if P1SCORE == 1:
            windowSurface.blit(ONE, [62,9])
        if P1SCORE == 2:
            windowSurface.blit(TWO, [62,9])
        if P1SCORE == 3:
            windowSurface.blit(THREE, [62,9])
        if P1SCORE == 4:
            windowSurface.blit(FOUR, [62,9])
        if P1SCORE == 5:
            windowSurface.blit(FIVE, [62,9])
        if P1SCORE == 6:
            windowSurface.blit(SIX, [62,9])
        if P1SCORE == 7:
            windowSurface.blit(SEVEN, [62,9])
        if P1SCORE == 8:
            windowSurface.blit(EIGHT, [62,9])
        if P1SCORE == 9:
            windowSurface.blit(NINE, [62,9])
        if P1SCORE == 10:
            windowSurface.blit(ONE, [44,9])
        if P1SCORE == 11:
            windowSurface.blit(ONE, [44,9])
            windowSurface.blit(ONE, [62,9])
        if P1SCORE == 12:
            windowSurface.blit(ONE, [44,9])
            windowSurface.blit(TWO, [62,9])
        if P1SCORE == 13:
            windowSurface.blit(ONE, [44,9])
            windowSurface.blit(THREE, [62,9])
        if P1SCORE == 14:
            windowSurface.blit(ONE, [44,9])
            windowSurface.blit(FOUR, [62,9])
        if P1SCORE == 15:
            windowSurface.blit(ONE, [44,9])
            windowSurface.blit(FIVE, [62,9])

        #Scoring System, Player 2
        if P2SCORE == 1:
            windowSurface.blit(ONE, [441,9])
        if P2SCORE == 2:
            windowSurface.blit(TWO, [441,9])
        if P2SCORE == 3:
            windowSurface.blit(THREE, [441,9])
        if P2SCORE == 4:
            windowSurface.blit(FOUR, [441,9])
        if P2SCORE == 5:
            windowSurface.blit(FIVE, [441,9])
        if P2SCORE == 6:
            windowSurface.blit(SIX, [441,9])
        if P2SCORE == 7:
            windowSurface.blit(SEVEN, [441,9])
        if P2SCORE == 8:
            windowSurface.blit(EIGHT, [441,9])
        if P2SCORE == 9:
            windowSurface.blit(NINE, [441,9])
        if P2SCORE == 10:
            windowSurface.blit(ONE, [423,9])
        if P2SCORE == 11:
            windowSurface.blit(ONE, [423,9])
            windowSurface.blit(ONE, [441,9])
        if P2SCORE == 12:
            windowSurface.blit(ONE, [423,9])
            windowSurface.blit(TWO, [441,9])
        if P2SCORE == 13:
            windowSurface.blit(ONE, [423,9])
            windowSurface.blit(THREE, [441,9])
        if P2SCORE == 14:
            windowSurface.blit(ONE, [423,9])
            windowSurface.blit(FOUR, [441,9])
        if P2SCORE == 15:
            windowSurface.blit(ONE, [423,9])
            windowSurface.blit(FIVE, [441,9])
        #I had a zero sprite, but I realised I never called it.

        #When a player wins, display a win screen, wait, then terminate.        
        if P1SCORE >= 15:
           windowSurface.blit(P1WIN, [60, 200])
           pygame.display.update()
           time.sleep(2)
           main()
           pygame.display.update()
        elif P2SCORE >= 15:
            windowSurface.blit(P2WIN, [60, 200])
            pygame.display.update()
            time.sleep(2)
            main()
            pygame.display.update()

        #Draw the player's rectangle
        windowSurface.blit(PLAYER, [playerRect.left, playerRect.top])
        windowSurface.blit(pygame.transform.flip(PLAYER, 1, 0), [playerRect2.left, playerRect2.top])

        #Bullet calculations and display
        if not P1BULLET==[]:    #checks if bullet is currently on screen
            if not P1BULLET[0]>=WINDOWWIDTH:    #if has gone off side of screen
                windowSurface.blit(BULLET, P1BULLET)    #display
                P1BULLET[0]+=7.5      #adds 7.5 units to x value, moving the bullet in turn
                if P1BULLET[0]>= playerRect2.left and P1BULLET[0]<= playerRect2.right:      #checks if within horizontal bounding box of other player
                    if P1BULLET[1]>= playerRect2.top and P1BULLET[1]<= playerRect2.bottom:  #checks if within vertical bounding box of other player
                        P1BULLET=[]     #removes bullet
                        P2BULLET=[]
                        pygame.mixer.Sound.play(hit)
                        windowSurface.blit(BLINKER, [275, 50])
                        pygame.display.update()
                        P1SCORE += 1
                        time.sleep(.5)
            else:
                P1BULLET=[]
        if not P2BULLET==[]:    #repeat of other section, but with slight modifications to work for the 2nd player bullet
            if not P2BULLET[0]<=0:
                windowSurface.blit(pygame.transform.flip(BULLET, 1, 0), P2BULLET)
                P2BULLET[0]-=7.5
                if P2BULLET[0]>= playerRect.left and P2BULLET[0]<= playerRect.right:
                    if P2BULLET[1]>= playerRect.top and P2BULLET[1]<= playerRect.bottom:
                        P2BULLET=[]
                        P1BULLET=[]
                        pygame.mixer.Sound.play(hit)
                        windowSurface.blit(BLINKER, [0, 50])
                        pygame.display.update()
                        P2SCORE += 1
                        time.sleep(.5)
            else:
                P2BULLET=[]

        pygame.display.flip()
        clock.tick(FPS)
main()
pygame.display.update()
#END
