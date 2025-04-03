import json
from tkinter import *
from tkinter import messagebox
import pandas as pd
import random
import pyperclip

FONT = ("Courier", 18)
WHITE = '#F4F6FF'
BLUE = '#99d6d1'
YELLOW = '#fac440'

try:
    manager_df = pd.read_csv('manager_data.csv')
except FileNotFoundError:
    manager_init_dict = {
        "website":[],
        "username":[],
        "email":[],
        "password":[]
    }
    manager_df = pd.DataFrame(manager_init_dict)


# /---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = (
            [random.choice(letters) for _ in range(nr_letters)] +
            [random.choice(symbols) for _ in range(nr_symbols)] +
            [random.choice(numbers) for _ in range(nr_numbers)]
    )

    random.shuffle(password_list)

    password = ''.join(password_list)
    password_input.delete(0, END)
    password_input.insert(END, password)
    pyperclip.copy(password)


# /---------------------------- SAVE PASSWORD  ------------------------------- #
def save_password():
    new_website = str(website_input.get())
    new_username = str(username_input.get())
    new_email = str(email_input.get())
    new_password = str(password_input.get())
    is_ok = None

    if (new_website == '') or (new_email == '') or (new_password == ''):
        messagebox.showerror(title='Empty entry', message='Not allow to save without email or website.')
        pass
    else:
        is_ok = messagebox.askokcancel(title=new_website,
                                       message=f'These are the details entered: \nEmail/Username: {new_username}'
                                               f'\nPassword: {new_password} \nIs it ok to save?')
    if is_ok and not ((new_website == '') or (new_email == '') or (new_password == '')):
        new_line = {
            'website': new_website,
            'username': new_username,
            'email': new_email,
            'password': new_password
        }
        if (new_website in manager_df['website'].values) and (new_email in manager_df['email'].values):
            messagebox.showwarning(title='Already registed', message='email already registed in the website')
        else:
            """
            with open('manager_data.json', 'r') as data_file:
                # json.dump(new_line,data_file,indent=4)
                # reading old data
                data = json.load(data_file)
                # updating old data with new data
                data.update(new_line)
            with open('manager_data.json', 'w') as data_file:
                # saving updated data
                json.dump(data, data_file, indent=4)
"""
            manager_df.loc[len(manager_df)] = new_line
            manager_df.to_csv(path_or_buf='manager_data.csv', index=False)
            messagebox.showinfo(title='Operation Sucessfull', message=f'Added {new_website} to data store')
            website_input.delete(0, END)
            username_input.delete(0, END)
            email_input.delete(0, END)
            password_input.delete(0, END)


# /---------------------------- CLEAR ENTRIES  ------------------------------- #
def clear_entries():
    website_input.delete(0, END)
    username_input.delete(0, END)
    email_input.delete(0, END)
    password_input.delete(0, END)


# /---------------------------- SEARCH ENTRY ------------------------------- #
def search_password():
    search_website = website_input.get()
    try:
        item_founded = manager_df[manager_df['website'] == search_website]
        clear_entries()
        website_input.insert(END, item_founded.website.values[0])
        username_input.insert(END, item_founded.username.values[0])
        email_input.insert(END, item_founded.email.values[0])
        password_input.insert(END, item_founded.password.values[0])
    except IndexError:
        messagebox.showwarning(title='Out of bands', message='Not website founded')
    else:
        pass
        # email_input.insert()


# /---------------------------- UI SETUP   ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=20, pady=20, bg=WHITE)

# ?Background image
canvas = Canvas(width=520, height=520, bg=WHITE, highlightthickness=0)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(265, 255, image=logo_img)
canvas.grid(column=1, row=0)

# ºwebsite item
website_label = Label(text='Website', width=10, bg=WHITE, font=FONT)
website_label.grid(column=0, row=1)
website_label.config(pady=5)

website_input = Entry(width=35, font=FONT)
website_input.grid(column=1, row=1)
website_input.focus()

# ºsearch item
search_button = Button(text='Search', width=15, font=("Courier", 12), bg=BLUE, command=search_password)
search_button.grid(column=2, row=1)

# ºusername item
username_label = Label(text='Username', width=10, bg=WHITE, font=FONT)
username_label.grid(column=0, row=2)

username_input = Entry(width=50, font=FONT)
username_input.grid(column=1, row=2, columnspan=2)
# ºemail item
email_label = Label(text='Email', width=10, bg=WHITE, font=FONT)
email_label.grid(column=0, row=3)
email_label.config(pady=5)

email_input = Entry(width=50, font=FONT)
email_input.grid(column=1, row=3, columnspan=2)

# ºpassword item
password_label = Label(text='Password', width=15, bg=WHITE, font=FONT)
password_label.grid(column=0, row=4)
password_label.config(pady=5)

password_input = Entry(width=35, font=FONT)
password_input.grid(column=1, row=4)

generate_button = Button(text='Generate Password', font=("Courier", 12), bg=BLUE, command=password_generator)
generate_button.grid(column=2, row=4)

# ºadd item
add_button = Button(text='Add', width=35, font=("Courier", 12, 'bold'), bg=BLUE, command=save_password)
add_button.grid(row=5, column=1)

# ºclear all entries
add_button = Button(text='Clear', width=10, font=("Courier", 12, 'bold'), bg=YELLOW, command=clear_entries)
add_button.grid(row=5, column=2)

# ¡prevent close window
window.mainloop()
