import tkinter as tk
from tkinter import messagebox
import random

# Define the Account class
class Account:
    def __init__(self, account_number, name, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        elif amount <= 0:
            return False
        else:
            self.balance -= amount
            return True

    def get_balance(self):
        return self.balance

    def display(self):
        return f"Account Number: {self.account_number}, Account Holder: {self.name}, Balance: {self.balance}"

# Define the Bank class
class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, account_number, name, initial_deposit=0.0):
        if account_number in self.accounts:
            return False
        else:
            account = Account(account_number, name, initial_deposit)
            self.accounts[account_number] = account
            return True

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def display_all_accounts(self):
        return [account.display() for account in self.accounts.values()]


# GUI Implementation with OTP
class BankGUI:
    def __init__(self, master):
        self.master = master

        self.master.title("Python Bank with OTP Verification")
        self.master.geometry("450x450")
        self.bank = Bank()
        self.current_otp = None
        self.pending_action = None  # Holds 'deposit' or 'withdraw' and data

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        bg_color = "#f0f8ff"
        label_font = ("Segoe UI", 10, "bold")
        entry_font = ("Segoe UI", 10)
        button_font = ("Segoe UI", 10, "bold")

        self.master.configure(bg=bg_color)

        # Account creation
        tk.Label(self.master, text="Account Number:", bg=bg_color, font=label_font).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.account_number_entry = tk.Entry(self.master, font=entry_font, bg="white")
        self.account_number_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Account Holder Name:", bg=bg_color, font=label_font).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(self.master, font=entry_font, bg="white")
        self.name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.master, text="Initial Deposit:", bg=bg_color, font=label_font).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.initial_deposit_entry = tk.Entry(self.master, font=entry_font, bg="white")
        self.initial_deposit_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.master, text="Create Account", command=self.create_account, font=button_font,
                  bg="#4CAF50", fg="white", activebackground="#45a049", width=20).grid(row=3, column=1, pady=10)

        # Deposit
        tk.Label(self.master, text="Deposit Amount:", bg=bg_color, font=label_font).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.deposit_amount_entry = tk.Entry(self.master, font=entry_font, bg="white")
        self.deposit_amount_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.master, text="Deposit", command=self.initiate_deposit, font=button_font,
                  bg="#2196F3", fg="white", activebackground="#1976D2", width=20).grid(row=5, column=1, pady=10)

        # Withdraw
        tk.Label(self.master, text="Withdraw Amount:", bg=bg_color, font=label_font).grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.withdraw_amount_entry = tk.Entry(self.master, font=entry_font, bg="white")
        self.withdraw_amount_entry.grid(row=6, column=1, padx=10, pady=5)

        tk.Button(self.master, text="Withdraw", command=self.initiate_withdraw, font=button_font,
                  bg="#f44336", fg="white", activebackground="#d32f2f", width=20).grid(row=7, column=1, pady=10)

        # Check Balance
        tk.Button(self.master, text="Check Balance", command=self.check_balance, font=button_font,
                  bg="#6c63ff", fg="white", activebackground="#5c52e2", width=20).grid(row=8, column=1, pady=5)
        # Display All Accounts
        tk.Button(self.master, text="Display All Accounts", command=self.display_all_accounts, font=button_font,
                  bg="#607d8b", fg="white", activebackground="#455a64", width=20).grid(row=9, column=1, pady=5)
        
    # Helper function to validate if a string contains only digits
    def is_valid_account_number(self, account_number):
        return account_number.isdigit() and len(account_number) > 0

    # Helper function to validate if a string contains only alphabetic characters and spaces
    def is_valid_name(self, name):
        return all(char.isalpha() or char.isspace() for char in name) and len(name) > 0

    def create_account(self):
        account_number = self.account_number_entry.get().strip()
        name = self.name_entry.get().strip()
        initial_deposit_str = self.initial_deposit_entry.get().strip()

        if not account_number:
            messagebox.showerror("Invalid Input", "Account number cannot be empty.")
            return
        if not self.is_valid_account_number(account_number):
            messagebox.showerror("Invalid Input", "Account number must contain only digits.")
            return
        if not name:
            messagebox.showerror("Invalid Input", "Account holder name cannot be empty.")
            return
        # Added validation for name field
        if not self.is_valid_name(name):
            messagebox.showerror("Invalid Input", "Account holder name must contain only letters and spaces.")
            return

        try:
            initial_deposit = float(initial_deposit_str)
            if initial_deposit < 0:
                messagebox.showerror("Invalid Input", "Initial deposit cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid initial deposit amount. Please enter a number.")
            return
        except tk.TclError:  # Handles cases where the entry is completely empty and float('') fails
            initial_deposit = 0.0

        if self.bank.create_account(account_number, name, initial_deposit):
            messagebox.showinfo("Success", "Account created successfully.")
            # Clear the input fields after successful creation
            self.account_number_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.initial_deposit_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Account number already exists.")

    def initiate_deposit(self):
        account_number = self.account_number_entry.get().strip()
        amount_str = self.deposit_amount_entry.get().strip()

        if not account_number:
            messagebox.showerror("Invalid Input", "Account number cannot be empty for deposit.")
            return
        if not self.is_valid_account_number(account_number):
            messagebox.showerror("Invalid Input", "Account number must contain only digits.")
            return
        if not amount_str:
            messagebox.showerror("Invalid Input", "Deposit amount cannot be empty.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Invalid Input", "Deposit amount must be positive.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid deposit amount. Please enter a number.")
            return

        account = self.bank.get_account(account_number)
        if not account:
            messagebox.showerror("Error", "Account not found.")
            return

        # Generate OTP
        self.current_otp = f"{random.randint(100000, 999999)}"
        self.pending_action = ("deposit", account, amount)
        messagebox.showinfo("OTP Sent", f"Your OTP is: {self.current_otp}\n(For demo purposes, OTP is shown here.)")
        self.prompt_otp()

    def initiate_withdraw(self):
        account_number = self.account_number_entry.get().strip()
        amount_str = self.withdraw_amount_entry.get().strip()

        if not account_number:
            messagebox.showerror("Invalid Input", "Account number cannot be empty for withdrawal.")
            return
        if not self.is_valid_account_number(account_number):
            messagebox.showerror("Invalid Input", "Account number must contain only digits.")
            return
        if not amount_str:
            messagebox.showerror("Invalid Input", "Withdrawal amount cannot be empty.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Invalid Input", "Withdrawal amount must be positive.")
                return
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid withdrawal amount. Please enter a number.")
            return

        account = self.bank.get_account(account_number)
        if not account:
            messagebox.showerror("Error", "Account not found.")
            return

        # Generate OTP
        self.current_otp = f"{random.randint(100000, 999999)}"
        self.pending_action = ("withdraw", account, amount)
        messagebox.showinfo("OTP Sent", f"Your OTP is: {self.current_otp}\n(For demo purposes, OTP is shown here.)")
        self.prompt_otp()

    def prompt_otp(self):
        self.otp_win = tk.Toplevel(self.master)
        self.otp_win.title("OTP Verification")
        self.otp_win.configure(bg="#e8f0fe")
        self.otp_win.grab_set() # Make the OTP window modal

        tk.Label(self.otp_win, text="Enter OTP:", font=("Segoe UI", 10, "bold"), bg="#e8f0fe").pack(padx=10, pady=5)
        self.otp_entry = tk.Entry(self.otp_win, font=("Segoe UI", 10))
        self.otp_entry.pack(padx=10, pady=5)
        tk.Button(self.otp_win, text="Verify", command=self.verify_otp, font=("Segoe UI", 10, "bold"),
                  bg="#4CAF50", fg="white").pack(pady=10)
        self.otp_win.protocol("WM_DELETE_WINDOW", self.on_otp_window_close) # Handle closing the OTP window

    def on_otp_window_close(self):
        # Reset pending action if OTP window is closed without verification
        self.current_otp = None
        self.pending_action = None
        self.otp_win.destroy()


    def verify_otp(self):
        input_otp = self.otp_entry.get().strip()
        if input_otp == self.current_otp:
            action, account, amount = self.pending_action
            if action == "deposit":
                success = account.deposit(amount)
                if success:
                    messagebox.showinfo("Success", f"{amount} deposited successfully.")
                    self.deposit_amount_entry.delete(0, tk.END) # Clear deposit field
                else:
                    messagebox.showerror("Error", "Deposit failed.")
            elif action == "withdraw":
                success = account.withdraw(amount)
                if success:
                    messagebox.showinfo("Success", f"{amount} withdrawn successfully.")
                    self.withdraw_amount_entry.delete(0, tk.END) # Clear withdraw field
                else:
                    messagebox.showerror("Error", "Withdrawal failed. Insufficient balance or invalid amount.")
            self.otp_win.destroy()
            self.current_otp = None
            self.pending_action = None
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")

    def check_balance(self):
        account_number = self.account_number_entry.get().strip()
        if not account_number:
            messagebox.showerror("Invalid Input", "Account number cannot be empty to check balance.")
            return
        if not self.is_valid_account_number(account_number):
            messagebox.showerror("Invalid Input", "Account number must contain only digits.")
            return

        account = self.bank.get_account(account_number)

        if account:
            messagebox.showinfo("Balance", f"Balance: {account.get_balance()}")
        else:
            messagebox.showerror("Error", "Account not found.")

    def display_all_accounts(self):
        accounts_info = self.bank.display_all_accounts()
        if accounts_info:
            messagebox.showinfo("All Accounts", "\n".join(accounts_info))
        else:
            messagebox.showinfo("All Accounts", "No accounts in the bank.")


# Run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()
