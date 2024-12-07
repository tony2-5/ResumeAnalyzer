import re
from collections import Counter

def generate_feedback(resume_text, job_description, required=None, preferred=None):
    if not resume_text or not job_description:
        return {"missing_keywords": []}

    def tokenize(text):
        return set(re.findall(r'\b\w+\b', text.lower()))

    # Tokenize resume and job description
    resume_tokens = tokenize(resume_text)

    # Convert required and preferred to sets for comparison
    required_tokens = set(required or [])
    preferred_tokens = set(preferred or [])

    # Identify missing keywords
    missing_keywords = list((required_tokens - resume_tokens) | (preferred_tokens - resume_tokens))
    missing_keywords.sort()

    return {"missing_keywords": missing_keywords}