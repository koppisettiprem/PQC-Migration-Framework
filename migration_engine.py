def add_migration_recommendation(data):

    level = data["risk_level"]

    if level == "CRITICAL":
        data["recommended_path"] = "Immediate Full PQC Migration (Kyber + Dilithium)"
        data["next_step"] = "Replace classical TLS completely"
        data["final_goal"] = "Quantum-Safe Infrastructure"

    elif level == "HIGH":
        data["recommended_path"] = "Hybrid Migration (Classical + Kyber)"
        data["next_step"] = "Enable PQC support in TLS layer"
        data["final_goal"] = "Full Migration to Kyber + Dilithium"

    else:
        data["recommended_path"] = "No Immediate Migration Required"
        data["next_step"] = "Monitor cryptographic updates"
        data["final_goal"] = "Maintain current configuration"

    return data