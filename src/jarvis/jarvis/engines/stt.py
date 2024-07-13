# MIT License

# Copyright (c) 2019 Georgios Papachristou

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import speech_recognition as sr
import time

import jarvis
from jarvis.core.console import ConsoleManager


class STTEngine:
    """
    Speech To Text Engine (STT)

    Google API Speech recognition settings
    SpeechRecognition API: https://pypi.org/project/SpeechRecognition/2.1.3
    """

    def __init__(self):
        super().__init__()
        self.console_manager = ConsoleManager()
        self.console_manager.console_output(info_log="Configuring Mic..")
        self.recognizer = sr.Recognizer()  # Capture the input audio
        self.recognizer.pause_threshold = 0.5  # when to stop listening
        self.microphone = sr.Microphone()  # initialize the microphone object
        self.console_manager.console_output(info_log="Microphone configured successfully!")

    def recognize_input(self, already_activated=False):
        """
        Recognize input from mic and returns transcript if activation tag (assistant name) exist
        """

        while True:
            transcript = self._recognize_speech_from_mic()  # voice input recognizer
            if already_activated or self._activation_name_exist(transcript):  # remove activation
                transcript = self._remove_activation_word(transcript)  # activation word remover
                return transcript
            else:
                print("Give a command with Activation word ('jarvis')")

    def _recognize_speech_from_mic(self):
        """
        Capture the words from the recorded audio (audio stream --> free text).
        Transcribe speech recorded from `microphone`.
        """

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Reduce noise when capturing audio
            audio = self.recognizer.listen(source)  # Listen to the audio from the microphone
            """with open('src/jarvis/jarvis/skills/collection/Speaker_identification/SampleData/speech.wav', 'wb') as f:
            	f.write(audio.get_wav_data())"""

        try:
            transcript = self.recognizer.recognize_google(audio).lower()  # Convert audio to text using Google STT engine
            self.console_manager.console_output(info_log='User said: {0}'.format(transcript))
        except sr.UnknownValueError:
            # Speech was unintelligible
            transcript = ''
            self.console_manager.console_output(info_log='Unable to recognize speech', refresh_console=False)
        except sr.RequestError as e:
            # API was unreachable or unresponsive
            transcript = ''
            error_message = f"Google API request error: {str(e)}"
            self.console_manager.console_output(error_log=error_message)
        except Exception as e:
            transcript = 'Failed'
            error_message = f"Speech recognition error: {str(e)}"
            self.console_manager.console_output(error_log=error_message)

        return transcript

    @staticmethod
    def _activation_name_exist(transcript):
        """
        Identifies the assistant name in the input transcript.
        """

        if transcript:
            transcript_words = transcript.split()
            print("Words captured:", transcript_words)
            return bool(
                set(transcript_words).intersection([jarvis.assistant_name]) or set(transcript_words).intersection(
                    ['jarvis']))  # Return True
        else:
            return False

    @staticmethod
    def _remove_activation_word(transcript):
        transcript = transcript.replace(jarvis.assistant_name, '')
        return transcript
