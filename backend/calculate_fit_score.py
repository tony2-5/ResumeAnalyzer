import re
from collections import Counter
from backend.generate_feedback import getStopWords, tokenize, extractSkillsFromJobDesc 

def calculateFitScore(resumeText, jobDescription):
    """
    Calculate a fit score based on keyword matches between a resume and a job description.

    :param resume_text: String containing the resume text.
    :param job_description: String containing the job description.
    :param required_keywords: List of required keywords (optional).
    :param preferred_keywords: List of preferred keywords (optional).
    :return: Fit score as a percentage (0–100).
    """
    
    if not resumeText or not jobDescription:
        return 0
    
    stopWords = getStopWords()

    resumeTokens = tokenize(resumeText)-stopWords
    jobTokens = tokenize(jobDescription)-stopWords

    # Convert required and preferred to sets for comparison
    categorizedJobTokens=extractSkillsFromJobDesc(jobDescription)
    requiredTokens = categorizedJobTokens['required'] or []
    preferredTokens = categorizedJobTokens['preferred'] or []

    # Count matches for required and preferred keywords
    resumeCounter = Counter(resumeTokens)

    requiredMatches = sum(resumeCounter[k] for k in requiredTokens)
    preferredMatches = sum(resumeCounter[k] for k in preferredTokens)

    totalRequired = len(requiredTokens)
    totalPreferred = len(preferredTokens)

    score = 0

    # If there are required keywords, give them 70% of the score
    if totalRequired > 0:
        score += (requiredMatches / totalRequired) * 70

    # If there are preferred keywords, give them 30% of the score
    if totalPreferred > 0:
        score += (preferredMatches / totalPreferred) * 30

    # For non-weighted keyword matches, calculate proportional score
    if not requiredTokens and not preferredTokens:
        # Count the total number of unique matching tokens
        totalJobTokens = len(set(jobTokens))
        matchingTokens = len(set(resumeTokens) & set(jobTokens))
        
        # Proportional score based on matching tokens
        if totalJobTokens > 0:
            score = (matchingTokens / totalJobTokens) * 100
        else:
            score = 0

    return round(score)
