# 🎮 Typing Attack Game for Learning Kivy Library

A educational game project demonstrating various features and capabilities of the Kivy framework through an interactive typing game. Perfect for Python developers looking to learn GUI development with Kivy.

## 📋 Table of Contents
- [Learning Objectives](#-learning-objectives)
- [Installation Requirements](#-installation-requirements)
- [Kivy Components Used](#-kivy-components-used)
- [Game Features](#-game-features)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)

## 📚 Learning Objectives

This project demonstrates the following Kivy concepts:
1. **Screen Management**
   - Multiple screen handling using `ScreenManager`
   - Screen transitions
   - Screen lifecycle management

2. **Widget System**
   - Custom widget creation
   - Widget inheritance (`BoxLayout`, `Widget`, `Screen`)
   - Dynamic widget management

3. **Event Handling**
   - Keyboard input processing
   - Touch events
   - Clock scheduling

4. **Graphics & Animation**
   - Custom drawing with canvas
   - Animation systems
   - Particle effects
   - Color management

5. **Sound System**
   - Audio loading and playback
   - Volume control
   - Multiple sound channel handling

## 🚀 Installation Requirements

1. Python Environment Setup:
```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # For Unix/MacOS
venv\Scripts\activate     # For Windows

# Install Kivy
pip install kivy
```

2. Project Setup:
```bash
git clone [your-repository]
cd typing-attack-game
```

## 🔧 Kivy Components Used

### Core Components
```python
from kivy.app import App                    # Main application class
from kivy.uix.widget import Widget          # Base widget class
from kivy.uix.screenmanager import *        # Screen management
from kivy.clock import Clock                # Event scheduling
from kivy.core.window import Window         # Window management
from kivy.core.audio import SoundLoader     # Audio handling
```

### UI Components
```python
from kivy.uix.boxlayout import BoxLayout    # Layout management
from kivy.uix.button import Button          # Button widgets
from kivy.uix.label import Label            # Text display
from kivy.uix.textinput import TextInput    # Text input field
from kivy.uix.popup import Popup            # Popup windows
```

### Graphics & Animation
```python
from kivy.animation import Animation        # Animation system
from kivy.graphics import *                 # Graphics instructions
from kivy.utils import get_color_from_hex   # Color management
```

## 🎯 Game Features

Each feature demonstrates specific Kivy capabilities:

1. **Screen Management**
   - Start Screen (Menu handling)
   - Game Screen (Main gameplay)
   - Game Over Screen (State transitions)
   - High Score Screen (Data persistence)

2. **Interactive Elements**
   - Text input system
   - Button handling
   - Dynamic scoring
   - Power-up system

3. **Visual Effects**
   - Particle systems
   - Color transitions
   - Dynamic backgrounds
   - Animation systems

## 📁 Project Structure

```
typing-attack-game/
│
├── main.py              # Main game implementation
├── words.txt            # Game content
├── high_score.txt       # Data persistence example
│
├── sound/               # Audio resources
│   ├── hit.mp3
│   ├── sound_miss.mp3
│   └── sound_sound6.mp3
│
└── README.md           # Project documentation
```

## 🎮 Key Code Examples

### Screen Management
```python
class TypingAttackApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(StartScreen(name='start'))
        screen_manager.add_widget(GameScreen(name='game'))
        return screen_manager
```

### Animation System
```python
def create_word_destroy_effect(self, pos, word_color):
    anim = Animation(
        pos=(pos[0] + dx, pos[1] + dy),
        opacity=0,
        duration=random.uniform(0.5, 1.0)
    )
    anim.start(particle)
```

### Event Handling
```python
def on_text_validate(self, instance):
    # Text input processing
    typed_word = instance.text.strip()
    # Game logic implementation
```

## 🚦 How to Run

1. Ensure all dependencies are installed
2. Navigate to the project directory
3. Run the main file:
```bash
python main.py
```

## 💡 Learning Resources

- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Kivy Examples](https://github.com/kivy/kivy/tree/master/examples)
- [Kivy Garden](https://github.com/kivy-garden)

## 🤝 Contributing

Feel free to use this project as a learning resource or extend it with your own features. Some ideas for learning exercises:
- Add new power-up types
- Implement different game modes
- Create custom animations
- Add multiplayer features
- Implement new scoring systems

## ⚠️ Note

This project is designed for educational purposes and demonstrates various Kivy features. The code is thoroughly commented to explain key concepts and implementation details.

For questions or suggestions about learning Kivy through this project, please contact the developer.
