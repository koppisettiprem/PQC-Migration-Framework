from flask import Flask, render_template, request, send_file
from pqc_framework import run_full_analysis
from db import (
    save_scan,
    get_all_scans,
    get_total_scans,
    get_risk_distribution,
    get_algorithm_distribution,
    get_scan_by_id
)
from migration_simulator import generate_migration_simulation
from readiness_engine import calculate_quantum_readiness

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

app = Flask(__name__)

# ---------------------------
# LOGIN
# ---------------------------
@app.route("/")
def login():
    return render_template("login.html")


# ---------------------------
# DASHBOARD
# ---------------------------
@app.route("/dashboard")
def dashboard():
    total_scans = get_total_scans()
    risk_data = get_risk_distribution()
    algo_data = get_algorithm_distribution()

    return render_template(
        "dashboard.html",
        total_scans=total_scans,
        risk_data=risk_data,
        algo_data=algo_data
    )


# ---------------------------
# SCAN PAGE
# ---------------------------
@app.route("/scan_page")
def scan_page():
    return render_template("scan.html")


# ---------------------------
# PERFORM SCAN
# ---------------------------
@app.route("/scan", methods=["POST"])
def scan():
    host = request.form["host"]
    port = int(request.form["port"])

    try:
        # Run TLS + Risk + Migration analysis
        data = run_full_analysis(host, port)

        # Add domain for DB storage
        data["domain"] = host

        # Save to database
        save_scan(data)

        return render_template("result.html", data=data)

    except Exception as e:
        return render_template("result.html", data={
            "algorithm": "Error",
            "impact": str(e)
        })


# ---------------------------
# HISTORY PAGE
# ---------------------------
@app.route("/history")
def history():
    scans = get_all_scans()
    return render_template("history.html", scans=scans)


# ---------------------------
# DETAILED REPORT
# ---------------------------
@app.route("/report/<int:scan_id>")
def report(scan_id):
    scan = get_scan_by_id(scan_id)

    if not scan:
        return "Report not found", 404

    simulation = generate_migration_simulation(scan)
    readiness = calculate_quantum_readiness(scan)

    return render_template(
        "report.html",
        scan=scan,
        simulation=simulation,
        readiness=readiness
    )


# ---------------------------
# PDF EXPORT
# ---------------------------
@app.route("/report/<int:scan_id>/pdf")
def download_pdf(scan_id):
    scan = get_scan_by_id(scan_id)

    if not scan:
        return "Report not found", 404

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Post-Quantum Migration Report", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))

    table_data = [
        ["Target", scan["domain"]],
        ["Algorithm", scan["algorithm"]],
        ["Key Size", scan["key_size"]],
        ["TLS Version", scan["tls_version"]],
        ["Cipher Suite", scan["cipher_suite"]],
        ["Risk Level", scan["risk_level"]],
        ["Quantum Threat", scan["quantum_threat"]],
        ["Impact", scan["impact"]],
        ["Recommended Path", scan["recommended_path"]],
        ["Next Step", scan["next_step"]],
        ["Final Goal", scan["final_goal"]],
        ["Scanned At", str(scan["scanned_at"])]
    ]

    table = Table(table_data, colWidths=[2.2 * inch, 3.8 * inch])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"scan_report_{scan_id}.pdf",
        mimetype='application/pdf'
    )


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(
        ssl_context=("certs/server.crt", "certs/server.key"),
        port=4433,
        debug=True
    )