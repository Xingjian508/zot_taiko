from signal_storage import SignalStorage
from identifier_double import run_identifier
import threading
import cv2
import time

def print_storage(storage: SignalStorage):
  while not storage.signal['terminate']:
    for key in storage.signal:
      if not key == 'frame':
        print(f'{key}: {storage.signal[key]}')
    # print(storage.signal)
    time.sleep(1)

if __name__ == "__main__":
  storage = SignalStorage()
  storage.signal['terminate'] = False

  cv2.namedWindow('Hand Tracking')
  cv2.resizeWindow('Hand Tracking', 1280, 720)
  cap = cv2.VideoCapture(0)

  t1 = threading.Thread(target=run_identifier, args=(storage, cap))
  t2 = threading.Thread(target=print_storage, args=(storage,))

  t1.start()
  t2.start()

  while not storage.signal['terminate']:
    if 'frame' in storage.signal:
      cv2.imshow('Hand Tracking', storage.signal['frame'])
    if cv2.waitKey(1) & 0xFF == ord('q'):
      storage.signal['terminate'] = True

  t1.join()
  t2.join()

  cap.release()
  cv2.destroyAllWindows()
  print("Done!")
