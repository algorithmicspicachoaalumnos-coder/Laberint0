import pygame
import sys

pygame.init()

# Ventana
win_width = 700
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Maze")

clock = pygame.time.Clock()

# Fondo predeterminado
try:
    background = pygame.transform.scale(
        pygame.image.load("background.jpg"),
        (win_width, win_height)
    )
except:
    background = pygame.Surface((win_width, win_height))
    background.fill((0, 0, 0))

# Clase base
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, x, y, speed):
        super().__init__()
        try:
            img = pygame.image.load(image_name)
            self.image = pygame.transform.scale(img, (65, 65))
        except:
            self.image = pygame.Surface((65, 65))
            self.image.fill((255, 0, 255))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Jugador
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 65:
            self.rect.y += self.speed

# Enemigo
class Enemy(GameSprite):
    def __init__(self, image_name, x, y, speed, start, end):
        super().__init__(image_name, x, y, speed)
        self.direction = 1
        self.start = start
        self.end = end

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.x <= self.start or self.rect.x >= self.end:
            self.direction *= -1

# Pared
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# COLOR DE LAS PAREDES
WALL_COLOR = (0, 255, 0)

# Jugador y enemigo
player = Player("hero.png", 5, win_height - 80, 4)
enemy = Enemy("cyborg.png", 500, win_height - 250, 3, 500, win_width - 65)

# Grupo de paredes
walls = pygame.sprite.Group()

# Crear paredes 
wall_data = [
    (200, 200, 10, 400),   # pared 1 parte superior
    (350, 0, 10, 300), # pared 2 parte inferior
    (500, 200, 10, 400),   # pared 3 parte superior
]

for x, y, w, h in wall_data:
    wall = Wall(x, y, w, h, WALL_COLOR)
    walls.add(wall)

# Loop principal
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.blit(background, (0, 0))

    player.update()
    enemy.update()

    player.reset()
    enemy.reset()

    for wall in walls:
        wall.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()