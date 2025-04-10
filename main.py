from Frontend. GUI import (
GraphicalUserInterface,
SetAssistantStatus,
ShowTextToScreen,
TempDirPath,
SetMicrophoneStatus,
AnswerModifier,
QueryModifier,
GetMicrophoneStatus,
GetAssistantStatus )
from Backend.decision_maker import FirstLayerDMM
from Backend.Automation import Automation
from Backend. STT import SpeechRecognition
from Backend.general_Ai import ChatBot
from Backend. TTS import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may i help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    File = open(r'Data\ChatLog.json',"r", encoding='utf-8')
    if len(File.read())<5:
        with open(TempDirPath('Database.data'), 'w', encoding='utf-8') as file:
            file.write("")

        with open(TempDirPath('Responses.data'), 'w', encoding='utf-8') as file:
            file.write(DefaultMessage)

def ReadChatLogJson():
    with open(r'Data\\ChatLog.json', 'r', encoding='utf-8') as file:
        chatlog_data = json. load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson( )
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content' ]}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content' ]}\n"

    formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant",Assistantname + " ")

    with open(os.path.join(TempDirPath, 'Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    # Correct file path construction
    file_path = os.path.join(TempDirPath, 'Database.data')

    # Open the file with 'with' to ensure it gets closed automatically
    with open(file_path, "r", encoding='utf-8') as file:
        data = file.read()

    # Check if the data is not empty
    if len(data) > 0:
        lines = data.split('\n')
        result = '\n'.join(lines)

        # Now write the result to 'Responses.data'
        response_file_path = os.path.join(TempDirPath, 'Responses.data')
        with open(response_file_path, "w", encoding='utf-8') as file:
            file.write(result)

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def MainExecution():

    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening ... ")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking ... ")
    Decision = FirstLayerDMM(Query)

    print("")
    print(f"Decision : {Decision}")
    print("")

    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime") ])

    Mearged_query = " and ".join(
        ["".join(i.split()[1:])for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True

    for queries in Decision:
        if TaskExecution == False:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

    if ImageExecution == True:

        with open(r"Frontend\\Files\\Image.data", "w") as file:
            file.write(f"{ImageGenerationQuery},True")

        try:

            p1 = subprocess. Popen(['python', r'Backend\\Image.py'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess. PIPE, shell=False)
            subprocesses.append(p1)

        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if G and R or R:

        SetAssistantStatus("Searching ... ")
        Answer = ChatBot(QueryModifier(Mearged_query))
        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ... ")
        TextToSpeech(Answer)
        return True

    else:

        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking ... ")
                QueryFinal = Queries.replace("general ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ... ")
                TextToSpeech(Answer)
                return True

            elif "realtime" in Queries:
                SetAssistantStatus("Searching ... ")
                QueryFinal = Queries.replace("realtime ", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ... ")
                TextToSpeech(Answer)
                return True
            
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname} : {Answer}")
                SetAssistantStatus("Answering ... ")
                TextToSpeech(Answer)
                SetAssistantStatus("Answering ... ")
                os ._exit(1)

def FirstThread():

    while True:

        CurrentStatus = GetMicrophoneStatus( )

        if CurrentStatus == "True":
            MainExecution()

        else:
            AIStatus = GetAssistantStatus()

            if "Available ... " in AIStatus:
                sleep(0.1)

            else:
                SetAssistantStatus("Available ... ")

def SecondThread():
    GraphicalUserInterface()

if __name__ == "__main__":
    thread2 = threading. Thread(target=FirstThread, daemon=True)
    thread2.start()
    SecondThread()