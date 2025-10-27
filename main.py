"""
Quiz Application Main Entry Point
Coordinates all modules and manages application flow
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.gui_login import LoginScreen
from modules.gui_dashboard import DashboardScreen
from utils import file_handler, data_manager, question_manager, score_calculator
from utils import achievements, sound_effects, confetti


class QuizApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz Application")
        self.current_user = None
        self.current_screen = None
        
        # Initialize data files
        file_handler.initialize_data_files()
        
        # Start with login screen
        self.show_login()
    
    def clear_screen(self):
        """Clear all widgets from root"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # ---------- Shared UI components ----------
    def add_top_nav(self, parent):
        """Add a compact navigation bar with quick actions"""
        nav = tk.Frame(parent, bg='#eef2ff', highlightthickness=1, highlightbackground='#e2e8f0')
        nav.pack(fill=tk.X)
        
        def nav_btn(text, command):
            return tk.Button(nav, text=text, font=('Segoe UI', 10, 'bold'),
                             bg='#eef2ff', fg='#374151', relief=tk.FLAT, bd=0, cursor='hand2',
                             activebackground='#e0e7ff', command=command)
        
        nav_btn('← Dashboard', self.show_dashboard).pack(side=tk.LEFT, padx=8, pady=6)
        nav_btn('📊 Analytics', self.show_analytics).pack(side=tk.LEFT, padx=8, pady=6)
        nav_btn('🏆 Leaderboard', self.show_leaderboard).pack(side=tk.LEFT, padx=8, pady=6)
        nav_btn('👤 Profile', self.show_profile).pack(side=tk.LEFT, padx=8, pady=6)
    
    def show_login(self):
        """Show login screen"""
        self.clear_screen()
        self.current_screen = LoginScreen(self.root, self.on_login_success)
    
    def on_login_success(self, username):
        """Handle successful login"""
        self.current_user = username
        self.show_dashboard()
    
    def show_dashboard(self):
        """Show main dashboard"""
        self.clear_screen()
        callbacks = {
            'start_quiz': self.show_quiz_setup,
            'view_analytics': self.show_analytics,
            'view_history': self.show_history,
            'leaderboard': self.show_leaderboard,
            'profile': self.show_profile,
            'logout': self.logout
        }
        self.current_screen = DashboardScreen(self.root, self.current_user, callbacks)
    
    def show_quiz_setup(self):
        """Show quiz setup screen with modern UI"""
        self.clear_screen()
        main_container = tk.Frame(self.root, bg='#f5f7fa')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Quick navigation bar
        self.add_top_nav(main_container)
        
        # Centered card
        setup_card = tk.Frame(main_container, bg='white', relief=tk.FLAT, bd=0,
                             highlightthickness=1, highlightbackground='#e2e8f0')
        setup_card.place(relx=0.5, rely=0.5, anchor='center', width=600, height=650)
        
        # Header with accent
        header = tk.Frame(setup_card, bg='#667eea', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🎯 Configure Your Quiz", font=('Segoe UI', 24, 'bold'),
                        bg='#667eea', fg='white')
        title.pack(pady=25)
        
        # Content area
        content = tk.Frame(setup_card, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # Category
        tk.Label(content, text="Category", font=('Segoe UI', 11, 'bold'),
                bg='white', fg='#4a5568', anchor='w').pack(fill=tk.X, pady=(0, 5))
        category_var = tk.StringVar()
        categories = question_manager.get_categories()
        category_dropdown = ttk.Combobox(content, textvariable=category_var, values=categories,
                                        state='readonly', font=('Segoe UI', 11), width=40)
        if categories:
            category_dropdown.current(0)
        category_dropdown.pack(pady=(0, 20))
        
        # Difficulty
        tk.Label(content, text="Difficulty", font=('Segoe UI', 11, 'bold'),
                bg='white', fg='#4a5568', anchor='w').pack(fill=tk.X, pady=(0, 5))
        difficulty_var = tk.StringVar()
        difficulties = ['Easy', 'Medium', 'Hard']
        difficulty_dropdown = ttk.Combobox(content, textvariable=difficulty_var, values=difficulties,
                                          state='readonly', font=('Segoe UI', 11), width=40)
        difficulty_dropdown.current(0)
        difficulty_dropdown.pack(pady=(0, 20))
        
        # Mode with info button
        mode_header_frame = tk.Frame(content, bg='white')
        mode_header_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(mode_header_frame, text="Mode", font=('Segoe UI', 11, 'bold'),
                bg='white', fg='#4a5568', anchor='w').pack(side=tk.LEFT)
        
        # Info button for mode descriptions
        info_btn = tk.Button(mode_header_frame, text="ℹ️", font=('Segoe UI', 10),
                            bg='#e0e7ff', fg='#667eea', relief=tk.FLAT, bd=0, cursor='hand2',
                            command=self.show_mode_info)
        info_btn.pack(side=tk.LEFT, padx=5)
        
        mode_var = tk.StringVar()
        modes = ['Practice', 'Timed', 'Survival']
        mode_dropdown = ttk.Combobox(content, textvariable=mode_var, values=modes,
                                    state='readonly', font=('Segoe UI', 11), width=40)
        mode_dropdown.current(0)
        mode_dropdown.pack(pady=(0, 20))
        
        # Bind mode selection to show description
        mode_dropdown.bind('<<ComboboxSelected>>', lambda e: self.show_mode_description(mode_var.get()))
        
        # Number of questions
        tk.Label(content, text="Number of Questions", font=('Segoe UI', 11, 'bold'),
                bg='white', fg='#4a5568', anchor='w').pack(fill=tk.X, pady=(0, 5))
        count_var = tk.IntVar(value=10)
        count_dropdown = ttk.Combobox(content, textvariable=count_var, values=[5, 10, 15, 20],
                                     state='readonly', font=('Segoe UI', 11), width=40)
        count_dropdown.current(1)
        count_dropdown.pack(pady=(0, 30))
        
        # Buttons
        start_btn = tk.Button(content, text="Start Quiz →", font=('Segoe UI', 13, 'bold'),
                             bg='#667eea', fg='white', relief=tk.FLAT, bd=0, cursor='hand2',
                             activebackground='#5568d3',
                             command=lambda: self.start_quiz(category_var.get(), difficulty_var.get(),
                                                           mode_var.get(), int(count_var.get())))
        start_btn.pack(fill=tk.X, pady=(0, 10), ipady=12)
        
        back_btn = tk.Button(content, text="← Back", font=('Segoe UI', 11),
                            bg='#f7fafc', fg='#667eea', relief=tk.FLAT, bd=0, cursor='hand2',
                            activebackground='#edf2f7', command=self.show_dashboard)
        back_btn.pack(fill=tk.X, ipady=12)
    
    def show_mode_info(self):
        """Show information about all quiz modes"""
        info_text = """\n🎯 QUIZ MODES\n
📝 Practice Mode:
• Untimed practice session
• Immediate feedback with explanations
• Perfect for learning
• No time pressure

⏱️ Timed Mode:
• 15-second countdown per question
• Time bonus points available:
  - Answer in ≤10s: +5 bonus points
  - Answer in ≤20s: +3 bonus points
• Test your speed and knowledge!

💪 Survival Mode:
• 3 lives only
• Game ends after 3 wrong answers
• 1.5x score multiplier for 5+ correct streak
• High stakes challenge!
"""
        messagebox.showinfo("Quiz Modes", info_text)
    
    def show_mode_description(self, mode):
        """Show description popup for selected mode"""
        descriptions = {
            'Practice': "📝 Practice Mode\n\nTake your time to learn!\n• No timer\n• Detailed explanations\n• Perfect for studying",
            'Timed': "⏱️ Timed Mode\n\nRace against the clock!\n• 15 seconds per question\n• Earn time bonuses\n• Fast answers = more points",
            'Survival': "💪 Survival Mode\n\nOnly 3 lives!\n• Game ends at 3 mistakes\n• 5+ streak = 1.5x multiplier\n• High risk, high reward"
        }
        
        if mode in descriptions:
            # Create a small popup window
            popup = tk.Toplevel(self.root)
            popup.title(f"{mode} Mode")
            popup.geometry("350x200")
            popup.configure(bg='white')
            
            # Center popup
            popup.transient(self.root)
            popup.grab_set()
            
            msg_label = tk.Label(popup, text=descriptions[mode], font=('Segoe UI', 11),
                               bg='white', fg='#2d3748', justify=tk.LEFT, padx=20, pady=20)
            msg_label.pack(expand=True, fill=tk.BOTH)
            
            ok_btn = tk.Button(popup, text="Got it!", font=('Segoe UI', 11, 'bold'),
                             bg='#667eea', fg='white', relief=tk.FLAT, command=popup.destroy,
                             cursor='hand2', activebackground='#5568d3')
            ok_btn.pack(pady=(0, 15), padx=50, fill=tk.X, ipady=8)
    
    def start_quiz(self, category, difficulty, mode, count):
        """Start the quiz"""
        # Get questions
        questions = question_manager.get_random_questions(category, difficulty, count)
        
        if not questions:
            messagebox.showerror("Error", "No questions available for this selection")
            return
        
        # Show quiz screen
        self.show_quiz_screen(questions, category, difficulty, mode)
    
    def show_quiz_screen(self, questions, category, difficulty, mode):
        """Display quiz interface"""
        self.clear_screen()
        
        # Update streak when starting quiz
        streak = achievements.update_streak(self.current_user)
        
        self.quiz_data = {
            'questions': questions,
            'current_index': 0,
            'correct': 0,
            'wrong': 0,
            'answers': [],
            'category': category,
            'difficulty': difficulty,
            'mode': mode,
            'question_start_time': None,
            'total_time': 0,
            'time_bonuses': [],
            'consecutive_correct': 0,
            'timer_seconds': 15,
            'timer_id': None,
            'hints_remaining': 3,  # 3 hints per quiz
            'hints_used': [],  # Track which questions used hints
            'eliminated_options': []  # Track eliminated options for current question
        }
        
        self.show_question()
    
    def show_question(self):
        """Display current question with modern UI"""
        self.clear_screen()
        
        # Main container with gradient-like effect
        main_container = tk.Frame(self.root, bg='#f5f7fa')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Quick navigation bar
        self.add_top_nav(main_container)
        
        # Quiz card (centered modern card design)
        quiz_frame = tk.Frame(main_container, bg='white', relief=tk.FLAT, bd=0, highlightthickness=2, highlightbackground='#e0e6ed')
        quiz_frame.place(relx=0.5, rely=0.5, anchor='center', width=800, height=600)
        
        data = self.quiz_data
        question = data['questions'][data['current_index']]
        
        # Reset timer for this question
        data['timer_seconds'] = 15
        data['question_start_time'] = time.time()
        
        # Top bar with gradient background
        top_bar = tk.Frame(quiz_frame, bg='#667eea', height=100)
        top_bar.pack(fill=tk.X, side=tk.TOP)
        top_bar.pack_propagate(False)
        
        # Question counter and mode
        mode_display = f" • {data['mode']} Mode" if data['mode'] != 'Practice' else ""
        header = tk.Label(top_bar, text=f"Question {data['current_index'] + 1} of {len(data['questions'])}{mode_display}",
                         font=('Segoe UI', 14, 'bold'), bg='#667eea', fg='white')
        header.pack(pady=8)
        
        # Score display
        score_text = f"✓ {data['correct']}  ✗ {data['wrong']}"
        if data['mode'] == 'Survival':
            lives = 3 - data['wrong']
            score_text += f"  •  Lives: {'❤️' * lives}"
        elif data['mode'] == 'Timed':
            score_text += f"  •  Bonus: {sum(data['time_bonuses'])}"
        
        score_label = tk.Label(top_bar, text=score_text, font=('Segoe UI', 11), bg='#667eea', fg='#ffffff')
        score_label.pack()
        
        # Timer display (show only in Timed mode)
        self.timer_label = tk.Label(top_bar, text="", font=('Segoe UI', 16, 'bold'), bg='#667eea', fg='#ffd700')
        self.timer_label.pack(pady=3)
        
        # Start countdown timer only for Timed mode
        if data['mode'] == 'Timed':
            self.timer_label.config(text=f"⏱ {data['timer_seconds']}")
            self.update_question_timer()
        else:
            self.timer_label.config(text="")
        
        # Content area
        content_frame = tk.Frame(quiz_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Question text with modern styling
        q_frame = tk.Frame(content_frame, bg='#f8f9fa', relief=tk.FLAT, bd=0, highlightthickness=1, highlightbackground='#dee2e6')
        q_frame.pack(fill=tk.X, pady=(0, 25))
        q_label = tk.Label(q_frame, text=question['question'], font=('Segoe UI', 13), bg='#f8f9fa', 
                          wraplength=680, justify=tk.LEFT, fg='#2d3748')
        q_label.pack(padx=25, pady=20)
        
        # Options with modern radio buttons and visual feedback
        self.selected_option = tk.IntVar(value=-1)
        options_frame = tk.Frame(content_frame, bg='white')
        options_frame.pack(fill=tk.BOTH, expand=True)
        
        # Store option containers for highlighting
        self.option_containers = []
        
        def on_option_select():
            """Highlight selected option container"""
            selected = self.selected_option.get()
            for idx, container in enumerate(self.option_containers):
                if idx == selected:
                    # Highlight selected
                    container.config(bg='#e0e7ff', highlightbackground='#667eea', highlightthickness=2)
                    for child in container.winfo_children():
                        child.config(bg='#e0e7ff')
                else:
                    # Reset others
                    container.config(bg='#ffffff', highlightbackground='#e2e8f0', highlightthickness=1)
                    for child in container.winfo_children():
                        child.config(bg='#ffffff')
        
        for i, option in enumerate(question['options']):
            option_container = tk.Frame(options_frame, bg='#ffffff', relief=tk.FLAT, bd=0, 
                                       highlightthickness=1, highlightbackground='#e2e8f0')
            option_container.pack(fill=tk.X, pady=6)
            self.option_containers.append(option_container)
            
            rb = tk.Radiobutton(option_container, text=f"{chr(65+i)}. {option}", variable=self.selected_option,
                               value=i, font=('Segoe UI', 11, 'bold'), bg='#ffffff', anchor='w', 
                               activebackground='#e0e7ff', selectcolor='#667eea', fg='#2d3748',
                               command=on_option_select, cursor='hand2')
            rb.pack(fill=tk.X, padx=15, pady=12)
        
        # Hint and Submit buttons container
        button_container = tk.Frame(content_frame, bg='white')
        button_container.pack(pady=15)
        
        # Hint button (50/50 lifeline)
        data = self.quiz_data
        if data['hints_remaining'] > 0:
            hint_btn = tk.Button(button_container, text=f"💡 Hint ({data['hints_remaining']} left)", 
                                font=('Segoe UI', 10, 'bold'),
                                bg='#f59e0b', fg='white', relief=tk.FLAT, cursor='hand2',
                                activebackground='#d97706', command=self.use_hint)
            hint_btn.pack(side=tk.LEFT, padx=5, ipady=8, ipadx=15)
        
        # Submit button with modern styling
        submit_btn = tk.Button(button_container, text="Submit Answer →", font=('Segoe UI', 12, 'bold'), 
                              bg='#667eea', fg='white', relief=tk.FLAT, cursor='hand2',
                              activebackground='#5568d3', command=self.submit_answer)
        submit_btn.pack(side=tk.LEFT, padx=5, ipady=8, ipadx=20)
    
    def _update_hint_button_recursive(self, widget):
        """Recursively find and update hint button"""
        try:
            if isinstance(widget, tk.Button) and '💡 Hint' in widget['text']:
                data = self.quiz_data
                if data['hints_remaining'] > 0:
                    widget.config(text=f"💡 Hint ({data['hints_remaining']} left)")
                else:
                    widget.config(state='disabled', bg='#d1d5db')
                return
            for child in widget.winfo_children():
                self._update_hint_button_recursive(child)
        except:
            pass
    
    def use_hint(self):
        """Use 50/50 hint - eliminate 2 wrong answers"""
        data = self.quiz_data
        
        if data['hints_remaining'] <= 0:
            messagebox.showwarning("No Hints", "You've used all your hints!")
            return
        
        question = data['questions'][data['current_index']]
        correct_answer = question['correct']
        
        # Get wrong answer indices
        wrong_indices = [i for i in range(4) if i != correct_answer]
        
        # Randomly eliminate 2 wrong answers
        import random
        to_eliminate = random.sample(wrong_indices, min(2, len(wrong_indices)))
        
        # Store eliminated options
        data['eliminated_options'] = to_eliminate
        data['hints_remaining'] -= 1
        
        # Play sound
        sound_effects.sound_manager.play_achievement()
        
        # Disable eliminated option buttons
        for idx in to_eliminate:
            container = self.option_containers[idx]
            # Grey out the container
            container.config(bg='#e5e7eb')
            for child in container.winfo_children():
                child.config(bg='#e5e7eb', fg='#9ca3af', state='disabled')
        
        # Update hint button text instead of refreshing entire question
        for widget in self.root.winfo_children():
            self._update_hint_button_recursive(widget)
    
    def update_timer(self):
        """Update timer display for Timed mode"""
        if not hasattr(self, 'timer_label') or not self.timer_label.winfo_exists():
            return
        
        data = self.quiz_data
        if data['question_start_time']:
            elapsed = int(time.time() - data['question_start_time'])
            self.timer_label.config(text=f"Time: {elapsed}s")
            # Schedule next update
            self.root.after(100, self.update_timer)
    
    def update_question_timer(self):
        """Update 15-second countdown timer for each question"""
        if not hasattr(self, 'timer_label') or not self.timer_label.winfo_exists():
            return
        
        # Ensure timer is only active in Timed mode
        if self.quiz_data.get('mode') != 'Timed':
            return
        
        data = self.quiz_data
        
        if data['timer_seconds'] > 0:
            # Update display
            self.timer_label.config(text=f"⏱ {data['timer_seconds']}")
            
            # Change color based on remaining time
            if data['timer_seconds'] <= 5:
                self.timer_label.config(fg='#ff4444')  # Red for last 5 seconds
            elif data['timer_seconds'] <= 10:
                self.timer_label.config(fg='#ff9800')  # Orange for 6-10 seconds
            else:
                self.timer_label.config(fg='#ffd700')  # Gold for 11-15 seconds
            
            # Decrement and schedule next update
            data['timer_seconds'] -= 1
            data['timer_id'] = self.root.after(1000, self.update_question_timer)
        else:
            # Time's up! Auto-submit as wrong answer
            self.timer_label.config(text="⏱ 0", fg='#ff0000')
            self.time_expired()
    
    def time_expired(self):
        """Handle timer expiration - mark as unanswered and move to next question"""
        # Cancel any pending timer
        if self.quiz_data.get('timer_id'):
            self.root.after_cancel(self.quiz_data['timer_id'])
        
        data = self.quiz_data
        question = data['questions'][data['current_index']]
        
        # Calculate time taken (full 15 seconds)
        time_taken = 15.0
        data['total_time'] += time_taken
        
        # Mark as wrong (unanswered)
        data['wrong'] += 1
        data['consecutive_correct'] = 0
        
        # Check Survival mode game over
        if data['mode'] == 'Survival' and data['wrong'] >= 3:
            self.show_results()
            return
        
        # Store answer as unanswered
        data['answers'].append({
            'question': question,
            'selected': -1,  # -1 indicates no answer (time expired)
            'correct': False,
            'time_taken': time_taken
        })
        
        # Show brief feedback that time expired
        self.show_time_expired_feedback(question)
    
    def submit_answer(self):
        """Process submitted answer"""
        # Cancel timer
        if self.quiz_data.get('timer_id'):
            self.root.after_cancel(self.quiz_data['timer_id'])
        
        selected = self.selected_option.get()
        
        if selected == -1:
            messagebox.showwarning("Warning", "Please select an answer")
            # Restart timer after warning
            self.update_question_timer()
            return
        
        data = self.quiz_data
        question = data['questions'][data['current_index']]
        correct_ans = question['correct']
        
        # Calculate time taken
        time_taken = 0
        if data['question_start_time']:
            time_taken = time.time() - data['question_start_time']
            data['total_time'] += time_taken
        
        # Check if correct
        is_correct = (selected == correct_ans)
        
        if is_correct:
            data['correct'] += 1
            data['consecutive_correct'] += 1
            
            # Play correct sound
            sound_effects.sound_manager.play_correct()
            
            # Calculate time bonus for Timed mode
            if data['mode'] == 'Timed':
                bonus = score_calculator.calculate_time_bonus(time_taken)
                data['time_bonuses'].append(bonus)
                if bonus > 0:
                    sound_effects.sound_manager.play_streak()  # Bonus sound
        else:
            data['wrong'] += 1
            data['consecutive_correct'] = 0
            
            # Play wrong sound
            sound_effects.sound_manager.play_wrong()
            
            # Check Survival mode game over
            if data['mode'] == 'Survival' and data['wrong'] >= 3:
                # Game over - show results immediately
                self.show_results()
                return
        
        # Store answer
        data['answers'].append({
            'question': question,
            'selected': selected,
            'correct': is_correct,
            'time_taken': time_taken
        })
        
        # Show feedback (or skip for Timed/Survival to keep pace)
        if data['mode'] == 'Practice':
            self.show_feedback(is_correct, question)
        else:
            # For Timed/Survival, show brief feedback then move on
            self.show_brief_feedback(is_correct, question)
    
    def show_feedback(self, is_correct, question):
        """Show answer feedback for Practice mode"""
        self.clear_screen()
        
        main_container = tk.Frame(self.root, bg='#f5f7fa')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Quick navigation bar
        self.add_top_nav(main_container)
        
        feedback_card = tk.Frame(main_container, bg='white', relief=tk.FLAT, bd=0,
                                highlightthickness=1, highlightbackground='#e2e8f0')
        feedback_card.place(relx=0.5, rely=0.5, anchor='center', width=700, height=500)
        
        # Result header
        if is_correct:
            result_text = "✓ Correct!"
            color = '#10b981'
        else:
            result_text = "✗ Incorrect"
            color = '#ef4444'
        
        result_label = tk.Label(feedback_card, text=result_text, font=('Segoe UI', 36, 'bold'),
                               fg=color, bg='white')
        result_label.pack(pady=(40, 20))
        
        # Correct answer
        correct_label = tk.Label(feedback_card, text=f"Correct Answer: {question['options'][question['correct']]}",
                                font=('Segoe UI', 14), bg='white', fg='#2d3748')
        correct_label.pack(pady=10)
        
        # Explanation
        exp_frame = tk.Frame(feedback_card, bg='#f8f9fa', relief=tk.FLAT, bd=0,
                            highlightthickness=1, highlightbackground='#dee2e6')
        exp_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        exp_label = tk.Label(exp_frame, text=f"Explanation:\n{question['explanation']}",
                            font=('Segoe UI', 11), bg='#f8f9fa', fg='#4a5568',
                            wraplength=600, justify=tk.LEFT)
        exp_label.pack(padx=25, pady=20)
        
        # Buttons
        btn_container = tk.Frame(feedback_card, bg='white')
        btn_container.pack(fill=tk.X, padx=40, pady=(0, 30))
        
        next_btn = tk.Button(btn_container, text="Next Question →", font=('Segoe UI', 12, 'bold'),
                            bg='#667eea', fg='white', relief=tk.FLAT, bd=0, cursor='hand2',
                            activebackground='#5568d3', command=self.next_question)
        next_btn.pack(fill=tk.X, pady=(0, 8), ipady=12)
        
        back_btn = tk.Button(btn_container, text="← Back to Dashboard", font=('Segoe UI', 10),
                            bg='#f7fafc', fg='#667eea', relief=tk.FLAT, bd=0, cursor='hand2',
                            activebackground='#edf2f7', command=self.show_dashboard)
        back_btn.pack(fill=tk.X, ipady=10)
    
    def show_time_expired_feedback(self, question):
        """Show feedback when time expires"""
        self.clear_screen()
        
        feedback_frame = tk.Frame(self.root, bg='#f5f7fa')
        feedback_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Time expired message
        result_label = tk.Label(feedback_frame, text="⏱ Time's Up!", font=('Segoe UI', 36, 'bold'), 
                               fg='#e74c3c', bg='#f5f7fa')
        result_label.pack(pady=60)
        
        # Show correct answer
        correct_label = tk.Label(feedback_frame, text=f"Correct Answer: {question['options'][question['correct']]}",
                                font=('Segoe UI', 16), bg='#f5f7fa', fg='#2d3748')
        correct_label.pack(pady=20)
        
        # Auto-advance after 1.5 seconds
        self.root.after(1500, self.next_question)
    
    def show_brief_feedback(self, is_correct, question):
        """Show brief feedback for Timed/Survival modes"""
        self.clear_screen()
        
        feedback_frame = tk.Frame(self.root, bg='#f5f7fa')
        feedback_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Result
        if is_correct:
            result_text = "✓ Correct!"
            color = '#27ae60'
        else:
            result_text = "✗ Incorrect"
            color = '#e74c3c'
        
        result_label = tk.Label(feedback_frame, text=result_text, font=('Segoe UI', 32, 'bold'), 
                               fg=color, bg='#f5f7fa')
        result_label.pack(pady=60)
        
        # Show correct answer if wrong
        if not is_correct:
            correct_label = tk.Label(feedback_frame, text=f"Correct Answer: {question['options'][question['correct']]}",
                                    font=('Segoe UI', 16), bg='#f5f7fa', fg='#2d3748')
            correct_label.pack(pady=20)
        
        # Mode-specific messages
        data = self.quiz_data
        if data['mode'] == 'Survival' and data['consecutive_correct'] >= 5:
            bonus_label = tk.Label(feedback_frame, text="🔥 5+ Streak! 1.5x Multiplier Active!",
                                  font=('Segoe UI', 14, 'bold'), bg='#f5f7fa', fg='#f39c12')
            bonus_label.pack(pady=10)
        elif data['mode'] == 'Timed' and len(data['time_bonuses']) > 0 and data['time_bonuses'][-1] > 0:
            bonus_label = tk.Label(feedback_frame, text=f"⚡ Time Bonus: +{data['time_bonuses'][-1]} points!",
                                  font=('Segoe UI', 14, 'bold'), bg='#f5f7fa', fg='#3498db')
            bonus_label.pack(pady=10)
        
        # Auto-advance after 1.5 seconds
        self.root.after(1500, self.next_question)
    
    def next_question(self):
        """Move to next question or show results"""
        data = self.quiz_data
        data['current_index'] += 1
        
        if data['current_index'] < len(data['questions']):
            self.show_question()
        else:
            self.show_results()
    
    def show_results(self):
        """Display quiz results"""
        self.clear_screen()
        
        data = self.quiz_data
        total = len(data['questions'])
        correct = data['correct']
        wrong = data['wrong']
        
        # Calculate score using NumPy based on mode
        percentage = score_calculator.calculate_percentage(correct, total)
        
        if data['mode'] == 'Timed':
            # Add time bonuses
            base_score = score_calculator.calculate_base_score(correct, data['difficulty'])
            time_bonus = sum(data['time_bonuses'])
            score = base_score + time_bonus
        elif data['mode'] == 'Survival':
            # Apply combo multiplier if applicable
            score = score_calculator.calculate_base_score(correct, data['difficulty'])
            if correct >= 5:
                score = int(score * 1.5)
        else:
            # Practice mode - base scoring
            score = score_calculator.calculate_base_score(correct, data['difficulty'])
        
        grade_info = score_calculator.get_grade_info(percentage)
        
        # Save to database
        time_taken = int(data['total_time'])
        data_manager.add_quiz_attempt(
            self.current_user, data['category'], data['difficulty'], total,
            correct, wrong, score, percentage, time_taken, data['mode']
        )
        
        # Check for new achievements
        new_achievements = achievements.check_and_unlock_achievements(self.current_user)
        
        # Play sound effects
        if percentage == 100:
            sound_effects.sound_manager.play_perfect_score()
        elif percentage >= 90:
            sound_effects.sound_manager.play_level_up()
        
        main_container = tk.Frame(self.root, bg='#f5f7fa')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Show confetti for perfect score
        if percentage == 100:
            confetti.show_confetti(main_container, duration=3000)
        
        # Results card - directly in main container, centered
        results_card = tk.Frame(main_container, bg='white', relief=tk.FLAT, bd=0,
                               highlightthickness=1, highlightbackground='#e2e8f0')
        results_card.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title with icon
        title = tk.Label(results_card, text="🏆 Quiz Complete!", font=('Segoe UI', 28, 'bold'),
                        bg='white', fg='#2d3748')
        title.pack(pady=20)
        
        # Score display with modern card
        score_frame = tk.Frame(results_card, bg=grade_info['color'], relief=tk.FLAT, bd=0)
        score_frame.pack(pady=15, padx=50, fill=tk.X)
        
        percentage_label = tk.Label(score_frame, text=f"{percentage:.1f}%",
                                    font=('Segoe UI', 48, 'bold'),
                                    bg=grade_info['color'], fg='white')
        percentage_label.pack(pady=(20, 5))
        
        grade_label = tk.Label(score_frame, text=grade_info['grade'],
                              font=('Segoe UI', 16, 'bold'),
                              bg=grade_info['color'], fg='white')
        grade_label.pack(pady=(0, 20))
        
        # Stats grid
        stats_container = tk.Frame(results_card, bg='white')
        stats_container.pack(fill=tk.X, padx=50, pady=15)
        
        stat_items = [
            ("📋", "Questions", total),
            ("✅", "Correct", correct),
            ("❌", "Wrong", wrong),
            ("⭐", "Score", score)
        ]
        
        for i, (icon, label, value) in enumerate(stat_items):
            stat_frame = tk.Frame(stats_container, bg='#f8f9fa', relief=tk.FLAT, bd=0,
                                 highlightthickness=1, highlightbackground='#e2e8f0')
            stat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            icon_label = tk.Label(stat_frame, text=icon, font=('Segoe UI', 18),
                                 bg='#f8f9fa')
            icon_label.pack(pady=(8, 0))
            
            value_label = tk.Label(stat_frame, text=str(value), font=('Segoe UI', 16, 'bold'),
                                  bg='#f8f9fa', fg='#2d3748')
            value_label.pack()
            
            label_text = tk.Label(stat_frame, text=label, font=('Segoe UI', 9),
                                 bg='#f8f9fa', fg='#718096')
            label_text.pack(pady=(0, 8))
        
        # Mode-specific bonus info
        if data['mode'] == 'Timed' and sum(data['time_bonuses']) > 0:
            bonus_label = tk.Label(results_card,
                                  text=f"⚡ Time Bonus: +{sum(data['time_bonuses'])} points | Total Time: {int(data['total_time'])}s",
                                  font=('Segoe UI', 10), bg='white', fg='#667eea')
            bonus_label.pack(pady=8)
        elif data['mode'] == 'Survival' and correct >= 5:
            bonus_label = tk.Label(results_card, text="🔥 1.5x Multiplier Applied!",
                                  font=('Segoe UI', 10, 'bold'), bg='white', fg='#f59e0b')
            bonus_label.pack(pady=8)
        
        # Show achievement notifications
        if new_achievements:
            achievement_frame = tk.Frame(results_card, bg='#fef3c7', relief=tk.FLAT, bd=0,
                                        highlightthickness=1, highlightbackground='#f59e0b')
            achievement_frame.pack(fill=tk.X, padx=50, pady=10)
            
            tk.Label(achievement_frame, text="🏆 New Achievements Unlocked!", 
                    font=('Segoe UI', 11, 'bold'), bg='#fef3c7', fg='#92400e').pack(pady=(10, 5))
            
            for achievement in new_achievements[:3]:  # Show up to 3
                achievement_text = f"{achievement['icon']} {achievement['name']}"
                tk.Label(achievement_frame, text=achievement_text, font=('Segoe UI', 9),
                        bg='#fef3c7', fg='#78350f').pack(pady=2)
            
            tk.Label(achievement_frame, text="" if len(new_achievements) <= 3 else f"+{len(new_achievements)-3} more",
                    font=('Segoe UI', 8), bg='#fef3c7', fg='#78350f').pack(pady=(0, 10))
        
        # Buttons - quick redirection row
        btn_container = tk.Frame(results_card, bg='white')
        btn_container.pack(fill=tk.X, padx=50, pady=(15, 25))
        
        def cta(text, color_bg, color_fg, cmd):
            return tk.Button(btn_container, text=text, font=('Segoe UI', 11, 'bold'),
                             bg=color_bg, fg=color_fg, relief=tk.FLAT, bd=0, cursor='hand2',
                             activebackground=color_bg, command=cmd)
        
        # Arrange in a single row
        dashboard_btn = cta('🏠 Dashboard', '#667eea', 'white', self.show_dashboard)
        analytics_btn = cta('📊 Analytics', '#f7fafc', '#667eea', self.show_analytics)
        leaderboard_btn = cta('🏆 Leaderboard', '#f7fafc', '#667eea', self.show_leaderboard)
        
        dashboard_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, ipady=10)
        analytics_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, ipady=10)
        leaderboard_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, ipady=10)
    
    def show_analytics(self):
        """Show analytics with matplotlib graphs"""
        try:
            from modules import gui_analytics
            self.clear_screen()
            gui_analytics.AnalyticsScreen(self.root, self.current_user, self.show_dashboard)
        except ImportError:
            # Fallback if matplotlib module not available
            messagebox.showinfo("Analytics", "Analytics feature requires additional setup")
            self.show_dashboard()
    
    def show_history(self):
        """Show quiz history"""
        try:
            from modules import gui_history
            self.clear_screen()
            gui_history.HistoryScreen(self.root, self.current_user, self.show_dashboard)
        except ImportError:
            messagebox.showinfo("History", f"Quiz history for {self.current_user}")
            self.show_dashboard()
    
    def show_leaderboard(self):
        """Show leaderboard with modern UI"""
        self.clear_screen()
        
        main_container = tk.Frame(self.root, bg='#f5f7fa')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Quick navigation bar
        self.add_top_nav(main_container)
        
        # Header
        header = tk.Frame(main_container, bg='#667eea', height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🏆 Leaderboard", font=('Segoe UI', 28, 'bold'),
                        bg='#667eea', fg='white')
        title.pack(pady=30)
        
        # Content
        content = tk.Frame(main_container, bg='#f5f7fa')
        content.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Get top scores
        top_scores = data_manager.get_top_scores(10)
        # Reset index for proper ranking
        top_scores = top_scores.reset_index(drop=True)
        
        # Create modern table card
        table_card = tk.Frame(content, bg='white', relief=tk.FLAT, bd=0,
                             highlightthickness=1, highlightbackground='#e2e8f0')
        table_card.pack(fill=tk.BOTH, expand=True)
        
        # Configure ttk style for modern look
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base
        
        # Configure Treeview style
        style.configure('Modern.Treeview',
                       background='white',
                       foreground='#2d3748',
                       fieldbackground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        style.configure('Modern.Treeview.Heading',
                       background='#f8f9fa',
                       foreground='#4a5568',
                       borderwidth=1,
                       relief='flat',
                       font=('Segoe UI', 11, 'bold'))
        
        style.map('Modern.Treeview',
                 background=[('selected', '#e0e7ff')],
                 foreground=[('selected', '#2d3748')])
        
        # Create Treeview
        columns = ('Rank', 'Username', 'Category', 'Score', 'Percentage', 'Date')
        tree = ttk.Treeview(table_card, columns=columns, show='headings', 
                           style='Modern.Treeview', height=10)
        
        # Define column headings and widths
        tree.heading('Rank', text='Rank')
        tree.heading('Username', text='Username')
        tree.heading('Category', text='Category')
        tree.heading('Score', text='Score')
        tree.heading('Percentage', text='Percentage')
        tree.heading('Date', text='Date')
        
        # Set column widths and alignment
        tree.column('Rank', width=80, anchor='center')
        tree.column('Username', width=150, anchor='center')
        tree.column('Category', width=180, anchor='center')
        tree.column('Score', width=80, anchor='center')
        tree.column('Percentage', width=100, anchor='center')
        tree.column('Date', width=120, anchor='center')
        
        # Add data rows
        for idx, row in top_scores.iterrows():
            row_num = idx + 1
            
            # Medal for top 3 or regular rank
            rank_text = {1: '🥇', 2: '🥈', 3: '🥉'}.get(row_num, str(row_num))
            
            values = (rank_text, row['username'], row['category'], str(row['score']),
                     f"{row['percentage']:.1f}%", row['date'])
            
            # Add row with tags for styling
            tags = ('evenrow',) if row_num % 2 == 0 else ('oddrow',)
            tree.insert('', tk.END, values=values, tags=tags)
        
        # Configure row colors
        tree.tag_configure('evenrow', background='#ffffff')
        tree.tag_configure('oddrow', background='#f9fafb')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_card, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Back button
        back_btn = tk.Button(content, text="← Back to Dashboard", font=('Segoe UI', 12, 'bold'),
                            bg='#667eea', fg='white', relief=tk.FLAT, bd=0, cursor='hand2',
                            activebackground='#5568d3', command=self.show_dashboard)
        back_btn.pack(fill=tk.X, pady=(20, 0), ipady=12)
    
    def show_profile(self):
        """Show user profile with modern UI"""
        self.clear_screen()
        
        main_container = tk.Frame(self.root, bg='#f5f7fa')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Quick navigation bar
        self.add_top_nav(main_container)
        
        # Header
        header = tk.Frame(main_container, bg='#667eea', height=120)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text=f"👤 {self.current_user}", font=('Segoe UI', 32, 'bold'),
                        bg='#667eea', fg='white')
        title.pack(pady=(30, 5))
        
        subtitle = tk.Label(header, text="Your Performance Stats", font=('Segoe UI', 12),
                           bg='#667eea', fg='#e0e7ff')
        subtitle.pack()
        
        # Create scrollable canvas for content
        canvas = tk.Canvas(main_container, bg='#f5f7fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_container, orient='vertical', command=canvas.yview)
        content = tk.Frame(canvas, bg='#f5f7fa')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 10))
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas_window = canvas.create_window((0, 0), window=content, anchor='nw')
        
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        content.bind('<Configure>', on_frame_configure)
        canvas.bind('<Configure>', on_frame_configure)
        
        # Add padding
        content_inner = tk.Frame(content, bg='#f5f7fa')
        content_inner.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Get stats
        stats = data_manager.get_user_stats_summary(self.current_user)
        
        # Stats grid
        stats_container = tk.Frame(content_inner, bg='#f5f7fa')
        stats_container.pack(fill=tk.X, pady=(0, 20))
        
        stat_items = [
            ("🏆", "Total Quizzes", stats['total_quizzes']),
            ("📊", "Average Score", f"{stats['average_score']:.1f}"),
            ("📈", "Average %", f"{stats['average_percentage']:.1f}%"),
            ("⭐", "Best Score", stats['best_score']),
            ("🎖️", "Best %", f"{stats['best_percentage']:.1f}%"),
            ("📝", "Total Questions", stats['total_questions']),
            ("✅", "Correct Answers", stats['total_correct']),
            ("📚", "Top Category", stats['most_attempted_category'])
        ]
        
        row, col = 0, 0
        for icon, label, value in stat_items:
            stat_card = tk.Frame(stats_container, bg='white', relief=tk.FLAT, bd=0,
                                highlightthickness=1, highlightbackground='#e2e8f0')
            stat_card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            icon_label = tk.Label(stat_card, text=icon, font=('Segoe UI', 24),
                                 bg='white')
            icon_label.pack(pady=(15, 5))
            
            value_label = tk.Label(stat_card, text=str(value), font=('Segoe UI', 18, 'bold'),
                                  bg='white', fg='#2d3748')
            value_label.pack()
            
            label_text = tk.Label(stat_card, text=label, font=('Segoe UI', 10),
                                 bg='white', fg='#718096')
            label_text.pack(pady=(0, 15))
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Configure grid
        for i in range(4):
            stats_container.grid_columnconfigure(i, weight=1)
        
        # Achievements Section
        achievement_header = tk.Label(content_inner, text="🏆 Achievements", font=('Segoe UI', 18, 'bold'),
                                     bg='#f5f7fa', fg='#2d3748')
        achievement_header.pack(pady=(20, 10))
        
        achievement_data = achievements.get_user_achievements_display(self.current_user)
        
        achievement_info = tk.Label(content_inner, 
                                   text=f"Unlocked {achievement_data['unlocked_count']} of {achievement_data['total']}",
                                   font=('Segoe UI', 11), bg='#f5f7fa', fg='#718096')
        achievement_info.pack()
        
        # Achievement display grid
        ach_container = tk.Frame(content_inner, bg='#f5f7fa')
        ach_container.pack(fill=tk.X, pady=10)
        
        # Show unlocked achievements
        row, col = 0, 0
        for ach in achievement_data['unlocked'][:8]:  # Show first 8 unlocked
            ach_card = tk.Frame(ach_container, bg='#10b981', relief=tk.FLAT, bd=0,
                               highlightthickness=1, highlightbackground='#059669')
            ach_card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            tk.Label(ach_card, text=ach['icon'], font=('Segoe UI', 20),
                    bg='#10b981').pack(pady=(8, 2))
            tk.Label(ach_card, text=ach['name'], font=('Segoe UI', 9, 'bold'),
                    bg='#10b981', fg='white', wraplength=100).pack(pady=(0, 8))
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Show some locked achievements
        for ach in achievement_data['locked'][:4]:  # Show first 4 locked
            ach_card = tk.Frame(ach_container, bg='#9ca3af', relief=tk.FLAT, bd=0,
                               highlightthickness=1, highlightbackground='#6b7280')
            ach_card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            tk.Label(ach_card, text="🔒", font=('Segoe UI', 20),
                    bg='#9ca3af').pack(pady=(8, 2))
            tk.Label(ach_card, text=ach['name'], font=('Segoe UI', 9),
                    bg='#9ca3af', fg='white', wraplength=100).pack(pady=(0, 8))
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Configure achievement grid
        for i in range(4):
            ach_container.grid_columnconfigure(i, weight=1, minsize=150)
        
        # Back button
        back_btn = tk.Button(content_inner, text="← Back to Dashboard", font=('Segoe UI', 12, 'bold'),
                            bg='#667eea', fg='white', relief=tk.FLAT, bd=0, cursor='hand2',
                            activebackground='#5568d3', command=self.show_dashboard)
        back_btn.pack(fill=tk.X, pady=(20, 0), ipady=12)
    
    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_login()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = QuizApplication()
    app.run()
