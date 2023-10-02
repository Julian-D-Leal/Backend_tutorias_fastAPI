import json
import random
from faker import Faker
from dataArrays import carreras, materias, metodos, kw
fake = Faker('es_ES')
nombres = [fake.name() for i in range(100)]
users = []

def createUsers():
    for nombre in nombres:
        nombre = nombre
        email=nombre.replace(" ","").lower()+"@gmail.com"
        password="1234"
        is_tutor=random.choice([True, False, False])
        if not is_tutor:
            is_student=True
        else:
            is_student=False
        
        availability = []

        if is_student:
            career = random.choice(carreras)
            semester = random.randint(1,10)
            availability = [{"day": random.randint(0, 5), "hour": random.randint(0, 12)} for _ in range(random.randint(1,10))]
            format = random.sample(["Presencial","Virtual"], k=random.randint(1,2))
            budget = random.randint(10, 50) * 1000
            method = random.sample(metodos, k=random.randint(1,5))
            type_group = random.sample(["Grupal","Individual"], k=random.randint(1,2))
            keywords = random.choices(kw, k=random.randint(1,10))    

            user = {
                "name": nombre,
                "email": email,
                "password": password,
                "is_tutor": is_tutor,
                "is_student": is_student,
                "availability": availability,
                "format": format,
                "budget": budget,
                "method": method,
                "type_group": type_group,
                "keywords": keywords,
                "semester": semester,
                "career": career,
            }
        
        if is_tutor:
            if availability :
                availability = availability
            else:
                availability = [{"day": random.randint(0, 5), "hour": random.randint(0, 12)} for _ in range(random.randint(1,10))]
            format_tutor = random.sample(["Presencial","Virtual"], k=random.randint(1,2))
            cost_tutor = random.randint(10, 50) * 1000
            type_tutor = random.choice(["Estudiante", "Profesor"])
            method_tutor = random.sample(metodos, k=random.randint(1,5))
            type_group_tutor = random.sample(["Grupal","Individual"], k=random.randint(1,2))
            tutor_opinions = [{"opinion": fake.text(), "calification_tutor": random.randint(1,5), "name_user": fake.name(), "url_img": "https://profilephotos2.blob.core.windows.net/tutoriapp/image_default.png"} for _ in range(random.randint(1,5))]
            subjects_tutor = random.sample(materias, k=random.randint(1,10))
            user = {
                "name": nombre,
                "email": email,
                "password": password,
                "is_tutor": is_tutor,
                "is_student": is_student,
                "availability": availability,
                "format_tutor": format_tutor,
                "cost_tutor": cost_tutor,
                "method_tutor": method_tutor,
                "type_group_tutor": type_group_tutor,
                "type_tutor": type_tutor,
                "tutor_opinions": tutor_opinions,
                "subjects_tutor": subjects_tutor,
            }
        users.append(user)

    for student in users:
        if student["is_student"]:
            tutors = [tutor for tutor in users if tutor["is_tutor"]]
            clicksxtutor = random.choices(tutors, k=random.randint(1,5))
            student["clicks"] = [tutor["email"] for tutor in clicksxtutor]

    with open('scripts/createUsers/users.json', 'w',encoding='utf-8') as json_file:
        json.dump(users, json_file, ensure_ascii=False, indent=2)