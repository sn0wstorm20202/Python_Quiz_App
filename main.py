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
        """Show quiz setup screen"""
        self.clear_screen()
        setup_window = tk.Frame(self.root, bg='#ecf0f1')
        setup_window.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        title = tk.Label(setup_window, text="Quiz Setup", font=('Arial', 24, 'bold'), bg='#ecf0f1')
        title.pack(pady=20)
        
        # Category
        tk.Label(setup_window, text="Select Category:", font=('Arial', 12), bg='#ecf0f1').pack(pady=5)
        category_var = tk.StringVar()
        categories = question_manager.get_categories()
        category_dropdown = ttk.Combobox(setup_window, textvariable=category_var, values=categories, state='readonly', width=30)
        if categories:
            category_dropdown.current(0)
        category_dropdown.pack(pady=5)
        
        # Difficulty
        tk.Label(setup_window, text="Select Difficulty:", font=('Arial', 12), bg='#ecf0f1').pack(pady=5)
        difficulty_var = tk.StringVar()
        difficulties = ['Easy', 'Medium', 'Hard']
        difficulty_dropdown = ttk.Combobox(setup_window, textvariable=difficulty_var, values=difficulties, state='readonly', width=30)
        difficulty_dropdown.current(0)
        difficulty_dropdown.pack(pady=5)
        
        # Mode
        tk.Label(setup_window, text="Select Mode:", font=('Arial', 12), bg='#ecf0f1').pack(pady=5)
        mode_var = tk.StringVar()
        modes = ['Practice', 'Timed', 'Survival']
        mode_dropdown = ttk.Combobox(setup_window, textvariable=mode_var, values=modes, state='readonly', width=30)
        mode_dropdown.current(0)
        mode_dropdown.pack(pady=5)
        
        # Number of questions
        tk.Label(setup_window, text="Number of Questions:", font=('Arial', 12), bg='#ecf0f1').pack(pady=5)
        count_var = tk.IntVar(value=10)
        count_dropdown = ttk.Combobox(setup_window, textvariable=count_var, values=[5, 10, 15, 20], state='readonly', width=30)
        count_dropdown.current(1)
        count_dropdown.pack(pady=5)
        
        # Buttons
        btn_frame = tk.Frame(setup_window, bg='#ecf0f1')
        btn_frame.pack(pady=30)
        
        start_btn = tk.Button(btn_frame, text="Start Quiz", font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                              width=15, height=2, command=lambda: self.start_quiz(category_var.get(), difficulty_var.get(), 
                                                                                   mode_var.get(), count_var.get()))
        start_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(btn_frame, text="Back", font=('Arial', 14), bg='#95a5a6', fg='white',
                            width=15, height=2, command=self.show_dashboard)
        back_btn.pack(side=tk.LEFT, padx=10)
    
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
            'consecutive_correct': 0
        }
        
        self.show_question()
    
    def show_question(self):
        """Display current question"""
        self.clear_screen()
        
        quiz_frame = tk.Frame(self.root, bg='white')
        quiz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        data = self.quiz_data
        question = data['questions'][data['current_index']]
        
        # Start timer for this question
        data['question_start_time'] = time.time()
        
        # Header with question counter and mode
        mode_display = f" [{data['mode']} Mode]" if data['mode'] != 'Practice' else ""
        header = tk.Label(quiz_frame, text=f"Question {data['current_index'] + 1}/{len(data['questions'])}{mode_display}",
                         font=('Arial', 16, 'bold'), bg='white')
        header.pack(pady=10)
        
        # Score display with mode-specific info
        score_text = f"Correct: {data['correct']} | Wrong: {data['wrong']}"
        if data['mode'] == 'Survival':
            lives = 3 - data['wrong']
            score_text += f" | Lives: {'❤️' * lives}"
        elif data['mode'] == 'Timed':
            score_text += f" | Bonus Points: {sum(data['time_bonuses'])}"
        
        score_label = tk.Label(quiz_frame, text=score_text, font=('Arial', 12), bg='white')
        score_label.pack(pady=5)
        
        # Timer label for Timed mode
        if data['mode'] == 'Timed':
            self.timer_label = tk.Label(quiz_frame, text="Time: 0s", font=('Arial', 14, 'bold'), bg='white', fg='#e74c3c')
            self.timer_label.pack(pady=5)
            self.update_timer()
        
        # Question text
        q_frame = tk.Frame(quiz_frame, bg='#f0f0f0', relief=tk.RAISED, bd=2)
        q_frame.pack(fill=tk.X, padx=20, pady=20)
        q_label = tk.Label(q_frame, text=question['question'], font=('Arial', 14), bg='#f0f0f0', wraplength=700, justify=tk.LEFT)
        q_label.pack(padx=20, pady=20)
        
        # Options
        self.selected_option = tk.IntVar(value=-1)
        options_frame = tk.Frame(quiz_frame, bg='white')
        options_frame.pack(pady=20)
        
        for i, option in enumerate(question['options']):
            rb = tk.Radiobutton(options_frame, text=f"{chr(65+i)}. {option}", variable=self.selected_option,
                               value=i, font=('Arial', 12), bg='white', anchor='w', width=60)
            rb.pack(pady=5, padx=20)
        
        # Submit button
        submit_btn = tk.Button(quiz_frame, text="Submit Answer", font=('Arial', 14, 'bold'), bg='#3498db',
                              fg='white', width=20, height=2, command=self.submit_answer)
        submit_btn.pack(pady=20)
    
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
    
    def submit_answer(self):
        """Process submitted answer"""
        selected = self.selected_option.get()
        
        if selected == -1:
            messagebox.showwarning("Warning", "Please select an answer")
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
            
            # Calculate time bonus for Timed mode
            if data['mode'] == 'Timed':
                bonus = score_calculator.calculate_time_bonus(time_taken)
                data['time_bonuses'].append(bonus)
        else:
            data['wrong'] += 1
            data['consecutive_correct'] = 0
            
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
        """Show answer feedback"""
        self.clear_screen()
        
        feedback_frame = tk.Frame(self.root, bg='white')
        feedback_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Result
        if is_correct:
            result_text = "✓ Correct!"
            color = '#27ae60'
        else:
            result_text = "✗ Incorrect"
            color = '#e74c3c'
        
        result_label = tk.Label(feedback_frame, text=result_text, font=('Arial', 24, 'bold'), fg=color, bg='white')
        result_label.pack(pady=20)
        
        # Correct answer
        correct_label = tk.Label(feedback_frame, text=f"Correct Answer: {question['options'][question['correct']]}",
                                font=('Arial', 14), bg='white')
        correct_label.pack(pady=10)
        
        # Explanation
        exp_frame = tk.Frame(feedback_frame, bg='#f0f0f0', relief=tk.RAISED, bd=2)
        exp_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        exp_label = tk.Label(exp_frame, text=f"Explanation:\n{question['explanation']}", font=('Arial', 12),
                            bg='#f0f0f0', wraplength=600, justify=tk.LEFT)
        exp_label.pack(padx=20, pady=20)
        
        # Next button
        next_btn = tk.Button(feedback_frame, text="Next Question", font=('Arial', 14, 'bold'), bg='#3498db',
                            fg='white', width=20, height=2, command=self.next_question)
        next_btn.pack(pady=20)
    
    def show_brief_feedback(self, is_correct, question):
        """Show brief feedback for Timed/Survival modes"""
        self.clear_screen()
        
        feedback_frame = tk.Frame(self.root, bg='white')
        feedback_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Result
        if is_correct:
            result_text = "✓ Correct!"
            color = '#27ae60'
        else:
            result_text = "✗ Incorrect"
            color = '#e74c3c'
        
        result_label = tk.Label(feedback_frame, text=result_text, font=('Arial', 32, 'bold'), fg=color, bg='white')
        result_label.pack(pady=60)
        
        # Show correct answer if wrong
        if not is_correct:
            correct_label = tk.Label(feedback_frame, text=f"Correct Answer: {question['options'][question['correct']]}",
                                    font=('Arial', 16), bg='white')
            correct_label.pack(pady=20)
        
        # Mode-specific messages
        data = self.quiz_data
        if data['mode'] == 'Survival' and data['consecutive_correct'] >= 5:
            bonus_label = tk.Label(feedback_frame, text="🔥 5+ Streak! 1.5x Multiplier Active!",
                                  font=('Arial', 14, 'bold'), bg='white', fg='#f39c12')
            bonus_label.pack(pady=10)
        elif data['mode'] == 'Timed' and len(data['time_bonuses']) > 0 and data['time_bonuses'][-1] > 0:
            bonus_label = tk.Label(feedback_frame, text=f"⚡ Time Bonus: +{data['time_bonuses'][-1]} points!",
                                  font=('Arial', 14, 'bold'), bg='white', fg='#3498db')
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
        
        results_frame = tk.Frame(self.root, bg='white')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        title = tk.Label(results_frame, text="Quiz Results", font=('Arial', 28, 'bold'), bg='white')
        title.pack(pady=20)
        
        # Score display
        score_frame = tk.Frame(results_frame, bg=grade_info['color'], relief=tk.RAISED, bd=3)
        score_frame.pack(pady=20, padx=40, fill=tk.X)
        
        percentage_label = tk.Label(score_frame, text=f"{percentage:.1f}%", font=('Arial', 48, 'bold'),
                                    bg=grade_info['color'], fg='white')
        percentage_label.pack(pady=20)
        
        grade_label = tk.Label(score_frame, text=grade_info['grade'], font=('Arial', 20, 'bold'),
                              bg=grade_info['color'], fg='white')
        grade_label.pack(pady=(0, 20))
        
        # Stats with mode-specific details
        stats_text = f"Total Questions: {total} | Correct: {correct} | Wrong: {wrong} | Score: {score}"
        if data['mode'] == 'Timed':
            stats_text += f" | Time Bonus: +{sum(data['time_bonuses'])} | Total Time: {int(data['total_time'])}s"
        elif data['mode'] == 'Survival':
            if correct >= 5:
                stats_text += " | 🔥 1.5x Multiplier Applied!"
        
        stats_label = tk.Label(results_frame, text=stats_text, font=('Arial', 12), bg='white')
        stats_label.pack(pady=20)
        
        # Buttons
        btn_frame = tk.Frame(results_frame, bg='white')
        btn_frame.pack(pady=20)
        
        dashboard_btn = tk.Button(btn_frame, text="Back to Dashboard", font=('Arial', 12, 'bold'),
                                 bg='#3498db', fg='white', width=18, height=2, command=self.show_dashboard)
        dashboard_btn.pack(side=tk.LEFT, padx=10)
        
        analytics_btn = tk.Button(btn_frame, text="View Analytics", font=('Arial', 12, 'bold'),
                                 bg='#e74c3c', fg='white', width=18, height=2, command=self.show_analytics)
        analytics_btn.pack(side=tk.LEFT, padx=10)
    
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
        """Show leaderboard"""
        self.clear_screen()
        
        leader_frame = tk.Frame(self.root, bg='#ecf0f1')
        leader_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        title = tk.Label(leader_frame, text="Leaderboard - Top 10 Scores", font=('Arial', 24, 'bold'), bg='#ecf0f1')
        title.pack(pady=20)
        
        # Get top scores
        top_scores = data_manager.get_top_scores(10)
        
        # Create treeview
        tree_frame = tk.Frame(leader_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ('Rank', 'Username', 'Category', 'Score', 'Percentage', 'Date')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='center')
        
        # Add data
        for idx, row in top_scores.iterrows():
            tree.insert('', tk.END, values=(
                idx + 1, row['username'], row['category'], row['score'],
                f"{row['percentage']:.1f}%", row['date']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        back_btn = tk.Button(leader_frame, text="Back to Dashboard", font=('Arial', 12, 'bold'),
                            bg='#3498db', fg='white', width=20, height=2, command=self.show_dashboard)
        back_btn.pack(pady=20)
    
    def show_profile(self):
        """Show user profile"""
        self.clear_screen()
        
        profile_frame = tk.Frame(self.root, bg='#ecf0f1')
        profile_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        title = tk.Label(profile_frame, text=f"Profile: {self.current_user}", font=('Arial', 24, 'bold'), bg='#ecf0f1')
        title.pack(pady=20)
        
        # Get stats
        stats = data_manager.get_user_stats_summary(self.current_user)
        
        stats_frame = tk.Frame(profile_frame, bg='white', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        stats_list = [
            ("Total Quizzes Taken", stats['total_quizzes']),
            ("Average Score", f"{stats['average_score']:.1f}"),
            ("Average Percentage", f"{stats['average_percentage']:.1f}%"),
            ("Best Score", stats['best_score']),
            ("Best Percentage", f"{stats['best_percentage']:.1f}%"),
            ("Total Questions Attempted", stats['total_questions']),
            ("Total Correct Answers", stats['total_correct']),
            ("Most Attempted Category", stats['most_attempted_category'])
        ]
        
        for label, value in stats_list:
            stat_row = tk.Frame(stats_frame, bg='white')
            stat_row.pack(fill=tk.X, padx=40, pady=10)
            
            tk.Label(stat_row, text=f"{label}:", font=('Arial', 12, 'bold'), bg='white', anchor='w').pack(side=tk.LEFT)
            tk.Label(stat_row, text=str(value), font=('Arial', 12), bg='white', anchor='e').pack(side=tk.RIGHT)
        
        back_btn = tk.Button(profile_frame, text="Back to Dashboard", font=('Arial', 12, 'bold'),
                            bg='#3498db', fg='white', width=20, height=2, command=self.show_dashboard)
        back_btn.pack(pady=20)
    
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
