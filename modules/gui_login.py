"""
Login/Register GUI Module
Provides user authentication interface
"""

import tkinter as tk
from tkinter import messagebox
from utils import data_manager


class LoginScreen:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Quiz App - Login")
        
        # Center window - larger modern size
        window_width = 500
        window_height = 650
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main gradient background
        main_frame = tk.Frame(self.root, bg='#f5f7fa')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Centered login card
        card_frame = tk.Frame(main_frame, bg='white', relief=tk.FLAT, bd=0, 
                             highlightthickness=0)
        card_frame.place(relx=0.5, rely=0.5, anchor='center', width=480, height=600)
        
        # Top accent bar
        accent_bar = tk.Frame(card_frame, bg='#667eea', height=6)
        accent_bar.pack(fill=tk.X, side=tk.TOP)
        
        # Content container
        content = tk.Frame(card_frame, bg='white')
        content.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        # Title with modern icon
        title_label = tk.Label(
            content,
            text="🎯 Quiz App",
            font=('Segoe UI', 32, 'bold'),
            bg='white',
            fg='#2d3748'
        )
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(
            content,
            text="Master your knowledge",
            font=('Segoe UI', 11),
            bg='white',
            fg='#718096'
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Username field
        username_label = tk.Label(
            content,
            text="Username",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#4a5568',
            anchor='w'
        )
        username_label.pack(fill=tk.X, pady=(0, 5))
        
        username_frame = tk.Frame(content, bg='#f7fafc', relief=tk.FLAT, bd=0,
                                 highlightthickness=1, highlightbackground='#e2e8f0')
        username_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.username_entry = tk.Entry(
            username_frame,
            font=('Segoe UI', 11),
            bg='#f7fafc',
            fg='#2d3748',
            relief=tk.FLAT,
            bd=0
        )
        self.username_entry.pack(fill=tk.X, padx=15, pady=12)
        self.username_entry.focus()
        
        # Password field
        password_label = tk.Label(
            content,
            text="Password",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#4a5568',
            anchor='w'
        )
        password_label.pack(fill=tk.X, pady=(0, 5))
        
        password_frame = tk.Frame(content, bg='#f7fafc', relief=tk.FLAT, bd=0,
                                 highlightthickness=1, highlightbackground='#e2e8f0')
        password_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=('Segoe UI', 11),
            bg='#f7fafc',
            fg='#2d3748',
            relief=tk.FLAT,
            bd=0,
            show='●'
        )
        self.password_entry.pack(fill=tk.X, padx=15, pady=12)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_button = tk.Button(
            content,
            text="Login",
            font=('Segoe UI', 12, 'bold'),
            bg='#667eea',
            fg='white',
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            activebackground='#5568d3',
            command=self.login
        )
        login_button.pack(fill=tk.X, pady=(0, 12), ipady=12)
        
        # Register button
        register_button = tk.Button(
            content,
            text="Create Account",
            font=('Segoe UI', 11),
            bg='#f7fafc',
            fg='#667eea',
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            activebackground='#edf2f7',
            command=self.register
        )
        register_button.pack(fill=tk.X, ipady=12)
        
        # Footer
        footer_label = tk.Label(
            content,
            text="BTech 2nd Year Project",
            font=('Segoe UI', 9),
            bg='white',
            fg='#a0aec0'
        )
        footer_label.pack(side=tk.BOTTOM, pady=(30, 0))
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Validate credentials
        if data_manager.validate_user(username, password):
            messagebox.showinfo("Success", f"Welcome back, {username}!")
            self.on_login_success(username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
    
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        
        # Try to add user
        if data_manager.add_user(username, password):
            messagebox.showinfo("Success", f"Account created successfully!\nWelcome, {username}!")
            self.on_login_success(username)
        else:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()
