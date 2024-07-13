import os
import speech_recognition as sr
from gtts import gTTS
import playsound
import pandas as pd
from jarvis.skills.skill import AssistantSkill

class EventSkill(AssistantSkill):
    def __init__(self):
        self.dataset_path = "/Users/pankaj/Documents/project1/Jarvis_voice_to_voice/src/jarvis/jarvis/skills/collection/input/event_dataset.csv"
        self.events = self.load_dataset()

    def load_dataset(self):
        if os.path.isfile(self.dataset_path):
            return pd.read_csv(self.dataset_path)
        else:
            return pd.DataFrame(columns=["Name", "Date", "Venue", "Details"])

    def call_event(self, skill, voice_transcript):
        # Initialize the speech recognition engine
        recognizer = sr.Recognizer()

        while True:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)

            try:
                # Convert the voice input to text
                voice_transcript = recognizer.recognize_google(audio)
                print("User: " + voice_transcript)

                if "event" in voice_transcript:
                    self.handle_add_event()
                elif "history" in voice_transcript:
                    self.handle_get_event_names()
                elif "about" in voice_transcript:
                    self.handle_get_event_information()
                elif "delete" in voice_transcript:
                    self.handle_delete_event()
                elif "jarvis" in voice_transcript:
                    break  # Exit the loop when "exit" command is spoken
                else:
                    self.speak_text("Unrecognized command.")

            except sr.UnknownValueError:
                self.speak_text("Sorry, I could not understand your speech.")
            except sr.RequestError:
                self.speak_text("Sorry, I'm currently experiencing technical issues with speech recognition. Please try again later.")

    def handle_add_event(self):
        self.speak_text("Please provide the event name.")
        event_name = self.get_user_input()

        self.speak_text("Please provide the event date.")
        event_date = self.get_user_input()

        self.speak_text("Please provide the event venue.")
        event_venue = self.get_user_input()

        self.speak_text("Please provide event details.")
        event_details = self.get_user_input()

        self.add_event(event_name, event_date, event_venue, event_details)

    def handle_get_event_names(self):
        if self.events.empty:
            self.speak_text("No events available.")
        else:
            self.speak_text("Here are the event names:")
            for event_name in self.events["Name"]:
                self.speak_text(event_name)

    def handle_get_event_information(self):
        if self.events.empty:
            self.speak_text("No events available.")
        else:
            self.speak_text("Here is the information about the events:")
            for _, event in self.events.iterrows():
                self.speak_text(f"Event: {event['Name']}")
                self.speak_text(f"Date: {event['Date']}")
                self.speak_text(f"Venue: {event['Venue']}")
                self.speak_text(f"Details: {event['Details']}")

    def handle_delete_event(self):
        if self.events.empty:
            self.speak_text("No events available to delete.")
            return

        self.speak_text("Please provide the name of the event to delete.")
        event_name = self.get_user_input()

        if event_name not in self.events["Name"].values:
            self.speak_text("Event not found.")
            return

        self.events = self.events[self.events["Name"] != event_name]
        self.speak_text("Event deleted successfully!")

    def add_event(self, event_name, event_date, event_venue, event_details):
        event = {
            "Name": event_name,
            "Date": event_date,
            "Venue": event_venue,
            "Details": event_details
        }

        self.events = pd.concat([self.events, pd.DataFrame(event, index=[0])], ignore_index=True)
        self.save_dataset()
        self.speak_text("Event added successfully!")

    def save_dataset(self):
        os.makedirs(os.path.dirname(self.dataset_path), exist_ok=True)
        self.events.to_csv(self.dataset_path, index=False)

    def get_user_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)

            try:
                user_input = recognizer.recognize_google(audio)
                print("User Input: " + user_input)
                return user_input

            except sr.UnknownValueError:
                self.speak_text("Sorry, I could not understand your speech.")
            except sr.RequestError:
                self.speak_text("Sorry, I'm currently experiencing technical issues with speech recognition. Please try again later.")

    def speak_text(self, text):
        tts = gTTS(text=text, lang='en')
        tts.save('output.mp3')
        playsound.playsound('output.mp3')
