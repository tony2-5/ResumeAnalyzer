import re

def generate_feedback(resume_text, job_description, required=None, preferred=None):
    if not resume_text or not job_description:
        return {"missing_keywords": [], "suggestions": []}

    def tokenize(text):
        return set(re.findall(r'\b\w+\b', text.lower()))


    # Tokenize resume and job description
    resume_tokens = tokenize(resume_text)
    print(job_description)
    job_tokens = tokenize(job_description)
    print(job_tokens)

    # Convert required and preferred to sets for comparison
    required_tokens = set(required or [])
    preferred_tokens = set(preferred or [])

    # If no required or preferred, default to job description tokens
    if not required and not preferred:
        required_tokens = job_tokens

    # Identify missing keywords
    stopwords = set(["a", "the", "and", "or", "to", "for", "with", "in", "on", "at", "by", "of", "as", "looking", "engineer", "software"])
    missing_keywords = list((required_tokens | preferred_tokens) - resume_tokens - stopwords)
    missing_keywords.sort()

    # Generate suggestions
    suggestions = []
    for keyword in missing_keywords:
        if keyword.isdigit():
            suggestions.append(f"Highlight achievements or experience related to {keyword} years.")
        elif keyword.isalpha():
            suggestions.append(f"Consider including '{keyword}' in your resume to align with the job description.")
        else:
            suggestions.append(f"Add details that demonstrate your expertise in '{keyword}'.")

    return {"missing_keywords": missing_keywords, "suggestions": suggestions}
