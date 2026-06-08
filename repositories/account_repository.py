import json

DATA_FILE = "accounts.json"


class AccountRepository:

    @staticmethod
    def load_accounts():
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_accounts(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)