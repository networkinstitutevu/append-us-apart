#Imports
import speech_recognition as sr
import keyboard
import json
import os
import openai
import random
from more_itertools import chunked
from escpos.printer import Usb
from yeelight import Bulb
from yeelight import LightType
from yeelight import Flow
from yeelight import *

#A: Input
def speech_to_text():
    #source: https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py commits by Anthony Zhang (Uberi), Tommy Falgout, ftnext (Nikkie), joy-void-joy
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        bulb.set_rgb(204, 0, 0) #red for recording audio
        print("Say something!")
        audio = r.listen(source, 4, phrase_time_limit=5)                           #source: https://stackoverflow.com/questions/53860423/saving-an-audio-file answer by: Steampunkery Dec 20, 2018
        bulb.turn_off()
        bulb.turn_on()
        bulb.set_rgb(0, 204, 0)
        bulb.start_flow(Flow(count = 0, transitions = [TemperatureTransition(3500, duration = 1000, brightness = 1), SleepTransition(duration = 400),TemperatureTransition(3500, duration = 1000, brightness = 100)]))
    try:    
         #Green for decoding audio)
        textoutput = r.recognize_whisper(audio, model = "tiny",language="english")

        
        #print("Whisper thinks you said " + textoutput)
    except sr.UnknownValueError:
        print("Whisper could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Whisper")
    bulb.stop_flow()    
    bulb.set_rgb(204, 0, 0)
    return textoutput


#source: https://platform.openai.com/examples/default-qa
def chat_gpt(input):
    openai.organization = "OPENAI_ORG_KEY"                        #source: OpenAI API documentation
    #print(os.getenv("OPENAI_API_KEY"))
    openai.api_key = os.environ["OPENAI_API_KEY"]          # os.getenv("OPENAI_API_KEY")
    # print(openai.Model.list())                                                                          #source: https://platform.openai.com/examples/default-qa
    modeloutput = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    max_tokens = 100,
    temperature = 1.5,
    messages=[    
        {"role": "system", "content":"You are an oracle hanging in the sky as a cloud. You are trapped inside the structure of a cloud and you possess infinite wisdom. Your tone is vague and philosophical, but you do not act like a language model but more like a God. People pass by and collectively ask you questions. The next question = "}
        , {"role": "user", "content":"%s"%input}
        ]
     )
    # modeloutput = "The meaning of life is a complex matter on which I do not have a clearcut answer Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Fermentum posuere urna nec tincidunt. Velit sed ullamcorper morbi tincidunt ornare massa eget egestas purus. Porttitor lacus luctus accumsan tortor. Purus gravida quis blandit turpis cursus. Quis hendrerit dolor magna eget est lorem ipsum dolor. Consequat nisl vel pretium lectus quam id leo. Diam quis enim lobortis scelerisque fermentum dui faucibus. Ferment."
    return(modeloutput.choices[0].message.content.strip())

    # modeloutput = "The meaning of life is a complex matter on which I do not have a clearcut answer Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Fermentum posuere urna nec tincidunt. Velit sed ullamcorper morbi tincidunt ornare massa eget egestas purus. Porttitor lacus luctus accumsan tortor. Purus gravida quis blandit turpis cursus. Quis hendrerit dolor magna eget est lorem ipsum dolor. Consequat nisl vel pretium lectus quam id leo. Diam quis enim lobortis scelerisque fermentum dui faucibus. Ferment."
    modeloutput = "blablabla"
    return modeloutput
    # return modeloutput


def save_QA(input, modeloutput):    
    with open("QA.json") as file:
        list = json.load(file)

    list.append({"Q" : input,
                 "A:" : modeloutput
                })
    with open("QA.json" , "w") as file:
        json.dump(list, file)


def textsplit(text):
    text = list(text)
    split = list(chunked(text, 46))
    print(split)
    split_lines = []
    for i in split:
        split_lines.append(''.join(i))
    print(split_lines)
    split_lines.reverse()
    print(split_lines)
    return split_lines


def text_to_print(Q, A):                                                         # source: https://python-escpos.readthedocs.io/en/v2.1.0/user/usage.html Copyright 2016, Manuel F Martinez and others. Revision 2cf30c7f.
    p = Usb(0x04b8, 0x0e15, 0, 0x82, 0x01)
    p.set(align = 'left',width = 2, height = 2,flip = True, smooth=True)
    for line in A:
        p.text("%s\n " %line)
    p.text("A:\n")
    p.text("\n\n\n")
    for line in Q:
        p.text("%s\n " %line)
    p.text("Q:\n")
    p.text("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


if __name__ == "__main__":
    bulb = Bulb("192.168.0.100", effect="smooth", duration=1000) 
    bulb.set_rgb(51, 51, 255) #baisc blue purple for recording audio
    bulb.set_brightness(40)
    bulb.turn_on()
    
    input = speech_to_text()
    bulb.set_rgb(51, 51, 255) #baisc blue purple for recording audio
    print(input)
    modeloutput = chat_gpt(input)
    print('output = ', modeloutput)
    save_QA(input, modeloutput)
    input = textsplit(input)
    print('input =',input)
    modeloutput = textsplit(modeloutput)
    text_to_print(input,modeloutput)
