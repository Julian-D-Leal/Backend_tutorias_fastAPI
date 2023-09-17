import spacy
from nltk.corpus import stopwords

stopwords = stopwords.words('spanish')
nlp = spacy.load("es_core_news_lg")

def searchEngine(keywords, subjects):
    totalScore = 0
    filteredKeywords = [keyword for keyword in keywords if keyword not in stopwords]
    for keyword in filteredKeywords:
        score = 0   
        keyword = keyword.lower()
        keyword = nlp.vocab[keyword]
        for subject in subjects:
            if " " in subject:
                words = subject.lower().split()
                filteredWords = [word for word in words if word not in stopwords]
                maxScore = 0
                for word in filteredWords:
                    word = word.lower()
                    word = nlp.vocab[word]
                    similarity = keyword.similarity(word)
                    if similarity > maxScore:
                        maxScore = similarity
                score += maxScore
                continue
            subject = subject.lower()
            subject = nlp.vocab[subject]
            score += keyword.similarity(subject)
        avgScore = score/len(subjects)
        totalScore += avgScore
    avgTotalScore = totalScore/len(keywords)
    return avgTotalScore