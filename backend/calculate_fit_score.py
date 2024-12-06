import re
from collections import Counter

def calculate_fit_score(resume_text, job_description, required=None, preferred=None):
    """
    Calculate a fit score based on keyword matches between a resume and a job description.

    :param resume_text: String containing the resume text.
    :param job_description: String containing the job description.
    :param required_keywords: List of required keywords (optional).
    :param preferred_keywords: List of preferred keywords (optional).
    :return: Fit score as a percentage (0–100).
    """
    def tokenize(text):
        """Tokenize and normalize the text."""
        return re.findall(r'\b\w+\b', text.lower())
    
    if not resume_text or not job_description:
        return 0

    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)

    # Count matches for required and preferred keywords
    resume_counter = Counter(resume_tokens)

    # If required and preferred are None, default to empty lists
    required = required or []
    preferred = preferred or []

    required_matches = sum(resume_counter[k] for k in required)
    preferred_matches = sum(resume_counter[k] for k in preferred)

    total_required = len(required)
    total_preferred = len(preferred)

    score = 0

    # If there are required keywords, give them 70% of the score
    if total_required > 0:
        score += (required_matches / total_required) * 70

    # If there are preferred keywords, give them 30% of the score
    if total_preferred > 0:
        score += (preferred_matches / total_preferred) * 30

    # For non-weighted keyword matches, calculate proportional score
    if not required and not preferred:
        # Count the total number of unique matching tokens
        total_job_tokens = len(set(job_tokens))
        matching_tokens = len(set(resume_tokens) & set(job_tokens))
        
        # Proportional score based on matching tokens
        if total_job_tokens > 0:
            score = (matching_tokens / total_job_tokens) * 100
        else:
            score = 0

    return round(score)
