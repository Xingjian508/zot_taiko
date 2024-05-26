import cv2
import mediapipe as mp
import numpy as np
import joblib
import warnings
from gesture_pack.signal_storage import SignalStorage

def run_identifier(storage: SignalStorage, cap):
  warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")
  warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.base")

  mp_hands = mp.solutions.hands
  mp_drawing = mp.solutions.drawing_utils

  model = joblib.load('gesture_pack/gesture_model.pkl')

  def predict_gesture(landmarks):
    landmarks = np.array(landmarks).reshape(1, -1)
    prediction = model.predict(landmarks)
    return prediction[0]

  with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened() and not storage.signal['terminate']:
      ret, frame = cap.read()
      if not ret:
        break

      height, width, _ = frame.shape
      left_frame = frame[:, :width//2]
      right_frame = frame[:, width//2:]

      left_image = cv2.cvtColor(left_frame, cv2.COLOR_BGR2RGB)
      left_image.flags.writeable = False
      left_results = hands.process(left_image)
      left_image.flags.writeable = True
      left_image = cv2.cvtColor(left_image, cv2.COLOR_RGB2BGR)

      right_image = cv2.cvtColor(right_frame, cv2.COLOR_BGR2RGB)
      right_image.flags.writeable = False
      right_results = hands.process(right_image)
      right_image.flags.writeable = True
      right_image = cv2.cvtColor(right_image, cv2.COLOR_RGB2BGR)

      gesture_don = None
      gesture_kat = None

      if left_results.multi_hand_landmarks:
        for hand_landmarks in left_results.multi_hand_landmarks:
          landmarks = []
          for landmark in hand_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
          gesture_kat = predict_gesture(landmarks)
          mp_drawing.draw_landmarks(left_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

      if right_results.multi_hand_landmarks:
        for hand_landmarks in right_results.multi_hand_landmarks:
          landmarks = []
          for landmark in hand_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
          gesture_don = predict_gesture(landmarks)
          mp_drawing.draw_landmarks(right_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

      combined_image = np.hstack((left_image, right_image))

      for i in range(0, height, 10):
        cv2.line(combined_image, (width//2, i), (width//2, i+5), (255, 255, 255), 3)

      storage.signal['frame'] = combined_image

      if gesture_don is not None or gesture_kat is not None:
        print((gesture_don, gesture_kat))
        storage.signal['don'] = gesture_don
        storage.signal['kat'] = gesture_kat
