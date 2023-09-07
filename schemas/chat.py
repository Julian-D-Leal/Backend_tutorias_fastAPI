def conversationEntity(conversation) -> dict:
    return{
        "_id": str(conversation["_id"]),
        "name": conversation["name"],
        "image_url": conversation["image_url"],
        "read": conversation["read"],
    }

def conversationsEntity(conversations) -> list:
    return [conversationEntity(conversation) for conversation in conversations]