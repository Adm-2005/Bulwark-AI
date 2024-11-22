import requests
import subprocess
import paramiko

def ping_network(ip_address):
    """
    Pings a network to verify if it can be reached.
    """
    try:
        subprocess.run(["ping", "-c", "1", ip_address], check=True, stdout=subprocess.DEVNULL)
        print(f"Ping to {ip_address} successful.")
        return True
    except subprocess.CalledProcessError:
        print(f"Ping to {ip_address} failed.")
        return False
    
def connect_via_ssh(ip_address, username, password):
    """
    Connects to a network via SSH.
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(hostname=ip_address, username=username, password=password, timeout=10)
        print(f"Successfully connected to {ip_address} via SSH.")
        return ssh  
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your credentials.")
        return None
    except paramiko.SSHException as e:
        print(f"Unable to establish SSH connection: {e}")
        return None
    except Exception as e:
        print(f"Exception occurred during SSH connection: {e}")
        return None
    
def connect_via_api(ip_address, token):
    """
    Connects to a network via an API endpoint.
    """
    url = f"http://{ip_address}/api/connect"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.post(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"Successfully connected to {ip_address} via API.")
            return response.json()
        else:
            print(f"Failed to connect: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during API connection: {e}")
        return None
    
def connect_to_network(ip_address, token=None, credentials=None):
    """
    Connects to a network using the available connection details.
    """
    if not ping_network(ip_address):
        print("Network is not reachable. Aborting connection.")
        return None

    if token:
        # When API connection is available
        return connect_via_api(ip_address, token)
    elif credentials:
        # When SSH connection is available
        return connect_via_ssh(ip_address, credentials.get("username"), credentials.get("password"))
    else:
        print("No valid connection method provided.")
        return None