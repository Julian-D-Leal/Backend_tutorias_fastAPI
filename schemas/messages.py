def messageEntity(message) -> dict:
    return{
        # "_id": str(message["_id"]),
        "message": message["message"],
        "sender": message["sender"],
        "receiver": message["receiver"],
        "date": message["date"],
        "time": message["time"],
        "read": message["read"],
    }

def messagesEntity(messages) -> list:
    return [messageEntity(message) for message in messages]