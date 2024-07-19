import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

def calculate_bmi(weight, height):
    return (weight / (height ** 2))

def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_data(name, weight, height, bmi, category):
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records
                      (name TEXT, weight REAL, height REAL, bmi REAL, category TEXT)''')
    cursor.execute("INSERT INTO bmi_records VALUES (?, ?, ?, ?, ?)",
                   (name, weight, height, bmi, category))
    conn.commit()
    conn.close()

def show_history():
    conn = sqlite3.connect('bmi_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bmi_records")
    records = cursor.fetchall()
    conn.close()

    if records:
        names, weights, heights, bmis, categories = zip(*records)
        plt.figure(figsize=(10, 5))
        plt.plot(names, bmis, marker='o', linestyle='-')
        plt.xlabel('Names')
        plt.ylabel('BMI')
        plt.title('BMI Trend')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Info", "No historical data found.")

def on_calculate():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        name = entry_name.get().strip()
        if not name:
            raise ValueError("Name cannot be empty")
        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)
        result_var.set(f"Your BMI is: {bmi:.2f}\nCategory: {category}")
        save_data(name, weight, height, bmi, category)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Set up the GUI
root = tk.Tk()
root.title("BMI Calculator")

# Increase the size of the window
root.geometry("400x300")

tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0, padx=10, pady=5)
entry_weight = tk.Entry(root)
entry_weight.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Height (m):").grid(row=2, column=0, padx=10, pady=5)
entry_height = tk.Entry(root)
entry_height.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Calculate BMI", command=on_calculate).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Show History", command=show_history).grid(row=4, column=0, columnspan=2, pady=10)

result_var = tk.StringVar()
tk.Label(root, textvariable=result_var, wraplength=300, justify="center").grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
