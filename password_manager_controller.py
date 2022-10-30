import base64
import hashlib
import random
from json import JSONDecodeError
from tkinter import END
from cryptography.fernet import Fernet
import pyperclip as clipboard

MIN_LENGTH = 15
MAX_LENGTH = 25

vault_name = "data"

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


class password_manager_controller:
    def __init__(self):
        self.model = None
        self.view = None
        self.key = self.generate_key("password")

    def inject_view_model(self, model, view):
        self.model = model
        self.view = view

    # ---------------------------- ENCRYPT VAULT ------------------------------- #
    def encrypt_vault(self, key):
        content = self.model.get_binary_vault_content(vault_name=vault_name)
        if content is not None:
            content_encrypted = Fernet(key).encrypt(content)
            return self.model.set_binary_vault_content(content=content_encrypted, vault_name=vault_name)
        return False

    def decrypt_vault(self, key):
        content = self.model.get_binary_vault_content(vault_name=vault_name)
        if content is not None:
            print(key)
            content_decrypted = Fernet(key).decrypt(content)
            return self.model.set_binary_vault_content(vault_name=vault_name, content=content_decrypted)
        return False

    def generate_key(self, encryption_password):
        word = encryption_password.encode('utf-8')
        hashes = hashlib.sha256(word).digest()
        return base64.urlsafe_b64encode(hashes)

    # ---------------------------- WEBSITE SEARCH ------------------------------- #
    def find_password(self):

        website = self.view.website_input.get()
        if len(website) == 0:
            self.view.show_warning_message(title="Empty Website field", message=f"Please, introduce the website")
            return

        decryption_state = self.decrypt_vault(self.key)
        data = self.model.get_vault_content(vault_name=vault_name)

        if data is None or not decryption_state:
            self.view.show_error_message(title="Error", message="No data found")
            return

        self.encrypt_vault(self.key)

        if website in data.keys():
            password_inside = data[website]["password"]
            email = data[website]["email"]
            clipboard.copy(password_inside)
            self.view.show_info_message(
                title="Password copied",
                message=f"The password for website '{website}' and email '{email}' has been copied to clipboard"
            )
        else:
            self.view.show_error_message(
                title="Website not found",
                message=f"No data for website '{website}' has been found"
            )

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #

    def generate_password(self):
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
                    list_ = LETTERS
                    nr_letters -= 1
                    done = True
                elif type_ == 1 and nr_numbers > 0:
                    list_ = NUMBERS
                    nr_numbers -= 1
                    done = True
                elif type_ == 2 and nr_symbols > 0:
                    list_ = SYMBOLS
                    nr_symbols -= 1
                    done = True
            password += random.choice(list_)
        return password

    # ---------------------------- SAVE PASSWORD ------------------------------- #
    def save_data(self):
        website = self.view.website_input.get()
        email = self.view.email_username_input.get()
        password_ = self.view.password_input.get()
        new_dict = {
            website: {
                "email": email,
                "password": password_,
            }
        }

        if len(website) == 0 or len(email) == 0 or len(password_) == 0:
            self.view.show_warning_message(title="Empty fields", message="There is, at least, one empty field")
            return

        is_ok = self.view.ask_ok_cancel(title=website, message=f"Are you sure you wanna save the data for {email}?")
        if is_ok:
            decryption_state = self.decrypt_vault(self.key)
            data = self.model.get_vault_content(vault_name=vault_name)
            if data is None or decryption_state:
                data = new_dict
            else:
                data.update(new_dict)

            state = self.model.set_vault_content(vault_name=vault_name, content=data)
            encryption_state = self.encrypt_vault(self.key)

            if not state or not encryption_state:
                self.view.show_error_message(title="Unknown Error", message="Unknown error while updating the password")
            else:
                self.view.show_info_message(
                    title="Password saved",
                    message="The password has been successfully updated"
                )
            self.view.website_input.delete(0, END)
            self.view.password_input.delete(0, END)
        pass

    def print_generated_password(self):
        self.view.password_input.delete(0, END)
        generated_password = self.generate_password()
        self.view.password_input.insert(0, generated_password)

    def get_vault_list(self):
        pass
