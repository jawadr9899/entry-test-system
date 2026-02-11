import customtkinter as ctk
from database.database_manager import DatabaseManager

class QuizView(ctk.CTkFrame):
    def __init__(self, master, user_data, on_logout,config):
        super().__init__(master, fg_color="transparent")
        self.config = config
        self.user_id, self.name, self.roll_no = user_data
        self.on_logout = on_logout
        
        self.questions = DatabaseManager.get_questions()
        self.total_q = len(self.questions)
        self.q_index = 0
        self.score = 0
        self.time_left = config.PER_QUESTION_TIME * self.total_q * 60
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_content()
        
        if self.total_q > 0:
            self.load_question()
            self.update_timer()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(5, weight=1) 

        # Student Details Display
        ctk.CTkLabel(self.sidebar, text="STUDENT PROFILE", font=("Roboto", 11, "bold"), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(30, 5))
        
        # Name
        ctk.CTkLabel(self.sidebar, text=self.name, font=("Roboto", 18, "bold"), wraplength=180, justify="left").grid(row=1, column=0, sticky="w", padx=20)
        
        # Roll No
        ctk.CTkLabel(self.sidebar, text=self.roll_no, font=("Roboto", 13)).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 20))

        ctk.CTkFrame(self.sidebar, height=1, fg_color="gray60").grid(row=3, column=0, sticky="ew", padx=20, pady=10)

        ctk.CTkLabel(self.sidebar, text="TIME REMAINING", font=("Roboto", 11, "bold"), text_color="gray").grid(row=4, column=0, sticky="w", padx=20, pady=(20, 5))
        self.timer_lbl = ctk.CTkLabel(self.sidebar, text="00:00", font=("Roboto", 30, "bold"), text_color="#3B8ED0")
        self.timer_lbl.grid(row=5, column=0, sticky="w", padx=20)

        self.progress_lbl = ctk.CTkLabel(self.sidebar, text="Q 1/10", font=("Roboto", 14))
        self.progress_lbl.grid(row=6, column=0, sticky="ew", pady=(0, 10))
        
        ctk.CTkButton(self.sidebar, text="Quit Test", fg_color="transparent", border_width=1, height=35,
                      text_color=("gray10", "gray90"), command=self.on_logout).grid(row=7, column=0, sticky="ew", padx=20, pady=30)

    def _build_main_content(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        self.q_card = ctk.CTkFrame(self.main_area, corner_radius=15, fg_color=("white", "gray20"))
        self.q_card.grid(row=0, column=0, sticky="nsew")
        self.q_card.grid_columnconfigure(0, weight=1)
        self.q_card.grid_rowconfigure(1, weight=1)

        self.q_text = ctk.CTkLabel(self.q_card, text="Loading...", font=self.config.FONT_HEADER, wraplength=500, justify="left")
        self.q_text.grid(row=0, column=0, sticky="w", padx=40, pady=(40, 20))

        self.opt_frame = ctk.CTkFrame(self.q_card, fg_color="transparent")
        self.opt_frame.grid(row=1, column=0, sticky="nsew", padx=40)
        
        self.var_opt = ctk.IntVar(value=0)
        self.radios = []
        for i in range(4):
            rb = ctk.CTkRadioButton(self.opt_frame, text=f"Option {i}", variable=self.var_opt, value=i+1,
                                    font=self.config.FONT_BODY, height=25, border_width_checked=5,
                                    command=self.enable_next)
            rb.grid(row=i, column=0, sticky="w", pady=10)
            self.radios.append(rb)

        self.next_btn = ctk.CTkButton(self.q_card, text="Next Question", font=self.config.FONT_BOLD, 
                                      height=45, width=180, corner_radius=10, state="disabled", command=self.next_question)
        self.next_btn.grid(row=2, column=0, sticky="e", padx=40, pady=40)

    def load_question(self):
        if self.q_index >= self.total_q:
            self.finish_test()
            return

        q = self.questions[self.q_index]
        self.progress_lbl.configure(text=f"Question {self.q_index + 1} / {self.total_q}")
        self.q_text.configure(text=f"{self.q_index + 1}. {q[1]}")
        
        self.var_opt.set(0)
        self.next_btn.configure(state="disabled")
        
        options = q[2:6]
        for i, txt in enumerate(options):
            self.radios[i].configure(text=txt)

    def enable_next(self):
        self.next_btn.configure(state="normal")

    def next_question(self):
        correct = self.questions[self.q_index][6]
        if self.var_opt.get()-1 == correct:
            self.score += 1
        self.q_index += 1
        self.load_question()

    def update_timer(self):
        if not self.winfo_exists():
             return
        if self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.timer_lbl.configure(text=f"{mins:02}:{secs:02}")
            self.time_left -= 1
            self.after(1000, self.update_timer)
        else:
            self.finish_test()

    def finish_test(self):
        DatabaseManager.save_score(self.user_id, self.score)
        for w in self.main_area.winfo_children(): 
            w.destroy()
        
        res = ctk.CTkFrame(self.main_area, corner_radius=15, border_width=1, border_color="gray30")
        res.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(res, text="Test Submitted", font=("Roboto Medium", 22)).pack(padx=80, pady=(40, 5))
        ctk.CTkLabel(res, text=f"{self.name}", font=("Roboto", 16, "bold")).pack()
        ctk.CTkLabel(res, text=f"{self.roll_no}", font=("Roboto", 14), text_color="gray").pack()
        
        score_col = "#2CC985" if self.score > self.total_q/2 else "#ff5555"
        ctk.CTkLabel(res, text=f"{self.score} / {self.total_q}", font=("Roboto", 50, "bold"), text_color=score_col).pack(pady=20)
        ctk.CTkButton(res, text="Save", height=40, command=self.on_logout).pack(pady=(10, 40))
