import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from animation import fig
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- GUI Setup ---
root = tk.Tk()
root.title("Mini AI Assistant")
root.geometry("600x500")

label = tk.Label(root, text="Mini AI Assistant", font=("Arial", 18, "bold"))
label.pack()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(root, height=10, width=70, font=("Arial", 10))
output_text.pack(pady=10)

def update_output_text(text):
    output_text.insert(tk.END, text + "\n")
    output_text.yview(tk.END)

# --- Greet User ---
def greet():
    current_hour = datetime.now().hour
    if 4 <= current_hour < 12:
        return "Good morning!"
    elif 12 <= current_hour < 16:
        return "Good afternoon!"
    elif 16 <= current_hour <= 20:
        return "Good evening!"
    else:
        return "It's your working time"