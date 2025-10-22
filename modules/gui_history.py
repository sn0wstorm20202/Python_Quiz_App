"""
History GUI Module
Displays quiz history using Treeview widget
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from utils import data_manager


class HistoryScreen:
    def __init__(self, root, username, back_callback):
        self.root = root
        self.username = username
        self.back_callback = back_callback
        self.root.title(f"Quiz History - {username}")
        
        # Set window size
        self.root.geometry("1000x600")
        
        # Track sort order for each column
        self.sort_reverse = {}
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#3498db', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text=f"Quiz History - {self.username}",
            font=('Arial', 20, 'bold'),
            bg='#3498db',
            fg='white'
        )
        title.pack(pady=25)
        
        # Get user history using pandas
        self.history_df = data_manager.get_user_history(self.username)
        
        if self.history_df.empty:
            no_data_label = tk.Label(
                main_frame,
                text="No quiz history available yet.\nTake some quizzes to see your history!",
                font=('Arial', 16),
                bg='#ecf0f1',
                fg='#7f8c8d'
            )
            no_data_label.pack(pady=100)
        else:
            # Sort by date descending
            self.history_df = self.history_df.sort_values(['date', 'time'], ascending=False)
            
            # Create treeview frame
            tree_frame = tk.Frame(main_frame, bg='white')
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Add scrollbars
            tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
            tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
            
            # Create Treeview widget
            columns = ('Date', 'Time', 'Category', 'Difficulty', 'Mode', 
                      'Questions', 'Correct', 'Wrong', 'Score', 'Percentage')
            
            self.tree = ttk.Treeview(
                tree_frame,
                columns=columns,
                show='headings',
                yscrollcommand=tree_scroll_y.set,
                xscrollcommand=tree_scroll_x.set
            )
            
            tree_scroll_y.config(command=self.tree.yview)
            tree_scroll_x.config(command=self.tree.xview)
            
            # Define column headings and widths
            column_widths = {
                'Date': 100,
                'Time': 80,
                'Category': 120,
                'Difficulty': 80,
                'Mode': 80,
                'Questions': 80,
                'Correct': 70,
                'Wrong': 70,
                'Score': 70,
                'Percentage': 90
            }
            
            for col in columns:
                self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
                self.tree.column(col, width=column_widths[col], anchor='center')
            
            # Insert data from pandas DataFrame
            for idx, row in self.history_df.iterrows():
                values = (
                    row['date'],
                    row['time'],
                    row['category'],
                    row['difficulty'],
                    row['mode'],
                    row['total_questions'],
                    row['correct'],
                    row['wrong'],
                    row['score'],
                    f"{row['percentage']:.1f}%"
                )
                self.tree.insert('', tk.END, values=values)
            
            # Pack treeview and scrollbars
            self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
            tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
            
            # Statistics summary
            self.create_summary_panel(main_frame)
        
        # Buttons
        btn_frame = tk.Frame(main_frame, bg='#ecf0f1')
        btn_frame.pack(pady=10)
        
        if not self.history_df.empty:
            export_btn = tk.Button(
                btn_frame,
                text="Export to CSV",
                font=('Arial', 12, 'bold'),
                bg='#27ae60',
                fg='white',
                width=15,
                height=2,
                command=self.export_history
            )
            export_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(
            btn_frame,
            text="Back to Dashboard",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            width=18,
            height=2,
            command=self.back_callback
        )
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def create_summary_panel(self, parent):
        """Create summary statistics panel"""
        summary_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        summary_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        title = tk.Label(
            summary_frame,
            text="Summary",
            font=('Arial', 14, 'bold'),
            bg='white'
        )
        title.pack(pady=5)
        
        # Calculate summary stats using pandas
        total_quizzes = len(self.history_df)
        avg_percentage = self.history_df['percentage'].mean()
        best_score = self.history_df['score'].max()
        total_questions = self.history_df['total_questions'].sum()
        total_correct = self.history_df['correct'].sum()
        
        summary_text = f"Total Quizzes: {total_quizzes} | " \
                      f"Average: {avg_percentage:.1f}% | " \
                      f"Best Score: {best_score} | " \
                      f"Total Questions Attempted: {total_questions} | " \
                      f"Total Correct: {total_correct}"
        
        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=('Arial', 11),
            bg='white'
        )
        summary_label.pack(pady=5)
    
    def sort_by_column(self, col):
        """Sort treeview by column with toggle between ascending/descending"""
        # Toggle sort order for this column
        if col not in self.sort_reverse:
            self.sort_reverse[col] = False
        else:
            self.sort_reverse[col] = not self.sort_reverse[col]
        
        # Get all items
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Sort items with proper type handling
        try:
            # Try to sort numerically if possible
            items.sort(key=lambda x: float(x[0].rstrip('%')), reverse=self.sort_reverse[col])
        except (ValueError, AttributeError):
            # Fall back to string sorting
            items.sort(key=lambda x: x[0], reverse=self.sort_reverse[col])
        
        # Rearrange items in sorted order
        for index, (val, item) in enumerate(items):
            self.tree.move(item, '', index)
    
    def export_history(self):
        """Export history to CSV file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"{self.username}_quiz_history.csv"
        )
        
        if file_path:
            try:
                # Export using pandas to_csv
                self.history_df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"History exported successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export history:\n{str(e)}")
