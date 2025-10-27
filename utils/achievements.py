"""
Achievement System Module
Tracks user achievements and milestones
Uses pandas to manage achievement data in CSV format
"""

import pandas as pd
import os
from datetime import datetime
from utils import data_manager


def get_achievements_path():
    """Get path to achievements CSV file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    return os.path.join(data_dir, 'achievements.csv')


def get_user_settings_path():
    """Get path to user settings CSV file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    return os.path.join(data_dir, 'user_settings.csv')


def initialize_achievements():
    """Create achievements CSV if it doesn't exist"""
    filepath = get_achievements_path()
    
    if not os.path.exists(filepath):
        # Create with headers
        df = pd.DataFrame(columns=['username', 'achievement_id', 'unlocked_date', 'unlocked_time'])
        df.to_csv(filepath, index=False)


def initialize_user_settings():
    """Create user settings CSV if it doesn't exist"""
    filepath = get_user_settings_path()
    
    if not os.path.exists(filepath):
        # Create with headers
        df = pd.DataFrame(columns=[
            'username', 'streak_count', 'last_played_date', 
            'daily_challenge_date', 'theme', 'sound_enabled'
        ])
        df.to_csv(filepath, index=False)


# Define all achievements
ACHIEVEMENTS = {
    'first_quiz': {
        'id': 'first_quiz',
        'name': 'Getting Started',
        'description': 'Complete your first quiz',
        'icon': '🌟',
        'condition': lambda stats: stats['total_quizzes'] >= 1
    },
    'quiz_master_10': {
        'id': 'quiz_master_10',
        'name': 'Quiz Master',
        'description': 'Complete 10 quizzes',
        'icon': '🎓',
        'condition': lambda stats: stats['total_quizzes'] >= 10
    },
    'quiz_legend_50': {
        'id': 'quiz_legend_50',
        'name': 'Quiz Legend',
        'description': 'Complete 50 quizzes',
        'icon': '👑',
        'condition': lambda stats: stats['total_quizzes'] >= 50
    },
    'perfect_score': {
        'id': 'perfect_score',
        'name': 'Perfectionist',
        'description': 'Score 100% on any quiz',
        'icon': '💯',
        'condition': lambda stats: stats.get('best_percentage', 0) == 100
    },
    'high_achiever': {
        'id': 'high_achiever',
        'name': 'High Achiever',
        'description': 'Maintain 90%+ average',
        'icon': '⭐',
        'condition': lambda stats: stats.get('average_percentage', 0) >= 90
    },
    'streak_5': {
        'id': 'streak_5',
        'name': '5 Day Streak',
        'description': 'Play for 5 consecutive days',
        'icon': '🔥',
        'condition': lambda stats: stats.get('streak_count', 0) >= 5
    },
    'streak_30': {
        'id': 'streak_30',
        'name': 'Dedication',
        'description': 'Play for 30 consecutive days',
        'icon': '🌟',
        'condition': lambda stats: stats.get('streak_count', 0) >= 30
    },
    'speed_demon': {
        'id': 'speed_demon',
        'name': 'Speed Demon',
        'description': 'Complete 10 Timed quizzes',
        'icon': '⚡',
        'condition': lambda stats: stats.get('timed_quizzes', 0) >= 10
    },
    'survivor': {
        'id': 'survivor',
        'name': 'Survivor',
        'description': 'Complete 10 Survival quizzes',
        'icon': '💪',
        'condition': lambda stats: stats.get('survival_quizzes', 0) >= 10
    },
    'knowledge_seeker': {
        'id': 'knowledge_seeker',
        'name': 'Knowledge Seeker',
        'description': 'Answer 500 questions correctly',
        'icon': '📚',
        'condition': lambda stats: stats.get('total_correct', 0) >= 500
    },
    'hard_mode_master': {
        'id': 'hard_mode_master',
        'name': 'Hard Mode Master',
        'description': 'Complete 10 Hard difficulty quizzes',
        'icon': '💎',
        'condition': lambda stats: stats.get('hard_quizzes', 0) >= 10
    }
}


def load_user_achievements(username):
    """
    Load achievements for a user
    
    Args:
        username: Username
        
    Returns:
        List of achievement IDs user has unlocked
    """
    initialize_achievements()
    filepath = get_achievements_path()
    
    try:
        df = pd.read_csv(filepath)
        user_achievements = df[df['username'] == username]
        return user_achievements['achievement_id'].tolist()
    except:
        return []


def unlock_achievement(username, achievement_id):
    """
    Unlock an achievement for a user
    
    Args:
        username: Username
        achievement_id: Achievement ID
        
    Returns:
        True if newly unlocked, False if already unlocked
    """
    initialize_achievements()
    filepath = get_achievements_path()
    
    # Check if already unlocked
    unlocked = load_user_achievements(username)
    if achievement_id in unlocked:
        return False
    
    # Add new achievement
    df = pd.read_csv(filepath)
    new_achievement = {
        'username': username,
        'achievement_id': achievement_id,
        'unlocked_date': datetime.now().strftime('%Y-%m-%d'),
        'unlocked_time': datetime.now().strftime('%H:%M:%S')
    }
    
    df = pd.concat([df, pd.DataFrame([new_achievement])], ignore_index=True)
    df.to_csv(filepath, index=False)
    
    return True


def check_and_unlock_achievements(username):
    """
    Check all achievements and unlock any newly earned ones
    
    Args:
        username: Username
        
    Returns:
        List of newly unlocked achievement details
    """
    # Get user statistics
    stats = data_manager.get_user_stats_summary(username)
    
    # Get user history for mode-specific counts
    history = data_manager.get_user_history(username)
    if not history.empty:
        stats['timed_quizzes'] = len(history[history['mode'] == 'Timed'])
        stats['survival_quizzes'] = len(history[history['mode'] == 'Survival'])
        stats['hard_quizzes'] = len(history[history['difficulty'] == 'Hard'])
    
    # Get streak count from user settings
    user_settings = get_user_settings(username)
    stats['streak_count'] = user_settings.get('streak_count', 0)
    
    # Check each achievement
    newly_unlocked = []
    
    for achievement_id, achievement_info in ACHIEVEMENTS.items():
        # Check if condition is met
        if achievement_info['condition'](stats):
            # Try to unlock
            if unlock_achievement(username, achievement_id):
                newly_unlocked.append(achievement_info)
    
    return newly_unlocked


def get_user_achievements_display(username):
    """
    Get formatted achievement data for display
    
    Args:
        username: Username
        
    Returns:
        Dict with locked and unlocked achievements
    """
    unlocked_ids = load_user_achievements(username)
    
    unlocked = []
    locked = []
    
    for achievement_id, info in ACHIEVEMENTS.items():
        achievement_data = {
            'id': achievement_id,
            'name': info['name'],
            'description': info['description'],
            'icon': info['icon']
        }
        
        if achievement_id in unlocked_ids:
            unlocked.append(achievement_data)
        else:
            locked.append(achievement_data)
    
    return {
        'unlocked': unlocked,
        'locked': locked,
        'total': len(ACHIEVEMENTS),
        'unlocked_count': len(unlocked)
    }


def get_user_settings(username):
    """
    Get user settings including streak and preferences
    
    Args:
        username: Username
        
    Returns:
        Dict with user settings
    """
    initialize_user_settings()
    filepath = get_user_settings_path()
    
    try:
        df = pd.read_csv(filepath)
        user_settings = df[df['username'] == username]
        
        if user_settings.empty:
            # Create default settings
            return {
                'username': username,
                'streak_count': 0,
                'last_played_date': None,
                'daily_challenge_date': None,
                'theme': 'light',
                'sound_enabled': True
            }
        
        return user_settings.iloc[0].to_dict()
    except:
        return {
            'username': username,
            'streak_count': 0,
            'last_played_date': None,
            'daily_challenge_date': None,
            'theme': 'light',
            'sound_enabled': True
        }


def update_user_settings(username, **kwargs):
    """
    Update user settings
    
    Args:
        username: Username
        **kwargs: Settings to update
    """
    initialize_user_settings()
    filepath = get_user_settings_path()
    
    df = pd.read_csv(filepath)
    
    # Check if user exists
    user_exists = not df[df['username'] == username].empty
    
    if user_exists:
        # Update existing
        for key, value in kwargs.items():
            df.loc[df['username'] == username, key] = value
    else:
        # Create new
        new_settings = {
            'username': username,
            'streak_count': 0,
            'last_played_date': None,
            'daily_challenge_date': None,
            'theme': 'light',
            'sound_enabled': True
        }
        new_settings.update(kwargs)
        df = pd.concat([df, pd.DataFrame([new_settings])], ignore_index=True)
    
    df.to_csv(filepath, index=False)


def update_streak(username):
    """
    Update user's daily streak
    
    Args:
        username: Username
        
    Returns:
        Current streak count
    """
    settings = get_user_settings(username)
    today = datetime.now().strftime('%Y-%m-%d')
    last_played = settings.get('last_played_date')
    
    if last_played is None:
        # First time playing
        streak_count = 1
    elif last_played == today:
        # Already played today
        streak_count = settings.get('streak_count', 1)
    else:
        # Check if consecutive day
        from datetime import datetime as dt, timedelta
        last_date = dt.strptime(last_played, '%Y-%m-%d')
        today_date = dt.strptime(today, '%Y-%m-%d')
        
        if (today_date - last_date).days == 1:
            # Consecutive day
            streak_count = settings.get('streak_count', 0) + 1
        else:
            # Streak broken
            streak_count = 1
    
    # Update settings
    update_user_settings(username, streak_count=streak_count, last_played_date=today)
    
    return streak_count


def can_play_daily_challenge(username):
    """
    Check if user can play daily challenge
    
    Args:
        username: Username
        
    Returns:
        True if can play, False if already played today
    """
    settings = get_user_settings(username)
    today = datetime.now().strftime('%Y-%m-%d')
    last_challenge = settings.get('daily_challenge_date')
    
    return last_challenge != today


def complete_daily_challenge(username):
    """
    Mark daily challenge as completed for today
    
    Args:
        username: Username
    """
    today = datetime.now().strftime('%Y-%m-%d')
    update_user_settings(username, daily_challenge_date=today)
