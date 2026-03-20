import tkinter as tk
from tkinter import messagebox
import json, os, math
from datetime import datetime
#last edited on 20/3/26

APP_NAME = "Attendify"
DATA_FILE = "attendance_data.json"
TARGET = 75

#data
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

#logic - it sucks man :(
def calculate():
    try:
        attended = attended_entry.get().strip()
        total = total_entry.get().strip()

        if not attended or not total:
            raise ValueError("Missing lecture data")

        attended = int(attended)
        total = int(total)

        if attended > total or total <= 0:
            raise ValueError("Invalid lecture values")

        day = day_var.get()
        month = month_var.get()
        year = year_var.get()

        if not day or not month or not year:
            raise ValueError("Date not selected")

        date_key = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

        if date_key in data:
            raise ValueError("Attendance for this date already exists")

        # Save date-wise data
        data[date_key] = {
            "attended": attended,
            "total": total
        }
        save_data(data)

        # Calculate totals
        total_attended = sum(d["attended"] for d in data.values())
        total_lectures = sum(d["total"] for d in data.values())

        percent = round((total_attended / total_lectures) * 100, 2)

        bunkable = math.floor((total_attended / (TARGET / 100)) - total_lectures)
        bunkable = max(0, bunkable)

        percent_value.config(text=f"{percent} %")
        percent_value.config(fg="green" if percent >= TARGET else "red")
        bunk_value.config(text=str(bunkable))

        # Clear inputs
        attended_entry.delete(0, tk.END)
        total_entry.delete(0, tk.END)

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except:
        messagebox.showerror("Error", "Something went wrong")

#gui
#fixed app size
root = tk.Tk()
root.title(APP_NAME)
root.geometry("500x650")
root.resizable(False, False)
root.configure(bg="black")

#header and title
tk.Label(root, text="Attendify",
         font=("Segoe UI", 26, "bold"),
         fg="white", bg="black").place(x=40, y=30)

tk.Label(root,
         text="Made by - SwarajSG\nGitHub - https://github.com/Swaraj-SG",
         font=("Segoe UI", 10),
         fg="gray", bg="black", justify="left").place(x=40, y=85)

#inputs
tk.Label(root, text="Lectures attended today :",
         font=("Segoe UI", 12),
         fg="white", bg="black").place(x=40, y=150)

attended_entry = tk.Entry(root, font=("Segoe UI", 12), width=10)
attended_entry.place(x=300, y=150)

tk.Label(root, text="Total number of lectures today :",
         font=("Segoe UI", 12),
         fg="white", bg="black").place(x=40, y=190)

total_entry = tk.Entry(root, font=("Segoe UI", 12), width=10)
total_entry.place(x=300, y=190)

#date entry
tk.Label(root, text="Enter the date for the attendance :",
         font=("Segoe UI", 12),
         fg="white", bg="black").place(x=40, y=235)

day_var = tk.StringVar()
month_var = tk.StringVar()
year_var = tk.StringVar()

tk.OptionMenu(root, day_var, *[str(i) for i in range(1, 32)]).place(x=40, y=270)
tk.OptionMenu(root, month_var, *[str(i) for i in range(1, 13)]).place(x=120, y=270)
tk.OptionMenu(root, year_var,
              *[str(y) for y in range(2025, 2041)]).place(x=200, y=270)

tk.Label(root, text="date / month / year",
         font=("Segoe UI", 9),
         fg="gray", bg="black").place(x=40, y=305)

#buttons
tk.Button(root, text="Calculate",
          font=("Segoe UI", 14),
          width=18, bg="white", fg="blue",
          relief="flat",
          command=calculate).place(x=40, y=340)

tk.Label(root, text="Calculated as per 75% attendance is mandatory",
         font=("Segoe UI", 9),
         fg="gray", bg="black").place(x=40, y=385)

#output
tk.Label(root, text="Attendance % :",
         font=("Segoe UI", 14, "bold"),
         fg="yellow", bg="black").place(x=40, y=435)

percent_value = tk.Label(root, text="—",
                         font=("Segoe UI", 14, "bold"),
                         fg="white", bg="black")
percent_value.place(x=200, y=435)

tk.Label(root, text="Number of lectures you can bunk :",
         font=("Segoe UI", 14, "bold"),
         fg="orange", bg="black").place(x=40, y=485)

bunk_value = tk.Label(root, text="—",
                      font=("Segoe UI", 14, "bold"),
                      fg="white", bg="black")
bunk_value.place(x=380, y=485)

root.mainloop()
