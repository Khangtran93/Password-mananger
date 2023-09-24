from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']



def generate_random():
    pw_entry.delete(0, END)
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_num = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbol = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_symbol + password_letter + password_num
    random.shuffle(password_list)

    password = "".join(password_list)
    pw_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox._show(title="Copy Password", message="Password copied to clipboard.")

    #pw_gen = False
def search():
    website = ws_entry.get().title()
    try:
        with open("data.json") as my_data:
            data = json.load(my_data)
    except FileNotFoundError:
        messagebox.showwarning(title="Not Found", message="File not found")
    else:

        if website in data:
            email = data[website]["Email"]
            password = data[website]["Password"]
            messagebox._show(title=f"{website}", message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showwarning(title="Not Found", message="No website found")

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    validated = True
    website_name = ws_entry.get().title()
    user_name = usn_entry.get().lower()
    user_password = pw_entry.get()

    if website_name =="":
        messagebox.showwarning(title="Error", message="Please fill out website name!")
        validated = False
    elif len(user_name) < 11:
        messagebox.showwarning(title="Error", message="Please fill out email!")
        validated = False
    elif user_password == "":
        messagebox.showwarning(title="Error", message="Please fill out password!")
        validated = False
    if validated:
        save_data = messagebox.askokcancel(title="Save", message=f"Website: {website_name}\nEmail: {user_name}\nPassword: {user_password}\nCorrect?")

        new_data = {website_name: {"Email": user_name, "Password": user_password}}

        if save_data:
            try:
                with open("data.json", mode="r") as my_data:
                    #my_data.write(f"{website_name}  |  {user_name}  |  {user_password}\n")
                    data = json.load(my_data)

            except FileNotFoundError:
                with open("data.json", mode="w") as my_data:
                    json.dump(new_data, my_data, indent=4)
            else:
                data.update(new_data)
                with open("data.json", mode="w") as my_data:
                    json.dump(data, my_data, indent=4)
            finally:
                ws_entry.delete(0, 'end')
                usn_entry.delete(0, 'end')
                pw_entry.delete(0, 'end')
                usn_entry.insert(0, "@gmail.com")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
# Canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")

canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
# Label
website = Label(text="Website:")
website.grid(row=1, column=0)
username = Label(text="Email/Username: ")
username.grid(row=2, column=0)
password = Label(text="Password:")
password.grid(row=3, column=0)

# Entries
ws_entry = Entry(width=32)
ws_entry.grid(row=1, column=1,sticky="W")
ws_entry.focus()

usn_entry = Entry(width=32)
usn_entry.grid(row=2, column=1, columnspan=2, sticky="W")
usn_entry.insert(0, "@gmail.com")
usn_entry.focus()

pw_entry = Entry(width=32)
pw_entry.grid(row=3, column=1, sticky="W")

# Buttons
generate_btn = Button(text="Generate Password", command=generate_random)
generate_btn.grid(row=3, column=2, sticky="EW")

add_btn = Button(text="Add", width=36, command=save)
add_btn.grid(row=4, column=1, columnspan=2, sticky="EW")

search_btn = Button(text="Search", command=search, bg="blue")
search_btn.grid(row=1, column=2, sticky="EW")



window.mainloop()