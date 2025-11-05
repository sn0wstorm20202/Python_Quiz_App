WARP.md

This document provides guidance to WARP (warp.dev) and developers when working with this repository.

⚙️ Commands
▶️ Running the Application
python main.py

📦 Installing Dependencies
pip install -r requirements.txt

🔍 Checking Installed Dependencies
pip list | Select-String -Pattern "numpy|pandas|matplotlib"

🧱 High-Level Architecture
🔄 Application Flow

This is a stateful, multi-screen Tkinter GUI application orchestrated by a centralized controller:

main.py defines the QuizApplication class, which manages all screen transitions, user state, and quiz data.

All navigation routes through controller methods (show_dashboard(), show_quiz_setup(), etc.).

clear_screen() ensures a clean transition by destroying existing widgets before new screens are rendered.

User session information is stored in QuizApplication.current_user.

🗂️ Module Organization
modules/ — GUI Screens

Each GUI module creates interface components but does not control navigation logic.
Navigation is handled via callback functions received from the controller.

gui_login.py — Uses on_login_success callback.

gui_dashboard.py — Accepts a callbacks dictionary for navigation functions.

gui_analytics.py and gui_history.py — Receive back_callback to return to the dashboard.

utils/ — Backend Logic

Contains non-GUI modules that handle data, scoring, and file operations.

file_handler.py — Handles raw file I/O (CSV/JSON read/write).

data_manager.py — Manages high-level data operations using pandas.

score_calculator.py — Performs all score and statistics computations using NumPy.

question_manager.py — Loads, filters, and randomizes questions.

📊 Data Flow Architecture
Storage Layer (data/)

users.csv — Stores user credentials.

quiz_history.csv — Tracks all quiz attempts.

questions.json — Stores the question bank.

Data Access Flow

file_handler.py → Raw file operations

data_manager.py → DataFrame loading, aggregation, and manipulation

score_calculator.py → Numerical processing with NumPy

GUI → Displays processed results

🧮 Integration Philosophy
NumPy Usage

All numeric operations go through score_calculator.py:

Use NumPy arrays for arithmetic and statistics.

Linear regression via np.polyfit() for trend analysis.

Avoid manual arithmetic on raw Python lists.

pandas Usage

All persistence and querying are handled in data_manager.py:

Load all quiz data as pandas DataFrames.

Use boolean indexing, groupby(), and aggregation for filtering and analytics.

Append new quiz results via pd.concat([...], ignore_index=True).

🧠 Key Design Patterns
Screen Lifecycle

clear_screen() → destroys widgets

Creates new frame hierarchy

Packs frames into self.root

Stores reference (optional) in self.current_screen

Quiz State Dictionary
{
    'questions': [...],
    'current_index': 0,
    'correct': 0,
    'wrong': 0,
    'answers': [],
    'category': str,
    'difficulty': str,
    'mode': str
}

Error Handling

File errors handled with try/except and safe defaults.

Missing files are auto-created via initialize_data_files().

GUI errors surfaced via messagebox.showerror().

🏆 Scoring System
Difficulty-Based Points
Difficulty	Points
Easy	10
Medium	15
Hard	25
Quiz Modes

Practice Mode: Base scoring, untimed, with explanations.

Timed Mode: Base + time bonus (+5 for <10s, +3 for <20s).

Survival Mode: Base + 1.5× multiplier after 5 consecutive correct answers.

📝 Question Structure (data/questions.json)
{
    "category": "Python|DSA|Computer Networks",
    "difficulty": "Easy|Medium|Hard",
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "correct": 0-3,
    "explanation": "Explanation text"
}


Categories are dynamically loaded using question_manager.get_categories().
New categories can be added without modifying any code.

📈 Matplotlib Integration

Analytics graphs are embedded via FigureCanvasTkAgg:

Create a Figure object

Add subplots and plot the data

Embed via FigureCanvasTkAgg(fig, master=parent_frame)

Call canvas.draw() and pack the widget

Trend lines are computed using NumPy’s linear regression (np.polyfit()).

🧩 Conventions & Coding Standards
File Paths

Always construct paths using helper functions like get_data_path() or get_user_data_path().

Quiz History CSV Columns

user_id, username, date, time, category, difficulty, total_questions, correct, wrong, score, percentage, time_taken, mode

Callback Pattern

GUI screens never control navigation directly — they call callbacks passed from QuizApplication.

Window Geometry

Screens are centered automatically using:

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

🧪 Testing Checklist

Before committing changes:

✅ Verify login & registration flow

✅ Test quizzes in all modes

✅ Confirm analytics graphs display correctly

✅ Ensure history and leaderboard screens work

✅ Check proper data recording in CSV files

🧑‍💻 Developer Guidelines (✨ New Section)

Use meaningful variable and function names that clearly describe their purpose.

Keep GUI code and business logic separate — follow the MVC pattern principle.

Commit frequently with clear, descriptive messages.

Test after every significant change to ensure backward compatibility.

Document new functions with concise docstrings following the PEP 257 style.

🚀 Performance Optimization Tips (✨ New Section)

Prefer vectorized pandas and NumPy operations over Python loops.

Use lazy loading for question banks to improve startup time.

Cache frequently used user data in memory for faster navigation.

Avoid unnecessary plt.show() calls when embedding figures in Tkinter.

🤝 Contribution Best Practices (✨ New Section)

Create a new branch for every new feature or bug fix.

Run flake8 or any linter before committing.

Ensure consistent indentation (4 spaces).

Add meaningful comments and update this documentation if architecture changes.

Use descriptive commit messages like “fix:”, “feat:”, or “refactor:”.

🐍 Python Environment Requirements
Package	Minimum Version
Python	3.8+
numpy	1.24.0
pandas	2.0.0
matplotlib	3.7.0
tkinter	Included in Python (Windows/macOS)
