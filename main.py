import paramiko
import argparse
import subprocess
import time

profiles = {
    'cryptonaut-ai': {'host': '127.0.0.69', 'username': 'new_jazz', 'password': 'xxxxx'},
}

def ssh_connect(profile_key):
    profile = profiles.get(profile_key)
    
    if not profile:
        print(f"Profile '{profile_key}' not found.")
        return
    
    host = profile['host']
    username = profile['username']
    password = profile['password']
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(hostname=host, username=username, password=password)
        print(f"Connected to {host} as {username}")
        
        shell = client.invoke_shell()
        print("Interactive shell session opened. Type 'exit' to close the session.")
        
        while True:
            shell.send('pwd\n')
            time.sleep(1)
            output = ""
            while shell.recv_ready():
                output += shell.recv(1024).decode()
                if len(output) > 0 and output[-1] == '\n':
                    break
            
            cwd = output.strip()
            colored_prompt = f"\033[42;31m{cwd}\033[0m "
            command = input(f"{colored_prompt}Enter command: ")
            if command.lower() == 'exit':
                break
            
            if command.lower().startswith('nano '):
                file_to_edit = command[5:].strip()
                subprocess.run(['nano', file_to_edit])
                continue
            
            shell.send(command + '\n')
            
            time.sleep(1)
            output = ""
            while shell.recv_ready():
                output += shell.recv(1024).decode()
                if len(output) > 0 and output[-1] == '\n':
                    break
            print(output)
        client.close()
        print("Connection closed.")
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        print(f"SSH Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH CLI Tool")
    parser.add_argument('profile', type=str, help='Profile name to connect with')
    args = parser.parse_args()
    profile_key = args.profile
    ssh_connect(profile_key)
