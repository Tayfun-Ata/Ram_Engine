import hashlib
import subprocess
import tempfile
import os
import string
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import logging

# === Logging Setup ===
logging.basicConfig(
    filename="ram_engine.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Configuration File ===
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

# === Password Hashing ===
def hash_password(password, algorithm="sha256"):
    try:
        if algorithm == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        elif algorithm == "md5":
            return hashlib.md5(password.encode()).hexdigest()
        else:
            raise ValueError("Unsupported hash algorithm.")
    except Exception as e:
        logging.error(f"Error hashing password: {e}")
        messagebox.showerror("Error", f"Error hashing password: {e}")
        return None

# === Dictionary Attack with Hashcat ===
def dictionary_attack(target_hash, hashcat_path, wordlist_path, hash_mode=1400):
    try:
        if not os.path.exists(hashcat_path):
            messagebox.showerror("Error", "Hashcat not found. Please select a valid Hashcat executable.")
            return
        if not os.path.exists(wordlist_path):
            messagebox.showerror("Error", "Wordlist file not found. Please select a valid wordlist.")
            return

        with tempfile.NamedTemporaryFile(delete=False, mode="w") as hash_file:
            hash_file.write(f"{target_hash}\n")
            hash_file_path = hash_file.name

        result = subprocess.run(
            [hashcat_path, "-m", str(hash_mode), hash_file_path, wordlist_path, "--quiet", "--show"],
            capture_output=True,
            text=True
        )

        os.remove(hash_file_path)

        if result.returncode == 0 and result.stdout.strip():
            messagebox.showinfo("Success", f"Password found: {result.stdout.strip()}")
        else:
            messagebox.showinfo("Result", "Password not found in wordlist.")
    except Exception as e:
        logging.error(f"Error during dictionary attack: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# === Brute Force Attack with Hashcat ===
def brute_force_attack(target_hash, hashcat_path, max_length=4, hash_mode=1400):
    try:
        if not os.path.exists(hashcat_path):
            messagebox.showerror("Error", "Hashcat not found. Please select a valid Hashcat executable.")
            return

        with tempfile.NamedTemporaryFile(delete=False, mode="w") as hash_file:
            hash_file.write(f"{target_hash}\n")
            hash_file_path = hash_file.name

        charset = "?l?d"  # Lowercase letters and digits
        mask = charset * max_length

        result = subprocess.run(
            [hashcat_path, "-m", str(hash_mode), hash_file_path, "-a", "3", mask, "--quiet", "--show"],
            capture_output=True,
            text=True
        )

        os.remove(hash_file_path)

        if result.returncode == 0 and result.stdout.strip():
            messagebox.showinfo("Success", f"Password found: {result.stdout.strip()}")
        else:
            messagebox.showinfo("Result", "Password not found.")
    except Exception as e:
        logging.error(f"Error during brute force attack: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")

# === Password Strength Checker ===
def check_password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = sum([has_upper, has_lower, has_digit, has_special])
    if length >= 12:
        score += 1

    if score <= 2:
        return "Weak"
    elif score == 3:
        return "Moderate"
    else:
        return "Strong"

# === GUI ===
def main():
    config = load_config()

    def select_hashcat():
        path = filedialog.askopenfilename(title="Select Hashcat Executable", filetypes=[("Executable Files", "*.exe")])
        if path:
            hashcat_path_var.set(path)
            config["hashcat_path"] = path
            save_config(config)

    def select_wordlist():
        path = filedialog.askopenfilename(title="Select Wordlist File", filetypes=[("Text Files", "*.txt")])
        if path:
            wordlist_path_var.set(path)
            config["wordlist_path"] = path
            save_config(config)

    def test_password_strength():
        password = password_entry.get().strip()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        strength = check_password_strength(password)
        messagebox.showinfo("Password Strength", f"Password Strength: {strength}")

    def run_dictionary_attack():
        password = password_entry.get().strip()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        target_hash = hash_password(password)
        if not target_hash:
            return
        dictionary_attack(target_hash, hashcat_path_var.get(), wordlist_path_var.get())

    def run_brute_force_attack():
        password = password_entry.get().strip()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return
        try:
            max_length = int(max_length_entry.get().strip())
            if max_length <= 0:
                messagebox.showerror("Error", "Maximum length must be a positive integer.")
                return
            target_hash = hash_password(password)
            if not target_hash:
                return
            brute_force_attack(target_hash, hashcat_path_var.get(), max_length)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for max length.")

    # Create the main window
    root = tk.Tk()
    root.title("Password Tester & Brute Force Simulator")

    # Hashcat Path
    tk.Label(root, text="Hashcat Path:").grid(row=0, column=0, sticky="w")
    hashcat_path_var = tk.StringVar(value=config.get("hashcat_path", ""))
    tk.Entry(root, textvariable=hashcat_path_var, width=50).grid(row=0, column=1)
    tk.Button(root, text="Browse", command=select_hashcat).grid(row=0, column=2)

    # Wordlist Path
    tk.Label(root, text="Wordlist Path:").grid(row=1, column=0, sticky="w")
    wordlist_path_var = tk.StringVar(value=config.get("wordlist_path", ""))
    tk.Entry(root, textvariable=wordlist_path_var, width=50).grid(row=1, column=1)
    tk.Button(root, text="Browse", command=select_wordlist).grid(row=1, column=2)

    # Password Entry
    tk.Label(root, text="Password:").grid(row=2, column=0, sticky="w")
    password_entry = tk.Entry(root, width=50, show="*")
    password_entry.grid(row=2, column=1)

    # Max Length for Brute Force
    tk.Label(root, text="Max Length (Brute Force):").grid(row=3, column=0, sticky="w")
    max_length_entry = tk.Entry(root, width=10)
    max_length_entry.insert(0, "4")
    max_length_entry.grid(row=3, column=1, sticky="w")

    # Buttons
    tk.Button(root, text="Test Password Strength", command=test_password_strength).grid(row=4, column=0, pady=10)
    tk.Button(root, text="Run Dictionary Attack", command=run_dictionary_attack).grid(row=4, column=1, pady=10)
    tk.Button(root, text="Run Brute Force Attack", command=run_brute_force_attack).grid(row=4, column=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")
