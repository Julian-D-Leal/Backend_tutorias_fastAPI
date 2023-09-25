# import json
# import pandas as pd
# import numpy as np
# from numpy.linalg import norm
# from sklearn.metrics.pairwise import cosine_similarity
# import spacy
# from spacy.lang.es.stop_words import STOP_WORDS

# def scaler(x,max):
#     scal = 1 - abs(x-max)/max
#     return round(scal,2)

# def similitud(a,b):
#     conjunto = a.union(b)
#     vector_a = []
#     vector_b = []
#     for elem in conjunto:
#         if elem in a:
#             vector_a.append(1)
#         else:
#             vector_a.append(0)
#         if elem in b:
#             vector_b.append(1)
#         else:
#             vector_b.append(0)
#     return round(cosine_similarity([vector_a],[vector_b])[0][0],2)

# def generateScoresTutors():
#     with open('scripts/createUsers/users.json','r',encoding='utf-8') as f:
#         users = json.load(f)

#     students = []
#     tutors = []
#     dataset = []

#     for user in users:
#         if user["is_student"]:
#             students.append(user)
#         if user["is_tutor"]:
#             tutors.append(user)

#     for tutor in tutors:
#         score_list = []
#         dispo = []

#         scores = tutor["tutor_opinions"]
#         for score in scores:
#             score_list.append(score["calification_tutor"])

#         disponibilidad = tutor["availability"]
#         for obj in disponibilidad:
#             dia,hora = obj["day"],obj["hour"]
#             dispo.append((dia,hora))

#         del tutor["name"]
#         del tutor["password"]
#         del tutor["is_tutor"]
#         del tutor["is_student"]
#         del tutor["availability"]
#         del tutor["type_tutor"]
#         del tutor["tutor_opinions"]
#         del tutor["subjects_tutor"]
#         tutor["scores"] = score_list
#         tutor["availability"] = dispo
    
#     for student in students:
#         dispo = []

#         disponibilidad = student["availability"]
#         for obj in disponibilidad:
#             dia,hora = obj["day"],obj["hour"]
#             dispo.append((dia,hora))
    
#         del student["name"]
#         del student["password"]
#         del student["is_tutor"]
#         del student["is_student"]
#         del student["availability"]
#         del student["semester"]
#         del student["career"]
#         del student["keywords"]
#         student["availability"] = dispo

#     #score de opiniones
#     for tutor in tutors:
#         auxscore = 0    
#         for score in tutor["scores"]:
#             auxscore += score
#         auxscore = auxscore/len(tutor["scores"])
#         tutor["scores"] = scaler(auxscore,5)


#     for student in students:
#         for tutor in tutors:
#             data_dict = {
#                 "estudiante" : student["email"],
#                 "tutor" : tutor["email"],
#                 "availability" : similitud(set(student["availability"]),set(tutor["availability"])),
#                 "format": 1 if set(student["format"]).intersection(set(tutor["format_tutor"])) else 0,
#                 "cost": 1 if student["budget"] >= tutor["cost_tutor"] else scaler(student["budget"],tutor["cost_tutor"]),
#                 "method": 1 if set(student["method"]).intersection(set(tutor["method_tutor"])) else 0,
#                 "type_group": 1 if set(student["type_group"]).intersection(set(tutor["type_group_tutor"])) else 0,
#                 "clicks": scaler(student["clicks"].count(tutor["email"]),len(student["clicks"])) if tutor["email"] in student["clicks"] else 0,
#                 "opinion": tutor["scores"]
#             }
#             total_score = data_dict["availability"] + data_dict["format"] + data_dict["cost"] + data_dict["method"] + data_dict["type_group"] + data_dict["clicks"] + data_dict["opinion"]
#             data_dict["availability"] = student["availability"]
#             data_dict["score"] = round(total_score/7,2)

#             dataset.append(data_dict)

#     final_dataset = []
#     for student in students:
#         for tutor in tutors:
#             for data in dataset:
#                 if student["email"] == data["estudiante"] and tutor["email"] == data["tutor"]: 
#                     data_dict = {
#                         "student_email" : student["email"],
#                         "tutor_email" : tutor["email"],
#                         "student_availability" : student["availability"],
#                         "format": student["format"],
#                         "budget": student["budget"],
#                         "method": student["method"],
#                         "type_group": student["type_group"],
#                         "clicks": student["clicks"],
#                         "tutor_availability" : tutor["availability"],
#                         "tutor_format": tutor["format_tutor"],
#                         "tutor_cost": tutor["cost_tutor"],
#                         "tutor_method": tutor["method_tutor"],
#                         "tutor_type_group": tutor["type_group_tutor"],
#                         "tutor_opinion": tutor["scores"],
#                         "score" : data["score"]
#                     }
#                     final_dataset.append(data_dict)
#     with open('scripts/generateScores/tutorScores.json', 'w',encoding='utf-8') as json_file:
#         json.dump(final_dataset, json_file, ensure_ascii=False, indent=2)

# def generateScoresSubjects():

#     nlp = spacy.load("es_core_news_lg")

#     with open('scripts/createUsers/users.json','r',encoding='utf-8') as f:
#         users = json.load(f)

#     subjects = pd.read_excel('scripts/generateScores/Asignaturas.xlsx').to_json(orient='records',force_ascii=False)
#     students = []
#     dataset = []

#     for user in users:
#         if user["is_student"]: 
#             students.append(user)

#     for student in students:
#         del student["name"]
#         del student["password"]
#         del student["is_tutor"]
#         del student["is_student"]
#         del student["availability"]
#         del student["format"]
#         del student["budget"]
#         del student["method"]
#         del student["type_group"]
#         del student["clicks"]

#     for student in students:
#         for subject in json.loads(subjects):
#             if student["career"] in subject["career"]:
#                 score = 0   
#                 for keyword in student["keywords"]:
#                     keyword = keyword.lower()
#                     keyword = nlp.vocab[keyword]
#                     if " " in subject["subject"]:
#                         words = subject["subject"].lower().split()
#                         filteredWords = [word for word in words if word not in STOP_WORDS]
#                         maxScore = 0
#                         for word in filteredWords:
#                             word = word.lower()
#                             word = nlp.vocab[word]
#                             similarity = keyword.similarity(word)
#                             if similarity > maxScore:
#                                 score = similarity
#                         score += maxScore
#                         continue
#                     s = subject["subject"].lower()
#                     s = nlp.vocab[s]
#                     score += keyword.similarity(s)
#                 avgScore = score/len(student["keywords"])
#                 data_dict = {
#                     "email" : student["email"],
#                     "asignatura": subject["subject"], 
#                     "score": round(avgScore,2)
#                 }
#                 dataset.append(data_dict)
#             else:
#                 data_dict = {
#                     "email" : student["email"],
#                     "asignatura": subject["subject"], 
#                     "score": 0
#                 }
#                 dataset.append(data_dict)
    
#     final_dataset = []
#     for student in students:
#         for subject in json.loads(subjects):
#             for data in dataset:
#                 if student["email"] == data["email"] and subject["subject"] == data["asignatura"]:
#                     final_dict = {
#                         "email" : student["email"],
#                         "career" : student["career"],
#                         "semester" : student["semester"],
#                         "keywords" : student["keywords"],
#                         "subject" : subject["subject"],
#                         "subject_career" : subject["career"],
#                         "subject_semester" : subject["semester"],
#                         "subject_score" : data["score"]
#                     }
#                     final_dataset.append(final_dict)
#     with open('scripts/generateScores/subjectScores.json', 'w',encoding='utf-8') as json_file:
#         json.dump(final_dataset, json_file, ensure_ascii=False, indent=2)
            
# # (generateScoresSubjects())
# # generateScoresTutors()