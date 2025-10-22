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
        
        # Center window
        window_width = 400
        window_height = 500
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Quiz Application",
            font=('Arial', 24, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            main_frame,
            text="with Score Analytics",
            font=('Arial', 12),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=5)
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, bd=2)
        form_frame.pack(pady=30, padx=20, fill=tk.BOTH, expand=True)
        
        # Username
        username_label = tk.Label(
            form_frame,
            text="Username:",
            font=('Arial', 12),
            bg='white'
        )
        username_label.pack(pady=(30, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=25
        )
        self.username_entry.pack(pady=5)
        self.username_entry.focus()
        
        # Password
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=('Arial', 12),
            bg='white'
        )
        password_label.pack(pady=(20, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=25,
            show='*'
        )
        self.password_entry.pack(pady=5)
        
        # Bind Enter key
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(pady=30)
        
        # Login button
        login_button = tk.Button(
            buttons_frame,
            text="Login",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            width=12,
            height=2,
            command=self.login,
            cursor='hand2'
        )
        login_button.pack(side=tk.LEFT, padx=10)
        
        # Register button
        register_button = tk.Button(
            buttons_frame,
            text="Register",
            font=('Arial', 12, 'bold'),
            bg='#2ecc71',
            fg='white',
            width=12,
            height=2,
            command=self.register,
            cursor='hand2'
        )
        register_button.pack(side=tk.LEFT, padx=10)
        
        # Footer
        footer_label = tk.Label(
            main_frame,
            text="BTech 2nd Year Project",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#95a5a6'
        )
        footer_label.pack(side=tk.BOTTOM, pady=10)
    
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
