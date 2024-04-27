import numpy as np
import pygame 
from network import Network
import time
import random
import rsa

playerID = random.randint(1, 100000)

width = 1024
height = 768
rows = 20 

skins = {
    "red": "assets/ghost_red.png",
    "green": "assets/ghost_green.png",
    "blue": "assets/ghost_blue.png",
    "yellow": "assets/ghost_yellow.png",
    "orange": "assets/ghost_orange.png",
    "purple": "assets/ghost_purple.png",
    "cyan": "assets/ghost_cyan.png",
    "white": "assets/ghost_white.png",
    "gray": "assets/ghost_gray.png",
    "black": "assets/ghost_black.png",
} 
skins_list = list(skins.values())

def drawBg(w, surface):
    global rows
    bg_dungeon = pygame.image.load("assets/dungeon.png")
    bg_dungeon = pygame.transform.scale(bg_dungeon, (w, w))
    surface.blit(bg_dungeon, (0,0))

    sizeBtwn = w // rows

    x = 0
    y = 0
    line_color = (255,255,255,0)
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

    #    pygame.draw.line(surface, (line_color), (x, 0),(x,w))  #rysowanie linii grid jak sie poruszaja postacie
    #    pygame.draw.line(surface, (line_color), (0, y),(w,y))

def drawThings(surface, positions, skin):
    global width, rows
    dis = width // rows
    sprite = pygame.image.load(skin)
    #sprite = pygame.transform.scale(sprite, (dis-2, dis-2))  # skalowanie spritea zeby miescil sie w kratce

    for pos_id, pos in enumerate(positions):
        i, j = pos
        surface.blit(sprite, (i * dis + 1, j * dis + 1))


def draw(surface, players):
    global skins_list

    surface.fill((0,0,0))
    drawBg(width, surface)
    for i, player in enumerate(players) : 
        skin = skins_list[i % len(skins_list)]
        drawThings(surface, player, skin = skin) 
    pygame.display.update()


def main():
    
    win = pygame.display.set_mode((width,height))
    
    n = Network()
    # Send key to server

    # Generate key pair
    public_key, private_key = rsa.newkeys(1024)
    public_partner = False
    # print(public_key, private_key)
    # tuple_as_string = json.dumps(public_key) 

    #Send public key
    n.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(n.recv())
    print("Public partner",public_partner)
    
    #Handle recieved ServerKey
    # Convert the string back to a tuple
    #restored_tuple = json.loads(tuple_as_string)
    #print(restored_tuple)

    flag = True
    
    #Send the client public key to the server
    #n.send()
    
    while flag:
        events = pygame.event.get()
        pos = None 
        ignore = False
        if len(events) > 0 :
            
            for event in events : 
                if event.type == pygame.QUIT:
                    flag = False
                    pos = n.send("quit", receive=True) 
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pos = n.send("left", receive = True)
                    elif event.key == pygame.K_RIGHT:
                        pos = n.send("right", receive = True)
                    elif event.key == pygame.K_UP:
                        pos = n.send("up", receive = True)
                    elif event.key == pygame.K_DOWN:
                        pos = n.send("down", receive = True)

                elif event.type == pygame.KEYUP:
                    # Send a 'stop' command when any movement key is released
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        pos = n.send("stop", receive=True)
        else:
            if ignore == False:
                pos = n.send("get", receive = True)
        
        players = []
        
        if pos is not None: 
            #print(pos)
            raw_players = pos.split("**")

            if raw_players == '' : 
                pass 
            else : 
                for raw_player in raw_players :
                    raw_positions = raw_player.split("*")
                    if len(raw_positions) == 0 :
                        continue
                    
                    positions = []
                    for raw_position in raw_positions :
                        if raw_position == "" :
                            continue
                        nums = raw_position.split(')')[0].split('(')[1].split(',')
                        positions.append((int(nums[0]), int(nums[1])))
                    players.append(positions)

        else:
            if pos is not None:
                print(pos)
            

        draw(win, players)
    
if __name__ == "__main__":
    main()