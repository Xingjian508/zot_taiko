from osupyparser import OsuFile
import time
import random

def find_frequency():
  data = OsuFile(
    "assets/Usami_Hiyori_-_Tenkiame_R_Futsuu.osu").parse_file()
  info = data.__dict__
  hit_objects = None
  for d, e in info.items():
    if d == 'hit_objects':
      hit_objects = e


  time_stamp = []
  for element in hit_objects:
    time_stamp.append(element.start_time)

  intervals = []
  for n in range(len(time_stamp) - 1):
    intervals.append(time_stamp[n + 1] - time_stamp[n])
  return intervals
