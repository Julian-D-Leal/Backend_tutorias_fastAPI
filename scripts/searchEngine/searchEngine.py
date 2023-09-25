# import spacy
# from spacy.lang.es.stop_words import STOP_WORDS

# nlp = spacy.load("es_core_news_lg")

# def searchEngine(keywords, subjects):
#     totalScore = 0
#     filteredKeywords = [keyword for keyword in keywords if keyword not in STOP_WORDS]
#     for keyword in filteredKeywords:
#         score = 0   
#         keyword = keyword.lower()
#         keyword = nlp.vocab[keyword]
#         for subject in subjects:
#             if " " in subject:
#                 words = subject.lower().split()
#                 filteredWords = [word for word in words if word not in STOP_WORDS]
#                 maxScore = 0
#                 for word in filteredWords:
#                     word = word.lower()
#                     word = nlp.vocab[word]
#                     similarity = keyword.similarity(word)
#                     if similarity > maxScore:
#                         maxScore = similarity
#                 score += maxScore
#                 continue
#             subject = subject.lower()
#             subject = nlp.vocab[subject]
#             score += keyword.similarity(subject)
#         avgScore = score/len(subjects)
#         totalScore += avgScore
#     avgTotalScore = totalScore/len(keywords)
#     return avgTotalScore