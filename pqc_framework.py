from crypto_detector import detect_algorithm
from analysis_engine import analyze_crypto
from migration_engine import add_migration_recommendation

def run_full_analysis(host, port):

    data = detect_algorithm(host, port)
    data = analyze_crypto(data)
    data = add_migration_recommendation(data)

    return data