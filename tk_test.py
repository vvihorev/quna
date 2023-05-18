import tkinter as tk


root = tk.Tk()

def callback(event):
    print(f"Caught {event.keysym}")
    if (event.state & 4 > 0):
        print(f"Caught {event.keysym}")

t = tk.Text(root)

root.bind("<Key>", callback)
t.pack()
root.mainloop()
