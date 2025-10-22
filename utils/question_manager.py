"""
Question Manager Module
Handles question loading, filtering, and randomization
"""

import random
import os
from utils.file_handler import load_json


def get_questions_path():
    """Get path to questions.json file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    return os.path.join(data_dir, 'questions.json')


def load_all_questions():
    """
    Load all questions from JSON file
    
    Returns:
        List of question dictionaries
    """
    filepath = get_questions_path()
    questions = load_json(filepath)
    return questions if questions else []


def filter_questions(category=None, difficulty=None):
    """
    Filter questions by category and/or difficulty
    
    Args:
        category: Category to filter by (optional)
        difficulty: Difficulty level to filter by (optional)
        
    Returns:
        List of filtered questions
    """
    all_questions = load_all_questions()
    
    filtered = all_questions
    
    if category:
        filtered = [q for q in filtered if q.get('category') == category]
    
    if difficulty:
        filtered = [q for q in filtered if q.get('difficulty') == difficulty]
    
    return filtered


def get_random_questions(category, difficulty, count):
    """
    Get random questions based on criteria
    
    Args:
        category: Category name
        difficulty: Difficulty level
        count: Number of questions to retrieve
        
    Returns:
        List of random questions (no duplicates)
    """
    questions = filter_questions(category, difficulty)
    
    # If requested count exceeds available questions, return all available
    if len(questions) <= count:
        return random.sample(questions, len(questions))
    
    # Return random sample without replacement
    return random.sample(questions, count)


def get_mixed_difficulty_questions(category, count):
    """
    Get questions with mixed difficulty levels
    
    Args:
        category: Category name
        count: Total number of questions
        
    Returns:
        List of questions with mixed difficulties
    """
    # Distribute questions across difficulties
    # Roughly 40% Easy, 40% Medium, 20% Hard
    easy_count = int(count * 0.4)
    medium_count = int(count * 0.4)
    hard_count = count - easy_count - medium_count
    
    questions = []
    
    # Get questions for each difficulty
    easy_q = filter_questions(category, 'Easy')
    medium_q = filter_questions(category, 'Medium')
    hard_q = filter_questions(category, 'Hard')
    
    # Add random questions from each difficulty
    if easy_q:
        questions.extend(random.sample(easy_q, min(easy_count, len(easy_q))))
    if medium_q:
        questions.extend(random.sample(medium_q, min(medium_count, len(medium_q))))
    if hard_q:
        questions.extend(random.sample(hard_q, min(hard_count, len(hard_q))))
    
    # Shuffle the combined list
    random.shuffle(questions)
    
    return questions[:count]


def get_categories():
    """
    Get list of unique categories
    
    Returns:
        List of category names
    """
    questions = load_all_questions()
    categories = list(set(q.get('category') for q in questions if q.get('category')))
    return sorted(categories)


def get_difficulties():
    """
    Get list of unique difficulty levels
    
    Returns:
        List of difficulty levels
    """
    return ['Easy', 'Medium', 'Hard']


def count_questions(category=None, difficulty=None):
    """
    Count available questions matching criteria
    
    Args:
        category: Category to filter by (optional)
        difficulty: Difficulty level to filter by (optional)
        
    Returns:
        Number of matching questions
    """
    questions = filter_questions(category, difficulty)
    return len(questions)


def validate_question(question):
    """
    Validate that a question has all required fields
    
    Args:
        question: Question dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['category', 'difficulty', 'question', 'options', 'correct', 'explanation']
    
    for field in required_fields:
        if field not in question:
            return False
    
    # Validate options list has 4 items
    if not isinstance(question['options'], list) or len(question['options']) != 4:
        return False
    
    # Validate correct answer index
    if not isinstance(question['correct'], int) or question['correct'] < 0 or question['correct'] > 3:
        return False
    
    return True


def get_question_stats():
    """
    Get statistics about question bank
    
    Returns:
        Dictionary with question statistics
    """
    questions = load_all_questions()
    
    if not questions:
        return {}
    
    stats = {
        'total': len(questions),
        'by_category': {},
        'by_difficulty': {}
    }
    
    # Count by category
    for category in get_categories():
        stats['by_category'][category] = count_questions(category=category)
    
    # Count by difficulty
    for difficulty in get_difficulties():
        stats['by_difficulty'][difficulty] = count_questions(difficulty=difficulty)
    
    return stats
