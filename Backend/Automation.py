from AppOpener import close, open as appopen # Import functions to open and close apps.
from webbrowser import open as webopen # Import web browser functionality.
from pywhatkit import search, playonyt # Import functions for Google search and YouTube playback.
from dotenv import dotenv_values # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup # Import BeautifulSoup for parsing HTML content.
from rich import print # Import rich for styled console output.
from groq import Groq # Import Groq for AI chat functionalities.
import webbrowser # Import webbrowser for opening URLs.
import subprocess # Import subprocess for interacting with the system.
import requests # Import requests for making HTTP requests.
import keyboard # Import keyboard for keyboard-related actions.
import asyncio # Import asyncio for asynchronous programming.
import os # Import os for operating system functionalities.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey") # Retrieve the api


# classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZØLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
# "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e",
# "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# Initialize the Groq client with the API key.
client =Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
"Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
"I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]
# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os. environ['Username']}, You're a content writer. You have to write content like letter"}]

# Function to perform a Google search.
def GoogleSearch(Topic):
    search(Topic) # Use pywhatkit's search function to perform a Google search.
    return True
# Function to generate content using AI and save it to a file.
def Content(Topic):
    # Ensure the Data directory exists
    if not os.path.exists('Data'):
        os.makedirs('Data')

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        try:
            completion = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=SystemChatBot + messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None
            )
            Answer = ''

            for chunk in completion:
                if chunk.choices[0].delta.content:
                    Answer += chunk.choices[0].delta.content

            Answer = Answer.replace("</s>", "")
            messages.append({"role": "assistant", "content": Answer})
            return Answer
        except Exception as e:
            print(f"Error generating content: {e}")
            return "Error generating content."

    Topic = Topic.replace("Content ", "").strip()
    ContentByAI = ContentWriterAI(Topic)

    # Save the generated content to a text file
    try:
        with open(rf"Data\{Topic.lower().replace(' ', '_')}.txt", "w", encoding="utf-8") as file:
            file.write(ContentByAI)
    except Exception as e:
        print(f"Error saving content to file: {e}")

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '_')}.txt")
    return True

# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" # Construct the YouTube search URL.
    webbrowser.open(Url4Search) # Open the search URL in a web browser.
    return True # Indicate success.

def PlayYoutube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True # Indicate success.

# Function to open an application or a relevant webpage.
def OpenApp(app):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)  # Attempt to open the app
        return True  # Indicate success
    except:
        print("app not found")

def CloseApp(app):

    if "edge" in app:
        pass # Skip if the app is Chrome.
    else:
        try:

            close(app, match_closest=True, output=True, throw_error=True)
            return True # Indicate success.
        except :
            return False # Indicate failure.
        
def System(command):

    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")

    # Nested function to unmute the system volume.
    def unmute():
        keyboard. press_and_release("volume mute")

    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up") # Simulate the volume un key press.

    def volume_down():
        keyboard.press_and_release("volume down")

# Execute the appropriate command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down( )

    return True

async def TranslateAndExecute(commands: list[str]):

    funcs = [] # List to store asynchronous tasks.

    for command in commands:

        if command.startswith("open "): # Handle "open" commands.

            if "open it" in command: # Ignore "open it" commands.
                pass

            if "open file" == command: # Ignore "open file" commands.
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) # Schedule app oper
                funcs.append(fun)

        elif command.startswith("general "): # Placeholder for general commands.
            pass

        elif command.startswith("realtime "): # Placeholder for real-time commands.
            pass

        elif command.startswith("close "): # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "): # Handle "play" commands.
            fun = asyncio. to_thread(PlayYoutube, command. removeprefix("play "))

        elif command.startswith("content "): # Handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content"))
            funcs.append(fun)

        elif command.startswith("google search "): # Handle Google search commands.
            fun = asyncio.to_thread(GoogleSearch, command. removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "): # Handle YouTube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search ")) # Schedule YouTube search.
            funcs.append(fun)

        elif command.startswith("system "): # Nandle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*funcs) 

    for result in results: # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynenronous function to automate command execurion.
async def Automation(commands: list[str]):

    async for result in TranslateAndExecute(commands): 
        pass

    return True

# Print an error for unrecognized commands.
