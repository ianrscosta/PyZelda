import pygame
from settings import *

from tile import Tile
from player import Player
from debug import debug
from support import *


class Level:
    def __init__(self):

        # get display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):

        layouts = {
            'boundary': import_csv_layout('Map/map_FloorBlocks.csv')
        }

        # drawing the map
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                      x = col_index * TILESIZE
                      y = row_index * TILESIZE
                      if style == 'boundary':
                          Tile((x, y), [self.obstacle_sprites], 'invisible')

        # starting the player
        self.player = Player(
            (2000, 1400), [self.visible_sprites], self.obstacle_sprites)

    def run(self):

        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # setting up the camera
        super().__init__()

        # getting the middle of the screen to fix the camera to it
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(
            'Graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # using the offset to draw the floor without moving the player from the middle
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # updatinng the position of all the sprites that are not the floor or the player
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
