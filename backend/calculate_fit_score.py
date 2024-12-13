from collections import Counter
from backend.generate_feedback import tokenize, extractReqSkillsFromJobDesc 

def calculateFitScore(resumeText, jobDescription, nlpResponse):
    """
    Calculate a fit score based on keyword matches between a resume and a job description.
    Averaged out with nlpResponse fit score
    :param resume_text: String containing the resume text.
    :param job_description: String containing the job description.
    :param required_keywords: List of required keywords (optional).
    :param preferred_keywords: List of preferred keywords (optional).
    :return: Fit score as a percentage (0–100).
    """
    
    if not resumeText or not jobDescription:
        return 0

    resumeTokens = tokenize(resumeText)
    jobTokens = tokenize(jobDescription)

    # Convert required and preferred to sets for comparison
    tokenizedRequiredNLP = tokenize(" ".join(nlpResponse['jobDescriptionSkills']['required']))
    tokenizedPreferredNLP = tokenize(" ".join(nlpResponse['jobDescriptionSkills']['preferred']))
    categorizedJobTokens=extractReqSkillsFromJobDesc(jobDescription)
    if(len(categorizedJobTokens)>0):
        requiredTokens = set(tokenizedRequiredNLP & categorizedJobTokens)
    else:
        requiredTokens = tokenizedRequiredNLP
    preferredTokens =  set(tokenizedPreferredNLP & jobTokens)

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
    
    # get matching tokens
    matchingKeywords=[]
    if requiredTokens or preferredTokens:
        for token in resumeTokens:
            if token in requiredTokens or token in preferredTokens:
                matchingKeywords.append(token)

    # For non-weighted keyword matches, calculate proportional score
    if not requiredTokens and not preferredTokens:
        # Count the total number of unique matching tokens
        totalJobTokens = len(set(jobTokens))
        matchingTokens = len(set(resumeTokens) & set(jobTokens))
        matchingKeywords.append(set(resumeTokens)&set(jobTokens))

        # Proportional score based on matching tokens
        if totalJobTokens > 0:
            score = (matchingTokens / totalJobTokens) * 100
        else:
            score = 0
    print(score, nlpResponse['fitScore'])
    return {"fitScore": round((score+nlpResponse['fitScore'])/2),"matchedKeywords":matchingKeywords}
