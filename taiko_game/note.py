import pygame

class Note(pygame.sprite.Sprite):
  def __init__(self, x, y, speed, note_image, note_type):
    super().__init__()
    self.image = note_image
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.speed = speed
    self.note_type = note_type
    self.missed = False

  def update(self, out_message):
    self.rect.x -= self.speed
    if self.rect.right < 0:
      out_message.miss()
      self.kill()
      self.missed = True
