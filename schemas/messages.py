def messageEntity(message) -> dict:
    return{
        "id": str(message["_id"]),
        "message": message["message"],
        "sender": message["sender"],
        "receiver": message["receiver"],
        "date": message["date"],
        "time": message["time"]
    }

def messagesEntity(messages) -> list:
    return [messageEntity(message) for message in messages]