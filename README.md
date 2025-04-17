# 🤖 Yuri AI Assistant

**Yuri** is an intelligent AI assistant designed to provide real-time interactions using speech recognition, decision-making, home automation, and image generation. It’s built with a modular structure, separating backend logic, data storage, and the user interface for clarity and scalability.

---

## 🧠 Overview

- **Name:** Yuri AI Assistant  
- **Architecture:** Modular (Backend, Frontend, Data)  
- **Key Features:**  
  - Speech-to-text & Text-to-speech  
  - AI decision-making  
  - Task & home automation  
  - Image generation with AI  
- **Main Entry Point:** `main.py`

---


---

## 🧩 Component Breakdown

### 🔙 Backend

The backend contains all the AI functionalities:

- `Automation.py`: Handles task automation features.
- `decision_maker.py`: Core decision-making system using logic or AI models.
- `general_Ai.py`: General-purpose intelligent processing.
- `Home_Ai.py`: Automates home-based tasks and IoT control.
- `Image.py`: Generates visuals using AI image models.
- `STT.py`: Converts spoken words into text (speech-to-text).
- `TTS.py`: Converts text into audio output (text-to-speech).

### 💾 Data

All logs, AI-generated content, and test files are stored here:

- `ChatLog.json`: Tracks all conversations with Yuri.
- `Generated Images/`: Directory storing images created by the assistant.
- `speech.mp3`: Latest voice output file.
- `voices.html`: A utility page to test voice outputs.

### 🎨 Frontend

User interface components, system data, and UI visuals:

- `GUI.py`: The core file for the graphical user interface.
- `Files/`: Stores runtime data like mic status, responses, and more.
- `Graphics/`: Contains visuals used in the assistant UI (icons, animations).

### 🚀 Entry Point

- `main.py`: Main script that initializes all systems and runs Yuri.

---

## ⚙️ Installation & Setup

### ✅ Prerequisites

Make sure you have the following installed:

- Python 3.8+ (recommended latest version)
- `pip` (Python package manager)

---

## ✨ Credits

Built with ❤️ by [Sujay K R Samal](https://github.com/sujay-kr-samal)



