from abc import ABC, abstractmethod


class UserInterface(ABC):
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        pass

    @abstractmethod
    def show_output(self, output: str) -> None:
        pass


class Console_UserInterface(UserInterface):
    def get_input(self, prompt: str) -> str:
        return input(prompt)

    def show_output(self, output: str) -> None:
        print(output)
