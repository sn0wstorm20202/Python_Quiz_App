"""
Score Calculator Module
Uses NumPy for all score calculations, statistics, and analysis
Provides weighted scoring based on difficulty levels
"""

import numpy as np


# Difficulty point values
DIFFICULTY_POINTS = {
    'Easy': 10,
    'Medium': 15,
    'Hard': 25
}

# Time bonus thresholds (in seconds)
TIME_BONUS_FAST = 10  # Answer within 10 seconds
TIME_BONUS_MODERATE = 20  # Answer within 20 seconds
BONUS_POINTS_FAST = 5
BONUS_POINTS_MODERATE = 3

# Survival mode multiplier
SURVIVAL_COMBO_MULTIPLIER = 1.5
SURVIVAL_COMBO_THRESHOLD = 5


def calculate_percentage(correct, total):
    """
    Calculate percentage score using NumPy
    
    Args:
        correct: Number of correct answers
        total: Total number of questions
        
    Returns:
        Percentage score (0-100)
    """
    if total == 0:
        return 0.0
    
    # Use NumPy arrays for calculation
    correct_array = np.array([correct], dtype=np.float64)
    total_array = np.array([total], dtype=np.float64)
    
    # Calculate percentage: (correct/total) * 100
    percentage = (correct_array / total_array) * 100
    
    return float(percentage[0])


def calculate_base_score(correct_count, difficulty):
    """
    Calculate base score based on correct answers and difficulty
    
    Args:
        correct_count: Number of correct answers
        difficulty: Difficulty level ('Easy', 'Medium', 'Hard')
        
    Returns:
        Base score (integer)
    """
    points = DIFFICULTY_POINTS.get(difficulty, 10)
    
    # Use NumPy for calculation
    correct_array = np.array([correct_count], dtype=np.int32)
    points_array = np.array([points], dtype=np.int32)
    
    score = np.multiply(correct_array, points_array)
    
    return int(score[0])


def calculate_weighted_score(easy_correct, medium_correct, hard_correct):
    """
    Calculate total weighted score based on difficulty distribution
    Uses NumPy arrays for efficient computation
    
    Args:
        easy_correct: Number of correct easy questions
        medium_correct: Number of correct medium questions
        hard_correct: Number of correct hard questions
        
    Returns:
        Total weighted score
    """
    # Create NumPy arrays for difficulty points and correct counts
    difficulties = np.array([
        DIFFICULTY_POINTS['Easy'],
        DIFFICULTY_POINTS['Medium'],
        DIFFICULTY_POINTS['Hard']
    ], dtype=np.int32)
    
    correct_counts = np.array([
        easy_correct,
        medium_correct,
        hard_correct
    ], dtype=np.int32)
    
    # Calculate total score: sum of (difficulty_points * correct_count)
    total_score = np.sum(np.multiply(difficulties, correct_counts))
    
    return int(total_score)


def calculate_time_bonus(time_taken):
    """
    Calculate bonus points based on time taken to answer
    
    Args:
        time_taken: Time in seconds
        
    Returns:
        Bonus points (0, 3, or 5)
    """
    if time_taken <= TIME_BONUS_FAST:
        return BONUS_POINTS_FAST
    elif time_taken <= TIME_BONUS_MODERATE:
        return BONUS_POINTS_MODERATE
    return 0


def calculate_timed_score(correct_count, difficulty, time_data):
    """
    Calculate score for timed mode with time bonuses
    
    Args:
        correct_count: Number of correct answers
        difficulty: Difficulty level
        time_data: List of times taken for each correct answer
        
    Returns:
        Total score including bonuses
    """
    base_score = calculate_base_score(correct_count, difficulty)
    
    # Calculate total bonus from time data
    if time_data and len(time_data) > 0:
        time_array = np.array(time_data, dtype=np.float64)
        # Calculate bonus for each answer time
        bonuses = np.array([calculate_time_bonus(t) for t in time_array])
        total_bonus = int(np.sum(bonuses))
    else:
        total_bonus = 0
    
    return base_score + total_bonus


def calculate_survival_score(correct_streak, difficulty):
    """
    Calculate score for survival mode with combo multiplier
    
    Args:
        correct_streak: Number of consecutive correct answers
        difficulty: Difficulty level
        
    Returns:
        Score with combo multiplier applied
    """
    base_score = calculate_base_score(correct_streak, difficulty)
    
    # Apply multiplier if streak threshold is met
    if correct_streak >= SURVIVAL_COMBO_THRESHOLD:
        score_array = np.array([base_score], dtype=np.float64)
        multiplier_array = np.array([SURVIVAL_COMBO_MULTIPLIER], dtype=np.float64)
        final_score = np.multiply(score_array, multiplier_array)
        return int(final_score[0])
    
    return base_score


def calculate_statistics(scores):
    """
    Calculate comprehensive statistics using NumPy
    
    Args:
        scores: List of score values
        
    Returns:
        Dictionary containing statistical measures
    """
    if not scores or len(scores) == 0:
        return {
            'mean': 0.0,
            'median': 0.0,
            'std_dev': 0.0,
            'min': 0.0,
            'max': 0.0,
            'total': 0
        }
    
    # Convert to NumPy array
    scores_array = np.array(scores, dtype=np.float64)
    
    # Calculate statistics using NumPy functions
    stats = {
        'mean': float(np.mean(scores_array)),
        'median': float(np.median(scores_array)),
        'std_dev': float(np.std(scores_array)),
        'min': float(np.min(scores_array)),
        'max': float(np.max(scores_array)),
        'total': len(scores)
    }
    
    return stats


def calculate_improvement_rate(scores):
    """
    Calculate improvement trend using linear regression
    Uses NumPy polyfit to find the slope of score progression
    
    Args:
        scores: List of scores in chronological order
        
    Returns:
        Improvement rate (slope) and trend direction
    """
    if not scores or len(scores) < 2:
        return {
            'rate': 0.0,
            'trend': 'insufficient_data'
        }
    
    # Create arrays for x (attempt numbers) and y (scores)
    attempts = np.arange(len(scores), dtype=np.float64)
    scores_array = np.array(scores, dtype=np.float64)
    
    # Calculate linear trend: polyfit returns [slope, intercept]
    coefficients = np.polyfit(attempts, scores_array, 1)
    slope = float(coefficients[0])
    
    # Determine trend direction
    if slope > 0.5:
        trend = 'improving'
    elif slope < -0.5:
        trend = 'declining'
    else:
        trend = 'stable'
    
    return {
        'rate': slope,
        'trend': trend
    }


def calculate_accuracy_by_difficulty(easy_correct, easy_total, 
                                     medium_correct, medium_total,
                                     hard_correct, hard_total):
    """
    Calculate accuracy percentage for each difficulty level
    
    Args:
        easy_correct, easy_total: Easy questions statistics
        medium_correct, medium_total: Medium questions statistics
        hard_correct, hard_total: Hard questions statistics
        
    Returns:
        Dictionary with accuracy percentages
    """
    accuracies = {}
    
    # Calculate accuracy for each difficulty
    for level, correct, total in [
        ('Easy', easy_correct, easy_total),
        ('Medium', medium_correct, medium_total),
        ('Hard', hard_correct, hard_total)
    ]:
        if total > 0:
            accuracies[level] = calculate_percentage(correct, total)
        else:
            accuracies[level] = 0.0
    
    return accuracies


def get_grade_info(percentage):
    """
    Get grade information based on percentage
    
    Args:
        percentage: Score percentage
        
    Returns:
        Dictionary with grade, color, and message
    """
    if percentage >= 90:
        return {
            'grade': 'Excellent',
            'color': '#28a745',  # Green
            'message': 'Outstanding performance!'
        }
    elif percentage >= 70:
        return {
            'grade': 'Good',
            'color': '#007bff',  # Blue
            'message': 'Well done!'
        }
    elif percentage >= 50:
        return {
            'grade': 'Average',
            'color': '#ffc107',  # Orange
            'message': 'Keep practicing!'
        }
    else:
        return {
            'grade': 'Needs Improvement',
            'color': '#dc3545',  # Red
            'message': 'More practice recommended'
        }


def calculate_percentile(score, all_scores):
    """
    Calculate percentile rank of a score using NumPy
    
    Args:
        score: The score to rank
        all_scores: List of all scores
        
    Returns:
        Percentile rank (0-100)
    """
    if not all_scores or len(all_scores) == 0:
        return 0.0
    
    scores_array = np.array(all_scores, dtype=np.float64)
    
    # Count how many scores are less than or equal to the given score
    percentile = (np.sum(scores_array <= score) / len(scores_array)) * 100
    
    return float(percentile)


def analyze_performance(user_scores, user_percentages):
    """
    Comprehensive performance analysis combining multiple metrics
    
    Args:
        user_scores: List of user's scores
        user_percentages: List of user's percentage scores
        
    Returns:
        Dictionary with comprehensive analysis
    """
    stats = calculate_statistics(user_percentages)
    improvement = calculate_improvement_rate(user_percentages)
    
    # Calculate additional metrics
    if len(user_percentages) > 0:
        recent_avg = float(np.mean(user_percentages[-5:])) if len(user_percentages) >= 5 else stats['mean']
        consistency = 100 - stats['std_dev']  # Higher std_dev = less consistent
    else:
        recent_avg = 0.0
        consistency = 0.0
    
    return {
        'statistics': stats,
        'improvement': improvement,
        'recent_average': recent_avg,
        'consistency_score': max(0, consistency),
        'total_attempts': len(user_scores)
    }
