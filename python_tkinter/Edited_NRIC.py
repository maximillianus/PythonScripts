from tkinter import *
import tkinter.messagebox as tm
import os


class LoginFrame(Frame):
    def __init__(self,master):
        super().__init__(master)

        self.label_1 = Label(self, text="NRIC")
       

        self.entry_1 = Entry(self)
      

        self.label_1.grid(row=0, sticky=E)
        
        self.entry_1.grid(row=0, column=1)
       

        

        self.logbtn = Button(self, text="Login", command = self._login_btn_clickked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clickked(self):

        #print("Clicked")
        NRIC = self.entry_1.get()


        with open("C:/Users/15059258/Desktop/Testing.txt") as f:
          for line in f:

           if NRIC in line:
            tm.showinfo("Login info", "Welcome S12345678A TIME REMAINING 5 MINS")
            break
           else:
               tm.showerror("Login error", "USER NOT FOUND" )
               break
        f.close()


root = Tk()
lf = LoginFrame(root)
root.mainloop()

