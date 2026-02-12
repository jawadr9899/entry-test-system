from PIL import Image
import customtkinter as ctk
from database.database_manager import DatabaseManager

class TestView(ctk.CTkFrame):
    def __init__(self, master, user_data, on_logout, config):
        super().__init__(master, fg_color="transparent")
        self.config = config
        self.user_id, self.name, self.roll_no, self.cnic, self.pic_path = user_data
        self.on_logout = on_logout
        
        # Database & Quiz State
        self.questions = DatabaseManager.get_questions()
        self.total_q = len(self.questions)
        self.q_index = 0
        self.score = 0
        
        # Timer Setup
        self.time_left = config.PER_QUESTION_TIME * self.total_q * 60
        self.timer_running = False
        self.timer_event = None

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_content()
        
        if self.total_q > 0:
            self.load_question()
            self.start_timer()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(6, weight=1) # Spacer row

        # --- Student Profile Section ---
        ctk.CTkLabel(self.sidebar, text="STUDENT PROFILE", font=("Roboto", 18, "bold"), text_color="gray").grid(row=0, column=0, sticky="w", padx=20, pady=(30, 15))
        
        # Profile Image
        try:
            img = Image.open(self.pic_path)
            ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
            self.img_label = ctk.CTkLabel(self.sidebar, image=ctk_image, text="")
            self.img_label.grid(row=1, column=0, padx=20, pady=(0, 15))
        except Exception:
            # Fallback if image fails
            ctk.CTkLabel(self.sidebar, text="[No Image]", text_color="gray").grid(row=1, column=0, pady=10)

        # Details
        info_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        info_frame.grid(row=2, column=0, sticky="ew", padx=20)
        
        ctk.CTkLabel(info_frame, text=f"Name:", font=("Roboto", 12, "bold"), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"{self.name}", font=("Roboto", 14), wraplength=200, justify="left").pack(anchor="w", pady=(0, 10))
        
        ctk.CTkLabel(info_frame, text=f"Roll No:", font=("Roboto", 12, "bold"), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"{self.roll_no}", font=("Roboto", 14)).pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(info_frame, text=f"CNIC:", font=("Roboto", 12, "bold"), text_color="gray").pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"{self.cnic}", font=("Roboto", 14)).pack(anchor="w")

        # Separator
        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray60").grid(row=3, column=0, sticky="ew", padx=20, pady=20)

        # --- Timer Section ---
        ctk.CTkLabel(self.sidebar, text="TIME REMAINING", font=("Roboto", 12, "bold"), text_color="gray").grid(row=4, column=0, sticky="w", padx=20)
        self.timer_lbl = ctk.CTkLabel(self.sidebar, text="00:00", font=("Roboto", 36, "bold"), text_color="#3B8ED0")
        self.timer_lbl.grid(row=5, column=0, sticky="ew", padx=20, pady=(0, 10))

        # Progress
        self.progress_lbl = ctk.CTkLabel(self.sidebar, text="Q 1/10", font=("Roboto", 14))
        self.progress_lbl.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        
        # Quit Button
        ctk.CTkButton(self.sidebar, text="Quit Test", fg_color="transparent", border_width=1, hover_color="#C0392B",
                      text_color=("gray10", "gray90"), command=self.handle_quit).grid(row=8, column=0, sticky="ew", padx=20, pady=30)

    def _build_main_content(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        # Question Card
        self.q_card = ctk.CTkFrame(self.main_area, corner_radius=15, fg_color=("white", "gray20"))
        self.q_card.grid(row=0, column=0, sticky="nsew")
        self.q_card.grid_columnconfigure(0, weight=1)
        self.q_card.grid_rowconfigure(1, weight=1)

        # Question Text
        self.q_text = ctk.CTkLabel(self.q_card, text="Loading...", font=self.config.FONT_HEADER, justify="left", anchor="w")
        self.q_text.grid(row=0, column=0, sticky="ew", padx=40, pady=(40, 30))
        # Bind event to dynamically wrap text
        self.q_card.bind("<Configure>", lambda e: self.q_text.configure(wraplength=self.q_card.winfo_width() - 80))

        # Options Container
        self.opt_frame = ctk.CTkFrame(self.q_card, fg_color="transparent")
        self.opt_frame.grid(row=1, column=0, sticky="nsew", padx=40)
        
        self.var_opt = ctk.IntVar(value=0)
        self.radios = []
        
        for i in range(4):
            rb = ctk.CTkRadioButton(self.opt_frame, text=f"Option {i}", variable=self.var_opt, value=i+1,
                                    font=self.config.FONT_BODY, height=30, border_width_checked=6,
                                    command=self.enable_next)
            rb.grid(row=i, column=0, sticky="w", pady=12)
            self.radios.append(rb)

        # Next Button
        self.next_btn = ctk.CTkButton(self.q_card, text="Next Question", font=self.config.FONT_BOLD, 
                                      height=50, width=200, corner_radius=10, state="disabled", command=self.next_question)
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
            if i < len(self.radios):
                self.radios[i].configure(text=txt)

    def enable_next(self):
        self.next_btn.configure(state="normal")

    def next_question(self):
        # 1. Check Answer
        correct_index = self.questions[self.q_index][6]
        # var_opt is 1-based, correct_index is usually 0-based
        if self.var_opt.get() - 1 == correct_index:
            self.score += 1
            
        # 2. Increment
        self.q_index += 1
        
        # 3. Load Next
        self.load_question()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return

        if self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            
            # Color change warning
            text_color = "#3B8ED0"
            if self.time_left < 60:
                 text_color = "#e74c3c"
            
            self.timer_lbl.configure(text=f"{int(mins):02}:{int(secs):02}", text_color=text_color)
            self.time_left -= 1
            self.timer_event = self.after(1000, self.update_timer)
        else:
            self.timer_lbl.configure(text="00:00", text_color="red")
            self.finish_test()

    def stop_timer(self):
        self.timer_running = False
        if self.timer_event:
            self.after_cancel(self.timer_event)
            self.timer_event = None

    def handle_quit(self):
        self.stop_timer()
        self.on_logout()

    def finish_test(self):
        # CRITICAL: Stop the timer before destroying widgets or saving
        self.stop_timer()
        
        DatabaseManager.save_score(self.user_id, self.score)
        
        # clear content
        for w in self.main_area.winfo_children(): 
            w.destroy()
        
        # Results Frame
        res = ctk.CTkFrame(self.main_area, corner_radius=15, border_width=1, border_color="gray30", fg_color=("white", "gray20"))
        res.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.6)
        
        ctk.CTkLabel(res, text="Test Submitted Successfully", font=("Roboto", 24, "bold")).pack(pady=(50, 10))
        
        ctk.CTkLabel(res, text=f"{self.name}", font=("Roboto", 18)).pack()
        ctk.CTkLabel(res, text=f"{self.roll_no}", font=("Roboto", 14), text_color="gray").pack(pady=(0, 20))
        
        # Score Logic
        percentage = (self.score / self.total_q) * 100
        score_col = "#2CC985" if percentage >= 50 else "#ff5555"
        
        ctk.CTkLabel(res, text="Your Score", font=("Roboto", 14, "bold"), text_color="gray").pack()
        ctk.CTkLabel(res, text=f"{self.score} / {self.total_q}", font=("Roboto", 60, "bold"), text_color=score_col).pack(pady=10)
        
        ctk.CTkButton(res, text="Return to Home", height=45, width=200, font=("Roboto", 14, "bold"), 
                      command=self.on_logout).pack(pady=(30, 40))