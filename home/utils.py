import language_tool_python
from spellchecker import SpellChecker
import re

tool = language_tool_python.LanguageTool('en-US')
spell = SpellChecker()

def check_essay(text):
    #  CLEAN TEXT
    text = re.sub(r'\s+', ' ', text.strip())

    #  GRAMMAR CHECK (counts ALL grammar issues)
    matches = tool.check(text)
    grammar_errors = len(matches)

    #  SPELLING CHECK (counts EVERY MISSPELLED OCCURRENCE)
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    misspelled = spell.unknown(words)
    spelling_errors = sum(1 for word in words if word in misspelled)

    return grammar_errors, spelling_errors
