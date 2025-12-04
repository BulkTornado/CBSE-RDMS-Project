import tkinter as tk

from functional_modules import ConnectToMySQL


class MainWindow:
    def __init__(self):
        self._root = tk.Tk()
        self._root.title("CBSE Database Manager")
        self._root.geometry("700x400")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb_value):
        print("Window closed")

    def __str__(self) -> str:
        return "Window of geometry 700x400"

    def __repr__(self) -> str:
        return ""

    def start(self):
        self._root.mainloop()


def main() -> None:
    root = MainWindow()
    root.start()


if __name__ == "__main__":
    print(f"Currently running {__file__} script.")
    main()
