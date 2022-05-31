import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):

        # setting up the player
        super().__init__(groups)
        self.image = pygame.image.load(
            './Graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        # setting up the hitbox
        self.hitbox = self.rect.inflate(0, -26)

        # stting up movement variables
        self.direction = pygame.math.Vector2()
        self.speed = 5

        # setting up the collision sprites
        self.obstacle_sprites = obstacle_sprites

    def input(self):

        # keyboard listenner
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):

        # moving the player
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):

        # colliding the player on horizontal moves
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right

        # colliding the player on vertical moves
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top

    def update(self):

        # calling the functions
        self.input()
        self.move(self.speed)
