import tkinter as tk


def calculate(operation):
    try:
        first = float(first_entry.get())
        second = float(second_entry.get())

        if operation == "+":
            answer = first + second
        elif operation == "-":
            answer = first - second
        elif operation == "*":
            answer = first * second
        elif operation == "/":
            if second == 0:
                result_label.config(text="Cannot divide by zero")
                return
            answer = first / second

        result_label.config(text=f"Result: {answer:g}")

    except ValueError:
        result_label.config(text="Please enter two numbers")


window = tk.Tk()
window.title("Simple Calculator")
window.geometry("320x250")

tk.Label(window, text="First number:").pack(pady=(15, 0))
first_entry = tk.Entry(window)
first_entry.pack()

tk.Label(window, text="Second number:").pack(pady=(10, 0))
second_entry = tk.Entry(window)
second_entry.pack()

button_frame = tk.Frame(window)
button_frame.pack(pady=15)

for symbol in ["+", "-", "*", "/"]:
    tk.Button(
        button_frame,
        text=symbol,
        width=4,
        command=lambda op=symbol: calculate(op)
    ).pack(side="left", padx=4)

result_label = tk.Label(window, text="Result:")
result_label.pack()

window.mainloop()
