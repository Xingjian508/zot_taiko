from gesture_pack.signal_storage import SignalStorage
from gesture_pack.identifier_double import run_identifier
from taiko_game.game import Game
import threading
import cv2
import time
import random
from pygame import mixer

def print_storage(storage: SignalStorage):
  while not storage.signal['terminate']:
    for key in storage.signal:
      if key != 'frame':
        print(f'{key}: {storage.signal[key]}')
    time.sleep(1)

def create_identifier_params():
  storage = SignalStorage()
  storage.signal['don'] = 'None'
  storage.signal['kat'] = 'None'
  storage.signal['terminate'] = False

  cv2.namedWindow('Hand Tracking')
  cv2.resizeWindow('Hand Tracking', 1280, 720)
  cap = cv2.VideoCapture(0)
  return storage, cap

def run_game_with_music():
  mixer.init()
  file = 'assets/tenkiame.mp3'
  mixer.music.load(file)
 
  storage, cap = create_identifier_params()
  game = Game()

  t1 = threading.Thread(target=run_identifier, args=(storage, cap))
  mixer.music.play()

  t1.start()

  left_zot = False
  right_zot = False
  while not storage.signal['terminate'] and mixer.music.get_busy():
    if 'frame' in storage.signal:
      cv2.imshow('Hand Tracking', storage.signal['frame'])
    if cv2.waitKey(1) & 0xFF == ord('q'):
      storage.signal['terminate'] = True
    
    new_left_zot = storage.signal['don'] == 'zot'
    new_right_zot = storage.signal['kat'] == 'zot'

    left_click = not left_zot and new_left_zot
    right_click = not right_zot and new_right_zot
    
    game.handle_events(left_click, right_click)
    with game.lock:
      game.add_notes()
      game.update_notes()
      game.draw()
    
    game.clock.tick(60)
    left_zot = new_left_zot
    right_zot = new_right_zot

  t1.join()
  cap.release()
  cv2.destroyAllWindows()
  print("Done!")

if __name__ == "__main__":
  run_game_with_music()
