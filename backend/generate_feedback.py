import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from pathlib import Path
from sklearn.pipeline import make_pipeline

stopwords_path = Path(__file__).parent / "stopwords.txt"

def categorizeSuggestions(suggestions):
    # Sample labeled data for training
    trainingData = [
        ("Add programming languages like Python and Java.", "skills"),
        ("Include soft skills like communication and teamwork.", "skills"),
        ("List skills in categories, such as technical and interpersonal.", "skills"),
        ("Mention relevant coursework in the education section.", "education"),
        ("Mention GPA in the education section.", "education"),
        ("Include online courses or certifications.", "education"),
        ("Describe work experience.", "experience"),
        ("List relevant projects with specific details.", "experience"),
        ("Use action verbs to describe job responsibilities.", "experience"),
        ("Highlight awards or certifications.", "achievements"),
        ("Quantify achievements with specific metrics.", "achievements"),
        ("Include notable accomplishments or recognitions.", "achievements")
    ]

    # Split training data into texts and labels
    texts, labels = zip(*trainingData)

    # Create and train a pipeline
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(texts, labels)

    # Predict categories for new suggestions
    if suggestions:
        predictions = model.predict(suggestions)
        # Format feedback as a list of dictionaries
        suggestions = [
            {"category": category, "text": suggestion}
            for suggestion, category in zip(suggestions, predictions)
        ]
    else:
        suggestions = []

    return {"suggestions": suggestions}

def getStopWords():
    # found list of stopwords at https://github.com/Alir3z4/stop-words?tab=readme-ov-file
    with open(stopwords_path, 'r', encoding="utf-8") as file:
        content = file.read().splitlines()

    return set(content)

def tokenize(text):
    return set(re.findall(r'[\w#+]+', text.lower()))
    

def extractReqSkillsFromJobDesc(jobDescription):
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

    return tokenize(requiredText)-getStopWords()

def generateFeedback(resumeText, jobDescription, nlpResponse):
    # Feedback is generated using both NLP input and own algorithm
    if not resumeText or not jobDescription:
        return {"missing_keywords": [], "suggestions": []}

    stopWords = getStopWords()
    # Tokenize resume and job description
    resumeTokens = tokenize(resumeText)
    jobTokens = tokenize(jobDescription)

    tokenizedRequiredNLP = tokenize(" ".join(nlpResponse['jobDescriptionSkills']['required']))
    tokenizedPreferredNLP = tokenize(" ".join(nlpResponse['jobDescriptionSkills']['preferred']))
    categorizedJobTokens=extractReqSkillsFromJobDesc(jobDescription)
    requiredTokens = set(tokenizedRequiredNLP & categorizedJobTokens)
    preferredTokens =  set(tokenizedPreferredNLP & jobTokens)

    # If no required or preferred, default to job description tokens
    if not requiredTokens and not preferredTokens:
        requiredTokens = jobTokens

    # Identify missing keywords
    missingKeywords = list((requiredTokens | preferredTokens) - resumeTokens - stopWords)
    missingKeywords.sort()
    # Generate suggestions
    suggestions = []
    nlpSuggestionString = " ".join(nlpResponse["suggestions"]).lower()
    for keyword in missingKeywords:
        # prevent duplicate suggestions when combining nlp and dynamically generated
        if keyword in nlpSuggestionString:
            continue
        if keyword.isdigit():
            suggestions.append(f"Highlight achievements or experience related to {keyword} years.")
        elif keyword.isalpha():
            suggestions.append(f"Consider including '{keyword}' in your resume to align with the job description.")
        else:
            suggestions.append(f"Add details that demonstrate your expertise in '{keyword}'.")

    return {"missingKeywords": missingKeywords, "feedback": categorizeSuggestions(suggestions+nlpResponse["suggestions"])}
