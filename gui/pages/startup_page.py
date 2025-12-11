import customtkinter as ctk

class StartupPage(ctk.CTkFrame):
    """Landing page with a clean, modern hero card and rounded design."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Grid setup
        self.grid_rowconfigure((0, 2), weight=1)
        self.grid_rowconfigure(1, weight=10)
        self.grid_columnconfigure(0, weight=1)

        self._create_main_content()
        self._create_footer()

    def _create_main_content(self):
        # Center container - reduced spacing for more compact UI
        center_container = ctk.CTkFrame(self, fg_color="transparent")
        center_container.grid(row=1, column=0, sticky="nsew", padx=60, pady=20)
        center_container.grid_columnconfigure(0, weight=1)
        center_container.grid_rowconfigure(0, weight=3)
        center_container.grid_rowconfigure(1, weight=1)

        # ------------------ HERO CARD ------------------
        hero_card = ctk.CTkFrame(
            center_container,
            corner_radius=40,       # more rounded
            fg_color="#132033",
            border_width=2,
            border_color="#00C4FF"
        )
        hero_card.grid(row=0, column=0, sticky="ew", pady=(5, 15), ipadx=10, ipady=10)

        hero_card.grid_columnconfigure(0, weight=1)

        # Inner content frame
        inner_frame = ctk.CTkFrame(hero_card, fg_color="transparent")
        inner_frame.grid(row=0, column=0, sticky="nsew", padx=25, pady=20)
        inner_frame.grid_columnconfigure(0, weight=1)

        # Status
        status_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        status_frame.grid(row=0, column=0, pady=(5, 5))
        ctk.CTkLabel(status_frame, text="●", text_color="#E53935", font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(
            status_frame,
            text="STATUS: DISCONNECTED",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#F44336"
        ).pack(side="left")

        # Main Title
        ctk.CTkLabel(
            inner_frame,
            text="Digital Fortress Awaits.",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#FFFFFF"
        ).grid(row=1, column=0, pady=(5, 10))

        # Subtitle
        ctk.CTkLabel(
            inner_frame,
            text="Log in or create an account to activate your secure connection.",
            font=ctk.CTkFont(size=13),
            text_color="#B0BEC5",
            justify="center",
            wraplength=420
        ).grid(row=2, column=0, pady=(0, 25))

        # Buttons
        btn_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(5, 25))

        login_btn = ctk.CTkButton(
            btn_frame, text="🔐 Log In", width=150, height=38, corner_radius=25,
            command=lambda: self.controller.show_page("LoginPage"),
            fg_color="#00C4FF", hover_color="#00A8D6",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        login_btn.grid(row=0, column=0, padx=10)

        signup_btn = ctk.CTkButton(
            btn_frame, text="✨ Create Account", width=150, height=38, corner_radius=25,
            command=lambda: self.controller.show_page("SignupPage"),
            fg_color="#1f6aa5", hover_color="#15486d",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        signup_btn.grid(row=0, column=1, padx=10)

        # ------------------ FEATURES ------------------
        features_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        features_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        features_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self._create_feature_label(features_frame, 0, "🛡️", "Kill Switch", "Zero IP leaks.")
        self._create_feature_label(features_frame, 1, "⚡", "Fast Speeds", "Optimized routing.")
        self._create_feature_label(features_frame, 2, "🌍", "Global Servers", "Worldwide access.")

    def _create_feature_label(self, parent, column, icon, title, desc):
        feature_item = ctk.CTkFrame(parent, fg_color="#1C3152", corner_radius=20, height=70)
        feature_item.grid(row=0, column=column, padx=10, sticky="nsew", pady=5)
        feature_item.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(feature_item, text=icon, font=ctk.CTkFont(size=24)).grid(row=0, column=0, rowspan=2, padx=10, pady=8)
        ctk.CTkLabel(feature_item, text=title, font=ctk.CTkFont(size=13, weight="bold"),text_color="#00C4FF").grid(row=0, column=1, sticky="w", pady=(8, 0))
        ctk.CTkLabel(feature_item, text=desc, font=ctk.CTkFont(size=11),text_color="#90A4AE").grid(row=1, column=1, sticky="w", pady=(0, 8))

    def _create_footer(self):
        footer = ctk.CTkLabel(
            self,
            text="© 2024 Nova Link VPN • AES-256 Encryption",
            font=ctk.CTkFont(size=11),
            text_color="#546E7A"
        )
        footer.grid(row=2, column=0, pady=(10, 10))
