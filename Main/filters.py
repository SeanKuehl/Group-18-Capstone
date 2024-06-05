import os
import re
from django.conf import settings

def load_terms(filename):
    file_path = os.path.join(settings.BASE_DIR, 'Group-18-Capstone', 'resources', filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        terms = [line.strip() for line in file if line.strip()]
    return terms

hate_speech = load_terms('hate.txt')
curse_words = load_terms('curses.txt')

hate_speech_patterns = [re.compile(term, re.IGNORECASE) for term in hate_speech]
curse_word_patterns = [re.compile(term, re.IGNORECASE) for term in curse_words]

def contains_hate_speech(text):
    for pattern in hate_speech_patterns:
        if pattern.search(text):
            return True
    return False

def contains_curse_words(text):
    for pattern in curse_word_patterns:
        if pattern.search(text):
            return True
    return False