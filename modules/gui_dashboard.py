"""
Dashboard GUI Module
Main dashboard with navigation and quick stats
"""

import tkinter as tk
from tkinter import messagebox
from utils import data_manager


class DashboardScreen:
    def __init__(self, root, username, callbacks):
        self.root = root
        self.username = username
        self.callbacks = callbacks
        self.root.title(f"Quiz App - Dashboard ({username})")
        
        # Set window size
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#3498db', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome, {self.username}!",
            font=('Arial', 24, 'bold'),
            bg='#3498db',
            fg='white'
        )
        welcome_label.pack(pady=30)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#ecf0f1')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Quick stats frame
        stats_frame = tk.Frame(content_frame, bg='white', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats_title = tk.Label(
            stats_frame,
            text="Quick Stats",
            font=('Arial', 16, 'bold'),
            bg='white'
        )
        stats_title.pack(pady=10)
        
        # Get user stats
        stats = data_manager.get_user_stats_summary(self.username)
        
        stats_text = f"Total Quizzes: {stats['total_quizzes']} | Best Score: {stats['best_score']} | Avg: {stats['average_percentage']:.1f}%"
        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            font=('Arial', 12),
            bg='white'
        )
        stats_label.pack(pady=10)
        
        # Buttons grid
        buttons_frame = tk.Frame(content_frame, bg='#ecf0f1')
        buttons_frame.pack(expand=True)
        
        button_configs = [
            ("Start New Quiz", '#27ae60', 'start_quiz'),
            ("View Analytics", '#e74c3c', 'view_analytics'),
            ("View History", '#f39c12', 'view_history'),
            ("Leaderboard", '#9b59b6', 'leaderboard'),
            ("Profile", '#34495e', 'profile'),
            ("Logout", '#95a5a6', 'logout')
        ]
        
        row, col = 0, 0
        for text, color, callback_key in button_configs:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=('Arial', 14, 'bold'),
                bg=color,
                fg='white',
                width=18,
                height=3,
                command=lambda k=callback_key: self.handle_action(k),
                cursor='hand2'
            )
            btn.grid(row=row, column=col, padx=15, pady=15)
            col += 1
            if col > 1:
                col = 0
                row += 1
    
    def handle_action(self, action):
        if action in self.callbacks:
            self.callbacks[action]()
