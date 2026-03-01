import re
from functools import lru_cache
from cefrpy import CEFRAnalyzer

# Initialize analyzer once
ANALYZER = CEFRAnalyzer()

@lru_cache(maxsize=1024)
def get_cefr_level(text):
    """Get CEFR level for text using CEFRAnalyzer"""
    if not text:
        return "-"
    
    # Split text into words and get CEFR level for each
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    if not words:
        return "-"
    
    # Get CEFR level for each word
    levels = []
    for word in words:
        level = ANALYZER.get_average_word_level_CEFR(word)
        if level:
            levels.append(int(level))
    
    if not levels:
        return "-"
    
    # Return the highest level among all words
    # CEFR levels: A1, A2, B1, B2, C1, C2 (represented as 1-6)
    highest_level = max(levels)
    
    # Convert integer value back to string name (A1, B2, etc.)
    level_names = {1: "A1", 2: "A2", 3: "B1", 4: "B2", 5: "C1", 6: "C2"}
    return level_names.get(int(highest_level), "-")
