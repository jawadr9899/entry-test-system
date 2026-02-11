import customtkinter as ctk
from .login_view import LoginView
from .quiz_view import QuizView


class EntryTestApp(ctk.CTk):
    def __init__(self,config):
        super().__init__()
        self.config = config
        self.title("University Entry Test System")
        self.geometry(config.APP_SIZE)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
        self.show_auth()

    def show_auth(self):
        self.clear_screen()
        LoginView(self, self.start_app,self.config).grid(row=0, column=0, sticky="nsew")

    def start_app(self, user_data):
        self.clear_screen()
        QuizView(self, user_data, self.show_auth,self.config).grid(row=0, column=0, sticky="nsew")

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()
