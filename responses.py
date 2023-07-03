def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'dang':
        return 'you cannot say that!'
