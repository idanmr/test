import tkinter

from GUI.home_screen import ResourceUI


def main():
    root: tkinter.Tk = tkinter.Tk()
    app: ResourceUI = ResourceUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
