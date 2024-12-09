import re

def generateFeedback(resumeText, jobDescription, required=None, preferred=None):
    if not resumeText or not jobDescription:
        return {"missingKeywords": [], "suggestions": []}

    def tokenize(text):
        return set(re.findall(r'[\w#/-]+(?:\+{2})?', text.lower()))

    # Tokenize resume and job description
    resumeTokens = tokenize(resumeText)
    print(jobDescription)
    jobTokens = tokenize(jobDescription)
    print(jobTokens)

    # Convert required and preferred to sets for comparison
    requiredTokens = set(required or [])
    preferredTokens = set(preferred or [])

    # If no required or preferred, default to job description tokens
    if not required and not preferred:
        requiredTokens = jobTokens

    # Identify missing keywords
    stopwords = set(["a", "the", "and", "or", "to", "for", "with", "in", "on", "at", "by", "of", "as", "looking", "engineer", "software"])
    missingKeywords = list((requiredTokens | preferredTokens) - resumeTokens - stopwords)
    missingKeywords.sort()

    # Generate suggestions
    suggestions = []
    for keyword in missingKeywords:
        if keyword.isdigit():
            suggestions.append(f"Highlight achievements or experience related to {keyword} years.")
        elif keyword.isalpha():
            suggestions.append(f"Consider including '{keyword}' in your resume to align with the job description.")
        else:
            suggestions.append(f"Add details that demonstrate your expertise in '{keyword}'.")

    return {"missingKeywords": missingKeywords, "suggestions": suggestions}
