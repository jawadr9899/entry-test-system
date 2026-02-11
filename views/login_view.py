import customtkinter as ctk
from database.database_manager import DatabaseManager


class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login_success, config):
        super().__init__(master, fg_color="transparent")
        self.config = config
        self.on_login_success = on_login_success
        
        # Grid Layout
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure((0, 2), weight=1)

        # Login Card
        self.card = ctk.CTkFrame(self, corner_radius=20)
        self.card.grid(row=1, column=1, sticky="ew", padx=20)
        self.card.grid_columnconfigure(0, weight=1)

        # UI Components
        ctk.CTkLabel(self.card, text="Student Login", font=self.config.FONT_HEADER).grid(row=0, column=0, pady=(40, 5))
        ctk.CTkLabel(self.card, text="Enter your Roll No & Password", font=("Roboto", 12), text_color="gray").grid(row=1, column=0, pady=(0, 20))

        self.error_frame = ctk.CTkFrame(self.card, fg_color="transparent", height=30)
        self.error_frame.grid(row=2, column=0, sticky="ew")
        
        self.error_msg = ctk.CTkLabel(self.error_frame, text="", text_color="#FF5555", font=("Roboto", 14, "bold"))
        self.error_msg.place(relx=0.5, rely=0.5, anchor="center") 


        # Inputs
        self.roll_entry = ctk.CTkEntry(self.card, placeholder_text="Roll No. (e.g., CS-2024-001)", height=50, font=self.config.FONT_BODY, corner_radius=12)
        self.roll_entry.grid(row=3, column=0, padx=40, pady=(10, 10), sticky="ew")

        self.pass_entry = ctk.CTkEntry(self.card, placeholder_text="Password", height=50, show="*", font=config.FONT_BODY, corner_radius=12)
        self.pass_entry.grid(row=4, column=0, padx=40, pady=(10, 30), sticky="ew")

        # Login Button
        self.login_btn = ctk.CTkButton(self.card, text="Start Test", height=45, font=config.FONT_BOLD, corner_radius=12, command=self.handle_login)
        self.login_btn.grid(row=5, column=0, padx=40, pady=(0, 40), sticky="ew")

    def handle_login(self):
        roll_no = self.roll_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not roll_no or not password:
            self.show_error("Both fields can't be empty")
            return

        user, error_msg = DatabaseManager.login_student(roll_no, password)
        
        if user:
            self.on_login_success(user)
        else:
            self.show_error(error_msg)
            
            if "Password" in error_msg:
                self.pass_entry.delete(0, 'end')

    def show_error(self, msg):
        self.error_msg.configure(text=msg)
        if hasattr(self, 'error_timer'):
            self.after_cancel(self.error_timer)
        self.error_timer = self.after(3000, lambda: self.error_msg.configure(text=""))
