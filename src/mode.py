import random
from pathlib import Path  # to run from any dir

class Mode:
    """main mode class"""
    def __init__(self) -> None:
        self.name = None
        self.file_path = Path(__file__).parent.parent / \
            'assets' / 'dictionary' / 'beginning.txt'
        self.len = 75
    def to_type(self) -> str:  
        """returns a string to type"""
        raise NotImplementedError("this must be in subclasses")

    def get_random_word(self) -> str:
        """gets random word from file"""
        with self.file_path.open("r") as file:
            words = [
                line.strip() for line in file if line.strip()
            ]  # Remove whitespace lines
        return random.choice(words) + " "


class BeginningMode(Mode):
    """subclass for beginning mode"""
    def __init__(self):
        super().__init__()
        self.name = "BeginningMode"

    def to_type(self, ):
        word = self.get_random_word()
        # Calculate how many times to repeat
        words_needed = self.len // len(word)
        return word * words_needed


class BaseMode(Mode):
    def __init__(self):
        super().__init__()
        self.name = "BaseMode"

    def to_type(self):
        line = ""
        while True:
            word = self.get_random_word()
            if len(word + line) > self.len - 2:
                return line
            line = line + word  # filling the line with different words


class TrainMode(Mode):
    def __init__(self):
        super().__init__()
        self.name = "TrainMode"

    def to_type(self):
        return (
            self.get_random_word() * 3
        )  # only 3 same words, but no margin for error


class PracticeMode(Mode):
    def __init__(self):
        super().__init__()
        self.index = random.randint(1000, 140000)
        self.name = "PracticeMode"
        self.file_path = self.file_path = Path(
            __file__).parent.parent / 'assets' / 'dictionary' / 'churchill.txt'

    def to_type(self):
        with self.file_path.open("r") as file:
            lines = file.readlines()
        self.index += 1  # print lines in sequence
        return lines[self.index % len(lines)].strip() + " "
