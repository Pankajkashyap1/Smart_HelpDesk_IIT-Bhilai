import cv2
import os
import time
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

# Haar cascade XML file for face detection
face_cascade = cv2.CascadeClassifier('/Users/pankaj/Documents/project1/Jarvis_voice_to_voice/src/jarvis/jarvis/skills/haarcascade_frontalface_default.xml')

# Directory to store the generated dataset
dataset_dir = '/Users/pankaj/Documents/project1/Jarvis_voice_to_voice/src/jarvis/jarvis/skills/collection/image/dataset'
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

def recognize_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Please state your name:")
        audio = r.record(source, duration=5)

    try:
        name = r.recognize_google(audio)
        return name
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    return ""

def is_person_in_dataset(dataset_dir, face_img):
    for name in os.listdir(dataset_dir):
        person_dir = os.path.join(dataset_dir, name)
        if os.path.isdir(person_dir):  # Check if it's a directory
            for filename in os.listdir(person_dir):
                image_path = os.path.join(person_dir, filename)
                known_face = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                result = cv2.matchTemplate(known_face, face_img, cv2.TM_CCOEFF_NORMED)
                similarity = result[0][0]
                if similarity > 0.7:
                    return True, name

    return False, ""

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save('speech.mp3')
    playsound('speech.mp3')
    os.remove('speech.mp3')

def generate_dataset_from_camera():
    cap = cv2.VideoCapture(0)
    known_faces = {}
    name=""
    terminate = False  # Flag to indicate if the process should be terminated

    while not terminate:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

        if len(faces) > 0:
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                face_detected, name = is_person_in_dataset(dataset_dir, face_img)

                if face_detected:
                    speak(f"Hello {name}!")
                    terminate = True
                else:
                    speak("Please state your name.")
                    name = recognize_speech()

                    if name:
                        dataset_subdir = os.path.join(dataset_dir, name)
                        if not os.path.exists(dataset_subdir):
                            os.makedirs(dataset_subdir)
                        face_filename = f'{name}_{str(int(time.time()))}.jpg'
                        face_path = os.path.join(dataset_subdir, face_filename)
                        cv2.imwrite(face_path, face_img)
                        print(f'Saved face: {face_path}')
                        speak(f"Hello {name}!")
                        terminate = True

                break

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) == ord('q'):
            terminate = True

        if "bye" in name.lower():  # Terminate if the name contains "bye" (assuming it's the exit keyword)
            terminate = True

    cap.release()
    cv2.destroyAllWindows()

generate_dataset_from_camera()
