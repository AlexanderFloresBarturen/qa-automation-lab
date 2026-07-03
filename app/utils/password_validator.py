import re


def validate_password_strength(password: str) -> str:
    if not re.search(r"[A-Z]", password):
        raise ValueError("The password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        raise ValueError("The password must contain at least one lowercase letter")

    if not re.search(r"[0-9]", password):
        raise ValueError("The password must contain at least one number")

    if not re.search(r"[!@#$_]", password):
        raise ValueError("The password must contain at least one special character")

    return password
