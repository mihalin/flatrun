import tkinter as tk
from typing import List
import logging
from argparse import ArgumentParser
from resources import icon_path
from flatpak import applications, run


class FlatRunner(tk.Frame):

    width = 40
    height = 8

    def __init__(self, master=None):
        super().__init__(master)

        self.__applications = applications()

        self.master = master
        self.pack()

        sv = tk.StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: self.edited(sv))

        self.__input = tk.Entry(self, width=self.width, textvariable=sv)
        self.__input.bind('<Return>', (lambda _: self.run()))
        self.__input.bind("<KeyRelease-Up>", (lambda _: self.keyup()))
        self.__input.bind("<KeyRelease-Down>", (lambda _: self.keydown()))
        self.__input.pack(side="top")

        self.__choices = tk.Listbox(self, width=self.width, height=self.height, selectmode=tk.SINGLE)
        self.__choices.pack(side="bottom")
        self.__choices.bind("<Return>", (lambda _: self.run()))
        self.__choices.bind("<KeyRelease-Up>", (lambda _: self.keyup()))
        self.__choices.bind("<KeyRelease-Down>", (lambda _: self.keydown()))

        self.__input.focus()

    def edited(self, var):
        filtered = self.__filter(var.get())
        self.__choices.delete(0, self.__choices.size())
        for i, val in enumerate(filtered):
            self.__choices.insert(i, val)
        if self.__choices.size():
            self.__choices.selection_set(0, 0)

    def run(self):
        selected = self.__choices.curselection()
        if selected:
            app = self.__choices.get(selected[0])
            run(app)
            exit(0)

    def keyup(self):
        selected = self.__choices.curselection()
        if selected and selected[0] > 0:
            self.__choices.selection_clear(selected[0])
            self.__choices.selection_set(selected[0] - 1)

    def keydown(self):
        selected = self.__choices.curselection()
        if selected and selected[0] < self.__choices.size() - 1:
            self.__choices.selection_clear(selected[0])
            self.__choices.selection_set(selected[0]+1)

    def __filter(self, search: str) -> List[str]:
        if not search:
            return []
        return list(
            filter(lambda x: search.lower() in x.lower(),
                   self.__applications)
        )[:self.height]  # limit with maximum


if __name__ == '__main__':
    root = tk.Tk(className="flatrun")
    root.resizable(0, 0)

    try:
        root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=icon_path))
    except Exception as err:
        logging.error(err)
        pass  # icon is not so important ...

    app = FlatRunner(master=root)

    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)

    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))

    app.mainloop()
