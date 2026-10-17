import tkinter as tk

count = 0


def add_one():
    global count
    count += 1
    label.config(text=f"Count: {count}")


window = tk.Tk()
window.title("Click Counter")
window.geometry("300x180")

label = tk.Label(window, text="Count: 0", font=("Arial", 20))
label.pack(pady=20)

button = tk.Button(window, text="Click me!", command=add_one)
button.pack()

window.mainloop()
