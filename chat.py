import random
import json
import torch
import pyttsx3 as pp
from gtts import gTTS
import playsound
import os
from Classes.NeuralNetwork import NeuralNetwork
from Utils.nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding="utf8") as data:
    intents = json.load(data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
output_size = data["output_size"]
hidden_size = data["hidden_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]


model = NeuralNetwork(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def speak(sentence):
    tts = gTTS(text=sentence, lang='bn', slow=False)
    tts.save('bangla_bot_speak.mp3')
    playsound.playsound('bangla_bot_speak.mp3', True)
    os.remove('bangla_bot_speak.mp3')

bot_name = "সারাফাত"


def get_response(msg):
    sentence = tokenize(msg)
    x = bag_of_words(sentence, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x).to(device)

    output = model(x)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "I don't understand..."
