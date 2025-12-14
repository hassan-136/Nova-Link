import customtkinter as ctk
from tkinter import messagebox
import json
import os
import bcrypt # Used for secure password hashing
from cryptography.fernet import Fernet # Used for symmetric data encryption (AES-based)
import datetime # Used for creating the signup timestamp


# --- CONFIGURATION CONSTANTS ---
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

def _save_users(users_data):
    """Saves all user data to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(users_data, f, indent=4)


# --- MAIN PAGE CLASS ---

class SignupPage(ctk.CTkFrame):
    """Account creation form with premium card design, theme matching, and secure backend logic."""

    def __init__(self, parent, controller):
        # Initialize encryption handler
        self.key = _load_or_generate_key()
        self.cipher = Fernet(self.key)
        
        # Set base frame to transparent to show the animated background
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Configure main grid for central alignment
        self.grid_rowconfigure(0, weight=1)  # Space above card
        self.grid_rowconfigure(1, weight=10) # Card container (takes most space)
        self.grid_rowconfigure(2, weight=1)  # Space below card / navigation
        self.grid_columnconfigure(0, weight=1)

        self._build_signup_card()
        self._build_bottom_navigation()

    def _build_signup_card(self):
        
        # --- Header outside the card ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(40, 0), sticky="s")
        
        header = ctk.CTkLabel(
            header_frame,
            text="Create Your Nova Link Account",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#4FC3F7"
        )
        header.pack(pady=(0, 5))

        caption = ctk.CTkLabel(
            header_frame,
            text="Secure your connection in just a few steps.",
            font=ctk.CTkFont(size=14),
            text_color="#B0BEC5"
        )
        caption.pack(pady=(0, 20))


        # ---------- Centered Signup Card (Themed) ----------
        card = ctk.CTkFrame(
            self,
            corner_radius=25,
            fg_color="#14263D",      # Darker interior color
            border_width=3,          # Thicker border for "glow"
            border_color="#00C4FF"   # Bright blue border
        )
        # Position card in the large center row
        card.grid(row=1, column=0, sticky="n", padx=100, pady=10) 
        
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)
        
        input_width = 220 # Set a consistent input width

        # --- Row 1: Name & Email ---
        self._create_labeled_entry(card, "Full Name", 
                                   "your full name", 
                                   0, 0, 
                                   entry_attr="name_entry",
                                   width=input_width)
        
        self._create_labeled_entry(card, "Email", 
                                   "name@example.com", 
                                   0, 1, 
                                   entry_attr="email_entry",
                                   width=input_width)

        # --- Row 2: Username & Password ---
        self._create_labeled_entry(card, "Username", 
                                   "choose a username", 
                                   2, 0, 
                                   entry_attr="user_entry",
                                   width=input_width)
        
        self._create_labeled_entry(card, "Password", 
                                   "create a strong password", 
                                   2, 1, 
                                   entry_attr="pass_entry",
                                   show="•",
                                   width=input_width)

        # --- Row 3: Confirm Password ---
        self._create_labeled_entry(card, "Confirm Password", 
                                   "re‑type password", 
                                   4, 0, 
                                   entry_attr="confirm_entry",
                                   show="•",
                                   width=input_width)
        
        # Terms Checkbox (Spanning two columns)
        self.terms_var = ctk.BooleanVar(value=False)
        terms_check = ctk.CTkCheckBox(
            card,
            text="I agree to the Terms & Privacy Policy",
            variable=self.terms_var,
            text_color="#B0BEC5"
        )
        terms_check.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(20, 10),
            padx=35,
            sticky="w",
        )

        # Signup button (Themed)
        signup_btn = ctk.CTkButton(
            card,
            text="Create Account",
            height=50,
            corner_radius=25,
            fg_color="#00C4FF",
            hover_color="#00B0E5",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._signup_clicked,
        )
        signup_btn.grid(
            row=7,
            column=0,
            columnspan=2,
            pady=(20, 30),
            padx=35,
            sticky="ew",
        )
    
    def _create_labeled_entry(self, parent, label_text, placeholder, row, column, entry_attr, show="", width=250):
        """Helper to create a themed label/entry pair."""
        
        # Label
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=13, weight="bold"), text_color="#B0BEC5")
        label.grid(row=row, column=column, pady=(20, 5), padx=35, sticky="w")
        
        # Entry
        entry = ctk.CTkEntry(
            parent, 
            placeholder_text=placeholder, 
            show=show, 
            width=width,
            height=40,
            corner_radius=10,
            fg_color="#1E3A5F" # Input field background color
        )
        entry.grid(row=row + 1, column=column, pady=(0, 15), padx=35, sticky="ew")
        setattr(self, entry_attr, entry) # Assign entry to instance attribute

    def _build_bottom_navigation(self):
        """Builds the navigation links at the bottom of the page."""
        switch_frame = ctk.CTkFrame(self, fg_color="transparent")
        switch_frame.grid(row=2, column=0, pady=(10, 30))

        # Back Button (Themed)
        back_btn = ctk.CTkButton(
            switch_frame,
            text="← Back to Startup",
            width=150,
            fg_color="transparent",
            hover_color="#1E2B3E",
            text_color="#B0BEC5",
            command=lambda: self.controller.show_page("StartupPage"),
        )
        back_btn.grid(row=0, column=0, padx=5)

        # Login Link
        label = ctk.CTkLabel(
            switch_frame,
            text="Already have an account?",
            font=ctk.CTkFont(size=14),
            text_color="#B0BEC5"
        )
        label.grid(row=0, column=1, padx=(10, 0))

        login_btn = ctk.CTkButton(
            switch_frame,
            text="Login here",
            fg_color="transparent",
            hover_color="#1E2B3E",
            text_color="#00C4FF", # Themed link color
            font=ctk.CTkFont(size=14, weight="bold", underline=True),
            command=lambda: self.controller.show_page("LoginPage"),
        )
        login_btn.grid(row=0, column=2, padx=(5, 0))


    # ---------- CRYPTOGRAPHIC CALLBACK ----------

    def _signup_clicked(self):
        """Handles signup, performs validation, hashing, and encryption."""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        confirm = self.confirm_entry.get()
        terms_ok = self.terms_var.get()

        # --- Validation ---
        if not all([name, email, username, password, confirm]):
            messagebox.showwarning("Missing data", "Please fill in all fields.")
            return
        if password != confirm:
            messagebox.showerror("Password mismatch", "Passwords do not match.")
            return
        if not terms_ok:
            messagebox.showwarning(
                "Terms Required",
                "You must agree to the Terms & Privacy Policy to create an account.",
            )
            return

        # --- Check for existing user ---
        users = _load_users()
        if username in users:
            messagebox.showerror("Signup Failed", "Username already exists. Please choose another.")
            return

        # --- 1. Hashing the Password (using bcrypt) ---
        password_bytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')

        # --- 2. Encrypting Sensitive Data (using AES/Fernet) ---
        encrypted_name = self.cipher.encrypt(name.encode()).decode()
        encrypted_email = self.cipher.encrypt(email.encode()).decode()

        # --- 3. Save to JSON (FIXED TIMESTAMP) ---
        new_user_data = {
            "name": encrypted_name,
            "email": encrypted_email,
            "hashed_password": hashed_password,
            "created_at": datetime.datetime.now().isoformat() # CORRECTED LINE
        }
        
        users[username] = new_user_data
        _save_users(users)
        
        print(f"[SIGNUP SUCCESS] User '{username}' created. Data encrypted and hashed.")
        messagebox.showinfo("Success", "Account created successfully! Proceeding to login.")
        
        # Clear fields and switch page
        self.name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.user_entry.delete(0, 'end')
        self.pass_entry.delete(0, 'end')
        self.confirm_entry.delete(0, 'end')
        self.terms_var.set(False)

        self.controller.show_page("LoginPage")