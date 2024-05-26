import pygame

class Drum(pygame.sprite.Sprite):
  def __init__(self, x, y, drum_image):
    super().__init__()
    self.image = drum_image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
