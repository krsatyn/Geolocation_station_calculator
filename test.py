import tkinter as tk
master = tk.Tk()
def focusText(event):
   w.config(state='normal')
   w.focus()
   w.config(state='disabled')



w = tk.Text(master, height=1, borderwidth=0)
w.insert(1.0, "Hello, world!")
w.pack()

w.configure(state="disabled")

w.bind('<Button-1>', focusText) 

master.mainloop()