def generate_migration_simulation(scan_data):

    algorithm = scan_data.get("algorithm", "")

    if "RSA" in algorithm:
        return {
            "current": {
                "algorithm": "RSA 2048",
                "risk": "High (Vulnerable to Shor’s Algorithm)",
                "key_size": "256 bytes",
                "security_model": "Classical Only"
            },
            "hybrid": {
                "algorithm": "RSA 2048 + Kyber",
                "risk": "Reduced (Hybrid Quantum Resistance)",
                "key_size": "~1.2 KB",
                "security_model": "Hybrid Transitional"
            },
            "full_pqc": {
                "algorithm": "Kyber",
                "risk": "Quantum Safe",
                "key_size": "~1 KB",
                "security_model": "Post-Quantum"
            }
        }

    elif "EllipticCurve" in algorithm:
        return {
            "current": {
                "algorithm": "ECDSA / ECDH",
                "risk": "High (Discrete Log Vulnerable)",
                "key_size": "64 bytes",
                "security_model": "Classical ECC"
            },
            "hybrid": {
                "algorithm": "ECC + Kyber",
                "risk": "Reduced (Hybrid)",
                "key_size": "~1.1 KB",
                "security_model": "Hybrid Transitional"
            },
            "full_pqc": {
                "algorithm": "Kyber + Dilithium",
                "risk": "Quantum Safe",
                "key_size": "~1.5 KB",
                "security_model": "Post-Quantum"
            }
        }

    else:
        return {
            "current": {
                "algorithm": algorithm,
                "risk": "Low",
                "key_size": "N/A",
                "security_model": "Unknown"
            },
            "hybrid": {
                "algorithm": "Not Required",
                "risk": "Stable",
                "key_size": "N/A",
                "security_model": "Monitoring Only"
            },
            "full_pqc": {
                "algorithm": "Optional",
                "risk": "Future Safe",
                "key_size": "N/A",
                "security_model": "Optional Upgrade"
            }
        }