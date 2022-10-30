import json
import os
from json import JSONDecodeError

based_route = ""
completed_route = ""


class password_manager_model:
    def __init__(self):
        self.controller = None

    def inject_controller(self, controller):
        self.controller = controller

    def get_vault_content(self, vault_name):
        try:
            with open(f"{based_route}{vault_name}.json", "r") as vault:
                data = json.load(vault)
        except FileNotFoundError:
            return None
        except JSONDecodeError:
            return None
        else:
            return data

    def set_vault_content(self, vault_name, content):
        try:
            with open(f"{based_route}{vault_name}.json", "w") as vault:
                json.dump(content, vault, indent=4)
        except FileNotFoundError:
            return False
        except JSONDecodeError:
            return False
        else:
            return True

    def get_binary_vault_content(self, vault_name):
        try:
            with open(f"{based_route}{vault_name}.json", "rb") as vault:
                data = vault.read()
        except FileNotFoundError:
            return None
        except JSONDecodeError:
            return None
        else:
            return data

    def set_binary_vault_content(self, vault_name, content):
        try:
            with open(f"{based_route}{vault_name}.json", "wb") as vault:
                vault.write(content)
        except FileNotFoundError:
            return False
        except JSONDecodeError:
            return False
        else:
            return True

    def create_storage_folder(self, username):
        global based_route, completed_route
        based_route = f"C:/Users/{username}" # trying to write on AppData/Local
        completed_route = based_route + "/PasswordManagerApp"
        print(completed_route)
        if os.path.exists(based_route) and not os.path.exists(completed_route):
            try:
                os.mkdir(completed_route)
            except OSError:
                return None
        return completed_route

    def add_new_vault(self, vault_name, master_password):
        try:
            with open(f"{completed_route}/{vault_name}.json", "r") as vault:
                content = json.load(vault)
        except FileNotFoundError:
            content = {vault_name: master_password}
        else:
            content.update({vault_name: master_password})
        finally:
            with open(f"{completed_route}/{vault_name}.json", "w") as vault:
                json.dump(content, vault, indent=4)



