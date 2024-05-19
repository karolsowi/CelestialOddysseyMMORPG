import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen dimensions
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Menu")

# Load background image
menu_bg = pygame.image.load('assets/menu_bg.png')
logo = pygame.image.load('assets/logo.png')
bg_x = 0
bg_speed = 0.25

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)

# Define fonts
font = pygame.font.Font(None, 36)

# Button class
class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.pos = pos
        self.callback = callback
        self.rect = pygame.Rect(pos[0], pos[1], 300, 50)
        self.highlighted = False

    def draw(self, screen):
        color = LIGHT_GRAY if self.highlighted else GRAY
        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.highlighted = self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.highlighted:
            self.callback()

# Input box class
class InputBox:
    def __init__(self, x, y, w, h, max_length=21, text='', input_type='text'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False
        self.max_length = max_length
        self.input_type = input_type

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = LIGHT_GRAY if self.active else WHITE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_length:
                    if self.input_type == 'number' and event.unicode.isdigit():
                        self.text += event.unicode
                    elif self.input_type == 'text':
                        self.text += event.unicode
                self.txt_surface = font.render(self.text, True, WHITE)

    def update(self):
        width = max(300, self.txt_surface.get_width())
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def draw_text(screen, text, pos):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, pos)

def join_game():
    global current_screen
    current_screen = "join"

def new_server():
    global current_screen
    current_screen = "new_server"

def quit_game():
    pygame.quit()
    sys.exit()

def go_back():
    global current_screen
    current_screen = "menu"

# Create buttons
buttons = [
    Button("Join Game", (362, 300), join_game),
    Button("New Server", (362, 400), new_server),
    Button("Quit", (362, 500), quit_game)
]

# Create back button
back_button = Button("Back", (362, 500), go_back)

# Input boxes for join game
ip_box_join = InputBox(362, 250, 300, 32, 21)
nickname_box_join = InputBox(362, 320, 300, 32, 12)

# Input boxes for new server
ip_box_server = InputBox(362, 230, 300, 32, 21)
nickname_box_server = InputBox(362, 300, 300, 32, 12)
player_limit_box = InputBox(362, 370, 300, 32, 5, '10', 'number')

# Main loop
running = True
current_screen = "menu"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_screen == "menu":
            for button in buttons:
                button.check_hover(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN and button.highlighted:
                    button.click()
        elif current_screen == "join":
            ip_box_join.handle_event(event)
            nickname_box_join.handle_event(event)
            back_button.check_hover(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.highlighted:
                back_button.click()
        elif current_screen == "new_server":
            ip_box_server.handle_event(event)
            nickname_box_server.handle_event(event)
            player_limit_box.handle_event(event)
            back_button.check_hover(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.highlighted:
                back_button.click()

    # Move background
    bg_x -= bg_speed
    if bg_x <= -menu_bg.get_width():
        bg_x = 0

    # Draw background
    screen.blit(menu_bg, (bg_x, 0))
    screen.blit(menu_bg, (bg_x + menu_bg.get_width(), 0))

    if current_screen == "menu":
        screen.blit(logo, (176, 150))
        for button in buttons:
            button.draw(screen)
    elif current_screen == "join":
        draw_text(screen, "IP Address:", (362, 220))
        ip_box_join.update()
        ip_box_join.draw(screen)
        draw_text(screen, "Nickname:", (362, 290))
        nickname_box_join.update()
        nickname_box_join.draw(screen)
        back_button.draw(screen)
    elif current_screen == "new_server":
        draw_text(screen, "IP Address:", (362, 200))
        ip_box_server.update()
        ip_box_server.draw(screen)
        draw_text(screen, "Nickname:", (362, 270))
        nickname_box_server.update()
        nickname_box_server.draw(screen)
        draw_text(screen, "Player Limit:", (362, 340))
        player_limit_box.update()
        player_limit_box.draw(screen)
        back_button.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
