# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Commands

### Running the Application
```powershell
python main.py
```

### Installing Dependencies
```powershell
pip install -r requirements.txt
```

### Checking Dependencies
```powershell
pip list | Select-String -Pattern "numpy|pandas|matplotlib"
```

## High-Level Architecture

### Application Flow
This is a **stateful, multi-screen Tkinter GUI application** with a centralized application controller:

- **`main.py`** contains the `QuizApplication` class - the single controller that manages all screen transitions and application state
- All screen navigation flows through `QuizApplication` methods (`show_dashboard()`, `show_quiz_setup()`, etc.)
- Screen clearing is handled centrally via `clear_screen()` which destroys all root widgets before showing new screens
- User authentication state is maintained in `QuizApplication.current_user`

### Module Organization

**`modules/`** - GUI screens (all return instances, not standalone)
- Each module creates UI components but doesn't manage navigation
- Screens receive callback functions from `QuizApplication` for navigation
- `gui_login.py` takes `on_login_success` callback
- `gui_dashboard.py` takes a `callbacks` dict with navigation functions
- `gui_analytics.py` and `gui_history.py` take `back_callback` for returning to dashboard

**`utils/`** - Pure backend logic (no GUI code)
- **`file_handler.py`**: Low-level file I/O (CSV/JSON read/write)
- **`data_manager.py`**: High-level data operations using pandas DataFrames
- **`score_calculator.py`**: All score/statistics calculations using NumPy
- **`question_manager.py`**: Question loading, filtering, and randomization

### Data Flow Architecture

**Storage Layer** (`data/`):
- `users.csv` - User credentials (managed by pandas)
- `quiz_history.csv` - All quiz attempts (managed by pandas)
- `questions.json` - Question bank (loaded with file_handler)

**Data Access Pattern**:
1. `file_handler.py` → Raw file operations
2. `data_manager.py` → Loads into pandas DataFrames, performs groupby/filter/aggregate
3. `score_calculator.py` → Extracts lists from DataFrames, converts to NumPy arrays
4. GUI modules → Display results from data_manager and score_calculator

### NumPy Integration Philosophy
All numerical calculations must go through `score_calculator.py` using NumPy:
- Percentage calculations use `np.array` division
- Statistical analysis uses `np.mean()`, `np.median()`, `np.std()`
- Trend analysis uses `np.polyfit()` for linear regression
- Never perform raw arithmetic on scores - always use NumPy arrays

### pandas Integration Philosophy
All data persistence and querying uses `data_manager.py` with pandas:
- Quiz history is always a DataFrame (`load_quiz_history()` returns DataFrame)
- User filtering uses DataFrame boolean indexing: `df[df['username'] == username]`
- Aggregations use `groupby()`: `df.groupby('category')['percentage'].mean()`
- New records appended with `pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)`

## Key Design Patterns

### Screen Lifecycle
1. `QuizApplication.clear_screen()` - Destroys all widgets
2. Create new Frame widget hierarchy
3. Pack into `self.root`
4. Screen instance may be stored in `self.current_screen` (but not always used)

### Quiz State Management
Quiz state is stored as a dictionary in `QuizApplication.quiz_data`:
```python
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
```

### Error Handling
- File operations: `try/except` with default returns (empty list, empty DataFrame)
- Auto-creation: `initialize_data_files()` creates missing CSV files with headers
- GUI validation: `messagebox.showerror()` for user input errors
- Missing modules: `try/except ImportError` with fallback behavior

## Scoring System

### Difficulty Points (defined in `score_calculator.py`)
- Easy: 10 points
- Medium: 15 points  
- Hard: 25 points

### Quiz Modes
- **Practice**: Base scoring only, untimed, shows explanations
- **Timed**: Base scoring + time bonuses (+5 for <10s, +3 for <20s)
- **Survival**: Base scoring + 1.5x multiplier after 5 consecutive correct

## Working with Questions

Questions are stored in `data/questions.json` with structure:
```json
{
    "category": "Python|DSA|Computer Networks",
    "difficulty": "Easy|Medium|Hard",
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "correct": 0-3,
    "explanation": "Explanation text"
}
```

Categories are dynamically loaded via `question_manager.get_categories()` - new categories can be added to JSON without code changes.

## Matplotlib Integration

Analytics graphs are embedded using `FigureCanvasTkAgg`:
1. Create `Figure` object from matplotlib
2. Add subplot and plot data
3. Create `FigureCanvasTkAgg(fig, master=parent_frame)`
4. Call `canvas.draw()` and `canvas.get_tk_widget().pack()`

Trend lines use `np.polyfit(x, y, 1)` for linear regression.

## Important Conventions

### File Paths
Always use `get_data_path()` or `get_user_data_path()` functions to construct paths - never hardcode paths.

### DataFrame Column Names
Quiz history columns (order matters for CSV writing):
`user_id, username, date, time, category, difficulty, total_questions, correct, wrong, score, percentage, time_taken, mode`

### Callback Pattern
Screens don't navigate directly - they call callbacks passed from `QuizApplication`:
```python
DashboardScreen(root, username, callbacks={
    'start_quiz': self.show_quiz_setup,
    'view_analytics': self.show_analytics,
    ...
})
```

### Window Geometry
Most screens center themselves using:
```python
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
```

## Testing Considerations

There are no automated tests. When making changes:
1. Test login/register flow
2. Take a quiz in each mode (Practice, Timed, Survival)
3. Verify analytics graphs render correctly
4. Check history table displays properly
5. Ensure leaderboard and profile screens work

## Python Requirements

- Python 3.8+
- numpy >= 1.24.0
- pandas >= 2.0.0  
- matplotlib >= 3.7.0
- tkinter (usually included with Python on Windows)
