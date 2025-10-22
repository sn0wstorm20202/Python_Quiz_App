"""
Data Manager Module
Uses pandas for DataFrame operations, data storage, and analysis
Manages quiz history and user data using CSV files
"""

import pandas as pd
import os
from datetime import datetime


def get_data_path(filename):
    """Get full path to data file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    return os.path.join(data_dir, filename)


def load_quiz_history():
    """
    Load quiz history from CSV into pandas DataFrame
    
    Returns:
        DataFrame with quiz history or empty DataFrame
    """
    filepath = get_data_path('quiz_history.csv')
    
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=[
            'user_id', 'username', 'date', 'time', 'category', 
            'difficulty', 'total_questions', 'correct', 'wrong', 
            'score', 'percentage', 'time_taken', 'mode'
        ])
    except Exception as e:
        print(f"Error loading quiz history: {e}")
        return pd.DataFrame()


def save_quiz_history(df):
    """
    Save quiz history DataFrame to CSV
    
    Args:
        df: pandas DataFrame with quiz history
        
    Returns:
        True if successful, False otherwise
    """
    filepath = get_data_path('quiz_history.csv')
    
    try:
        df.to_csv(filepath, index=False)
        return True
    except Exception as e:
        print(f"Error saving quiz history: {e}")
        return False


def add_quiz_attempt(username, category, difficulty, total_questions, 
                     correct, wrong, score, percentage, time_taken, mode):
    """
    Add a new quiz attempt to history using pandas
    
    Args:
        username: Username
        category: Quiz category
        difficulty: Difficulty level
        total_questions: Total number of questions
        correct: Number of correct answers
        wrong: Number of wrong answers
        score: Total score
        percentage: Percentage score
        time_taken: Time taken in seconds
        mode: Quiz mode (Practice/Timed/Survival)
        
    Returns:
        True if successful, False otherwise
    """
    # Load existing data
    df = load_quiz_history()
    
    # Create new attempt data
    new_attempt = {
        'user_id': len(df) + 1,
        'username': username,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M:%S'),
        'category': category,
        'difficulty': difficulty,
        'total_questions': total_questions,
        'correct': correct,
        'wrong': wrong,
        'score': score,
        'percentage': percentage,
        'time_taken': time_taken,
        'mode': mode
    }
    
    # Append new attempt using pd.concat
    df = pd.concat([df, pd.DataFrame([new_attempt])], ignore_index=True)
    
    # Save updated DataFrame
    return save_quiz_history(df)


def get_user_history(username):
    """
    Get all quiz attempts for a specific user
    
    Args:
        username: Username to filter by
        
    Returns:
        DataFrame with user's quiz history
    """
    df = load_quiz_history()
    
    if df.empty:
        return df
    
    # Filter DataFrame for specific user
    user_df = df[df['username'] == username]
    return user_df


def get_category_statistics(username=None):
    """
    Calculate average scores by category using pandas groupby
    
    Args:
        username: Optional username to filter by
        
    Returns:
        Series with average percentage by category
    """
    df = load_quiz_history()
    
    if df.empty:
        return pd.Series()
    
    # Filter by username if provided
    if username:
        df = df[df['username'] == username]
    
    # Group by category and calculate mean percentage
    category_stats = df.groupby('category')['percentage'].mean()
    return category_stats


def get_difficulty_statistics(username=None):
    """
    Calculate statistics by difficulty level
    
    Args:
        username: Optional username to filter by
        
    Returns:
        DataFrame with statistics by difficulty
    """
    df = load_quiz_history()
    
    if df.empty:
        return pd.DataFrame()
    
    # Filter by username if provided
    if username:
        df = df[df['username'] == username]
    
    # Group by difficulty and calculate stats
    difficulty_stats = df.groupby('difficulty').agg({
        'percentage': ['mean', 'count'],
        'correct': 'sum',
        'total_questions': 'sum'
    })
    
    return difficulty_stats


def get_top_scores(limit=10):
    """
    Get top scores across all users using pandas
    
    Args:
        limit: Number of top scores to return
        
    Returns:
        DataFrame with top scores
    """
    df = load_quiz_history()
    
    if df.empty:
        return df
    
    # Sort by score descending and get top N
    top_scores = df.nlargest(limit, 'score')
    return top_scores[['username', 'category', 'score', 'percentage', 'date', 'difficulty']]


def get_user_stats_summary(username):
    """
    Get comprehensive statistics summary for a user
    
    Args:
        username: Username
        
    Returns:
        Dictionary with various statistics
    """
    df = get_user_history(username)
    
    if df.empty:
        return {
            'total_quizzes': 0,
            'average_score': 0.0,
            'average_percentage': 0.0,
            'best_score': 0,
            'best_percentage': 0.0,
            'total_correct': 0,
            'total_questions': 0,
            'most_attempted_category': 'None'
        }
    
    # Calculate statistics using pandas functions
    stats = {
        'total_quizzes': len(df),
        'average_score': df['score'].mean(),
        'average_percentage': df['percentage'].mean(),
        'best_score': df['score'].max(),
        'best_percentage': df['percentage'].max(),
        'total_correct': df['correct'].sum(),
        'total_questions': df['total_questions'].sum(),
        'most_attempted_category': df['category'].mode()[0] if not df['category'].mode().empty else 'None'
    }
    
    return stats


def get_time_series_data(username):
    """
    Get time series data for performance over attempts
    
    Args:
        username: Username
        
    Returns:
        Lists of attempt numbers and corresponding scores
    """
    df = get_user_history(username)
    
    if df.empty:
        return [], []
    
    # Sort by date and time
    df = df.sort_values(['date', 'time'])
    
    # Get attempt numbers and percentages
    attempts = list(range(1, len(df) + 1))
    percentages = df['percentage'].tolist()
    
    return attempts, percentages


def filter_by_date_range(username, start_date, end_date):
    """
    Filter quiz history by date range
    
    Args:
        username: Username
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        
    Returns:
        Filtered DataFrame
    """
    df = get_user_history(username)
    
    if df.empty:
        return df
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Filter by date range
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    filtered_df = df[mask]
    
    return filtered_df


def export_user_history(username, output_path):
    """
    Export user's quiz history to CSV file
    
    Args:
        username: Username
        output_path: Path to save the CSV file
        
    Returns:
        True if successful, False otherwise
    """
    df = get_user_history(username)
    
    if df.empty:
        return False
    
    try:
        df.to_csv(output_path, index=False)
        return True
    except Exception as e:
        print(f"Error exporting history: {e}")
        return False


def get_recent_attempts(username, count=5):
    """
    Get most recent quiz attempts for a user
    
    Args:
        username: Username
        count: Number of recent attempts to retrieve
        
    Returns:
        DataFrame with recent attempts
    """
    df = get_user_history(username)
    
    if df.empty:
        return df
    
    # Sort by date and time descending, get last N
    df = df.sort_values(['date', 'time'], ascending=False)
    return df.head(count)


def get_performance_by_mode(username):
    """
    Analyze performance across different quiz modes
    
    Args:
        username: Username
        
    Returns:
        DataFrame with stats by mode
    """
    df = get_user_history(username)
    
    if df.empty:
        return pd.DataFrame()
    
    # Group by mode and calculate statistics
    mode_stats = df.groupby('mode').agg({
        'percentage': ['mean', 'count'],
        'score': 'mean'
    })
    
    return mode_stats


def load_users():
    """
    Load users from CSV
    
    Returns:
        DataFrame with user data
    """
    filepath = get_data_path('users.csv')
    
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=['username', 'password', 'created_date'])
    except Exception as e:
        print(f"Error loading users: {e}")
        return pd.DataFrame()


def save_users(df):
    """
    Save users DataFrame to CSV
    
    Args:
        df: pandas DataFrame with user data
        
    Returns:
        True if successful, False otherwise
    """
    filepath = get_data_path('users.csv')
    
    try:
        df.to_csv(filepath, index=False)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False


def add_user(username, password):
    """
    Add a new user using pandas
    
    Args:
        username: Username
        password: Password (should be hashed in production)
        
    Returns:
        True if successful, False if user exists
    """
    df = load_users()
    
    # Check if username already exists
    if not df.empty and username in df['username'].values:
        return False
    
    # Create new user
    new_user = {
        'username': username,
        'password': password,
        'created_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Append new user
    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    
    # Save updated DataFrame
    return save_users(df)


def validate_user(username, password):
    """
    Validate user credentials
    
    Args:
        username: Username
        password: Password
        
    Returns:
        True if valid, False otherwise
    """
    df = load_users()
    
    if df.empty:
        return False
    
    # Check if user exists with correct password
    user = df[(df['username'] == username) & (df['password'] == password)]
    return not user.empty
