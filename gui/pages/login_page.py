import customtkinter as ctk
from tkinter import messagebox
import json
import os
import bcrypt # Used for secure password hashing
from cryptography.fernet import Fernet # Used for symmetric data encryption (AES-based)
import datetime # Included for completeness


# --- CONFIGURATION CONSTANTS (Must match SignupPage) ---
DATA_FILE = "users.json"
KEY_FILE = "secret.key"


# --- HELPER FUNCTIONS FOR ENCRYPTION/DECRYPTION/FILE I/O ---

def _load_or_generate_key():
    """Loads the encryption key from file or generates a new one."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

def _load_users():
    """Loads all user data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {DATA_FILE}. Returning empty user list.")
        return {}


# --- MAIN PAGE CLASS ---

class LoginPage(ctk.CTkFrame):
    """Modern login page with card design that matches the premium theme, and cryptographic authentication."""
    
    def __init__(self, parent, controller):
        # 1. Initialize encryption handler and key
        self.key = _load_or_generate_key()
        self.cipher = Fernet(self.key)
        
        # Set base frame to transparent to show the animated background
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Configure main grid for central alignment
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1) # Card placement
        self.grid_rowconfigure(2, weight=1) # Navigation placement
        self.grid_columnconfigure(0, weight=1)

        # Build the content card and navigation
        self._build_login_card()
        self._build_bottom_navigation()

    def _build_login_card(self):
        # ---------- Centered Login Card (Themed) ----------
        card = ctk.CTkFrame(
            self, 
            corner_radius=25, 
            fg_color="#14263D",  # Darker interior color
            border_width=3,      # Thicker border for "glow"
            border_color="#00C4FF" # Bright blue border
        )
        card.grid(row=1, column=0, sticky="") # Center the card in row 1
        
        # Configure card's inner grid
        card.grid_columnconfigure(0, weight=1)

        # --- Header ---
        header = ctk.CTkLabel(
            card,
            text="Login to Nova Link VPN",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4FC3F7"
        )
        header.grid(row=0, column=0, pady=(40, 5), sticky="n")

        caption = ctk.CTkLabel(
            card,
            text="Enter your credentials to access your secure VPN.",
            font=ctk.CTkFont(size=14),
            text_color="#B0BEC5"
        )
        caption.grid(row=1, column=0, pady=(0, 30), sticky="n")

        # --- Inputs ---
        self.user_entry = ctk.CTkEntry(
            card, 
            placeholder_text="Username", 
            width=350, 
            height=45, 
            corner_radius=10,
            fg_color="#1E3A5F"
        )
        self.user_entry.grid(row=2, column=0, padx=40, pady=(0, 15), sticky="ew")

        self.pass_entry = ctk.CTkEntry(
            card, 
            placeholder_text="Password", 
            show="•", 
            width=350, 
            height=45, 
            corner_radius=10,
            fg_color="#1E3A5F"
        )
        self.pass_entry.grid(row=3, column=0, padx=40, pady=(0, 5), sticky="ew")

        # --- Options ---
        options_frame = ctk.CTkFrame(card, fg_color="transparent")
        options_frame.grid(row=4, column=0, padx=40, pady=(5, 20), sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)
        options_frame.grid_columnconfigure(1, weight=1)

        self.remember_var = ctk.BooleanVar(value=True)
        remember_check = ctk.CTkCheckBox(options_frame, text="Remember me", variable=self.remember_var)
        remember_check.grid(row=0, column=0, sticky="w")
        
        self.show_pw_var = ctk.BooleanVar(value=False)
        show_pw_check = ctk.CTkCheckBox(
            options_frame, 
            text="Show Password", 
            variable=self.show_pw_var,
            command=self._toggle_password
        )
        show_pw_check.grid(row=0, column=1, sticky="e")
        
        # --- Login Button ---
        login_btn = ctk.CTkButton(
            card, 
            text="Login", 
            width=350, 
            height=50, 
            corner_radius=25,
            fg_color="#00C4FF", 
            hover_color="#00B0E5", 
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._login_clicked
        )
        login_btn.grid(row=5, column=0, pady=(20, 30), padx=40, sticky="ew")

    def _build_bottom_navigation(self):
        """Builds the 'Back to Startup' button below the main card."""
        
        # --- Back Button (placed in row 2) ---
        back_btn = ctk.CTkButton(
            self, 
            text="← Back to Startup", 
            width=180, 
            fg_color="transparent",
            hover_color="#1E2B3E", # Dark hover to match theme
            text_color="#B0BEC5",
            # This command is correct for navigating back to the start page
            command=lambda: self.controller.show_page("StartupPage")
        )
        back_btn.grid(row=2, column=0, pady=(10, 20), sticky="n")


    def _toggle_password(self):
        """Toggles the visibility of the password entry."""
        self.pass_entry.configure(show="" if self.show_pw_var.get() else "•")

    def _login_clicked(self):
        """Handles the login attempt by verifying the password against the stored hash."""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Missing data", "Please enter your username and password.")
            return
            
        users = _load_users()
        
        if username not in users:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            return

        user_data = users[username]
        stored_hash = user_data.get("hashed_password", "").encode('utf-8')
        password_bytes = password.encode('utf-8')
        
        try:
            # Verify the entered password against the stored hash
            if bcrypt.checkpw(password_bytes, stored_hash):
                # --- Successful Login ---
                
                # Decrypting name for demonstration purposes
                encrypted_name = user_data["name"].encode()
                decrypted_name = self.cipher.decrypt(encrypted_name).decode()
                
                print(f"[LOGIN SUCCESS] User: {username} ({decrypted_name}) logged in.")
                messagebox.showinfo("Login Successful", f"Welcome back, {decrypted_name}!")
                
                # Logic to switch to the main VPN dashboard page goes here.
                self.controller.show_page("DashboardPage")
                
            else:
                # --- Failed Login: Password Mismatch ---
                messagebox.showerror("Login Failed", "Invalid username or password.")
        
        except ValueError:
             # Catches issues like a malformed stored hash
            messagebox.showerror("Login Error", "A critical authentication error occurred. Please contact support.")
            print(f"[ERROR] Bad hash format detected for user: {username}")
        except Exception as e:
            # Catches other potential issues during I/O or decryption
            messagebox.showerror("Error", "An unexpected error occurred during login.")
            print(f"[ERROR] during login for {username}: {e}")