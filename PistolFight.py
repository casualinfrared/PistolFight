##PistolFight, multiplayer shooter game version 2.
##Copyright © 2019-2025 Nathaniel Crosby
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

#Game Settings
version = '2.0'
copyrightyear = '2019-2025'
preRelease = False #change the title bar text and start text if set to True to make it known this is a pre-release
titleScreenEnable = True #toggle the title screen

#print GNU terminal disclaimer
print(f"Pistol Fight version {version}, Copyright © {copyrightyear} Nathaniel Crosby\nThis program comes with ABSOLUTELY NO WARRANTY\nThis is free software, and you are welcome to redistribute it\nunder certain conditions")

#import modules
import pygame, sys, os
from pygame.locals import * #import all pygame libraries

#Initialise pygame
pygame.init()
clock = pygame.time.Clock() #set up pygame clock for FPS

#Define all necessary sprites
ICON = pygame.image.load('resources//sprites//icon.png') #window icon
FENCES = pygame.image.load('resources//sprites//main.png') #fence graphic in main game screen
HUD = pygame.image.load('resources//sprites//hud.png') #yellow HUD, first 100px of window
ZERO = pygame.image.load('resources//sprites//zero.png') #numbers 0-15
ONE = pygame.image.load('resources//sprites//one.png') 
TWO = pygame.image.load('resources//sprites//two.png')
THREE = pygame.image.load('resources//sprites//three.png')
FOUR = pygame.image.load('resources//sprites//four.png')
FIVE = pygame.image.load('resources//sprites//five.png')
SIX = pygame.image.load('resources//sprites//six.png')
SEVEN = pygame.image.load('resources//sprites//seven.png')
EIGHT = pygame.image.load('resources//sprites//eight.png')
NINE = pygame.image.load('resources//sprites//nine.png')
TEN = pygame.image.load('resources//sprites//ten.png')
ELEVEN = pygame.image.load('resources//sprites//eleven.png')
TWELVE = pygame.image.load('resources//sprites//twelve.png')
THIRTEEN = pygame.image.load('resources//sprites//thirteen.png')
FOURTEEN = pygame.image.load('resources//sprites//fourteen.png')
FIFTEEN = pygame.image.load('resources//sprites//fifteen.png')
PLAYER = pygame.image.load('resources//sprites//player.png') #player graphic
BULLET = pygame.image.load('resources//sprites//bullet.png') #bullet graphic

#Set up sound system and define our sounds
pygame.mixer.pre_init(44100, 16, 1, 512) #starts pygame mixer, with mono CD-Quality audio, with 512 byte buffer.
gunshot = pygame.mixer.Sound('resources//sounds//gunshot.wav')
hit = pygame.mixer.Sound('resources//sounds//hit.wav')

#set up our custom font and text to use
pygame.font.init()
disclaimerText = pygame.font.Font('resources//fonts//ARCADEPI.TTF', 24) #we'll need one for the disclaimer here
bigYellowText = pygame.font.Font('resources//fonts//ARCADEPI.TTF', 192) #for our title and win graphics
smallerYellowText = pygame.font.Font('resources//fonts//ARCADEPI.TTF', 140) #for our title and win graphics
titleLine1Text = bigYellowText.render('PISTOL', True, (255, 242, 0))
titleLine2Text = bigYellowText.render('FIGHT', True, (255, 242, 0))
p1WinTextLine1 = smallerYellowText.render('PLAYER 1', True, (255, 242, 0))
p2WinTextLine1 = smallerYellowText.render('PLAYER 2', True, (255, 242, 0))
playerWinTextLine2 = smallerYellowText.render('WINS!', True, (255,242, 0))
titleVerText = disclaimerText.render(f'COPYRIGHT © {copyrightyear} NATHANIEL CROSBY. VERSION {version}', True, (255, 255, 255))
beginText = disclaimerText.render(f'PRESS ANY KEY TO BEGIN', True, (255, 255, 255))


#set up the game window
os.environ['SDL_VIDEO_CENTERED'] = '1' #centre the game window
WINDOWWIDTH = 1000 #set width and height to 1000px
WINDOWHEIGHT = 1000
pygame.display.set_icon(ICON) #set the icon of the window for the titlebar and taskbar
pygame.display.set_caption(f'Pistol Fight {version}') #Window title for titlebar and taskbar is "Pistol Fight"
pygame.mouse.set_visible(False) #hides the OS cursor when it's in the game window

#Function that terminates the program upon pressing X on the window or Esc on the keyboard
def terminate():
    print ("Quitting...") #warn the user we're quitting
    pygame.mixer.quit() #shut down the sound system
    pygame.display.quit() #shut down pygame's display system
    pygame.quit() #shut down pygame
    sys.exit() #gracefully terminate

#Pause on the title screen, wait for player to press ESC to quit or any key to begin
def waitForPlayerToPressKey():
     while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                   terminate()
                return

#set up our windowSurface so we can blit and Rect to it
windowSurface = pygame.display.set_mode((1000, 1000), 0, 32) #sets window mode
hudSurface = pygame.Rect(0, 0, 1000, 100) #for HUD
gameSurface = pygame.Rect(0, 100, 1000, 900) #for game window
p1PlayArea = pygame.Rect(0, 100, 491, 900) #for new player 1 blinker
p2PlayArea = pygame.Rect(509, 100, 491, 900) #for new player 2 blinker

#Draw HUD
windowSurface.fill((255,242,0), hudSurface) #fill our HUD area with "Pistol Fight Yellow"
windowSurface.blit(HUD, [88, 2]) #draw the tiny p1 and p2 graphic on the HUD
windowSurface.blit(ZERO, [88 ,18]) #draw the zeroes for when we start
windowSurface.blit(ZERO, [846, 18])

#Pre-release version check, we want to change the start text and title bar text if we're pre-release
if preRelease == True:
    beginText = disclaimerText.render('PRE-RELEASE VERSION', True, (255, 255, 255)) #change start text
    pygame.display.set_caption(f'Pistol Fight {version}' + ' PRE-RELEASE') #append PRE-RELEASE on title bar

#Game loop function
def main():
    
    #Player Score Variables
    P1SCORE = 0
    P2SCORE = 0

    #Bullet position lists
    P1BULLET=[]
    P2BULLET=[]

    #Booleans for player movement
    moveLeft1 = moveRight1 = moveUp1 = moveDown1 = False
    moveLeft2 = moveRight2 = moveUp2 = moveDown2 = False

    #Define our player hitboxes, we need two for both players
    playerRect1 = PLAYER.get_rect() #Player 1's hitbox, get from size of PLAYER graphic
    playerRect2 = PLAYER.get_rect() #Ditto for Player 2

    #allow the players to move
    PLAYERMOVERATE = 15 #How fast we want them to move
    playerRect1.topleft = (80, 160)
    playerRect2.topleft = (WINDOWWIDTH - 160, 160)

    #Booleans to determine who got shot
    player1Shot = False
    player2Shot = False
    
    #Booleans to determine who won
    player1Won = False
    player2Won = False

    #Title screen function
    def titleScreen():
        #render our text
        windowSurface.blit(titleLine1Text, [90, 240]) #draw the title graphic
        windowSurface.blit(titleLine2Text, [150, 400])
        windowSurface.blit(titleVerText, [50, 955]) #copyright and version string
        windowSurface.blit(beginText, [300, 600])
        pygame.display.update()
        waitForPlayerToPressKey() #wait for any key
                
    #Functions to handle how far our players can move in the window
    def handle_player1_movement(player, move_left1, move_right1, move_up1, move_down1):

        #Limits where player 1 can move
        if move_left1 and player.left > 5:
            player.move_ip(-1 * PLAYERMOVERATE, 0)
        elif move_right1 and player.right < 480:
            player.move_ip(PLAYERMOVERATE, 0)
        elif move_up1 and player.top > 100:
            player.move_ip(0, -1 * PLAYERMOVERATE)
        elif move_down1 and player.bottom < 990:
            player.move_ip(0, PLAYERMOVERATE)
        return

    #The same function copied for Player 2
    def handle_player2_movement(player, move_left2, move_right2, move_up2, move_down2):

        #limits where player 2 can move
        if move_left2 and player.left > 525:
            player.move_ip(-1 * PLAYERMOVERATE, 0)
        elif move_right2 and player.right < 1000:
            player.move_ip(PLAYERMOVERATE, 0)
        elif move_up2 and player.top > 100:
            player.move_ip(0, -1 * PLAYERMOVERATE)
        elif move_down2 and player.bottom < 990:
            player.move_ip(0, PLAYERMOVERATE)

    def someoneGotShot(): ##NOT USED CURRENTLY - BROKEN##
        P1BULLET=[]     #removes both bullets to allow players to shoot again
        P2BULLET=[]
        pygame.mixer.Sound.play(hit) #play our hit sound
        if player1Shot == True:
            windowSurface.fill((0,0,0), p1PlayArea) #blank P1's play area
        elif player2Shot == True:
            windowSurface.fill((0,0,0), p2PlayArea) #blank P2's play area
        pygame.display.update()     
        pygame.time.delay(500) #Stop game for half a second, substitute for invincibility frames

    #Game end function
    def someoneWon():
        windowSurface.fill((0,0,0), gameSurface) #clear the game screen to remove the fence and players
        if player1Won == True: #check who won
            windowSurface.blit(p1WinTextLine1, [90, 240]) #display text 
            windowSurface.blit(playerWinTextLine2, [250, 350])  
        elif player2Won == True:
            windowSurface.blit(p2WinTextLine1, [70, 240])
            windowSurface.blit(playerWinTextLine2, [250, 350])
        pygame.display.update() #update the game screen to show who won
        pygame.time.delay(2000) #pause game logic for 2 seconds for winning player to bask in their win
        main() #restart game logic, AKA go back to title screen

    #clears screen for when we go back here from our game loop
    windowSurface.fill((0,0,0), gameSurface) 

    #game has been properly set up, check if we want to display the title screen
    if titleScreenEnable == True:
        titleScreen()

    #Our main game loop
    while True:

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
                    moveLeft1 = True
                elif event.key == K_w:
                    moveUp1 = True
                elif event.key == K_s:
                    moveDown1 = True
                elif event.key == K_d:
                    moveRight1 = True
                elif event.key == K_LCTRL:
                    if P1BULLET==[]:
                        pygame.mixer.Sound.play(gunshot)
                        P1BULLET=[playerRect1.left+73, playerRect1.top+47]

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
                        P2BULLET=[playerRect2.left-33, playerRect2.top+47]
                    
            elif event.type == pygame.KEYUP:

                # Player 1
                if event.key == K_a:
                    moveLeft1 = False
                elif event.key == K_w:
                    moveUp1 = False
                elif event.key == K_s:
                    moveDown1 = False
                elif event.key == K_d:
                    moveRight1 = False

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
        handle_player1_movement(playerRect1, moveLeft1, moveRight1, moveUp1, moveDown1)
        handle_player2_movement(playerRect2, moveLeft2, moveRight2, moveUp2, moveDown2)

        #Render the main game interface over the title screen
        windowSurface.fill((0,0,0), gameSurface) #overwrite title graphics with a black void
        windowSurface.blit (FENCES, [490, 100]) #the fences blocking off both players from each other

        #Scoring System sprite display loop, Player 1
        scoreList = [ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, ELEVEN, TWELVE, THIRTEEN, FOURTEEN, FIFTEEN]
        for i in range(len(scoreList)): #run through the list
            if P1SCORE == i: #does P1's score match the place in the list?
                windowSurface.blit(scoreList[i], [88 ,18]) #put the appropritate number on the screen
            if P2SCORE == i:
                windowSurface.blit(scoreList[i], [846, 18])

        #check to see if a player has won        
        if P1SCORE >= 15: #if the score ever equals or exceeds 15 (this should never happen but it prevents the game from continuing if it ever does)
            player1Won = True #set up someoneWon function
            someoneWon() #run function
        elif P2SCORE >= 15: #the same thing for Player 2
            player2Won = True
            someoneWon()

        #Draw the player sprites based on their rectangle
        windowSurface.blit(PLAYER, [playerRect1.left, playerRect1.top])
        windowSurface.blit(pygame.transform.flip(PLAYER, 1, 0), [playerRect2.left, playerRect2.top]) #flip the sprite for Player 2

        #Bullet calculations and display
        if not P1BULLET==[]:    #checks if bullet is currently on screen
            if not P1BULLET[0]>=WINDOWWIDTH:    #if has gone off side of screen
                windowSurface.blit(BULLET, P1BULLET)    #display
                P1BULLET[0]+=15      #adds 15 units to x value, moving the bullet in turn
                if P1BULLET[0]>= playerRect2.left and P1BULLET[0]<= playerRect2.right:      #checks if within horizontal bounding box of other player
                    if P1BULLET[1]>= playerRect2.top and P1BULLET[1]<= playerRect2.bottom:  #checks if within vertical bounding box of other player
                        P1BULLET=[]     #removes bullet
                        P2BULLET=[]
                        pygame.mixer.Sound.play(hit)
                        windowSurface.fill((0,0,0), p2PlayArea)
                        pygame.display.update()
                        P1SCORE += 1
                        pygame.time.delay(500)
            else:
                P1BULLET=[] #allows the player to shoot another bullet if it's gone off screen
                
        if not P2BULLET==[]: #repeat of other section, but with slight modifications to work for the 2nd player bullet
            if not P2BULLET[0]<=0:
                windowSurface.blit(pygame.transform.flip(BULLET, 1, 0), P2BULLET) #flip P2's bullet
                P2BULLET[0]-=15
                if P2BULLET[0]>= playerRect1.left and P2BULLET[0]<= playerRect1.right:
                    if P2BULLET[1]>= playerRect1.top and P2BULLET[1]<= playerRect1.bottom:
                        P2BULLET=[]
                        P1BULLET=[]
                        pygame.mixer.Sound.play(hit)
                        windowSurface.fill((0,0,0), p1PlayArea)
                        pygame.display.update()
                        P2SCORE += 1
                        pygame.time.delay(500)
            else:
                P2BULLET=[]

        pygame.display.flip()
        clock.tick(60) #make the clock tick 60 times per second, the number in the brackets is our FPS
           
main() #do the game loop
