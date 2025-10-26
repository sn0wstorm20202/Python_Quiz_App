"""
Analytics GUI Module
Displays performance analytics with matplotlib graphs
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils import data_manager, score_calculator


class AnalyticsScreen:
    def __init__(self, root, username, back_callback):
        self.root = root
        self.username = username
        self.back_callback = back_callback
        self.root.title(f"Analytics - {username}")
        
        # Set window size
        self.root.geometry("1000x700")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame with modern bg
        main_frame = tk.Frame(self.root, bg='#f5f7fa')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Modern header
        header_frame = tk.Frame(main_frame, bg='#667eea', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text=f"📊 Analytics - {self.username}",
            font=('Segoe UI', 26, 'bold'),
            bg='#667eea',
            fg='white'
        )
        title.pack(pady=(25, 5))
        
        subtitle = tk.Label(
            header_frame,
            text="Track your progress and performance",
            font=('Segoe UI', 11),
            bg='#667eea',
            fg='#e0e7ff'
        )
        subtitle.pack()
        
        # Content frame with canvas and scrollbar
        canvas_frame = tk.Frame(main_frame, bg='#f5f7fa')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg='#f5f7fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f5f7fa')
        
        # Keep canvas scrollregion updated
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Make inner frame match canvas width so content can be centered within
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(window_id, width=e.width)
        )
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Centered content container with max width
        content_container = tk.Frame(scrollable_frame, bg='#f5f7fa')
        content_container.pack(anchor='n', pady=10)
        content_container.configure(width=900)
        
        # Get user data
        user_history = data_manager.get_user_history(self.username)
        
        if user_history.empty:
            no_data_label = tk.Label(
                content_container,
                text="No quiz history available yet.\nTake some quizzes to see analytics!",
                font=('Arial', 16),
                bg='#ecf0f1',
                fg='#7f8c8d'
            )
            no_data_label.pack(pady=100)
        else:
            # Statistics panel
            self.create_stats_panel(content_container, user_history)
            
            # Graphs
            self.create_performance_trend_graph(content_container, user_history)
            self.create_category_performance_graph(content_container, user_history)
            self.create_difficulty_accuracy_graph(content_container, user_history)
            self.create_correct_incorrect_pie(content_container, user_history)
        
        # Modern back button
        btn_container = tk.Frame(main_frame, bg='#f5f7fa')
        btn_container.pack(fill=tk.X, padx=40, pady=15)
        
        back_btn = tk.Button(
            btn_container,
            text="← Back to Dashboard",
            font=('Segoe UI', 12, 'bold'),
            bg='#667eea',
            fg='white',
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            activebackground='#5568d3',
            command=self.back_callback
        )
        back_btn.pack(fill=tk.X, ipady=12)
    
    def create_stats_panel(self, parent, df):
        """Create statistics summary panel"""
        stats_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title = tk.Label(
            stats_frame,
            text="Summary Statistics (NumPy Calculations)",
            font=('Arial', 16, 'bold'),
            bg='white'
        )
        title.pack(pady=10)
        
        # Calculate statistics using NumPy through score_calculator
        percentages = df['percentage'].tolist()
        stats = score_calculator.calculate_statistics(percentages)
        improvement = score_calculator.calculate_improvement_rate(percentages)
        
        stats_grid = tk.Frame(stats_frame, bg='white')
        stats_grid.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        stat_items = [
            ("Total Attempts", len(df)),
            ("Mean Score", f"{stats['mean']:.2f}%"),
            ("Median Score", f"{stats['median']:.2f}%"),
            ("Std Deviation", f"{stats['std_dev']:.2f}"),
            ("Best Score", f"{stats['max']:.2f}%"),
            ("Worst Score", f"{stats['min']:.2f}%"),
            ("Trend", improvement['trend'].title()),
            ("Improvement Rate", f"{improvement['rate']:.2f}%/quiz")
        ]
        
        row, col = 0, 0
        for label, value in stat_items:
            stat_box = tk.Frame(stats_grid, bg='#f8f9fa', relief=tk.FLAT, bd=0,
                               highlightthickness=1, highlightbackground='#e2e8f0')
            stat_box.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
            
            tk.Label(stat_box, text=label, font=('Segoe UI', 9), bg='#f8f9fa', fg='#718096').pack(pady=(10, 2))
            tk.Label(stat_box, text=str(value), font=('Segoe UI', 13, 'bold'), bg='#f8f9fa', fg='#2d3748').pack(pady=(0, 10), padx=10)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Configure grid columns for equal sizing with minimum width
        for i in range(4):
            stats_grid.grid_columnconfigure(i, weight=1, uniform='stat', minsize=150)
    
    def create_performance_trend_graph(self, parent, df):
        """Create line graph showing score trends over time"""
        graph_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        graph_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        title = tk.Label(
            graph_frame,
            text="Performance Trend Over Time",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        title.pack(pady=10)
        
        # Create matplotlib figure
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Sort by date
        df_sorted = df.sort_values(['date', 'time'])
        attempts = list(range(1, len(df_sorted) + 1))
        percentages = df_sorted['percentage'].tolist()
        
        # Plot data
        ax.plot(attempts, percentages, marker='o', color='#3498db', linewidth=2, markersize=6)
        ax.set_xlabel('Attempt Number', fontsize=10)
        ax.set_ylabel('Score Percentage (%)', fontsize=10)
        ax.set_title('Score Progression', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 105)
        
        # Add trend line
        if len(attempts) > 1:
            import numpy as np
            z = np.polyfit(attempts, percentages, 1)
            p = np.poly1d(z)
            ax.plot(attempts, p(attempts), "--", color='#e74c3c', alpha=0.7, label='Trend')
            ax.legend()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def create_category_performance_graph(self, parent, df):
        """Create bar chart showing average performance by category"""
        graph_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        graph_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        title = tk.Label(
            graph_frame,
            text="Average Performance by Category",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        title.pack(pady=10)
        
        # Create figure
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Get category averages using pandas groupby
        category_avg = df.groupby('category')['percentage'].mean()
        
        # Plot bar chart
        colors = ['#3498db', '#e74c3c', '#f39c12']
        ax.bar(category_avg.index, category_avg.values, color=colors[:len(category_avg)])
        ax.set_xlabel('Category', fontsize=10)
        ax.set_ylabel('Average Score (%)', fontsize=10)
        ax.set_title('Category-wise Performance', fontsize=12)
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3)
        
        # Rotate labels if needed
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=15, ha='right')
        
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def create_difficulty_accuracy_graph(self, parent, df):
        """Create bar chart showing accuracy by difficulty level"""
        graph_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        graph_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        title = tk.Label(
            graph_frame,
            text="Accuracy by Difficulty Level",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        title.pack(pady=10)
        
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Calculate accuracy for each difficulty using pandas
        difficulty_avg = df.groupby('difficulty')['percentage'].mean()
        
        # Ensure order
        ordered_difficulties = ['Easy', 'Medium', 'Hard']
        values = [difficulty_avg.get(d, 0) for d in ordered_difficulties]
        
        colors = ['#27ae60', '#f39c12', '#e74c3c']
        ax.bar(ordered_difficulties, values, color=colors)
        ax.set_xlabel('Difficulty Level', fontsize=10)
        ax.set_ylabel('Average Accuracy (%)', fontsize=10)
        ax.set_title('Performance by Difficulty', fontsize=12)
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3)
        
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def create_correct_incorrect_pie(self, parent, df):
        """Create pie chart showing correct vs incorrect distribution"""
        graph_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        graph_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        title = tk.Label(
            graph_frame,
            text="Overall Correct vs Incorrect Distribution",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        title.pack(pady=10)
        
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Calculate totals using pandas sum
        total_correct = df['correct'].sum()
        total_wrong = df['wrong'].sum()
        
        # Create pie chart
        labels = ['Correct', 'Incorrect']
        sizes = [total_correct, total_wrong]
        colors = ['#27ae60', '#e74c3c']
        explode = (0.05, 0)
        
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')
        ax.set_title(f'Total Questions: {total_correct + total_wrong}', fontsize=12)
        
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
