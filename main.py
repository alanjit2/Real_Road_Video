import os  # type: ignore
from register import *


# Create database instance
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
# Create tables in the database for first name, last name, username, password and salt
cursor.execute('''CREATE TABLE IF NOT EXISTS user_information (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  first_name TEXT,
                  last_name TEXT,
                  username TEXT,
                  password_hash BLOB,
                  salt BLOB)''')
connection.commit()
connection.close()


def exit_app():  # Function to exit the program
    root.quit()


# Create starting login/register window
# Create a width for all the buttons
button_width = 10
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Login with an existing account:").grid(row=0,column=0,padx=20,pady=10)
login_button = ttk.Button(frm, text="Login", command=login_menu,width=button_width)
login_button.grid(row=0, column=1, padx=20, pady=10)

ttk.Label(frm, text="Or register a new account:").grid(row=1,column=0,padx=20,pady=10)
register_button = ttk.Button(frm, text="Register", command=register_menu,width=button_width)
register_button.grid(row=1, column=1, padx=20, pady=10)

exit_button = ttk.Button(frm, text="Exit", command=exit_app)
exit_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

root.mainloop()