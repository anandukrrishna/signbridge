# import cv2
# import pickle
# import mediapipe as mp
# import numpy as np
# import time
# from deep_translator import GoogleTranslator
# from gtts import gTTS
# from playsound import playsound
# import os




# # ==============================
# # Load trained model
# # ==============================
# with open(r"D:\ISLtranslator\ISLtranslator\data\isl_model.pkl", "rb") as f:
#     model = pickle.load(f)

# # ==============================
# # Mediapipe setup
# # ==============================
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(
#     static_image_mode=False,
#     max_num_hands=1,
#     min_detection_confidence=0.7
# )
# mp_drawing = mp.solutions.drawing_utils

# # ==============================
# # Translator
# # ==============================
# translator = GoogleTranslator(source='en', target='ml')

# # ==============================
# # Sentence variables
# # ==============================
# sentence = ""
# last_sign = None
# same_sign_counter = 0
# last_spoken_time = time.time()


# def generate_frames():
#     global sentence, last_sign, same_sign_counter, last_spoken_time

#     # 🔴 OPEN CAMERA INSIDE GENERATOR
#     cap = cv2.VideoCapture(0)

#     try:
#         while True:
#             success, frame = cap.read()
#             if not success:
#                 break

#             frame = cv2.flip(frame, 1)
#             img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = hands.process(img_rgb)

#             sign_label = None

#             if results.multi_hand_landmarks:
#                 for hand_landmarks in results.multi_hand_landmarks:
#                     landmarks = []
#                     for lm in hand_landmarks.landmark:
#                         landmarks.extend([lm.x, lm.y, lm.z])

#                     X = np.array(landmarks).reshape(1, -1)
#                     sign_label = model.predict(X)[0]

#                     mp_drawing.draw_landmarks(
#                         frame,
#                         hand_landmarks,
#                         mp_hands.HAND_CONNECTIONS
#                     )

#             # ==============================
#             # Sentence logic
#             # ==============================
#             if sign_label is not None:
#                 if sign_label == last_sign:
#                     same_sign_counter += 1
#                 else:
#                     same_sign_counter = 0

#                 if same_sign_counter == 30:
#                     if sign_label == "space":
#                         sentence += " "
#                     else:
#                         sentence += sign_label
#                     same_sign_counter = 0

#                 last_sign = sign_label
#                 last_spoken_time = time.time()

#             else:
#                 if time.time() - last_spoken_time > 3 and sentence.strip():
#                     malayalam_text = translator.translate(sentence)

#                     tts = gTTS(text=malayalam_text, lang="ml")
#                     tts.save("malayalam.mp3")
#                     playsound("malayalam.mp3")
#                     os.remove("malayalam.mp3")

#                     sentence = ""
#                     last_spoken_time = time.time()

#             # ==============================
#             # Display text
#             # ==============================
#             cv2.putText(frame, f"Current: {sign_label}", (10, 40),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#             cv2.putText(frame, f"Sentence: {sentence}", (10, 80),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

#             # ==============================
#             # Encode frame
#             # ==============================
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     except GeneratorExit:
#         print("Client disconnected")

#     finally:
#         # ✅ CAMERA RELEASED HERE
#         cap.release()
#         cv2.destroyAllWindows()
#         print("Camera released successfully")



# ///////////////////////////////////////////////////////////////////////


from django.conf import settings

import time

# ==============================
# GLOBALS (lazy initialized)
# ==============================
model = None
hands = None
translator = None

sentence = ""
last_sign = None
same_sign_counter = 0
last_spoken_time = time.time()
import cv2
import numpy as np

def initialize():
    
    import pickle
    import mediapipe as mp
    import os

    from deep_translator import GoogleTranslator


    """Initialize heavy resources ONLY when video starts"""
    global model, hands, translator

    if model is None:
        model_path = os.path.join(settings.BASE_DIR, "data", "isl_model.pkl")
        with open(model_path, "rb") as f:
            model = pickle.load(f)

    if hands is None:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7
        )

    if translator is None:
        translator = GoogleTranslator(source="en", target="en")


def generate_frames():
    initialize()
    from gtts import gTTS
    from playsound import playsound
    import os



    global sentence, last_sign, same_sign_counter, last_spoken_time

    cap = cv2.VideoCapture(1)

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            sign_label = None

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = []
                    for lm in hand_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])

                    X = np.array(landmarks).reshape(1, -1)
                    sign_label = model.predict(X)[0]

            # ==============================
            # Sentence logic
            # ==============================
            if sign_label is not None:
                if sign_label == last_sign:
                    same_sign_counter += 1
                else:
                    same_sign_counter = 0

                if same_sign_counter == 30:
                    sentence += " " if sign_label == "space" else sign_label
                    same_sign_counter = 0

                last_sign = sign_label
                last_spoken_time = time.time()

            else:
                if time.time() - last_spoken_time > 4 and sentence.strip():
                    mal_text = translator.translate(sentence)

                    tts = gTTS(text=mal_text, lang="ta")
                    tts.save("temp.mp3")
                    playsound("temp.mp3")
                    os.remove("temp.mp3")

                    sentence = ""
                    last_spoken_time = time.time()

            # ==============================
            # DISPLAY TEXT ON FRAME
            # ==============================
            current_text = sign_label if sign_label else "Detecting..."
            display_sentence = sentence[-40:]

            cv2.putText(
                frame,
                f"Current: {current_text}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Sentence: {display_sentence}",
                (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,0, 0),
                2
            )

            # ==============================
            # STREAM FRAME
            # ==============================
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )

    finally:
        cap.release()
        cv2.destroyAllWindows()