import re
from collections import Counter

def calculateFitScore(resumeText, jobDescription, required=None, preferred=None):
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
    
    if not resumeText or not jobDescription:
        return 0

    resumeTokens = tokenize(resumeText)
    jobTokens = tokenize(jobDescription)

    # Count matches for required and preferred keywords
    resumeCounter = Counter(resumeTokens)

    # If required and preferred are None, default to empty lists
    required = required or []
    preferred = preferred or []

    requiredMatches = sum(resumeCounter[k] for k in required)
    preferredMatches = sum(resumeCounter[k] for k in preferred)

    totalRequired = len(required)
    totalPreferred = len(preferred)

    score = 0

    # If there are required keywords, give them 70% of the score
    if totalRequired > 0:
        score += (requiredMatches / totalRequired) * 70

    # If there are preferred keywords, give them 30% of the score
    if totalPreferred > 0:
        score += (preferredMatches / totalPreferred) * 30

    # For non-weighted keyword matches, calculate proportional score
    if not required and not preferred:
        # Count the total number of unique matching tokens
        totalJobTokens = len(set(jobTokens))
        matchingTokens = len(set(resumeTokens) & set(jobTokens))
        
        # Proportional score based on matching tokens
        if totalJobTokens > 0:
            score = (matchingTokens / totalJobTokens) * 100
        else:
            score = 0

    return round(score)
