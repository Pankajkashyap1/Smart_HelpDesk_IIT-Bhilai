[![CodeFactor](https://www.codefactor.io/repository/github/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai/badge)](https://www.codefactor.io/repository/github/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai)
[![Maintainability](https://api.codeclimate.com/v1/badges/8c90305e22186cc2c9d5/maintainability)](https://codeclimate.com/github/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai/maintainability)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://app.travis-ci.com/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai.svg?branch=master)](https://app.travis-ci.com/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai)

![alt text](https://github.com/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai/blob/master/imgs/jarvis_logo.png)

# Jarvis - An Intelligent AI Help Desk assistant 
Jarvis is a smart voice commanding assistant service for help desk in IIT Bhilai.
It can recognise human face and take input through recognise there speech, talk to user and execute basic commands.

It can provide information about IIT Bhilai campus facilities, academic programs, events, and resources. Need to know about the schedule for an upcoming seminar? Simply ask, and the assistant will retrieve the details instantly.

# Objective of Project
Create a smart voice assistant for help desk of  IIT Bhilai 
By implementing a smart voice assistant, the project aims to streamline the help desk process and provide quick and accurate responses to user inquiries.

Personalisation and User Engagement: The integration of efficient face recognition technology enables the assistant to personalise interactions with individuals. Recognising users by name, understanding their preferences, and tailoring responses accordingly enhances the sense of belonging and satisfaction within the IIT Bhilai community.

The aim is to create a state-of-the-art help desk system that leverages AI and face recognition technology to optimise efficiency, personalise interactions, and enhance the overall help desk experience for students, faculty, and staff at IIT Bhilai.

#### Requirements

* Operation system: **Ubuntu 20.04 (Focal Fossa)**
* Python Version: **3.8.x**


#### Assistant Skills 
*   **Tell me about IIT Bhilai**,(e.g 'how many courses are offered by IIT Bhilai')
*   **Tell me about events**,(e.g 'events, events list, create events')
*   **Recognise me**,(e.g 'jarvis detect my face')
*   **Opens a web page** (e.g 'Jarvis open wikipedia, YouTube')
*   **Increase/decrease** the speakers master volume (also can set max/mute speakers volume) (e.g 'Jarvis volume up!')
*   **Tells about something**, by searching on the internet (e.g 'Jarvis tells me about oranges')
*   **Tells the weather** for a place (e.g 'Jarvis tell_the_skills me the weather in London')
*   **Tells the current time and/or date** (e.g 'Jarvis tell me time or date')

#### Assistant Features
*   **Asynchronous command execution & speech recognition and interpretation**
*   Supports **user input mode (speech)**, user speek in the mic.
*   Answers in **general questions** (via call Wolfram API), e.g ('Jarvis tell me the highest building')
*   By using **BERT model** Jarvis gives the answer of all the queries related to IIT Bhilai
*   **Change input mode on run time**, triggered by a phrase e.g 'Jarvis change settings')
*   Easy **voice-command customization**
*   **Log preview** in console
*   **Vocal or/and text response**
*   **Keeps commands history and learned skills** in MongoDB.'

## Getting Started
### Create KEYs for third party APIs
Jarvis assistant uses third party APIs for speech recognition,web information search, weather forecasting etc.
All the following APIs have free no-commercial API calls. Subscribe to the following APIs in order to take FREE access KEYs.
*   [OPENAI](https://platform.openai.com/account/api-keys): API for openAI services.
*   [OpenWeatherMap](https://openweathermap.org/appid): API for weather forecast.
*   [WolframAlpha](https://developer.wolframalpha.com/portal/myapps/): API for answer questions.
*   [IPSTACK](https://ipstack.com/signup/free): API for current location.
### Setup Jarvis in Ubuntu/Debian system
* Download the Jarvis repo locally:
```bash
git clone https://github.com/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai.git --branch master
```

**Run the requirements.txt and install all the tools**:
```bash
python -m pip install requirements.txt
```
*Install MongoDB*
```bash
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#std-label-install-mdb-community-ubuntu
```
*   Change working directory and activate Environment
```bash
cd Jarvis
```
```bash
source jarvis_virtualenv/bin/activate
```
*   Setup Jarvis and system dependencies:
```bash
bash setup.sh
```

*   Put the Keys in settings

**NOTE:** *For better exprerience, before you start the application you can put the free KEYs in the settings.py*

```bash
nano Jarvis/src/jarvis/jarvis/setting.py
```

### Start voice commanding assistant
![alt text](https://github.com/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai/blob/master/imgs/Jarvis_printscreen.PNG)

*   Start the assistant service:
```bash
bash run_jarvis.sh
```

### How to add a new Skill to assistant
You can easily add a new skill in two steps.
*   Create a new configurationin SKILLS in **skills/registry.py**
```python
{ 
  'enable': True,
  'func': Skills.new_skill,
  'tags': 'tag1, tag2',
  'description': 'skill description..'
}               
```
*   Create a new skill module in **skills/collection**

### Desicion Model
![alt text](https://github.com/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai/blob/master/imgs/desicion_model.png)

### Extract skill
The skill extraction implement in a matrix of [TF-IDF features](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) for each skill.
In the following example he have a dimensional space with three skills.
The user input analyzed in this space and by using a similarity metric (e.g cosine) we find the most similar skill.
![alt text](https://github.com/Pankajkashyap1/Smart_HelpDesk_IIT-Bhilai/blob/master/imgs/skill_space_desicion.png)

---

