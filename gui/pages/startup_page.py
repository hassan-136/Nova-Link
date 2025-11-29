import customtkinter as ctk

class StartupPage(ctk.CTkFrame):
    """Landing page with a premium, engaging hero card and feature overview."""

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
        # Center container
        center_container = ctk.CTkFrame(self, fg_color="transparent")
        center_container.grid(row=1, column=0, sticky="nsew", padx=80, pady=30)
        center_container.grid_columnconfigure(0, weight=1)
        center_container.grid_rowconfigure(0, weight=3)
        center_container.grid_rowconfigure(1, weight=1)

        # Hero Card
        hero_card = ctk.CTkFrame(
            center_container,
            corner_radius=30,
            fg_color="#14263D",
            border_width=3,
            border_color="#00C4FF"
        )
        hero_card.grid(row=0, column=0, sticky="ew", pady=(10, 20))
        hero_card.grid_columnconfigure(0, weight=1)
        hero_card.grid_rowconfigure(0, weight=1)
        hero_card.grid_rowconfigure(5, weight=1)

        inner_frame = ctk.CTkFrame(hero_card, fg_color="transparent")
        inner_frame.grid(row=1, column=0, rowspan=4, sticky="nsew")
        inner_frame.grid_columnconfigure(0, weight=1)

        # Status
        status_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        status_frame.grid(row=0, column=0, pady=(15, 10))
        ctk.CTkLabel(status_frame, text="●", text_color="#E53935", font=ctk.CTkFont(size=18)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(
            status_frame,
            text="STATUS: DISCONNECTED",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#F44336"
        ).pack(side="left")

        # Main Title
        ctk.CTkLabel(
            inner_frame,
            text="Digital Fortress Awaits.",
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#FFFFFF"
        ).grid(row=1, column=0, pady=(10, 15), sticky="n")

        # Subtitle
        ctk.CTkLabel(
            inner_frame,
            text="Welcome to Nova Link. Log in or create an account to activate and secure your connection.",
            font=ctk.CTkFont(size=14),
            text_color="#B0BEC5",
            justify="center",
            wraplength=500
        ).grid(row=2, column=0, pady=(0, 25), sticky="n")

        # Buttons
        btn_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        btn_frame.grid(row=3, column=0, pady=(10, 35))

        login_btn = ctk.CTkButton(
            btn_frame, text="🔐 Log In", width=160, height=40, corner_radius=20,
            command=lambda: self.controller.show_page("LoginPage"),
            fg_color="#00C4FF", hover_color="#00B0E5",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        login_btn.grid(row=0, column=0, padx=15)

        signup_btn = ctk.CTkButton(
            btn_frame, text="✨ Create New Account", width=160, height=40, corner_radius=20,
            command=lambda: self.controller.show_page("SignupPage"),
            fg_color="#1f6aa5", hover_color="#144870",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        signup_btn.grid(row=0, column=1, padx=15)

        # Features Strip
        features_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        features_frame.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        features_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self._create_feature_label(features_frame, 0, "🛡️", "Kill Switch", "Never leak your real IP.")
        self._create_feature_label(features_frame, 1, "⚡", "Blazing Speeds", "Optimized for 4K streaming.")
        self._create_feature_label(features_frame, 2, "🌍", "Global Access", "50+ virtual locations.")

    def _create_feature_label(self, parent, column, icon, title, desc):
        feature_item = ctk.CTkFrame(parent, fg_color="#1E3A5F", corner_radius=10, height=80)
        feature_item.grid(row=0, column=column, padx=10, sticky="nsew")
        feature_item.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(feature_item, text=icon, font=ctk.CTkFont(size=22)).grid(row=0, column=0, rowspan=2, padx=10, pady=8)
        ctk.CTkLabel(feature_item, text=title, font=ctk.CTkFont(size=14, weight="bold"), anchor="w", text_color="#00C4FF").grid(row=0, column=1, sticky="w", pady=(8, 0))
        ctk.CTkLabel(feature_item, text=desc, font=ctk.CTkFont(size=12), anchor="w", text_color="#90A4AE").grid(row=1, column=1, sticky="w", pady=(0, 8))

    def _create_footer(self):
        footer = ctk.CTkLabel(
            self,
            text="© 2024 Nova Link VPN • Fully Audited AES-256 Encryption",
            font=ctk.CTkFont(size=12),
            text_color="#546E7A"
        )
        footer.grid(row=2, column=0, pady=(15, 15))
