# Quiz Application with Score Analytics

A comprehensive Python-based quiz application built with Tkinter GUI, featuring advanced score analytics using NumPy, data management with pandas, and performance visualization with Matplotlib.

## 🎯 Project Overview

This is a BTech 2nd-year project that demonstrates proficiency in Python GUI development, data analysis, and file handling. The application provides an interactive quiz experience with three difficulty levels, multiple quiz modes, and detailed performance analytics.

## ✨ Features

### Quiz Functionality
- **Multiple Categories**: Python Programming, Data Structures & Algorithms, Computer Networks
- **Difficulty Levels**: Easy (10 points), Medium (15 points), Hard (25 points)
- **Quiz Modes**:
  - Practice Mode: Untimed with explanations
  - Timed Challenge: Countdown timer with bonus points
  - Survival Mode: 3 wrong answers ends the game
- **Interactive Feedback**: Color-coded correct/wrong answers with explanations
- **Question Bank**: 60+ professionally crafted MCQ questions
- **Review System**: Review all answers at the end of each quiz

### Score Tracking & Analytics
- User registration and login system
- Comprehensive attempt tracking (date, time, category, score, difficulty)
- **NumPy-powered calculations**:
  - Weighted scoring based on difficulty
  - Statistical analysis (mean, median, standard deviation)
  - Performance trends and improvement rates
- **pandas DataFrame management**:
  - Store and analyze quiz history
  - Filter by user, category, date range, difficulty
  - Export personal history
- **Matplotlib visualizations**:
  - Score trends over time (line graph)
  - Performance by category (bar chart)
  - Accuracy by difficulty (bar chart)
  - Correct vs incorrect distribution (pie chart)
  - Time taken analysis (line graph)

### Additional Features
- User profile with personal statistics
- Leaderboard showing top 10 scores
- Quiz history with sortable columns
- Data export to CSV
- Adaptive difficulty (optional)
- Progress bars and loading indicators

## 🛠️ Technology Stack

- **GUI**: Tkinter (all interface components)
- **Numerical Analysis**: NumPy (score calculations, statistics)
- **Data Management**: pandas (DataFrames, CSV operations)
- **Visualization**: Matplotlib (performance graphs)
- **File Handling**: JSON for questions, CSV for user data and history

## 📁 File Structure

```
quiz_app/
├── main.py                    # Main application entry point
├── data/
│   ├── questions.json         # Question bank (60+ questions)
│   ├── users.csv              # User credentials
│   └── quiz_history.csv       # All quiz attempts
├── modules/
│   ├── gui_login.py           # Login/register GUI
│   ├── gui_dashboard.py       # Main dashboard
│   ├── gui_quiz.py            # Quiz interface
│   ├── gui_results.py         # Results screen
│   ├── gui_analytics.py       # Analytics with matplotlib
│   └── gui_history.py         # History display
├── utils/
│   ├── file_handler.py        # Read/write CSV and JSON
│   ├── score_calculator.py    # NumPy calculations
│   ├── data_manager.py        # pandas operations
│   └── question_manager.py    # Question selection logic
├── requirements.txt
└── README.md
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd quiz_app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Required packages:
   - numpy >= 1.24.0
   - pandas >= 2.0.0
   - matplotlib >= 3.7.0

## ▶️ How to Run

Simply execute the main file:

```bash
python main.py
```

The application will:
1. Load existing data or create new CSV files if they don't exist
2. Display the login/register screen
3. Allow you to create an account or login with existing credentials

## 📖 Usage Guide

### First Time Setup
1. Run the application
2. Click "Register" to create a new account
3. Enter username and password
4. Login with your credentials

### Taking a Quiz
1. From the dashboard, click "Start New Quiz"
2. Select category (Python, DSA, or Computer Networks)
3. Choose difficulty level (Easy, Medium, Hard)
4. Select quiz mode (Practice, Timed, Survival)
5. Choose number of questions (5, 10, 15, or 20)
6. Answer questions and receive immediate feedback
7. View results and detailed statistics

### Viewing Analytics
1. Click "View Analytics" from dashboard
2. Explore multiple graphs:
   - Performance trends over time
   - Category-wise performance comparison
   - Difficulty-level accuracy
   - Overall correct/incorrect distribution
3. View calculated statistics (mean, median, std dev, etc.)

### Reviewing History
1. Click "View History" from dashboard
2. Browse all past quiz attempts
3. Sort by any column
4. Export history to CSV if needed

## 🎓 Scoring System

### Base Points by Difficulty
- Easy: 10 points per question
- Medium: 15 points per question
- Hard: 25 points per question

### Time Bonus (Timed Mode Only)
- Answer within 10 seconds: +5 bonus points
- Answer within 20 seconds: +3 bonus points

### Survival Mode
- Combo multiplier: 1.5x for 5 consecutive correct answers

### Percentage Grading
- 90-100%: Excellent (Green)
- 70-89%: Good (Blue)
- 50-69%: Average (Orange)
- Below 50%: Needs Improvement (Red)

## 📊 NumPy Usage Examples

The application extensively uses NumPy for calculations:

```python
# Calculate percentage
scores = np.array([correct_answers])
total = np.array([total_questions])
percentage = (scores / total) * 100

# Weighted scoring
difficulties = np.array([10, 15, 25])  # Easy, Medium, Hard
correct_per_difficulty = np.array([easy_correct, medium_correct, hard_correct])
total_score = np.sum(difficulties * correct_per_difficulty)

# Statistical analysis
all_scores = np.array(user_score_history)
mean_score = np.mean(all_scores)
std_dev = np.std(all_scores)
improvement_trend = np.polyfit(attempts, all_scores, 1)[0]
```

## 📈 pandas Usage Examples

Data management with pandas:

```python
# Load quiz history
quiz_data = pd.read_csv('data/quiz_history.csv')

# Filter user data
user_stats = quiz_data[quiz_data['username'] == 'john_doe']

# Group analysis
category_avg = quiz_data.groupby('category')['percentage'].mean()

# Save new attempt
quiz_data = pd.concat([quiz_data, pd.DataFrame([new_attempt])], ignore_index=True)
quiz_data.to_csv('data/quiz_history.csv', index=False)
```

## 🎨 GUI Screenshots

*(Screenshots will be added after implementation)*

- Login Screen
- Main Dashboard
- Quiz Interface
- Results Screen
- Analytics Dashboard
- History View

## ➕ Adding More Questions

To add questions to the question bank:

1. Open `data/questions.json`
2. Add new question objects following this structure:

```json
{
    "category": "Python",
    "difficulty": "Medium",
    "question": "What is the output of print(type([]))?",
    "options": ["<class 'list'>", "<class 'array'>", "<class 'tuple'>", "<class 'dict'>"],
    "correct": 0,
    "explanation": "[] creates an empty list, and type() returns <class 'list'>"
}
```

3. Save the file - changes take effect immediately

## 🔧 Error Handling

The application includes comprehensive error handling:
- File not found: Creates missing CSV/JSON files automatically
- Invalid login credentials: Clear error messages
- Empty question bank: Prevents quiz from starting
- Data corruption: Validates CSV structure on load

## 🚀 Future Enhancements

Potential improvements for future versions:
- Multi-language support
- Question difficulty adaptation based on performance
- Social features (friend challenges)
- Mobile app version
- Cloud storage for cross-device sync
- More question categories
- Achievement badges system
- Dark mode theme
- Sound effects for feedback
- Export results as PDF

## 👨‍💻 Development Notes

### Code Organization
- Modular design with separate GUI and utility modules
- Clear separation of concerns (data, logic, presentation)
- Extensive comments explaining NumPy and pandas operations
- Error handling at all file I/O points

### Best Practices
- PEP 8 compliant code style
- Descriptive variable and function names
- Docstrings for all major functions
- Type hints where applicable
- Git version control

## 📝 License

This is an educational project created for BTech coursework.

## 🤝 Contributing

This is a student project, but suggestions and improvements are welcome!

## 📧 Contact

For questions or feedback about this project, please contact the developer.

---

**Built with ❤️ using Python, Tkinter, NumPy, pandas, and Matplotlib**
