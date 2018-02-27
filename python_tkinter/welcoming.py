import tkinter as tk

LARGE_FONT = ("Verdana", 12)

class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="bottom", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=2)
        container.grid_columnconfigure(0, weight=2)

        self.frames = {}

        frame = StartPage(container, self)

        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def qf(quickPrint):
    print(quickPrint)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome To Desk Borrowing System", font=LARGE_FONT)
        label.pack(pady=20, padx=20)

        button = tk.Button(self, text="Enter NRIC",)
        button.pack()

app = SeaofBTCapp()
app.mainloop()