def check_phishing(text):
    
    if not text.strip():
     return 0, []

    text = text.lower()

    score = 0
    reasons = []

    suspicious_words = [
        "urgent",
        "verify",
        "password",
        "otp",
        "login",
        "account",
        "bank",
        "confirm",
        "update",
        "suspended",
        "click here",
        "winner",
        "prize",
        "free",
        "payment",
        "refund",
        "credit card",
        "debit card",
        "personal information",
        "reset password"
    ]

    if "http://" in text:
        score += 2
        reasons.append("Suspicious URL detected")

    if "bit.ly" in text:
        score += 2
        reasons.append("Shortened URL detected")

    if "tinyurl" in text:
        score += 2
        reasons.append("Shortened URL detected")



    if "goo.gl" in text:
        score += 2
        reasons.append("Shortened URL detected")

    if "t.co" in text:
        score += 2
        reasons.append("Shortened URL detected")

    if "is.gd" in text:
        score += 2
        reasons.append("Shortened URL detected")

    if ".ru" in text:
        score += 1
        reasons.append("Suspicious domain detected (.ru)")

    if ".tk" in text:
        score += 1
        reasons.append("Suspicious domain detected (.tk)")

    if ".xyz" in text:
        score += 1
        reasons.append("Suspicious domain detected (.xyz)")

    if ".top" in text:
        score += 1
        reasons.append("Suspicious domain detected (.top)")

    if ".click" in text:
        score += 1
        reasons.append("Suspicious domain detected (.click)")    

    for word in suspicious_words:

        if word in text:

            score += 1
            reasons.append(
                f"Suspicious word detected: {word}"
            )

    return score, reasons