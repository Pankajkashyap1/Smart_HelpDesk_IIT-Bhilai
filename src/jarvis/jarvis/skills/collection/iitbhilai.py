import subprocess
from jarvis.skills.skill import AssistantSkill

class IITSkill(AssistantSkill):
  def call_chatbot(self,voice_transcript,skill):
    # Call the chatbot.py file using subprocess
    subprocess.call(["python3", "/Users/pankaj/Documents/project1/Jarvis_voice_to_voice/chatbot-main/chatbot.py"])


