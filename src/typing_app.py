import time
from functools import partial
from typing import List
from src.mode import Mode, BaseMode, BeginningMode, PracticeMode, TrainMode
from src.keyboard import OnScreenKeyboard
import npyscreen



class TypingApp(npyscreen.NPSAppManaged):  # main class of my app, pretty small XD
    """class of npyscreen app which contains one form"""
    def onStart(self) -> None:
        self.form = self.addForm(
            "MAIN",
            BodyForm,
            name="TUIperun",
            lines=29,
            columns=85,
        )


class InputBox(npyscreen.BoxTitle):
    """npyscreen widget class for making input field inside the box"""
    _contained_widget = (
        npyscreen.MultiLineEdit
    )  # defining an npyscreen module which is editable text line inside the box


class BodyForm(npyscreen.FormBaseNew):
    """main form of my application"""        
    def create(self) -> None:

        # definition of variables and objects
        if not hasattr(self, "app_mode"):
            self.app_mode = BeginningMode()  # setting initial mode
        if not hasattr(self, "zenmode"):
            self.zenmode = 0  # zenmode is disabled
        self.to_type = (
            self.app_mode.to_type()
        )  # getting the text to type from mode class
        self.start_time = None  # begiinning of typing the line
        self.typing_speed = None
        
        self.user_info = [
            "       ctrl + A: BaseMode    ctrl + T: TrainMode    ctrl + L: PracticeMode",
            "",
            "     ctrl + B: BeginningMode    ctrl + F: ZenMode    enter: to start and retry  ",
            "",
            "                              ctrl + Q: Quit",
        ]
        self.add_handlers(  # keybinds setup
            {
                "^Q": self.quit,
                "^A": lambda _: self.switch_to_mode(BaseMode()),
                "^T": lambda _: self.switch_to_mode(TrainMode()),
                "^L": lambda _: self.switch_to_mode(PracticeMode()),
                "^B": lambda _: self.switch_to_mode(BeginningMode()),
                "^F": lambda _: self.toggle_zenmode(),
            }
        )

        # Widgets (modules in body of my app)

        self.title = self.add(
            npyscreen.TitleFixedText,
            value=self.app_mode.name,
            name="Current Mode:",
            max_height=1,
        )  # shows the name of current mode

        self.input_box = (
            self.add(  # shows the input field (type was defined in the InputBox class)
                InputBox,
                name="",
                max_width=80,
                rely=3,
                max_height=3,
                value="",
            )
        )
        self.input_box.when_value_edited = partial(
            self.check_input
        )  # an action to do when we type sth
        self.symbol = self.to_type[
            len(self.input_box.value)
        ]  # getting the next symbol to type

        self.text = self.add(
            npyscreen.FixedText,
            value=self.to_type,  # showing the text to type
            rely=6,
            relx=4,
            max_height=1,
        )

        self.keyboard_widget = self.add(
            npyscreen.MultiLine,
            values=OnScreenKeyboard(symbol=self.symbol).keyboard,
            editable=False,
            max_height=12,
            relx=8,
        )  # getting the keyboard layout with the self.symbol highlighted from the class
        self.user_keybinds = self.add(
            npyscreen.MultiLine, values=self.user_info, rely=22, relx=1, max_height=5
        )
        self.type_speed_widget = self.add(
            npyscreen.TitleFixedText,
            rely=20,
            relx=15,
            name="Speed:",
            value=f"{self.typing_speed} LPM",
            max_height=1,
        )  # showing typing speed

    def toggle_zenmode(self) -> None:
        """switches zenmode on/off"""
        self.zenmode = 1 - self.zenmode
        self.keyboard_widget.hidden = self.zenmode == 1
        self.keyboard_widget.update(clear=True)

    def display_keyboard(self) -> None:
        """updates onscreen keyboard"""
        self.keyboard_widget.values = OnScreenKeyboard(
            symbol=self.symbol).keyboard
        self.keyboard_widget.update(clear=False)

    def switch_to_mode(self, new_mode) -> None:
        """switches between modes"""
        self.app_mode = new_mode
        self.to_type = self.app_mode.to_type()

        self.title.value = self.app_mode.name

        self.text.value = self.to_type

        self.input_box.value = ""
        self.symbol = self.to_type[len(self.input_box.value)]
        self.display_keyboard()
        self.title.update(clear=False)
        self.input_box.update(clear=False)
        self.text.update(clear=True)
        self.display_keyboard()

    def completed_line(self) -> None:
        """action to do when we have completed typing the line"""
        self.inputbox_clear()
        self.typing_speed = round(
            60 * len(self.to_type) // (time.time() - self.start_time)
        )  # getting typing speed
        self.type_speed_widget.value = f"{self.typing_speed} LPM"
        self.type_speed_widget.update(clear=False)
        self.to_type = self.app_mode.to_type()
        self.text.value = self.to_type
        self.text.color = 'GOOD'

    def check_input(self) -> None:
        """action to do when we input sth"""
        if (
            len(self.input_box.value) >= len(self.to_type)
            and self.input_box.value != self.to_type
        ):
            self.text.color = "CRITICAL"
        if len(self.input_box.value) >= self.input_box.width - 2:
            self.inputbox_clear()
        if self.input_box.value == "":
            self.text.color = "GOOD"
            self.symbol = self.to_type[0]
            self.display_keyboard()
            self.text.update(clear=True)
            return
        if self.input_box.value[-1] == "\n":
            if self.input_box.value == self.to_type[0:-1] + "\n":
                self.completed_line()
            self.inputbox_clear()
            self.text.color = "GOOD"
            self.text.update(clear=True)
            return
        if self.input_box.value != self.to_type[: len(self.input_box.value)]:
            if self.app_mode.name == "TrainMode":
                self.text.color = "GOOD"
                self.inputbox_clear()
            else:
                self.text.color = "CRITICAL"  # mistake highlight
        else:
            self.text.color = "GOOD"
        if len(self.input_box.value) == 1:
            self.start_time = time.time()  # start timer
        if self.input_box.value == self.to_type:  # if we  have typed line till the end
            self.completed_line()
        if self.text.color == "CRITICAL":  # if mistaken
            self.symbol = "⌫"  # press backspace
        else:
            self.symbol = self.to_type[len(self.input_box.value)]
        self.title.update(clear=False)
        self.input_box.update(clear=False)
        self.display_keyboard()
        self.text.update(clear=True)
        self.user_keybinds.update(clear=False)

    def quit(self, *args, **keywords) -> None:
        """to quit the app"""
        self.parentApp.setNextForm(None)
        self.parentApp.switchFormNow()

    def inputbox_clear(self, *args, **keywords) -> None:
        """clears the inputbox"""
        self.input_box.value = ""
        self.input_box.update(clear=True)
        self.symbol = self.to_type[0]
        self.display_keyboard()
