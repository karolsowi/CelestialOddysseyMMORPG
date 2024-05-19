import pygame
import random
import tkinter as tk
from tkinter import messagebox
import os

class Cube:
    rows = 20
    w = 500

    def __init__(self, start, skin="assets/ghost.png"):
        self.pos = start
        if os.path.exists(skin):
            self.skin = pygame.image.load(skin)
            self.skin = pygame.transform.scale(self.skin, (self.w // self.rows, self.w // self.rows))
        else:
            self.skin = pygame.image.load("assets/ghost.png")
            self.skin = pygame.transform.scale(self.skin, (self.w // self.rows, self.w // self.rows))

    def move(self, dirnx, dirny):
        self.pos = (self.pos[0] + dirnx, self.pos[1] + dirny)

    def draw(self, surface):
        dis = self.w // self.rows
        surface.blit(self.skin, (self.pos[0] * dis + 1, self.pos[1] * dis + 1))

class Player:
    def __init__(self, skin, pos):
        self.head = Cube(pos, skin)
        self.dirnx = 0
        self.dirny = 0  

    def move(self, key):
        if key == 'left':
            self.dirnx = -1
        if key == 'right':
            self.dirnx = 1
        if key == 'up':
            self.dirny = -1
        if key == 'down':
            self.dirny = 1
        if key == 'stop_x':
            self.dirnx = 0
        if key == 'stop_y':
            self.dirny = 0
        self.head.move(self.dirnx, self.dirny)

    def draw(self, surface):
        self.head.draw(surface)

    def get_pos(self):
        return str(self.head.pos)

class Game:

    def __init__(self, rows) : 
        self.rows = rows
        self.players = {} 
    
    def add_player(self, user_id, skin) : 
        self.players[user_id] = Player(skin, (10,10))
    
    def remove_player(self, user_id) :
        self.players.pop(user_id)
    
    def move(self, moves) :
        moves_ids = set([m[0] for m in moves])
        still_ids = set(self.players.keys()) - moves_ids 
        for move in moves : 
            self.move_player(move[0], move[1])

        for still_id in still_ids :
            self.move_player(still_id, None)

    def move_player(self, user_id, key = None) : 
        self.players[user_id].move(key)

    def get_player(self, user_id) : 
        return self.players[user_id].head.pos
    
    def get_state(self) : 
        players_pos = [p.get_pos() for p in self.players.values()]
        players_pos_str = "**".join(players_pos)

        return players_pos_str
    
    
if __name__ == "__main__":
    pass