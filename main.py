import types
import customtkinter as ctk
from views import EntryTestApp
from database.loader import load_data

#config
config_dict = {
    "PER_QUESTION_TIME" : 0.1, # mins  
    "APP_SIZE" : "900x600",
    "THEME_COLOR" : "dark-blue",
    "FONT_HEADER" : ("Roboto Medium", 26),
    "FONT_BODY" : ("Roboto", 14),
    "FONT_BOLD" : ("Roboto", 14, "bold"),
    "DB_NAME":"data.db"
}
config = types.SimpleNamespace(**config_dict)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme(config.THEME_COLOR)

if __name__ == "__main__":
    load_data(config.DB_NAME)
    app = EntryTestApp(config)
    app.mainloop()