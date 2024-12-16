from collections import Counter
from backend.generate_feedback import tokenize, extractReqSkillsFromJobDesc, getStopWords

def calculateFitScore(resumeText, jobDescription, nlpResponse):
    """
    Calculate a fit score based on keyword matches between a resume and a job description.
    Averaged out with nlpResponse fit score
    :param resumeText: String containing the resume text.
    :param jobDescription: String containing the job description.
    :param nlpResponse: response from nlp api
    :return: Fit score as a percentage (0–100). Matched keywords as a list
    """
    
    if not resumeText or not jobDescription:
        return 0

    stopWords = getStopWords()

    resumeTokens = tokenize(resumeText)-stopWords
    jobTokens = tokenize(jobDescription)-stopWords

    # Convert required and preferred to sets for comparison
    if(nlpResponse):
        tokenizedRequiredNLP = tokenize(" ".join(nlpResponse['jobDescriptionSkills']['required']))
        tokenizedPreferredNLP = tokenize(" ".join(nlpResponse['jobDescriptionSkills']['preferred']))
        categorizedJobTokens=extractReqSkillsFromJobDesc(jobDescription)
        if(len(categorizedJobTokens)>0):
            requiredTokens = set(tokenizedRequiredNLP & categorizedJobTokens)
        else:
            requiredTokens = tokenizedRequiredNLP
        preferredTokens =  set(tokenizedPreferredNLP & jobTokens)
    else:
        requiredTokens = extractReqSkillsFromJobDesc(jobDescription)
        preferredTokens =  set(jobTokens - requiredTokens)

    # Count matches for required and preferred keywords
    resumeCounter = Counter(resumeTokens)

    requiredMatches = sum(resumeCounter[k] for k in requiredTokens)
    preferredMatches = sum(resumeCounter[k] for k in preferredTokens)

    totalRequired = len(requiredTokens)
    totalPreferred = len(preferredTokens)

    score = 0
    # edge case where no preferred
    if totalPreferred == 0 and totalRequired > 0:
        score += (preferredMatches / totalRequired) * 100
    elif totalRequired > 0:
        # If there are required keywords, give them 70% of the score
        score += (requiredMatches / totalRequired) * 70

    # edge case where no required tokens
    if totalRequired == 0 and totalPreferred > 0:
        score += (preferredMatches / totalPreferred) * 100
    elif totalPreferred > 0:
         # If there are preferred keywords, give them 30% of the score
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

    if(nlpResponse):
        return {"fitScore": round((score+nlpResponse['fitScore'])/2),"matchedKeywords":matchingKeywords}
    else:
        return {"fitScore": round(score),"matchedKeywords":matchingKeywords}
