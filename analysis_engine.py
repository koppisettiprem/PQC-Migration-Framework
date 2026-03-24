def analyze_crypto(data):

    algo = data["algorithm"].lower()
    key_size = data["key_size"]
    tls_version = data["tls_version"]
    signature = data["signature_algorithm"].lower()

    if "rsa" in algo:
        category = "Classical Public Key Cryptography"
        math_problem = "Integer Factorization"
    elif "elliptic" in algo or "ec" in algo:
        category = "Elliptic Curve Cryptography"
        math_problem = "Discrete Logarithm Problem"
    else:
        category = "Unknown Cryptographic Family"
        math_problem = "Unknown"

    if "ecdsa" in signature:
        usage = "Digital Signature (ECDSA)"
    elif "rsa" in signature:
        usage = "Digital Signature (RSA)"
    else:
        usage = "General TLS Authentication"

    if math_problem == "Integer Factorization":
        threat = "Shor's Algorithm can factor large integers"
        impact = "RSA private key compromise"
    elif math_problem == "Discrete Logarithm Problem":
        threat = "Shor's Algorithm can solve discrete logarithm"
        impact = "ECC private key compromise"
    else:
        threat = "Requires manual quantum analysis"
        impact = "Unknown quantum impact"

    score = 0

    if "rsa" in algo:
        score += 4
    elif "elliptic" in algo:
        score += 3

    if isinstance(key_size, int):
        if key_size <= 2048:
            score += 2
        elif key_size <= 3072:
            score += 1

    if tls_version == "TLSv1.3":
        score += 0
    elif tls_version == "TLSv1.2":
        score += 1
    elif tls_version == "TLSv1.1":
        score += 3
    else:
        score += 2

    if score >= 8:
        risk_level = "CRITICAL"
    elif score >= 5:
        risk_level = "HIGH"
    elif score >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    data.update({
        "category": category,
        "usage": usage,
        "quantum_threat": threat,
        "impact": impact,
        "risk_score": f"{score} / 10",
        "risk_level": risk_level
    })

    return data