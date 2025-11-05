# 🧭 WARP.md  
### _Developer & Repository Guidance for WARP (warp.dev)_

---

## ⚙️ Commands

### ▶️ Running the Application
```bash
python main.py
```

### 📦 Installing Dependencies
```bash
pip install -r requirements.txt
```

### 🔍 Checking Installed Dependencies
```bash
pip list | Select-String -Pattern "numpy|pandas|matplotlib"
```

---

## 🧱 High-Level Architecture

### 🔄 Application Flow
This is a **stateful, multi-screen Tkinter GUI application** orchestrated by a centralized controller:

- **`main.py`** defines the `QuizApplication` class, managing all screen transitions, user state, and quiz data.  
- All navigation routes through controller methods like `show_dashboard()` or `show_quiz_setup()`.  
- **`clear_screen()`** ensures a clean transition by destroying existing widgets before new ones are rendered.  
- User session data is stored in **`QuizApplication.current_user`**.

---

## 🗂️ Module Organization

### 🖥️ `modules/` — GUI Screens
Each GUI module creates interface components but doesn’t control navigation logic.  
Navigation happens via **callback functions** provided by the controller.

| Module | Description |
|---------|--------------|
| `gui_login.py` | Handles login; uses `on_login_success` callback. |
| `gui_dashboard.py` | Main hub; receives a callbacks dictionary for navigation. |
| `gui_analytics.py`, `gui_history.py` | Use `back_callback` to return to the dashboard. |

### ⚙️ `utils/` — Backend Logic
Handles non-GUI functionality like data, scoring, and file operations.

| Module | Function |
|---------|-----------|
| `file_handler.py` | Raw file I/O (CSV/JSON read/write). |
| `data_manager.py` | High-level data ops using pandas. |
| `score_calculator.py` | Scoring and statistics using NumPy. |
| `question_manager.py` | Loads, filters, and randomizes questions. |

---

## 📊 Data Flow Architecture

### 🗃️ Storage Layer (`data/`)
| File | Purpose |
|------|----------|
| `users.csv` | User credentials |
| `quiz_history.csv` | Quiz attempt history |
| `questions.json` | Question bank |

### 🔁 Data Access Flow
```
file_handler.py → data_manager.py → score_calculator.py → GUI
```

- `file_handler.py`: Handles raw file operations.  
- `data_manager.py`: Loads DataFrames, filters, and aggregates data.  
- `score_calculator.py`: Performs numerical computations via NumPy.  
- `GUI`: Displays processed results.

---

## 🧮 Integration Philosophy

### 🔢 NumPy Usage
All numerical operations go through `score_calculator.py`:
- Use **NumPy arrays** for arithmetic and statistics.
- Perform trend analysis via `np.polyfit()`.
- Avoid manual arithmetic on Python lists.

### 🧬 pandas Usage
All persistence and querying go through `data_manager.py`:
- Load quiz data as **DataFrames**.
- Use **boolean indexing**, **groupby()**, and **aggregation** for analytics.
- Append new results via:
  ```python
  pd.concat([...], ignore_index=True)
  ```

---

## 🧠 Key Design Patterns

### 🖼️ Screen Lifecycle
```text
clear_screen() → destroys widgets
→ creates new frame hierarchy
→ packs frames into self.root
→ stores current screen reference
```

### 🧾 Quiz State Dictionary
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

### ⚠️ Error Handling
- File errors handled via `try/except` with safe defaults.  
- Missing files auto-created via `initialize_data_files()`.  
- GUI errors displayed via `messagebox.showerror()`.

---

## 🏆 Scoring System

| Difficulty | Points |
|-------------|---------|
| Easy | 10 |
| Medium | 15 |
| Hard | 25 |

### 🎮 Quiz Modes
- **Practice Mode:** Base scoring, untimed, with explanations.  
- **Timed Mode:** Base + time bonus (+5 for <10s, +3 for <20s).  
- **Survival Mode:** Base + 1.5× multiplier after 5 consecutive correct answers.

---

## 📝 Question Structure (`data/questions.json`)
```json
{
  "category": "Python|DSA|Computer Networks",
  "difficulty": "Easy|Medium|Hard",
  "question": "Question text",
  "options": ["A", "B", "C", "D"],
  "correct": 0,
  "explanation": "Explanation text"
}
```
✅ Categories are dynamically loaded using `question_manager.get_categories()`.  
New categories can be added **without modifying code**.

---

## 📈 Matplotlib Integration
Analytics graphs are embedded using `FigureCanvasTkAgg`:

```python
fig = Figure()
ax = fig.add_subplot(111)
ax.plot(x, y)

canvas = FigureCanvasTkAgg(fig, master=parent_frame)
canvas.draw()
canvas.get_tk_widget().pack()
```
Trend lines use NumPy’s linear regression via `np.polyfit()`.

---

## 🧩 Conventions & Coding Standards

### 📁 File Paths
Always construct paths using helpers like:
```python
get_data_path(), get_user_data_path()
```

### 🧾 Quiz History CSV Columns
`user_id, username, date, time, category, difficulty, total_questions, correct, wrong, score, percentage, time_taken, mode`

### 🔗 Callback Pattern
GUI screens **never control navigation directly** — they use callbacks from `QuizApplication`.

### 🪟 Window Geometry
```python
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
```

---

## 🧪 Testing Checklist
Before committing, verify:

✅ Login & registration flow  
✅ All quiz modes (Practice, Timed, Survival)  
✅ Analytics graphs render correctly  
✅ History & leaderboard screens function properly  
✅ Data correctly recorded in CSVs  

---

## 🧑‍💻 Developer Guidelines (✨ New Section)
- Use meaningful, self-explanatory names.  
- Keep GUI and logic separate — follow **MVC principles**.  
- Commit frequently with clear messages.  
- Test after every major change.  
- Write docstrings following **PEP 257**.

---

## 🚀 Performance Optimization Tips (✨ New Section)
- Prefer **vectorized NumPy/pandas** ops over loops.  
- Use **lazy loading** for question banks.  
- Cache frequently used user data.  
- Avoid redundant `plt.show()` calls in embedded graphs.

---

## 🤝 Contribution Best Practices (✨ New Section)
- Create a **new branch** per feature or fix.  
- Run `flake8` or a linter before committing.  
- Maintain consistent **4-space indentation**.  
- Update docs if architecture changes.  
- Follow commit message conventions:  
  ```
  feat:, fix:, refactor:
  ```

---

## 🐍 Python Environment Requirements
| Package | Minimum Version |
|----------|-----------------|
| Python | 3.8+ |
| numpy | 1.24.0 |
| pandas | 2.0.0 |
| matplotlib | 3.7.0 |
| tkinter | Included (Windows/macOS) |

---
