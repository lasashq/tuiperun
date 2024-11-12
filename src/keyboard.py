from pathlib import Path


class OnScreenKeyboard:
    """class which controls the OnScreenKeyboard and highlights needed symbol"""
    def __init__(self, symbol):
        self.file_path = Path(__file__).parent.parent / \
            'assets' / 'keyboard.txt'
        with self.file_path.open('r') as file:
            self.keyboard = file.readlines()
        # here comes a million of if statements

        if symbol == " ":
            self.keyboard = [
                line.replace(" Space ", "[Space]") for line in self.keyboard
            ]

        self.ShiftToggle = (
            False  # shift is not pressed as default, but we will check it
        )
        if ord(symbol) in range(65, 91):  # if capital letter
            self.ShiftToggle = True
        if ord(symbol) in range(97, 122):
            symbol = chr(
                ord(symbol) - 32
            )  # if small letter, make it capital to lazy-replace

        # here i was too lazy to create a dictionary for all the symbols
        if symbol == '"':
            self.ShiftToggle = True
            symbol = "'"
        if symbol == "?":
            self.ShiftToggle = True
            symbol = "/"

        self.keyboard = [
            line.replace("┊ " + symbol + " ┊", "┃[" + symbol + "]┃")
            for line in self.keyboard
        ]  # highlighting the self symbol
        if self.ShiftToggle:
            self.keyboard = [
                line.replace(" ⇧ ", "[⇧]") for line in self.keyboard
            ]  # highlighting shift, if needed
        if symbol == "⌫":
            self.keyboard = [
                line.replace(" ⌫ ", "[⌫]") for line in self.keyboard
            ]  # highlighting backspace, if user is mistaken
