import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import calendar
from datetime import datetime
def load_data(file_path):
    """Load data from a JSON file. Create an empty file if it does not exist."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, create it and return an empty list
        with open(file_path, "w") as file:
            json.dump([], file)
        return []
def save_data(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Paths
USERS_DIR = "users"


# Ensure the users directory exists
os.makedirs(USERS_DIR, exist_ok=True)


def user_exists(username):
    return os.path.exists(os.path.join(USERS_DIR, username))
def create_user(username, password):
    user_dir = os.path.join(USERS_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    with open(os.path.join(user_dir, "password.json"), "w") as file:
        json.dump({"password": password}, file)
    # Create empty data files for the user
    for file in ["activities.json", "events.json", "budget.json"]:
        with open(os.path.join(user_dir, file), "w") as f:
            json.dump([], f)
def authenticate_user(username, password):
    if not user_exists(username):
        return False
    with open(os.path.join(USERS_DIR, username, "password.json"), "r") as file:
        data = json.load(file)
        return data.get("password") == password

class ActivityManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Manager")
        self.root.geometry("800x600")
        self.current_user = None

        # Show the login screen initially
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=50)

        tk.Label(frame, text="Login", font=("Arial", 18), fg="maroon").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Username:",fg="maroon").grid(row=1, column=0, padx=5, pady=5)
        self.login_username_entry = tk.Entry(frame)
        self.login_username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Password:",fg="maroon").grid(row=2, column=0, padx=5, pady=5)
        self.login_password_entry = tk.Entry(frame, show="*")
        self.login_password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Login", command=self.login).grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Sign Up", command=self.show_signup_screen).grid(row=3, column=1, pady=10)

    def show_signup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root)
        frame.pack(pady=50)

        tk.Label(frame, text="Sign Up", font=("Arial", 18), fg="maroon").grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Username:", fg="maroon").grid(row=1, column=0, padx=5, pady=5)
        self.signup_username_entry = tk.Entry(frame)
        self.signup_username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Password:", fg="maroon").grid(row=2, column=0, padx=5, pady=5)
        self.signup_password_entry = tk.Entry(frame, show="*")
        self.signup_password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Sign Up", command=self.signup).grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        if authenticate_user(username, password):
            self.current_user = username
            self.show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        if not username or not password:
            messagebox.showerror("Sign Up Failed", "Username and password cannot be empty.")
            return
        if user_exists(username):
            messagebox.showerror("Sign Up Failed", "Username already exists.")
            return
        create_user(username, password)
        messagebox.showinfo("Success", "Account created! Please log in.")
        self.show_login_screen()

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.tab_control = ttk.Notebook(self.root)
        self.tab_dashboard = ttk.Frame(self.tab_control)
        self.tab_activities = ttk.Frame(self.tab_control)
        self.tab_events = ttk.Frame(self.tab_control)
        self.tab_budget = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_dashboard, text="Dashboard")
        self.tab_control.add(self.tab_activities, text="Activities")
        self.tab_control.add(self.tab_events, text="Events")
        self.tab_control.add(self.tab_budget, text="Budget")
        self.tab_control.pack(expand=1, fill="both")

        self.create_dashboard_tab()
        self.create_activities_tab()
        self.create_events_tab()
        self.create_budget_tab()

    def create_dashboard_tab(self):
        label = tk.Label(self.tab_dashboard, text=f"Welcome, {self.current_user}!", font=("Arial", 16))
        label.pack(pady=20)

    def create_activities_tab(self):
        # Construct the file path for the current user's activities
        activities_file = os.path.join(USERS_DIR, self.current_user, "activities.json")
        print(f"Loading activities from: {activities_file}")  # Debugging line

    # Load user-specific activities
        self.activities = load_data(activities_file)

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

        # Populate the list with loaded activities
        self.load_activities()


    def add_activity(self):
        name = self.activity_name_entry.get()
        desc = self.activity_desc_entry.get()
        if name and desc:
            self.activities.append({"name": name, "description": desc})
            activities_file = os.path.join(USERS_DIR, self.current_user, "activities.json")
            save_data(activities_file, self.activities)
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
        tk.Label(self.tab_events, text="Events Management (Still more to come!)",fg="maroon" ,font=("Arial", 14)).pack(pady=20)

                # Calendar graphic
        today = datetime.today()
        month = today.month
        year = today.year

        # Create and display the calendar
        cal_frame = tk.Frame(self.tab_events)
        cal_frame.pack(pady=20)
        self.create_calendar(cal_frame, year, month)

    def create_calendar(self, parent, year, month):
        # Display the current month name above the calendar
        month_name = calendar.month_name[month]  # Get the full name of the month
        tk.Label(parent, text=f"{month_name} {year}", font=("Arial", 14, "bold"),fg="maroon").grid(row=0, column=0, columnspan=7, pady=10)

        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        days_header = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(days_header):
            header = tk.Label(parent, text=day, font=("Arial", 12, "bold"), width=10, anchor="center",fg="maroon" )
            header.grid(row=1, column=col, padx=5, pady=5)

        for row, week in enumerate(month_days, start=2):  # Start at row 2 because row 0 and 1 are used for headers
            for col, day in enumerate(week):
                if day == 0:  # Empty day slots
                    cell = tk.Label(parent, text="", font=("Arial", 10), width=10, height=2, bg="lightgray")
                else:
                    cell = tk.Label(parent, text=str(day), font=("Arial", 10), width=10, height=2, bg="white")
                cell.grid(row=row, column=col, padx=5, pady=5)


    def create_budget_tab(self):
        tk.Label(self.tab_budget, text="Budget Tracker (Still working on it!)", font=("Arial", 14)).pack(pady=20)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityManagerApp(root)
    root.mainloop()
