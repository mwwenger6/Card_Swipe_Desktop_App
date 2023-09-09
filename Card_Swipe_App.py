from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import pyodbc

server = 'MWDESKTOP'
database = 'CMPSC487_Project1'
username = 'CollegeUser'  
password = 'UIO*uio8'  

connection = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = connection.cursor()

swipe_table = None
id_entry = None
date_from_entry = None
date_to_entry = None
user_type_entry = None
app = None
simulate = tk.Tk()
simulate.title("Simulate Swipe")
simulate.geometry("400x400")
username_entry = None
password_entry = None


def clear_filters(main_app):
    global user_type_entry, id_entry, date_from_entry, date_to_entry
    user_type_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    date_from_entry.delete(0, tk.END)
    date_to_entry.delete(0, tk.END)
    create_table(main_app)


def filter_data(main_app):
    global user_type_entry, id_entry, date_from_entry, date_to_entry
    user = user_type_entry.get()
    id = id_entry.get()
    date_from = date_from_entry.get()
    date_to = date_to_entry.get()
    filters = ""
    
    if user != "":
        filters += f"UserType = '{user}'"
    if id != "":
        if filters:
            filters += " AND "
        filters += f"IdNumber = {id}"
    if date_from != "":
        if filters:
            filters += " AND "
        filters += f"SwipeTimeStamp >= '{date_from}'"
    if date_to != "":
        if filters:
            filters += " AND "
        filters += f"SwipeTimeStamp <= '{date_to}'"

    if filters:
        filters = "WHERE " + filters

    create_table(main_app, filters)



def change_access(main_app):
    selected_item = swipe_table.selection()[0]
    id = swipe_table.item(selected_item, 'values')[0]
    access_type = swipe_table.item(selected_item, 'values')[4]
    top = tk.Toplevel(main_app)
    top.title("Select Action")
    top.geometry("150x150")  
    label = tk.Label(top, text=f"User ID: {id}")
    label.pack()

    activate_button = tk.Button(top, text="Activate", command=lambda: on_action_selected(id, 1, top, main_app))
    suspend_button = tk.Button(top, text="Suspend", command=lambda: on_action_selected(id, 2, top, main_app))
    terminate_button = tk.Button(top, text="Terminate", command=lambda: on_action_selected(id, 3, top, main_app))
    
    activate_button.pack()
    suspend_button.pack()
    terminate_button.pack()

    if access_type == "Active":
        activate_button.config(state=tk.DISABLED)
    elif access_type == "Suspend":
        suspend_button.config(state=tk.DISABLED)
    else:
        terminate_button.config(state=tk.DISABLED)

def on_action_selected(id, action, top, main_app):
    cursor.execute(f"UPDATE Users SET AccessId = {action} WHERE IdNumber = {id}")
    top.destroy()
    create_table(main_app)


def create_table(main_app, filters=""):
    for item in swipe_table.get_children():
        swipe_table.delete(item)
    cursor.execute("SELECT * FROM vwSwipes " + filters + " ORDER BY SwipeTimeStamp DESC")
    rows = cursor.fetchall()
    for row in rows:
        id = row[5]
        swipeType = row[1]
        if swipeType == 1:
            swipeType = "In"
        elif swipeType == 0:
            swipeType = "Out"
        swipeTime = row[2].strftime('%m-%d-%Y %H:%M:%S')
        userType = row[3]
        change_access_data = row[4]

        swipe_table.insert('', 'end', values=(id, swipeType, swipeTime, userType, change_access_data))
    swipe_table.bind('<ButtonRelease-1>', lambda event, main_app=main_app: change_access(main_app))



def main_page():
    app.destroy()
    main_app = tk.Tk()
    main_app.title("Main Application")
    main_app.geometry("1100x400")

    back_button = tk.Button(main_app, text="Back", command=lambda: login_screen(main_app))
    back_button.pack(side=tk.TOP, padx=10, anchor=tk.W)

    def pick_datetime(entry):
        def set_datetime():
            selected_datetime = calendar.get_date()
            time = time_entry.get()
            formatted_datetime = f"{selected_datetime} {time}"
            entry.delete(0, tk.END)
            entry.insert(0, formatted_datetime)
            top.destroy()

        top = tk.Toplevel()
        top.title("Date and Time Picker")

        calendar = Calendar(top)
        calendar.pack(padx=10, pady=10)

        time_label = tk.Label(top, text="Time (HH:MM:SS):")
        time_label.pack(padx=10, pady=5)

        time_entry = tk.Entry(top)
        time_entry.pack(padx=10, pady=10)

        set_button = tk.Button(top, text="Set Date & Time", command=set_datetime)
        set_button.pack(padx=10, pady=10)

    global user_type_entry, id_entry, date_from_entry, date_to_entry

    id_filter_frame = tk.Frame(main_app)
    id_filter_frame.pack(side=tk.TOP, fill=tk.X)
    id_label = tk.Label(id_filter_frame, text="ID:")
    id_label.pack(side=tk.LEFT, pady=5, padx=10)
    id_entry = tk.Entry(id_filter_frame)
    id_entry.pack(side=tk.LEFT, pady=5, padx=55)

    date_filter_frame = tk.Frame(main_app)
    date_filter_frame.pack(side=tk.TOP, fill=tk.X)
    date_from_label = tk.Label(date_filter_frame, text="Date From:")
    date_from_label.pack(side=tk.LEFT, pady=5, padx=10)
    date_from_entry = tk.Entry(date_filter_frame)
    date_from_entry.pack(side=tk.LEFT, pady=5, padx=10)
    date_from_entry.bind("<Button-1>", lambda event: pick_datetime(date_from_entry))
    date_to_label = tk.Label(date_filter_frame, text="Date To:")
    date_to_label.pack(side=tk.LEFT, pady=5, padx=10)
    date_to_entry = tk.Entry(date_filter_frame)
    date_to_entry.pack(side=tk.LEFT, pady=5, padx=10)
    date_to_entry.bind("<Button-1>", lambda event: pick_datetime(date_to_entry))


    user_filter_frame = tk.Frame(main_app)
    user_filter_frame.pack(side=tk.TOP, fill=tk.X)
    user_type_label = tk.Label(user_filter_frame, text="User Type:")
    user_type_label.pack(side=tk.LEFT, pady=5, padx=11)
    user_type_entry = tk.Entry(user_filter_frame)
    user_type_entry.pack(side=tk.LEFT, pady=5, padx=11)

    button_frame = tk.Frame(main_app)
    button_frame.pack(side=tk.TOP, fill=tk.X)
    filter_button = tk.Button(button_frame, text="Apply Filters", command=lambda: filter_data(main_app))
    filter_button.pack(side=tk.LEFT, pady=5, padx=480)
    other_frame = tk.Frame(main_app)
    other_frame.pack(side=tk.TOP, fill=tk.X)
    clear_button = tk.Button(other_frame, text="Clear Filters  ", command=lambda: clear_filters(main_app))
    clear_button.pack(side=tk.LEFT, padx=480)

    instructions_label = tk.Label(main_app, text="*Click on a row to change a user's status")
    instructions_label.pack(pady=10)

    global swipe_table
    swipe_table = ttk.Treeview(main_app, columns=("ID", "Swipe Type", "Swipe Time Stamp", "User Type", "Change Access"),
                            selectmode="browse")
    swipe_table['show'] = 'headings'
    swipe_table.heading("#1", text="ID")
    swipe_table.heading("#2", text="Swipe Type")
    swipe_table.heading("#3", text="Swipe Time Stamp")
    swipe_table.heading("#4", text="User Type")
    swipe_table.heading("#5", text="Current Access")
    swipe_table.pack(padx=20, pady=20)
    create_table(main_app, "")
    

def login():
    global username_entry, password_entry
    username = username_entry.get()
    password = password_entry.get()
    cursor.execute("SELECT Password FROM Logins WHERE Username = ?", (username,))
    stored_password = cursor.fetchone()
    if stored_password is not None and password == stored_password[0]:
        main_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def login_screen(app_screen):
    global app, username_entry, password_entry
    app_screen.destroy()
    app = tk.Tk()
    app.title("Login Screen")
    app.geometry("250x350")

    username_label = tk.Label(app, text="Username:")
    username_label.pack(pady=10)
    username_entry = tk.Entry(app)
    username_entry.pack(pady=5)

    password_label = tk.Label(app, text="Password:")
    password_label.pack(pady=10)
    password_entry = tk.Entry(app, show="*")  # Passwords are hidden with asterisks
    password_entry.pack(pady=5)

    login_button = tk.Button(app, text="Login", command=login)
    login_button.pack(pady=10)

    simulate_swipe_button = tk.Button(app, text="Simulate Swipe", command=simulate_swipe)
    simulate_swipe_button.pack(pady=10)


def submit_swipe(swipe):
    id_num = swipe.get()
    cursor.execute("SELECT UserId, AccessId, IsSwipedIn FROM Users WHERE IdNumber = ?", (id_num,))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
        access_id = user[1]
        is_swiped_in = user[2]
        
        if access_id == 1:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Format the timestamp
            if is_swiped_in:
                cursor.execute(f"INSERT INTO Swipes VALUES(0, {user_id}, '{timestamp}')")
                cursor.execute(f"UPDATE Users SET IsSwipedIn = 0 WHERE UserId = {user_id}")
            else:
                cursor.execute(f"INSERT INTO Swipes VALUES (1, {user_id}, '{timestamp}')")
                cursor.execute(f"UPDATE Users SET IsSwipedIn = 1 WHERE UserId = {user_id}")
            connection.commit()
        else:
            messagebox.showerror("Swipe Failed", "User is Suspended or Terminated")
    else:
        messagebox.showerror("Swipe Failed", "Invalid User")
    swipe.delete(0, tk.END)



def simulate_swipe():
    global app
    app.destroy()

    global simulate
    simulate = tk.Tk()
    simulate.title("Simulate Swipe")
    simulate.geometry("350x120")

    back_button = tk.Button(simulate, text="Back", command=lambda: login_screen(simulate))
    back_button.pack(side=tk.TOP, padx=10, anchor=tk.W)

    swipe_frame = tk.Frame(simulate)
    swipe_frame.pack(side=tk.TOP, fill=tk.X)
    swipe_label = tk.Label(simulate, text="User Type:")
    swipe_label.pack(side=tk.LEFT, pady=5, padx=11)
    swipe_entry = tk.Entry(simulate)
    swipe_entry.pack(side=tk.LEFT, pady=5, padx=11)
    submit_button = tk.Button(simulate, text="Submit", command=lambda:submit_swipe(swipe_entry))
    submit_button.pack(side=tk.LEFT, pady=5, padx=11)

login_screen(simulate)

app.mainloop()
cursor.close()
connection.close()


