def send_password_reset_email(email: str, token: str) -> bool:
    print(f"Sending password reset token to {email}: {token}")

    return True
