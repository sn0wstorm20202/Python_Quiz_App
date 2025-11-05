# Quick Start Guide

## Installation

1. **Ensure Python 3.8+ is installed:**
   ```bash
   python --version
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Simply run:
```bash
python main.py
```

## First Time Use

1. The application will automatically create necessary data files
2. Click **Register** to create a new account
3. Enter a username (minimum 3 characters) and password (minimum 4 characters)
4. After registration, you'll be logged in automatically and your credentials will be saved


## Taking Your First Quiz

1. From the dashboard, click **Start New Quiz**
2. Select:
   - **Category**: Python, DSA, or Computer Networks
   - **Difficulty**: Easy, Medium, or Hard
   - **Mode**: Practice, Timed, or Survival
   - **Number of Questions**: 5, 10, 15, or 20
3. Click **Start Quiz**
4. Answer questions and receive immediate feedback
5. View your results at the end

## Features Overview

### Practice Mode
- Untimed quiz with explanations
- Learn at your own pace
- See correct answers and explanations after each question

### Timed Challenge
- Countdown timer for each question
- Bonus points for quick answers (< 10s: +5pts, < 20s: +3pts)
- Track your speed improvement

### Survival Mode
- Game ends after 3 wrong answers
- Combo multiplier for 5 consecutive correct answers (1.5x)
- Test your knowledge under pressure

### Analytics Dashboard
- **Performance Trends**: Line graph showing score progression
- **Category Performance**: Bar chart comparing average scores
- **Difficulty Analysis**: Accuracy by difficulty level
- **Overall Stats**: Pie chart of correct vs incorrect answers
- **NumPy Statistics**: Mean, median, std deviation, improvement rate

### History
- View all past quiz attempts in a sortable table
- Export your history to CSV
- See summary statistics

### Leaderboard
- Top 10 scores across all users
- Compare your performance with others

### Profile
- View personal statistics
- Track total quizzes taken
- See your best scores and averages

## Technology Stack

- **GUI**: Tkinter
- **Score Calculations**: NumPy
- **Data Management**: pandas
- **Visualizations**: Matplotlib
- **File Storage**: CSV and JSON

## Scoring System

### Base Points
- Easy: 10 points per correct answer
- Medium: 15 points per correct answer
- Hard: 25 points per correct answer

### Time Bonuses (Timed Mode)
- Answer within 10 seconds: +5 bonus points
- Answer within 20 seconds: +3 bonus points

### Grading
- 90-100%: Excellent (Green)
- 70-89%: Good (Blue)
- 50-69%: Average (Orange)
- Below 50%: Needs Improvement (Red)

## Tips

1. Start with Easy difficulty to learn the question style
2. Use Practice Mode to understand concepts before taking timed quizzes
3. Check the Analytics dashboard regularly to track your improvement
4. Review your history to identify weak areas
5. The application uses NumPy for all statistical calculations
6. All data is stored locally in CSV files in the `data/` directory

## Troubleshooting

**Issue: Missing libraries**
```bash
pip install numpy pandas matplotlib
```

**Issue: Data files not found**
- The application will create them automatically on first run
- Files are in the `data/` directory

**Issue: Empty question bank**
- Verify `data/questions.json` exists
- File should contain 60+ questions

## Project Structure

```
quiz_app/
├── main.py                 # Run this file to start
├── requirements.txt        # Dependencies
├── README.md              # Full documentation
├── data/
│   ├── questions.json     # 60+ questions
│   ├── users.csv          # User accounts
│   └── quiz_history.csv   # Quiz attempts
├── modules/               # GUI components
│   ├── gui_login.py
│   ├── gui_dashboard.py
│   ├── gui_analytics.py
│   └── gui_history.py
└── utils/                 # Backend logic
    ├── file_handler.py
    ├── score_calculator.py   # NumPy calculations
    ├── data_manager.py       # pandas operations
    └── question_manager.py
```

## Support

For issues or questions about this BTech project, refer to the full README.md or contact the developer.

---

**Enjoy learning with the Quiz Application! 🎓**
