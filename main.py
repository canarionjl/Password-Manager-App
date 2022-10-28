import base64
import hashlib
from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox, simpledialog
import random
import json
import pyperclip as clipboard
from cryptography.fernet import Fernet

BACKGROUND_COLOR = "white"
LABEL_COLOR = "#ffffff"

WEBSITE_LABEL = "Website: "
EMAIL_USERNAME_LABEL = "Email/Username: "
PASSWORD_LABEL = "Password: "
DEFAULT_EMAIL = "canarionjl@gmail.com"

FONT = ("Arial", 10, "normal")

MIN_LENGTH = 15
MAX_LENGTH = 25

master_password = None


# ---------------------------- ENCRYPT VAULT ------------------------------- #
def encrypt_vault(key):
    try:
        with open("data.json", "rb") as vault:
            contents = vault.read()
            contents_encrypted = Fernet(key).encrypt(contents)
        with open("data.json", "wb") as vault:
            vault.write(contents_encrypted)
    except FileNotFoundError:
        pass
    except JSONDecodeError:
        pass


def decrypt_vault(key):
    try:
        with open("data.json", "rb") as vault:
            contents = vault.read()
            contents_decrypted = Fernet(key).decrypt(contents)
        with open("data.json", "wb") as vault:
            vault.write(contents_decrypted)
    except FileNotFoundError:
        pass
    except JSONDecodeError:
        pass


def generate_key(password):
    word = password.encode('utf-8')
    hashes = hashlib.sha256(word).digest()
    return base64.urlsafe_b64encode(hashes)


# ---------------------------- WEBSITE SEARCH ------------------------------- #
def find_password():
    def exception_message():
        messagebox.showerror(
            title="Error",
            message=f"No data found"
        )

    website = website_input.get()
    if len(website) == 0:
        messagebox.showwarning(
            title="Empty Website field",
            message=f"Please, introduce the website"
        )
        return

    try:
        with open("data.json", "r") as vault:
            data = json.load(vault)
    except FileNotFoundError:
        exception_message()
    except JSONDecodeError:
        exception_message()
    else:
        if website in data.keys():
            password = data[website]["password"]
            email = data[website]["email"]
            clipboard.copy(password)
            messagebox.showinfo(
                title="Password copied",
                message=f"The password for website '{website}' and email '{email}' has been copied to clipboard"
            )
        else:
            messagebox.showwarning(
                title="Website not found",
                message=f"No data for website '{website}' has been found"
            )


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    length = random.randint(MIN_LENGTH, MAX_LENGTH)
    nr_letters = random.randint(0, length)
    length -= nr_letters
    nr_symbols = random.randint(0, length)
    length -= nr_symbols
    nr_numbers = length

    password_length = nr_letters + nr_symbols + nr_numbers
    password = ""

    for _ in range(0, password_length):
        done = False
        while not done:
            type_ = random.randint(0, 2)
            if type_ == 0 and nr_letters > 0:
                list_ = letters
                nr_letters -= 1
                done = True
            elif type_ == 1 and nr_numbers > 0:
                list_ = numbers
                nr_numbers -= 1
                done = True
            elif type_ == 2 and nr_symbols > 0:
                list_ = symbols
                nr_symbols -= 1
                done = True
        password += random.choice(list_)

    return password


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_input.get()
    email = email_username_input.get()
    password_ = password_input.get()
    new_dict = {
        website: {
            "email": email,
            "password": password_,
        }
    }
    data = new_dict

    if len(website) == 0 or len(email) == 0 or len(password_) == 0:
        messagebox.showwarning(title="Empty fields", message="There is, at least, one empty field")
        return

    is_ok = messagebox.askokcancel(title=website, message=f"Are you sure you wanna save the data for {email}?")

    if is_ok:
        try:
            with open("data.json", "r") as vault:
                data = json.load(vault)  # reading all data
                data.update(new_dict)  # updating the new password into the data
        except FileNotFoundError:
            pass
        except JSONDecodeError:
            pass
        finally:
            with open("data.json", "w") as vault:
                json.dump(data, vault, indent=4)  # writing the new data over the json file

        messagebox.showinfo(title="Password saved", message="The password has been successfully updated")
        website_input.delete(0, END)
        password_input.delete(0, END)


def print_password():
    password_input.delete(0, END)
    password = generate_password()
    password_input.insert(0, password)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=210, height=210, bg=BACKGROUND_COLOR, highlightthickness=0)
password_image = PhotoImage(file="logo.png")
canvas.create_image(105, 105, image=password_image)
canvas.grid(row=0, column=1)

website_label = Label(text=WEBSITE_LABEL, font=FONT, bg=BACKGROUND_COLOR)
website_label.grid(row=1, column=0, sticky="w")

email_username_label = Label(text=EMAIL_USERNAME_LABEL, font=FONT, bg=BACKGROUND_COLOR)
email_username_label.grid(row=2, column=0, sticky="w")

password_label = Label(text=PASSWORD_LABEL, font=FONT, bg=BACKGROUND_COLOR)
password_label.grid(row=3, column=0, sticky="w")

generate_password_button = Button(text="Generate Password", bg=BACKGROUND_COLOR, command=print_password)
generate_password_button.grid(row=3, column=2, sticky="e", pady=2)

add_password_button = Button(text="Add", bg=BACKGROUND_COLOR, width=46, command=save_data)
add_password_button.grid(row=4, column=1, columnspan=2, pady=3)

search_button = Button(text="Search", bg=BACKGROUND_COLOR, command=find_password, width=14)
search_button.grid(row=1, column=2, sticky="e", pady=3)

website_input = Entry(width=33, bg=LABEL_COLOR)
website_input.grid(row=1, column=1, sticky="w")
website_input.focus()  # set the focus on the website input

email_username_input = Entry(width=55, bg=LABEL_COLOR)
email_username_input.grid(row=2, column=1, columnspan=2, sticky="w")
email_username_input.insert(0, DEFAULT_EMAIL)

password_input = Entry(width=33, bg=LABEL_COLOR)
password_input.grid(row=3, column=1, sticky="w", columnspan=2)

password = simpledialog.askstring(title="Master Password",
                                  prompt="What's your Master Password?")
master_password = generate_key(password)

window.mainloop()


#Crear nuevos vaults --> cada vault es un fichero json cuyo nombre es solicitado al usuario
#Cada vault tendrá una contraseña maestra solicitada al momento de la creación
#Se mostrará una lista desplegable con todos los vaults disponible para que el usuario elija cual quiere
#Para comprobar la contraseña se tratará de decodificar el archivo y si da error (teniendo en cuenta que el vault existe pq esta mostrado --> estará vacío o la contraseña es incorrecta
#Otra forma es guardar las contraseñas de los vaules hasheadas por md5 (ya que sha256 se está utilizando para generar las claves de cifrado) en un fichero json y comprobar si la contraseña maestra hasehada por md5 coincide con la almacenada
#La ultima opción me gusta más -> Evaluar cual de las dos es más óptima