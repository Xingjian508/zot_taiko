import pygame
import sys
import random
import threading
from taiko_game.drum import Drum
from taiko_game.note import Note
from taiko_game.message import Message
from taiko_game.find_frequency import find_frequency

class Game:
  def __init__(self):
    pygame.init()
    self.drum_path = 'assets/drum.png'
    self.note1_path = 'assets/note1.png'
    self.note2_path = 'assets/note2.png'
    self.background_path = 'assets/background.png'
    self.SCREEN_WIDTH = 1200
    self.SCREEN_HEIGHT = 900
    self.WHITE = (255, 255, 255)
    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    pygame.display.set_caption('Taiko no Tatsujin')
    self.drum_image = pygame.image.load(self.drum_path)
    self.note1_image = pygame.image.load(self.note1_path)
    self.note2_image = pygame.image.load(self.note2_path)
    self.background_image = pygame.image.load(self.background_path)
    self.background_image = pygame.transform.scale(self.background_image, (1200, 900))
    self.drums = pygame.sprite.Group()
    self.notes = pygame.sprite.Group()
    self.drum = Drum(0, self.SCREEN_HEIGHT // 2 - self.drum_image.get_height() + 45, self.drum_image)
    self.drums.add(self.drum)
    self.score = 0
    self.font = pygame.font.Font(None, 74)
    self.message_font = pygame.font.Font(None, 50)
    self.message = ""
    self.message_timer = 0
    self.message_duration = 1000
    self.last_action_time = 0
    self.clock = pygame.time.Clock()
    self.running = True
    self.count = 0
    self.index = 0
    self.interval = find_frequency()
    self.lock = threading.Lock()
    self.logic_thread = threading.Thread(target=self.game_logic)
    self.logic_thread.daemon = True

  def run(self):
    self.logic_thread.start()
    while self.running:
      self.handle_events()
      self.draw()
      self.clock.tick(60)

    pygame.quit()
    sys.exit()

  def game_logic(self):
    while self.running:
      with self.lock:
        self.add_notes()
        self.update_notes()
      pygame.time.delay(1000 // 60)

  def handle_events(self, left_click=False, right_click=False):
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_f:
          self.last_action_time = current_time
          with self.lock:
            self.check_hit('note1', current_time)
        elif event.key == pygame.K_j:
          self.last_action_time = current_time
          with self.lock:
            self.check_hit('note2', current_time)
    if left_click:
      self.last_action_time = current_time
      with self.lock:
        self.check_hit('note1', current_time)
    if right_click:
      self.last_action_time = current_time
      with self.lock:
        self.check_hit('note2', current_time)
 

  def check_hit(self, note_type, current_time):
    hits = pygame.sprite.spritecollide(self.drum, self.notes, False)
    hit_detected = False
    for hit in hits:
      if hit.note_type == note_type:
        hit.kill()
        self.score += 10
        hit_detected = True
        self.message = "Hit!"
        self.message_timer = current_time
        print(f"Hit {note_type}!")
    if not hit_detected:
      self.message = "Empty Hit!"
      self.message_timer = current_time

  def add_notes(self):
    if self.index < len(self.interval) and self.interval[self.index] - 50 < self.count < self.interval[self.index] + 50:
      note_type = 'note1' if random.randint(0, 1) == 0 else 'note2'
      note_image = self.note1_image if note_type == 'note1' else self.note2_image
      note = Note(self.SCREEN_WIDTH, self.SCREEN_HEIGHT // 2 - 58, 5, note_image, note_type)
      self.notes.add(note)
      self.count = 0
      self.index += 1
      if self.index >= len(self.interval):
        self.running = False
    self.count += 7.5

  def update_notes(self):
    out_message = Message('')
    self.notes.update(out_message)
    if out_message.message == 'miss':
      self.message = "MISS!"
      self.message_timer = pygame.time.get_ticks()

  def draw(self):
    self.screen.blit(self.background_image, (0, 0))
    self.drums.draw(self.screen)
    self.notes.draw(self.screen)
    score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
    self.screen.blit(score_text, (10, 10))
    current_time = pygame.time.get_ticks()
    if current_time - self.message_timer < self.message_duration:
      message_text = self.message_font.render(self.message, True, self.WHITE)
      self.screen.blit(message_text, (self.SCREEN_WIDTH // 2 - message_text.get_width() // 2, self.SCREEN_HEIGHT // 4 - message_text.get_height() // 2))
    pygame.display.flip()
