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

        pygame.draw.line(surface, (line_color), (x, 0),(x,w))
        pygame.draw.line(surface, (line_color), (0, y),(w,y))

def drawThings(surface, positions, skin):
    global width, rows
    dis = width // rows
    sprite = pygame.image.load(skin)
    sprite = pygame.transform.scale(sprite, (dis-2, dis-2))  # Scale sprite to fit the cell

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