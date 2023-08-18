def userEntity(user) -> dict:
    return{
        "id": str(user["_id"]),
        "name": user["name"],
        "career": user["career"],
        "semester": user["semester"],
        "avaliability": user["avaliability"],	
        "format": user["format"],	
        "format_tutor": user["format_tutor"],
        "is_tutor": user["is_tutor"],
        "is_student": user["is_student"],
        "cost_tutor": user["cost_tutor"],
        "type_tutor": user["type_tutor"],
        "password": user["password"],
        "email": user["email"],
        "budget": user["budget"],
        "method": user["method"],
        "method_tutor": user["method_tutor"],
        "type_group": user["type_group"],
        "type_group_tutor": user["type_group_tutor"],
        "tutor_opinions": user["tutor_opinions"],
        "subjects_tutor": user["subjects_tutor"],
        "keywords": user["keywords"],
        "calification": user["calification"],
        "clicks": user["clicks"]
    }

def usersEntity(users) -> list:
    return [userEntity(user) for user in users]

