def password_resetEntity(password_reset) -> dict:
    return{
        "_id": str(password_reset["_id"]),
        "email": password_reset["email"],
        "token": password_reset["token"],
        "expires": password_reset["expires"]
    }
def password_resetsEntity(password_resets) -> list:
    return [password_resetEntity(password_reset) for password_reset in password_resets]

