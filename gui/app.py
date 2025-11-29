import customtkinter as ctk
from PIL import Image, ImageDraw
import tkinter as tk
import math
import random
from gui.pages.startup_page import StartupPage
from gui.pages.login_page import LoginPage
from gui.pages.signup_page import SignupPage
from gui.pages.dashboard_page import DashboardPage # <-- ADDED: Import the DashboardPage

class SecureVPNApp(ctk.CTk):
    """Main application window with premium design."""

    def __init__(self):
        super().__init__()

        # ---------- Premium Window Config ----------
        self.title("Nova Link – Secure VPN Client")
        self.geometry("1400x900")
        self.minsize(1200, 800)

        # Center on screen with elegant size
        self.update_idletasks()
        w, h = 1400, 900
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Premium theme configuration
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure grid for responsive layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Build UI
        self._build_premium_brand_panel()
        self._build_premium_page_container()
        self._create_pages()
        self.show_page("StartupPage")

        # Add modern window controls
        self._add_window_controls()

    # ---------- Window Controls ----------
    def _add_window_controls(self):
        control_frame = ctk.CTkFrame(self, fg_color="transparent", height=40)
        control_frame.place(relx=0.98, rely=0.02, anchor="ne")

        minimize_btn = ctk.CTkButton(
            control_frame,
            text="─",
            width=30,
            height=30,
            fg_color="#2A3F5F",
            hover_color="#3A4F6F",
            command=self._minimize_window,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        minimize_btn.pack(side="right", padx=(5, 0))

        close_btn = ctk.CTkButton(
            control_frame,
            text="✕",
            width=30,
            height=30,
            fg_color="#2A3F5F",
            hover_color="#E53935",
            command=self.quit,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        close_btn.pack(side="right", padx=(5, 0))

    def _minimize_window(self):
        self.iconify()

    # ---------- Brand Panel ----------
    def _build_premium_brand_panel(self):
        self.brand_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#0F1C2E")
        self.brand_frame.grid(row=0, column=0, sticky="nsew")
        self.brand_frame.grid_rowconfigure(0, weight=1)
        self.brand_frame.grid_columnconfigure(0, weight=1)

        main_container = ctk.CTkFrame(self.brand_frame, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)

        self._build_header_section(main_container)
        self._build_features_section(main_container)
        self._build_footer_section(main_container)

    def _build_header_section(self, parent):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 30))

        logo_container = ctk.CTkFrame(
            header_frame, width=80, height=80, corner_radius=20,
            fg_color="#4A6FA5", border_width=2, border_color="#6A8FC5"
        )
        logo_container.pack(pady=(0, 20))
        logo_container.grid_propagate(False)

        logo_label = ctk.CTkLabel(logo_container, text="🔒", font=ctk.CTkFont(size=32), fg_color="transparent")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack()

        title = ctk.CTkLabel(
            title_frame, text="Nova Link VPN",
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color="#4FC3F7"
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            title_frame, text="PREMIUM SECURITY • LIGHTNING FAST",
            font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
            text_color="#81D4FA"
        )
        subtitle.pack(pady=(5, 0))

        status_frame = ctk.CTkFrame(
            header_frame, fg_color="#1E3A5F", corner_radius=15,
            border_width=1, border_color="#2A4F7F"
        )
        status_frame.pack(pady=20)

        status_dot = ctk.CTkLabel(status_frame, text="●", text_color="#4CAF50", font=ctk.CTkFont(size=12))
        status_dot.pack(side="left", padx=(15, 5), pady=10)

        status_text = ctk.CTkLabel(
            status_frame, text="Ready to Connect • 50+ Locations Available",
            font=ctk.CTkFont(size=12, weight="bold"), text_color="#E0E0E0"
        )
        status_text.pack(side="left", padx=(0, 15), pady=10)

    # ---------- Features Section ----------
    def _build_features_section(self, parent):
        features_frame = ctk.CTkFrame(parent, fg_color="transparent")
        features_frame.grid(row=1, column=0, sticky="nsew")
        features_frame.grid_columnconfigure(0, weight=1)
        features_frame.grid_columnconfigure(1, weight=1)

        section_title = ctk.CTkLabel(
            features_frame, text="Why Choose Nova Link?",
            font=ctk.CTkFont(size=18, weight="bold"), text_color="#4FC3F7"
        )
        section_title.grid(row=0, column=0, sticky="w", pady=(0, 20), columnspan=2)

        features = [
            {"icon": "🛡️", "title": "Military-Grade Encryption", "desc": "AES-256 bit encryption protects all your data", "color": "#4FC3F7"},
            {"icon": "🌍", "title": "Global Server Network", "desc": "1000+ servers across 50+ countries", "color": "#4CAF50"},
            {"icon": "🚫", "title": "Strict No-Logs Policy", "desc": "We never track or store your activity", "color": "#FF9800"},
            {"icon": "⚡", "title": "Lightning Fast Speeds", "desc": "Optimized servers for streaming & gaming", "color": "#9C27B0"},
            {"icon": "🔒", "title": "Kill Switch Protection", "desc": "Automatic protection if VPN disconnects", "color": "#F44336"},
            {"icon": "📱", "title": "Multi-Device Support", "desc": "Protect up to 5 devices simultaneously", "color": "#00BCD4"}
        ]

        self.feature_cards = []

        for i, feature in enumerate(features):
            row = (i // 2) + 1
            col = i % 2

            feature_card = ctk.CTkFrame(
                features_frame, corner_radius=15,
                fg_color="#1E3A5F", border_width=1, border_color="#2A4F7F"
            )
            feature_card.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            feature_card.grid_columnconfigure(1, weight=1)

            icon_label = ctk.CTkLabel(
                feature_card, text=feature["icon"], font=ctk.CTkFont(size=20), fg_color="transparent"
            )
            icon_label.grid(row=0, column=0, padx=15, pady=15, sticky="nw")

            content_frame = ctk.CTkFrame(feature_card, fg_color="transparent")
            content_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

            title_label = ctk.CTkLabel(
                content_frame, text=feature["title"], font=ctk.CTkFont(size=14, weight="bold"),
                text_color=feature["color"], anchor="w"
            )
            title_label.pack(fill="x")

            desc_label = ctk.CTkLabel(
                content_frame, text=feature["desc"], font=ctk.CTkFont(size=12),
                text_color="#B0BEC5", anchor="w", wraplength=1
            )
            desc_label.pack(fill="both", expand=True, pady=(2, 0))

            self.feature_cards.append((feature_card, content_frame, desc_label))

        # Configure rows dynamically
        for r in range(1, 4):
            features_frame.grid_rowconfigure(r, weight=1)

        # Responsive wraplength
        def update_wrap(event):
            for _, _, label in self.feature_cards:
                label.configure(wraplength=label.winfo_width() - 10)
        features_frame.bind("<Configure>", update_wrap)

    # ---------- Footer ----------
    def _build_footer_section(self, parent):
        footer_frame = ctk.CTkFrame(parent, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew", pady=(30, 0))

        stats_frame = ctk.CTkFrame(
            footer_frame, corner_radius=15, fg_color="#1E3A5F", border_width=1, border_color="#2A4F7F"
        )
        stats_frame.pack(fill="x", pady=(0, 20))

        stats_data = [("50+", "Countries", "#4FC3F7"), ("1K+", "Servers", "#4CAF50"),
                      ("10ms", "Avg Ping", "#FF9800"), ("∞", "Bandwidth", "#9C27B0")]

        for i, (value, label, color) in enumerate(stats_data):
            stat_item = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_item.grid(row=0, column=i, padx=20, pady=15, sticky="nsew")
            stats_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(stat_item, text=value, font=ctk.CTkFont(size=20, weight="bold"), text_color=color).pack()
            ctk.CTkLabel(stat_item, text=label, font=ctk.CTkFont(size=11), text_color="#90A4AE").pack()

        theme_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        theme_frame.pack(fill="x")
        ctk.CTkLabel(theme_frame, text="Interface Theme:", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#90A4AE").pack(side="left", padx=(0, 10))

        self.theme_switch = ctk.CTkSegmentedButton(
            theme_frame, values=["Light", "Dark", "Auto"], command=self._toggle_theme,
            font=ctk.CTkFont(size=12), selected_color="#4FC3F7", selected_hover_color="#29B6F6"
        )
        self.theme_switch.set("Dark")
        self.theme_switch.pack(side="left")

        ctk.CTkLabel(
            footer_frame, text="© 2024 Nova Link VPN • Protecting Digital Freedom Worldwide",
            font=ctk.CTkFont(size=10), text_color="#546E7A"
        ).pack(pady=(15, 0))

    def _toggle_theme(self, value: str):
        if value == "Auto":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode(value.lower())

    # ---------- Page Container ----------
    def _build_premium_page_container(self):
        self.page_container = ctk.CTkFrame(self, corner_radius=0, fg_color="#1E2B3E")
        self.page_container.grid(row=0, column=1, sticky="nsew")
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

        self._create_animated_background()

    def _create_animated_background(self):
        try:
            self.bg_canvas = tk.Canvas(self.page_container, highlightthickness=0, bg="#1E2B3E")
            self.bg_canvas.grid(row=0, column=0, sticky="nsew")
            self.particles = []
            self._create_particles()
            self._animate_particles()
        except Exception as e:
            # Added a fallback print in case tk.Canvas fails on some environments
            print(f"Background animation error: {e}")

    def _create_particles(self):
        canvas_width = self.page_container.winfo_width() or 700
        canvas_height = self.page_container.winfo_height() or 900

        for _ in range(30):
            x = random.randint(0, canvas_width)
            y = random.randint(0, canvas_height)
            size = random.randint(1, 3)
            speed = random.uniform(0.5, 2)
            color = random.choice(["#2C3E50", "#34495E", "#3D566E"])
            particle = self.bg_canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
            self.particles.append({"id": particle, "x": x, "y": y, "speed": speed, "size": size})

    def _animate_particles(self):
        for particle in self.particles:
            self.bg_canvas.move(particle["id"], 0, particle["speed"])
            particle["y"] += particle["speed"]
            if particle["y"] > self.page_container.winfo_height():
                self.bg_canvas.coords(
                    particle["id"], particle["x"], -10, particle["x"] + particle["size"], -10 + particle["size"]
                )
                particle["y"] = -10
        self.after(50, self._animate_particles)

    # ---------- Pages ----------
    def _create_pages(self):
        self.pages = {}
        # FIX: Added DashboardPage to the list of pages to register
        for PageClass in (StartupPage, LoginPage, SignupPage, DashboardPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.page_container, controller=self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name: str):
        frame = self.pages.get(page_name)
        if frame:
            frame.tkraise()
        else:
            # Enhanced error message for missing pages
            messagebox.showerror("Navigation Error", f"Cannot find page: '{page_name}'. Please check registration.")
            print(f"[ERROR] Page '{page_name}' not found in controller registration.")

if __name__ == "__main__":
    app = SecureVPNApp()
    app.mainloop()