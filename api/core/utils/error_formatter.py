def format_serializer_errors(errors):
    """
    Formats serializer validation error
    """
    error_messages = []

    for field, errors_list in errors.items():
        for error in errors_list:
            if field == "message":
                return {"message": error}  
            error_messages.append(f"{field}, {error}".lower())

    return {"message": error_messages[0]} if error_messages else {"message": "An unknown error occurred"}
