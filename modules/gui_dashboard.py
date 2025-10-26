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
        # Main background
        main_frame = tk.Frame(self.root, bg='#f5f7fa')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Modern header with gradient effect
        header_frame = tk.Frame(main_frame, bg='#667eea', height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome back, {self.username}!",
            font=('Segoe UI', 28, 'bold'),
            bg='#667eea',
            fg='white'
        )
        welcome_label.pack(pady=(30, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Ready to test your knowledge?",
            font=('Segoe UI', 12),
            bg='#667eea',
            fg='#e0e7ff'
        )
        subtitle_label.pack()
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#f5f7fa')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Quick stats cards
        stats = data_manager.get_user_stats_summary(self.username)
        
        stats_container = tk.Frame(content_frame, bg='#f5f7fa')
        stats_container.pack(fill=tk.X, pady=(0, 30))
        
        stat_items = [
            ("🏆", "Total Quizzes", stats['total_quizzes'], '#667eea'),
            ("⭐", "Best Score", stats['best_score'], '#f59e0b'),
            ("📈", "Average", f"{stats['average_percentage']:.1f}%", '#10b981')
        ]
        
        for i, (icon, label, value, color) in enumerate(stat_items):
            stat_card = tk.Frame(stats_container, bg='white', relief=tk.FLAT, bd=0,
                                highlightthickness=1, highlightbackground='#e2e8f0')
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8)
            
            icon_label = tk.Label(stat_card, text=icon, font=('Segoe UI', 28),
                                 bg='white', fg=color)
            icon_label.pack(pady=(15, 5))
            
            value_label = tk.Label(stat_card, text=str(value),
                                  font=('Segoe UI', 24, 'bold'),
                                  bg='white', fg='#2d3748')
            value_label.pack()
            
            label_text = tk.Label(stat_card, text=label,
                                 font=('Segoe UI', 10),
                                 bg='white', fg='#718096')
            label_text.pack(pady=(0, 15))
        
        # Action cards grid
        cards_frame = tk.Frame(content_frame, bg='#f5f7fa')
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        button_configs = [
            ("📝 Start New Quiz", '#667eea', 'start_quiz'),
            ("📊 View Analytics", '#ec4899', 'view_analytics'),
            ("📜 View History", '#f59e0b', 'view_history'),
            ("🏆 Leaderboard", '#8b5cf6', 'leaderboard'),
            ("👤 Profile", '#06b6d4', 'profile'),
            ("🚪 Logout", '#64748b', 'logout')
        ]
        
        row, col = 0, 0
        for text, color, callback_key in button_configs:
            card = tk.Frame(cards_frame, bg=color, relief=tk.FLAT, bd=0,
                           highlightthickness=0, cursor='hand2')
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            btn = tk.Button(
                card,
                text=text,
                font=('Segoe UI', 13, 'bold'),
                bg=color,
                fg='white',
                relief=tk.FLAT,
                bd=0,
                command=lambda k=callback_key: self.handle_action(k),
                cursor='hand2',
                activebackground=color
            )
            btn.pack(fill=tk.BOTH, expand=True, padx=2, pady=2, ipady=40)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            cards_frame.grid_rowconfigure(i, weight=1)
    
    def handle_action(self, action):
        if action in self.callbacks:
            self.callbacks[action]()
