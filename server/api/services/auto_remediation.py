import pika
import subprocess

def send_alert(anomalies, severity):
    """
    Sends alert using RabbitMQ.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue="alerts")
    alert_message = {"anomalies": anomalies, "severity": severity}
    channel.basic_publish(exchange="", routing_key="alerts", body=str(alert_message))
    print("Alert sent via RabbitMQ:", alert_message)
    connection.close()

def auto_remediate(severity):
    """
    Executes Ansible playbook for auto-remediation.
    """
    if severity in ["High", "Critical"]:
        playbook_path = "../../playbook.yml"
        command = ["ansible-playbook", playbook_path]
        try:
            subprocess.run(command, check=True)
            print("Auto-remediation playbook executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing playbook: {e}")

# from flask import Blueprint, jsonify, request
# from services.log_service import ingest_logs, send_alert, auto_remediate

# logs_bp = Blueprint("logs", __name__)

# @logs_bp.route("/ingest", methods=["POST"])
# def ingest():
#     logs = request.json.get("logs", [])
#     if not logs:
#         return jsonify({"error": "No logs provided"}), 400

#     anomalies = ingest_logs(logs)  
#     if anomalies:
#         severity = classify_threat(anomalies)
#         send_alert(anomalies, severity)  
#         auto_remediate(severity)  
#         return jsonify({"message": "Logs processed with anomalies detected", "severity": severity}), 200
#     return jsonify({"message": "No anomalies detected"}), 200