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
import subprocess
from jarvis import settings  # default settings: assistant name, input mode etc.
from jarvis.utils.startup import internet_connectivity_check
from jarvis.core.processor import Processor
from jarvis.core.console import ConsoleManager


def main():
    """
    Do initial checks, clear the console and print the assistant logo.
    """

    console_manager = ConsoleManager() # output console
    console_manager.console_output(info_log='Wait a second for startup checks..')
    internet_connectivity_check()      # check the internet connectivity for online commands
    console_manager.console_output(info_log='Application started')
    console_manager.console_output(info_log="I'm ready! Say something :-)")
    subprocess.call(["python3", "/Users/pankaj/Documents/project1/Jarvis_voice_to_voice/src/jarvis/jarvis/core/face_recog.py"])

    # jaggu start from here with default setting:
    # 'assistant_name': 'Jaggu',
    # 'input_mode': VOICE,
    # 'response_in_speech': True,
    processor = Processor(console_manager=console_manager, settings_=settings) 

    while True:
        processor.run()


if __name__ == '__main__':
    main()

