from src.mode import Mode, BaseMode, BeginningMode, PracticeMode, TrainMode
from src.keyboard import OnScreenKeyboard
from src.typing_app import TypingApp, InputBox, BodyForm
from functools import partial
import time
import npyscreen

if __name__ == "__main__":
    app = TypingApp()
    app.run()
