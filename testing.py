import tkinter as tk
from tkinter import ttk
import calendar
from datetime import datetime

class ActivityManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Activity Manager")
        self.root.geometry("800x600")
        self.current_user = "Test User"

        # Initialize the dashboard
        self.show_dashboard()

    def show_dashboard(self):
        # Create tab control
        self.tab_control = ttk.Notebook(self.root)
        self.tab_dashboard = ttk.Frame(self.tab_control)
        self.tab_activities = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_dashboard, text="Dashboard")
        self.tab_control.add(self.tab_activities, text="Activities")
        self.tab_control.pack(expand=1, fill="both")

        self.create_dashboard_tab()

    def create_dashboard_tab(self):
        # Welcome Label
        label = tk.Label(self.tab_dashboard, text=f"Welcome, {self.current_user}!", font=("Arial", 16))
        label.pack(pady=10)

        # Calendar graphic
        today = datetime.today()
        month = today.month
        year = today.year

        # Create and display the calendar
        cal_frame = tk.Frame(self.tab_dashboard)
        cal_frame.pack(pady=20)
        self.create_calendar(cal_frame, year, month)

    def create_calendar(self, parent, year, month):
        # Display the current month name above the calendar
        month_name = calendar.month_name[month]  # Get the full name of the month
        tk.Label(parent, text=f"{month_name} {year}", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=7, pady=10)

        # Generate calendar for the given month and year with Sunday as the first day
        cal = calendar.Calendar(firstweekday=6)
        month_days = cal.monthdayscalendar(year, month)

        # Header for days of the week
        days_header = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(days_header):
            header = tk.Label(parent, text=day, font=("Arial", 12, "bold"), width=10, anchor="center")
            header.grid(row=1, column=col, padx=5, pady=5)

        # Display the days in the calendar
        for row, week in enumerate(month_days, start=2):  # Start at row 2 because row 0 and 1 are used for headers
            for col, day in enumerate(week):
                if day == 0:  # Empty day slots
                    cell = tk.Label(parent, text="", font=("Arial", 10), width=10, height=2, bg="lightgray")
                else:
                    cell = tk.Label(parent, text=str(day), font=("Arial", 10), width=10, height=2, bg="white")
                cell.grid(row=row, column=col, padx=5, pady=5)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityManagerApp(root)
    root.mainloop()
