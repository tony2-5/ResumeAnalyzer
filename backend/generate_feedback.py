import re

def getStopWords():
    # found list of stopwords at https://github.com/Alir3z4/stop-words?tab=readme-ov-file
    with open('stopwords.txt', 'r') as file:
        content = file.read().splitlines()

    return set(content)

def tokenize(text):
    return set(re.findall(r'[\w#/-]+(?:\+{2})?', text.lower()))

def extractSkillsFromJobDesc(jobDescription):
    """
    Extracts required and preferred skills from the job description dynamically.
    Handles both structured and unstructured job descriptions.
    """
    # Use regex to identify potential section headers
    sections = re.split(r"(?i)^\s*(Responsibilities|Requirements|Core Skills|Preferred|Bonus|Qualifications|Key Skills)\b:?", jobDescription, flags=re.MULTILINE)
    # Initialize containers for skills
    sectionMap = {
        "Responsibilities": "",
        "Requirements": "",
        "Core Skills": "",
        "Preferred": "",
        "Bonus": "",
        "Qualifications": "",
        "Key Skills": ""
    }

    # Extract sections
    for i in range(0, len(sections)-1):
        sectionName = sections[i].strip().capitalize()
        if sectionName in sectionMap:
            sectionMap[sectionName] += " "+sections[i + 1].replace('\n'," ").strip()

    # Combine relevant sections into required and preferred skills
    requiredText = " ".join([sectionMap[key] for key in ["Requirements", "Core Skills", "Qualifications", "Key Skills"]])
    preferredText = " ".join([sectionMap[key] for key in ["Preferred", "Bonus"]])

    print(requiredText)
    return {
        "required": tokenize(requiredText)-getStopWords(),
        "preferred": tokenize(preferredText)-getStopWords()
    }

def generateFeedback(resumeText, jobDescription, required=None, preferred=None):
    print(extractSkillsFromJobDesc(jobDescription))
    if not resumeText or not jobDescription:
        return {"missing_keywords": [], "suggestions": []}

    # Tokenize resume and job description
    resumeTokens = tokenize(resumeText)
    jobTokens = tokenize(jobDescription)

    # Convert required and preferred to sets for comparison
    requiredTokens = set(required or [])
    preferredTokens = set(preferred or [])

    # If no required or preferred, default to job description tokens
    if not required and not preferred:
        requiredTokens = jobTokens

    # Identify missing keywords
    stopWords = getStopWords()
    missingKeywords = list((requiredTokens | preferredTokens) - resumeTokens - stopWords)
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
