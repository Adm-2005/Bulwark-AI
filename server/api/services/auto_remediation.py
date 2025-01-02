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
