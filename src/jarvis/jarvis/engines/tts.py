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
import queue
import threading
import time
from gtts import gTTS
from pygame import mixer

from jarvis.core.console import ConsoleManager


class TTS:
    """
    Text To Speech Engine (TTS)
    """

    def __init__(self):
        self.tts_engine = None

    def run_engine(self):
        try:
            mixer.init()
            mixer.music.load('temp.mp3')
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
        except RuntimeError:
            pass


class TTSEngine(TTS):
    def __init__(self):
        super().__init__()
        self.logger = logging
        self.message_queue = queue.Queue(maxsize=9)  # Maxsize is the size of the queue / capacity of messages
        self.stop_speaking = False
        self.console_manager = ConsoleManager()

    def assistant_response(self, message, refresh_console=True):
        """
        Assistant response in voice.
        :param refresh_console: boolean
        :param message: string
        """
        self._insert_into_message_queue(message)
        try:
            speech_thread = threading.Thread(target=self._speech_and_console, args=(refresh_console,))
            speech_thread.start()
        except RuntimeError as e:
            self.logger.error('Error in assistant response thread with message {0}'.format(e))

    def _insert_into_message_queue(self, message):
        try:
            self.message_queue.put(message)
        except Exception as e:
            self.logger.error("Unable to insert message to queue with error message: {0}".format(e))

    def _speech_and_console(self, refresh_console):
        """
        Speech method translates text batches to speech and prints them in the console.
        :param refresh_console: boolean
        """
        try:
            while not self.message_queue.empty():
                cumulative_batch = ''
                message = self.message_queue.get()
                if message:
                    self.tts_engine = gTTS(text=message, lang='en')
                    self.tts_engine.save('temp.mp3')
                    cumulative_batch += message
                    self.console_manager.console_output(cumulative_batch, refresh_console=refresh_console)
                    self.run_engine()
                    if self.stop_speaking:
                        self.logger.debug('Speech interruption triggered')
                        self.stop_speaking = False
                        break
        except Exception as e:
            self.logger.error("Speech and console error message: {0}".format(e))
