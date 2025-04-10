from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt
import time

# Load environment variables
env_vars = dotenv_values(".env")
InputLang = env_vars.get("InputLang")

# HTML code for speech recognition
Htmlcode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (webkitSpeechRecognition || SpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Update the language in the HTML
Htmlcode = str(Htmlcode).replace("recognition.lang = '';", f"recognition.lang = '{InputLang}';")
with open(r"Data\\voices.html", "w") as f:
    f.write(Htmlcode)

# Set up Edge options
current_dir = os.getcwd()
link = f"{current_dir}/Data/voices.html"

edge_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
edge_options.add_argument(f'user-agent={user_agent}')
edge_options.add_argument("--use-fake-ui-for-media-stream")
edge_options.add_argument("--use-fake-device-for-media-stream")
edge_options.add_argument("--headless")  # Enable headless mode

# Initialize the Edge WebDriver
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

# Define the path for temporary files
TempDirPath = rf"{current_dir}/Frontend/Files"

# Function to set the assistant's status
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify queries
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "can you", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

# Function to translate text
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function for speech recognition
def SpeechRecognition():
    driver.get("file:///" + link)
    driver.find_element(by=By.ID, value="start").click()

    while True:
        try:
            Text = driver.find_element(by=By.ID, value="output").text

            if Text:
                driver.find_element(by=By.ID, value="end").click()
                if InputLang.lower() == "en" or "en" in InputLang.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating ... ")
                    return QueryModifier(UniversalTranslator(Text))
                
            time.sleep(0.5)  # Small delay to prevent CPU overload

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(1)  # Pause before retrying

# Main loop to continuously recognize speech

