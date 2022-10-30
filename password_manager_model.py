import json
from json import JSONDecodeError

BASED_ROUTE = ""


class password_manager_model:
    def __init__(self):
        self.controller = None

    def inject_controller(self, controller):
        self.controller = controller

    def get_vault_content(self, vault_name):
        try:
            with open(f"{BASED_ROUTE}{vault_name}.json", "r") as vault:
                data = json.load(vault)
        except FileNotFoundError:
            return None
        except JSONDecodeError:
            return None
        else:
            return data

    def set_vault_content(self, vault_name, content):
        try:
            with open(f"{BASED_ROUTE}{vault_name}.json", "w") as vault:
                json.dump(content, vault, indent=4)
        except FileNotFoundError:
            return False
        except JSONDecodeError:
            return False
        else:
            return True

    def get_binary_vault_content(self, vault_name):
        try:
            with open(f"{BASED_ROUTE}{vault_name}.json", "rb") as vault:
                data = vault.read()
        except FileNotFoundError:
            return None
        except JSONDecodeError:
            return None
        else:
            return data

    def set_binary_vault_content(self, vault_name, content):
        try:
            with open(f"{BASED_ROUTE}{vault_name}.json", "wb") as vault:
                vault.write(content)
        except FileNotFoundError:
            return False
        except JSONDecodeError:
            return False
        else:
            return True
