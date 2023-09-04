def conversationEntity(conversation) -> dict:
    return{
        "id": str(conversation["_id"]),
        "name": conversation["name"],
        "image_url": conversation["image_url"]
    }

def conversationsEntity(conversations) -> list:
    return [conversationEntity(conversation) for conversation in conversations]