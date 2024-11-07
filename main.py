import os
import json
from tkinter import *
from tkinter import messagebox


# Load users from file
def load_users():
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


# Save users to file
def save_users(users):
    with open("users.txt", "w") as file:
        json.dump(users, file)


# Display message on main screen
def show_message(message):
    for widget in body.winfo_children():
        widget.destroy()
    Label(body, text=message, font=("Helvetica", 14), fg="maroon2", anchor="center").pack(pady=20)
    Button(body, text="Back", command=show_login_page, font=("Helvetica", 12)).pack(pady=10)


# Collect user information
def collect_user_info():
    for widget in body.winfo_children():
        widget.destroy()

    Label(body, text="Fill Out User Information", font=("Helvetica", 16), fg="maroon2").pack(pady=10)

    questions = [
        "First Name", "Last Name", "Age", "Gender (M/F)",
        "Personality (Introvert/Extrovert)", "Hobbies (comma separated)",
        "Adventure Lover (True/False)", "Stay In or Go Out (In/Out)",
        "Likes Pets (True/False)", "Morning Person (True/False)"
    ]

    entries = {}
    for question in questions:
        Label(body, text=question, font=("Helvetica", 12)).pack()
        entry = Entry(body, font=("Helvetica", 12))
        entry.pack()
        entries[question] = entry

    def save_user():
        user_data = {question: entries[question].get() for question in entries}
        username = user_data["First Name"]

        # Load current users and add new user if username is unique
        users = load_users()
        if username not in users:
            users[username] = {"info": user_data, "password": signup_password_entry.get()}
            save_users(users)
            show_message("User registered successfully!")
        else:
            show_message("Username already exists!")

    Button(body, text="Submit", command=save_user, font=("Helvetica", 12), bg="maroon2", fg="white").pack(pady=10)


# Enhanced matchmaking logic
def generate_matches():
    users = load_users()
    if not users:
        show_message("No users found. Please add users first.")
        return

    # Calculate match score for each pair
    def calculate_match_score(user1_data, user2_data):
        score = 0

        # Personality compatibility
        if user1_data["Personality (Introvert/Extrovert)"] == user2_data["Personality (Introvert/Extrovert)"]:
            score += 3  # Personality match is worth 3 points

        # Shared hobbies
        hobbies1 = set(user1_data["Hobbies (comma separated)"].split(", "))
        hobbies2 = set(user2_data["Hobbies (comma separated)"].split(", "))
        score += len(hobbies1.intersection(hobbies2)) * 2  # Each shared hobby is worth 2 points

        # Lifestyle preferences
        if user1_data["Adventure Lover (True/False)"] == user2_data["Adventure Lover (True/False)"]:
            score += 2
        if user1_data["Stay In or Go Out (In/Out)"] == user2_data["Stay In or Go Out (In/Out)"]:
            score += 2
        if user1_data["Likes Pets (True/False)"] == user2_data["Likes Pets (True/False)"]:
            score += 1
        if user1_data["Morning Person (True/False)"] == user2_data["Morning Person (True/False)"]:
            score += 1

        return score

    # Generate matches for each user
    matches = {}
    for user1 in users:
        matches[user1] = []
        user1_data = users[user1]["info"]
        for user2 in users:
            if user1 == user2:
                continue
            user2_data = users[user2]["info"]

            # Calculate similarity score
            score = calculate_match_score(user1_data, user2_data)
            matches[user1].append((user2, score))

    # Display match results
    match_display = ""
    for user in matches:
        sorted_matches = sorted(matches[user], key=lambda x: x[1], reverse=True)
        match_display += f"{user}:\n"
        for other_user, score in sorted_matches:
            match_display += f"    {other_user}: {score} points\n"
        match_display += "\n"

    show_message(f"Matchmaking results:\n{match_display}")


# Check login credentials
def check_login():
    username = login_username_entry.get()
    password = login_password_entry.get()
    users = load_users()

    if username in users and users[username]["password"] == password:
        show_main_menu()
    else:
        show_message("Invalid username or password!")


# Check signup credentials
def check_signup():
    users = load_users()
    username = signup_username_entry.get()
    password = signup_password_entry.get()

    if username in users:
        show_message("Username already exists!")
    else:
        users[username] = {"info": {}, "password": password}
        save_users(users)
        show_message("User registered successfully!")


# Show login page with Haunted Hearts style
def show_login_page():
    for widget in body.winfo_children():
        widget.destroy()

    logo_image = PhotoImage(file="images/FinalHHLogo.png")
    logo = Label(body, image=logo_image)
    logo.image = logo_image  # Keep a reference to avoid garbage collection
    logo.pack(pady=10)

    subtitle = Label(body, text="Welcome to Haunted Hearts!\nFind your perfect match here.", font=("Helvetica", 14),
                     fg="maroon2")
    subtitle.pack(pady=10)

    login_frame = Frame(body)
    login_frame.pack(pady=10)

    Label(login_frame, text="Username:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
    Label(login_frame, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)

    global login_username_entry, login_password_entry
    login_username_entry = Entry(login_frame, font=("Helvetica", 12))
    login_password_entry = Entry(login_frame, font=("Helvetica", 12), show="*")
    login_username_entry.grid(row=0, column=1, padx=5, pady=5)
    login_password_entry.grid(row=1, column=1, padx=5, pady=5)

    Button(body, text="Login", font=("Helvetica", 12), bg="maroon2", fg="white", command=check_login).pack(pady=10)

    Label(body, text="Don't have an account? Sign up below!", font=("Helvetica", 12)).pack(pady=(20, 0))

    signup_frame = Frame(body)
    signup_frame.pack(pady=10)

    Label(signup_frame, text="Username:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
    Label(signup_frame, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)

    global signup_username_entry, signup_password_entry
    signup_username_entry = Entry(signup_frame, font=("Helvetica", 12))
    signup_password_entry = Entry(signup_frame, font=("Helvetica", 12), show="*")
    signup_username_entry.grid(row=0, column=1, padx=5, pady=5)
    signup_password_entry.grid(row=1, column=1, padx=5, pady=5)

    Button(body, text="Sign Up", font=("Helvetica", 12), bg="maroon2", fg="white", command=check_signup).pack(pady=10)


# Show main menu after login
def show_main_menu():
    for widget in body.winfo_children():
        widget.destroy()
    Label(body, text="Main Menu", font=("Helvetica", 16), fg="maroon2").pack(pady=20)
    Button(body, text="Generate Matches", font=("Helvetica", 12), command=generate_matches).pack(pady=10)
    Button(body, text="Fill Out Info", font=("Helvetica", 12), command=collect_user_info).pack(pady=10)
    Button(body, text="Log Out", font=("Helvetica", 12), command=show_login_page).pack(pady=10)


# Main application window setup
window = Tk()
window.title("Haunted Hearts Matchmaking")
window.geometry("500x600")

body = Frame(window)
body.pack(fill=BOTH, expand=True)

# Start with the login page
show_login_page()

window.mainloop()
