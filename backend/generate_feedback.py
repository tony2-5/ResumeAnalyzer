import re

def getStopWords():
    # found list of stopwords at https://github.com/Alir3z4/stop-words?tab=readme-ov-file
    with open('stopwords.txt', 'r') as file:
        content = file.read().splitlines()

    return set(content)

def tokenize(text):
    return set(re.findall(r'[\w#+]+', text.lower()))
    

def extractSkillsFromJobDesc(jobDescription):
    """
    Extracts required and preferred skills from the job description dynamically.
    Handles both structured and unstructured job descriptions.
    """
    # Use regex to identify potential section headers
    sections = re.split(
    r"(?i)^\s*(responsibilities|requirements|required|core\s+skills|preferred|bonus|qualifications|key\s+skills|education|experience)\s*:?",jobDescription,flags=re.MULTILINE)
    # Initialize containers for skills
    sectionMap = {
        "responsibilities": "",
        "requirements": "",
        "required": "",
        "core skills": "",
        "preferred": "",
        "bonus": "",
        "qualifications": "",
        "key skills": "",
        "experience": "",
        "education": "",
    }
    # Extract sections
    for i in range(0, len(sections)-1):
        sectionName = sections[i].strip().lower()
        if sectionName in sectionMap:
            sectionMap[sectionName] += " "+sections[i + 1].replace('\n'," ").strip()
    # Combine relevant sections into required and preferred skills
    requiredText = " ".join([sectionMap[key] for key in ["requirements", "required", "core skills", "qualifications", "key skills", "education", "experience"]])
    preferredText = " ".join([sectionMap[key] for key in ["preferred", "bonus"]])

    return {
        "required": tokenize(requiredText)-getStopWords(),
        "preferred": tokenize(preferredText)-getStopWords()
    }

def generateFeedback(resumeText, jobDescription):
    if not resumeText or not jobDescription:
        return {"missing_keywords": [], "suggestions": []}

    # Tokenize resume and job description
    resumeTokens = tokenize(resumeText)
    jobTokens = tokenize(jobDescription)

    categorizedJobTokens=extractSkillsFromJobDesc(jobDescription)
    requiredTokens = categorizedJobTokens['required']
    preferredTokens = categorizedJobTokens['preferred']
    print(resumeTokens)

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
