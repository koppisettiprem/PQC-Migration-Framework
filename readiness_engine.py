def calculate_quantum_readiness(scan_data):
    score = 100
    reasons = []

    algorithm = scan_data.get("algorithm", "")
    key_size = scan_data.get("key_size", 0)
    tls_version = scan_data.get("tls_version", "")

    # Algorithm penalty
    if "RSA" in algorithm:
        score -= 40
        reasons.append("RSA vulnerable to Shor’s algorithm")
    elif "EllipticCurve" in algorithm:
        score -= 35
        reasons.append("ECC vulnerable to discrete log attack")

    # Key size penalty
    try:
        if int(key_size) <= 2048:
            score -= 15
            reasons.append("Key size considered weak for future quantum era")
    except:
        pass

    # TLS version penalty
    if "TLSv1.2" in tls_version:
        score -= 15
        reasons.append("TLS 1.2 less future-ready than TLS 1.3")

    # Normalize
    if score < 0:
        score = 0

    # Urgency classification
    if score < 40:
        urgency = "CRITICAL"
    elif score < 60:
        urgency = "HIGH"
    elif score < 80:
        urgency = "MEDIUM"
    else:
        urgency = "LOW"

    return {
        "score": score,
        "urgency": urgency,
        "reasons": reasons
    }