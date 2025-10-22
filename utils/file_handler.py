"""
File Handler Module
Provides utilities for reading and writing CSV and JSON files
with comprehensive error handling
"""

import json
import csv
import os
from datetime import datetime


def load_json(filepath):
    """
    Load data from a JSON file
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Parsed JSON data (list or dict)
        Returns empty list on error
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {filepath}: {e}")
        return []
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []


def save_json(filepath, data):
    """
    Save data to a JSON file
    
    Args:
        filepath: Path to the JSON file
        data: Data to save (list or dict)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to {filepath}: {e}")
        return False


def load_csv(filepath):
    """
    Load data from a CSV file
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of dictionaries (each row as a dict)
        Returns empty list if file doesn't exist or is empty
    """
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found, creating new file")
        return []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return []


def save_csv(filepath, data, fieldnames):
    """
    Save data to a CSV file
    
    Args:
        filepath: Path to the CSV file
        data: List of dictionaries to save
        fieldnames: List of field names (column headers)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Error saving to {filepath}: {e}")
        return False


def append_csv(filepath, data, fieldnames):
    """
    Append a single row to a CSV file
    
    Args:
        filepath: Path to the CSV file
        data: Dictionary representing one row
        fieldnames: List of field names (column headers)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
        
        with open(filepath, 'a', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        return True
    except Exception as e:
        print(f"Error appending to {filepath}: {e}")
        return False


def ensure_file_exists(filepath, default_content=""):
    """
    Ensure a file exists, create it with default content if it doesn't
    
    Args:
        filepath: Path to the file
        default_content: Content to write if file doesn't exist
        
    Returns:
        True if file exists or was created successfully
    """
    if not os.path.exists(filepath):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(default_content)
            return True
        except Exception as e:
            print(f"Error creating {filepath}: {e}")
            return False
    return True


def get_user_data_path(filename):
    """
    Get the full path for a data file
    
    Args:
        filename: Name of the file
        
    Returns:
        Full path to the file in the data directory
    """
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level and into data directory
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    return os.path.join(data_dir, filename)


def initialize_data_files():
    """
    Initialize all required data files if they don't exist
    Creates users.csv and quiz_history.csv with headers
    
    Returns:
        True if all files are ready
    """
    users_csv = get_user_data_path('users.csv')
    history_csv = get_user_data_path('quiz_history.csv')
    
    # Ensure users.csv exists
    if not os.path.exists(users_csv):
        ensure_file_exists(users_csv, "username,password,created_date\n")
    
    # Ensure quiz_history.csv exists
    if not os.path.exists(history_csv):
        ensure_file_exists(
            history_csv,
            "user_id,username,date,time,category,difficulty,total_questions,correct,wrong,score,percentage,time_taken,mode\n"
        )
    
    return True
