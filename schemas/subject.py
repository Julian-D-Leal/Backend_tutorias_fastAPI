def subjectEntity(subject) -> dict:
    return{
        "id": str(subject["_id"]),
        "name": subject["name"],
        "careers": subject["careers"],	
        "semester": subject["semester"]
    }

def subjectsEntity(subjects) -> list:
    return [subjectEntity(subject) for subject in subjects]