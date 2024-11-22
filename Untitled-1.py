import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# File paths for data
ACTIVITIES_FILE = "data/activities.json"
EVENTS_FILE = "data/events.json"
BUDGET_FILE = "data/budget.json"

# Ensure data files exist
os.makedirs("data", exist_ok=True)
for file in [ACTIVITIES_FILE, EVENTS_FILE, BUDGET_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)

# Utility functions to load/save data
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file)

# Main Application Class
class ActivityManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Manager")
        self.root.geometry("800x600")

        # Tabs
        self.tab_control = ttk.Notebook(root)
        self.tab_dashboard = ttk.Frame(self.tab_control)
        self.tab_activities = ttk.Frame(self.tab_control)
        self.tab_events = ttk.Frame(self.tab_control)
        self.tab_budget = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_dashboard, text="Dashboard")
        self.tab_control.add(self.tab_activities, text="Activities")
        self.tab_control.add(self.tab_events, text="Events")
        self.tab_control.add(self.tab_budget, text="Budget")
        self.tab_control.pack(expand=1, fill="both")

        # Populate Tabs
        self.create_dashboard_tab()
        self.create_activities_tab()
        self.create_events_tab()
        self.create_budget_tab()

    def create_dashboard_tab(self):
        label = tk.Label(self.tab_dashboard, text="Welcome to the Activity Manager Dashboard!", font=("Arial", 16))
        label.pack(pady=20)

    def create_activities_tab(self):
        self.activities = load_data(ACTIVITIES_FILE)

        # UI Components
        frame = tk.Frame(self.tab_activities)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(frame, text="Activity Name:").grid(row=0, column=0, padx=5, pady=5)
        self.activity_name_entry = tk.Entry(frame)
        self.activity_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.activity_desc_entry = tk.Entry(frame)
        self.activity_desc_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame, text="Add Activity", command=self.add_activity).grid(row=2, column=1, pady=10)

        # Activity List
        self.activity_list = ttk.Treeview(frame, columns=("Name", "Description"), show="headings")
        self.activity_list.heading("Name", text="Name")
        self.activity_list.heading("Description", text="Description")
        self.activity_list.grid(row=3, column=0, columnspan=2, pady=10)
        self.load_activities()

    def add_activity(self):
        name = self.activity_name_entry.get()
        desc = self.activity_desc_entry.get()
        if name and desc:
            self.activities.append({"name": name, "description": desc})
            save_data(ACTIVITIES_FILE, self.activities)
            self.load_activities()
            self.activity_name_entry.delete(0, tk.END)
            self.activity_desc_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Activity added successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def load_activities(self):
        for row in self.activity_list.get_children():
            self.activity_list.delete(row)
        for activity in self.activities:
            self.activity_list.insert("", tk.END, values=(activity["name"], activity["description"]))

    def create_events_tab(self):
        tk.Label(self.tab_events, text="Events Management (Under Development)", font=("Arial", 14)).pack(pady=20)

    def create_budget_tab(self):
        tk.Label(self.tab_budget, text="Budget Tracker (Under Development)", font=("Arial", 14)).pack(pady=20)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityManagerApp(root)
    root.mainloop()
