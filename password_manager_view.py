from tkinter import PhotoImage, Canvas, Label, Button, Entry, Tk, messagebox, simpledialog
from tkinter.ttk import Combobox

BACKGROUND_COLOR = "white"
LABEL_COLOR = "#ffffff"

WEBSITE_LABEL = "Website: "
EMAIL_USERNAME_LABEL = "Email/Username: "
PASSWORD_LABEL = "Password: "
VAULT_LABEL = "Choose Vault: "
DEFAULT_EMAIL = "canarionjl@gmail.com"

FONT = ("Arial", 10, "normal")


class password_manager_view:

    def __init__(self):
        self.search_button = None
        self.create_vault_button = None
        self.add_password_button = None
        self.generate_password_button = None
        self.vault_list = None
        self.website_input = None
        self.email_username_input = None
        self.password_label = None
        self.email_username_label = None
        self.password_input = None
        self.website_label = None
        self.controller = None
        self.vault_label = None

    def inject_controller(self, controller):
        self.controller = controller

    def configure_window(self):
        #  ---- Background Windows ----

        window = Tk()
        window.title("Password Manager")
        window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        #  ---- Canvas with Logo ----

        canvas = Canvas(width=210, height=210, bg=BACKGROUND_COLOR, highlightthickness=0)
        password_image = PhotoImage(file="logo.png")
        canvas.create_image(105, 105, image=password_image)
        canvas.grid(row=0, column=1)

        #  ---- Label ----

        self.vault_label = Label(text=VAULT_LABEL, font=FONT, bg=BACKGROUND_COLOR)
        self.vault_label.grid(row=1, column=0, sticky="w")
        self.website_label = Label(text=WEBSITE_LABEL, font=FONT, bg=BACKGROUND_COLOR)
        self.website_label.grid(row=2, column=0, sticky="w")

        self.email_username_label = Label(text=EMAIL_USERNAME_LABEL, font=FONT, bg=BACKGROUND_COLOR)
        self.email_username_label.grid(row=3, column=0, sticky="w")

        self.password_label = Label(text=PASSWORD_LABEL, font=FONT, bg=BACKGROUND_COLOR)
        self.password_label.grid(row=4, column=0, sticky="w")

        #  ---- Input ----

        self.website_input = Entry(width=33, bg=LABEL_COLOR)
        self.website_input.grid(row=2, column=1, sticky="w")
        self.website_input.focus()  # set the focus on the website input

        self.email_username_input = Entry(width=55, bg=LABEL_COLOR)
        self.email_username_input.grid(row=3, column=1, columnspan=2, sticky="w")
        self.email_username_input.insert(0, DEFAULT_EMAIL)

        self.password_input = Entry(width=33, bg=LABEL_COLOR)
        self.password_input.grid(row=4, column=1, sticky="w", columnspan=2)

        self.vault_list = Combobox(state="readonly", value=self.controller.get_vault_list, width=30)
        self.vault_list.grid(row=1, column=1, sticky="w")

        #  ---- Buttons ----

        self.generate_password_button = Button(text="Generate Password",
                                               bg=BACKGROUND_COLOR,
                                               command=self.controller.print_generated_password
                                               )

        self.generate_password_button.grid(row=4, column=2, sticky="e", pady=2)

        self.add_password_button = Button(text="Add", bg=BACKGROUND_COLOR, width=46, command=self.controller.save_data)
        self.add_password_button.grid(row=5, column=1, columnspan=2, pady=3)

        self.create_vault_button = Button(text="New Vault", bg=BACKGROUND_COLOR, width="14")
        self.create_vault_button.grid(row=1, column=2, pady=3, sticky="e")

        self.search_button = Button(text="Search", bg=BACKGROUND_COLOR, command=self.controller.find_password, width=14)
        self.search_button.grid(row=2, column=2, sticky="e", pady=3)

        #  ---- Mainloop ----

        window.mainloop()

    def init_view(self):
        self.configure_window()

    def show_info_message(self, title, message):
        messagebox.showinfo(
            title=title,
            message=message
        )

    def show_warning_message(self, title, message):
        messagebox.showwarning(
            title=title,
            message=message
        )

    def show_error_message(self, title, message):
        messagebox.showerror(
            title=title,
            message=message
        )

    def ask_simple_dialog(self, title, prompt):
        answer = simpledialog.askstring(
            title=title,
            prompt=prompt
        )
        return answer

    def ask_ok_cancel(self, title, message):
        return messagebox.askokcancel(title=title, message=message)