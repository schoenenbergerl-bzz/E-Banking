import random
import string


class Account:
    def __init__(self, contract_code, password, is_admin=False):
        self.contract_code = contract_code
        self.password = password
        self.iban = self.generate_iban()
        self.balance = 0 if not is_admin else float('inf')
        self.is_admin = is_admin

    def generate_iban(self):
        country_code = 'CH'
        bank_code = ''.join(random.choices(string.digits, k=5))
        account_number = ''.join(random.choices(string.digits, k=12))
        return f"{country_code}{bank_code}{account_number}"

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def show_balance(self):
        return f"Balance: {self.balance:.2f} CHF"


class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self.create_admin_account()

    def create_admin_account(self):
        admin = Account("admin0000", "adminpass", is_admin=True)
        self.accounts[admin.contract_code] = admin

    def create_account(self, contract_code, password):
        if contract_code in self.accounts:
            print(f"Error: An account with contract code {contract_code} already exists. No new account was created.")
            return None
        account = Account(contract_code, password)
        self.accounts[contract_code] = account
        print(f"Account with contract code {contract_code} created successfully.")
        return account

    def authenticate(self, contract_code, password):
        account = self.accounts.get(contract_code)
        if account and account.password == password:
            return account
        return None

    def transfer_money(self, from_account, to_iban, amount):
        for account in self.accounts.values():
            if account.iban == to_iban:
                if from_account.withdraw(amount):
                    account.deposit(amount)
                    return True
        return False

    def delete_account(self, contract_code):
        if contract_code in self.accounts:
            del self.accounts[contract_code]
            print(f"Account {contract_code} deleted.")
        else:
            print("Account not found.")

    def show_all_accounts(self):
        for account in self.accounts.values():
            print(f"Contract Code: {account.contract_code}, IBAN: {account.iban}, Balance: {account.show_balance()}")

    def deposit_to_account(self, contract_code, amount):
        account = self.accounts.get(contract_code)
        if account:
            account.deposit(amount)
            print(f"{amount:.2f} CHF has been deposited to account {contract_code}.")
        else:
            print("Account not found.")

    def withdraw_from_account(self, contract_code, amount):
        account = self.accounts.get(contract_code)
        if account:
            if account.withdraw(amount):
                print(f"{amount:.2f} CHF has been withdrawn from account {contract_code}.")
            else:
                print("Insufficient funds.")
        else:
            print("Account not found.")


def main():
    bank = BankingSystem()

    while True:
        print("\n--- E-Banking System ---")
        print("1. Log in")
        print("2. Create new account")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            contract_code = input("Enter contract code: ")
            password = input("Enter password: ")
            account = bank.authenticate(contract_code, password)

            if account:
                if account.is_admin:
                    while True:
                        print("\n--- Admin Menu ---")
                        print("1. View all accounts")
                        print("2. Delete an account")
                        print("3. Deposit to an account")
                        print("4. Withdraw from an account")
                        print("5. Log out")
                        admin_choice = input("Select an option: ")

                        if admin_choice == '1':
                            bank.show_all_accounts()
                        elif admin_choice == '2':
                            del_contract_code = input("Enter contract code of the account to delete: ")
                            bank.delete_account(del_contract_code)
                        elif admin_choice == '3':
                            dep_contract_code = input("Enter contract code of the account to deposit to: ")
                            amount = float(input("Enter amount to deposit: "))
                            bank.deposit_to_account(dep_contract_code, amount)
                        elif admin_choice == '4':
                            withdraw_contract_code = input("Enter contract code of the account to withdraw from: ")
                            amount = float(input("Enter amount to withdraw: "))
                            bank.withdraw_from_account(withdraw_contract_code, amount)
                        elif admin_choice == '5':
                            break
                        else:
                            print("Invalid option.")
                else:
                    while True:
                        print("\n--- Account Menu ---")
                        print(f"1. View Balance ({account.show_balance()})")
                        print(f"2. View IBAN ({account.iban})")
                        print("3. Transfer Money")
                        print("4. Log out")
                        user_choice = input("Select an option: ")

                        if user_choice == '1':
                            print(account.show_balance())
                        elif user_choice == '2':
                            print(f"Your IBAN: {account.iban}")
                        elif user_choice == '3':
                            to_iban = input("Enter IBAN of recipient: ")
                            amount = float(input("Enter amount to transfer: "))
                            if bank.transfer_money(account, to_iban, amount):
                                print("Transfer successful.")
                            else:
                                print("Transfer failed. Check balance or IBAN.")
                        elif user_choice == '4':
                            break
                        else:
                            print("Invalid option.")
            else:
                print("Authentication failed. Please try again.")

        elif choice == '2':
            contract_code = input("Enter a 9-digit contract code: ")
            if len(contract_code) != 9:
                print("Contract code must be 9 digits long.")
            elif contract_code in bank.accounts:
                print(f"Error: An account with contract code {contract_code} already exists.")
            else:
                password = input("Enter a password: ")
                bank.create_account(contract_code, password)

        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
