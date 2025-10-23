import tkinter as tk


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("CBSE Database Manager")
        self.root.geometry("700x400")

    def __str__(self) -> str:
        return "Window of geometry 700x400"

    def __repr__(self) -> str:
        return ""


def main() -> None:
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    print(f"Currently running {__file__} script.")  # .split('\\')[-1]
    main()
