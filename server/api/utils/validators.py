import re

def password_validator(password: str) -> bool:
    """
    Validates password strength.

    Args
        password: password to validate

    Returns
        [bool]: True if password is valid
    """
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'    
    return re.match(pattern, password)

def email_validator(email: str) -> bool:
    """
    Validates email format.

    Args
        email: email to validate

    Returns
        [bool]: True if email is valid
    """
    return re.match(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 
        email
    )