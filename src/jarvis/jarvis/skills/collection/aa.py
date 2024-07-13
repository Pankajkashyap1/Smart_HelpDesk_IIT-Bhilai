import subprocess
from jarvis.skills.skill import AssistantSkill

class face_recog(AssistantSkill):
  def call_face(voice_transcript,skill):
    subprocess.call(["python3", "/Users/pankaj/Documents/project1/Jarvis_voice_to_voice/src/jarvis/jarvis/skills/face_recog.py"])