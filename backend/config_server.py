import logging
import json
from websocket_server import WebsocketServer
import subprocess
from decouple import config
import pexpect

host = config('CONFIG_SERVER_HOST')
port = config('CONFIG_SERVER_PORT', cast=int)
traffic_generator_username = config('TRAFFIC_GENERATOR_USERNAME')
traffic_generator_ip = config('TRAFFIC_GENERATOR_IP')

bridge_20_username = config('BRIDGE_20_USERNAME')
bridge_20_ip = config('BRIDGE_20_IP')

bridge_22_username = config('BRIDGE_22_USERNAME')
bridge_22_ip = config('BRIDGE_22_IP')

bridge = "relyum20"

# Initialize logger for notifications
logger = logging.getLogger('mylogger-notif')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./logs/dgsec_sockets_notifications.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)   
import pexpect

def execute_ssh_commands(username, host, command):
    """
    Function to execute a single command via SSH.
    """
    ssh_command = f'ssh {username}@{host} soce_cli'
    child = pexpect.spawn(ssh_command, timeout=10)
    
    try:
        # Expect the prompt after connecting via SSH
        child.expect('soce_cli#')

        # Execute the command
        child.sendline(command)
        # Wait for the prompt after sending the command
        child.expect('soce_cli#')

        # Close the SSH connection
        child.sendline('exit')
        child.expect(pexpect.EOF)

    except pexpect.exceptions.EOF:
        print("Error: Connection closed unexpectedly.")
    except pexpect.TIMEOUT:
        print("Error: Timeout occurred.")

def check_bridge(ip_address):
    """
    Function to check if the IP address is reachable by pinging it.
    Returns True if reachable, False otherwise.
    """
    try:
        subprocess.run(['ping', '-c', '1', '-W', '1', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# WebSocket server callbacks
def new_client(client, server):
    logger.info('A new client is registered for NOTIFICATIONS: %s', client)

def message_received(client, server, message):
    global bridge
    if check_bridge(bridge_20_ip):
        bridge = "relyum20"
    else:
        bridge = "relyum22"

    if message == "enable-tas":
        try:   
            if bridge == "relyum20":        
                subprocess.run(['ssh', f'{bridge_20_username}@{bridge_20_ip}', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/tas.json', '-n', '1'], check=True)
            else:
                command = 'ieee8021qbv change_current_configuration PORT_1 /usr/local/src/tsn_lidar/tas.json'
                execute_ssh_commands(bridge_22_username, bridge_22_ip, command)
            response = {"command": "enable-tas",
                        "status": "button_success", 
                        "message": "Configuration applied successfully"}
        except subprocess.CalledProcessError as e:
            response = {"command": "enable-tas",
                        "status": "button_error", 
                        "message": f"Error executing command: {e}"}
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)

    elif message == "enable-negative":
        try:           
            # subprocess.run(['ssh',  f'{traffic_generator_username}@{traffic_generator_ip}', '-t' ,'python3', 'stop_traf_gen.py', '--port', '0'], check=True)
            if bridge == "relyum20":        
                subprocess.run(['ssh', f'{bridge_20_username}@{bridge_20_ip}', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/negative-tas.json', '-n', '1'], check=True)
            else:
                command = 'ieee8021qbv change_current_configuration PORT_1 /usr/local/src/tsn_lidar/negative-tas22.json'
                execute_ssh_commands(bridge_22_username, bridge_22_ip, command)

            subprocess.run(['ssh', f'{traffic_generator_username}@{traffic_generator_ip}', '-t' ,'python3', 'config_traf_gen.py', '--port', '0', '-s', '1500', '-vtag', '1', '-p', '5', '-vid', '300', '-pr', '100'], check=True)
            subprocess.run(['ssh', f'{traffic_generator_username}@{traffic_generator_ip}', '-t' ,'python3', 'start_traf_gen.py', '--port', '0'], check=True)
            response = {"command": "enable-negative",
                        "status": "button_success", 
                        "message": "Configuration applied successfully"}
        except subprocess.CalledProcessError as e:
            response = {"command": "enable-negative",
                        "status": "button_error", 
                        "message": f"Error executing command: {e}"}
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)

    elif message == "disable-negative":
        try:           
            subprocess.run(['ssh', f'{traffic_generator_username}@{traffic_generator_ip}', '-t' ,'python3', 'stop_traf_gen.py', '--port', '0'], check=True)
            if bridge == "relyum20":        
                subprocess.run(['ssh', f'{bridge_20_username}@{bridge_20_ip}', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/disable-tas.json', '-n', '1'], check=True)
            else: 
                command = 'ieee8021qbv change_current_configuration PORT_1 /usr/local/src/tsn_lidar/disable-tas22.json'
                execute_ssh_commands(bridge_22_username, bridge_22_ip, command)
            response = {"command": "disable-negative",
                        "status": "button_success", 
                        "message": "Configuration applied successfully"}
        except subprocess.CalledProcessError as e:
            response = {"command": "disable-negative",
                        "status": "button_error", 
                        "message": f"Error executing command: {e}"}
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)
    elif message == "stop-lidar":
        try:     
            if bridge == "relyum20":        
                subprocess.run(['ssh', f'{bridge_20_username}@{bridge_20_ip}', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/stop-lidar.json', '-n', '1'], check=True)
            else: 
                command = 'ieee8021qbv change_current_configuration PORT_1 /usr/local/src/tsn_lidar/stop-lidar22.json'
                execute_ssh_commands(bridge_22_username, bridge_22_ip, command)
            response = {"command": "stop-lidar",
                        "status": "button_success", 
                        "message": "Configuration applied successfully"}
        except subprocess.CalledProcessError as e:
            response = {"command": "stop-lidar",
                        "status": "button_error", 
                        "message": f"Error executing command: {e}"}
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)

    elif message == "disable-tas":
        try:    
            if bridge == "relyum20":        
                subprocess.run(['ssh', f'{bridge_20_username}@{bridge_20_ip}', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/disable-tas.json', '-n', '1'], check=True)
            else: 
                command = 'ieee8021qbv change_current_configuration PORT_1 /usr/local/src/tsn_lidar/disable-tas22.json'
                execute_ssh_commands(bridge_22_username, bridge_22_ip, command)
            
            response = {"command": "disable-tas",
                        "status": "button_success", 
                        "message": "Configuration applied successfully"}
        except subprocess.CalledProcessError as e:
            response = {"command": "disable-tas",
                        "status": "button_error", 
                        "message": f"Error executing command: {e}"}
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)

    elif message == "enable-noise":
        try:          
            subprocess.run(['ssh', f'{traffic_generator_username}@{traffic_generator_ip}', '-t' ,'python3', 'start_traf_gen.py', '--port', '0'], check=True)
            response = {"command": "enable-noise",
                        "status": "button_success", 
                        "message": "Configuration applied successfully"}
        except subprocess.CalledProcessError as e:
            response = {"command": "enable-noise",
                        "status": "button_error", 
                        "message": f"Error executing command: {e}"}
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)
    elif message == "disable-noise":
        try:           
            subprocess.run(['ssh', f'{traffic_generator_username}@{traffic_generator_ip}', '-t' ,'python3', 'stop_traf_gen.py', '--port', '0'], check=True)
            response = {"command": "disable-noise",
                        "status": "button_success", 
                        "message": "Configuration applied successfully"}
        except subprocess.CalledProcessError as e:
            response = {"command": "disable-noise",
                        "status": "button_error", 
                        "message": f"Error executing command: {e}"}
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)
    elif message == "reset-tas":
        try:  
            if bridge == "relyum20":        
                subprocess.run(['ssh', f'{bridge_20_username}@{bridge_20_ip}', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/lidar_tas.json', '-n', '1'], check=True)
            else: 
                command = 'ieee8021qbv change_current_configuration PORT_1 /usr/local/src/tsn_lidar/lidar_tas22.json'
                execute_ssh_commands(bridge_22_username, bridge_22_ip, command)
            response = {"command": "reset-tas",
                        "status": "button_success", 
                        "message": "Configuration applied successfully"}
        except subprocess.CalledProcessError as e:
            response = {"command": "reset-tas",
                        "status": "button_error", 
                        "message": f"Error executing command: {e}"}
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)

    elif "qbv_gate_parameters" in message:
        bridge = "relyum20"

        with open("tas.json", "w") as outfile:
            outfile.write(message)
        try:
            # scp sample.json relyum@192.168.4.64:/usr/local/src/tsn_lidar
            subprocess.run(['scp', 'tas.json', f'{bridge_20_username}@{bridge_20_ip}:/usr/local/src/tsn_lidar'], check=True, timeout=7)
            response = {"command": "qbv_gate_parameters",
                        "status": "success", 
                        "message": "Configuration applied successfully"}
        except subprocess.TimeoutExpired:
            response = {"command": "qbv_gate_parameters",
                        "status": "timeout", 
                        "message": "Connection to hardware timed out"}
        except subprocess.CalledProcessError as e:
            response = {"command": "qbv_gate_parameters",
                        "status": "error", 
                        "message": f"Error executing command: {e}"}
        
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)
    
    elif "gateEnabled" in message:
        bridge = "relyum22"
        with open("tas.json", "w") as outfile:
            outfile.write(message)
        try:
            # scp sample.json relyum@192.168.4.64:/usr/local/src/tsn_lidar
            subprocess.run(['scp', 'tas.json', f'{bridge_22_username}@{bridge_22_ip}:/usr/local/src/tsn_lidar'], check=True, timeout=7)
            response = {"command": "gateEnabled",
                        "status": "success", 
                        "message": "Configuration applied successfully"}
        except subprocess.TimeoutExpired:
            response = {"command": "gateEnabled",
                        "status": "timeout", 
                        "message": "Connection to hardware timed out"}
        except subprocess.CalledProcessError as e:
            response = {"command": "gateEnabled",
                        "status": "error", 
                        "message": f"Error executing command: {e}"}
        
        response_json = json.dumps(response)
        server.send_message_to_all(response_json)

    elif "--frame_size" in message:
        # print("Noise message: ", message.split(' '))
        try:          
            tmp = ['ssh', f'{traffic_generator_username}@{traffic_generator_ip}', '-t' ,'python3', 'config_traf_gen.py', '--port', '0', '-vtag', '1', '-vid', '300']
            tmp.extend(message.split(' '))
            subprocess.run(tmp, check=True, timeout=7)
            response = {"command": "--frame_size",
                        "status": "success", 
                        "message": "Configuration applied successfully"}
        except subprocess.TimeoutExpired:
            response = {"command": "--frame_size",
                        "status": "timeout", 
                        "message": "Connection to hardware timed out"}
        except subprocess.CalledProcessError as e:
            response = {"command": "--frame_size",
                        "status": "error", 
                        "message": f"Error executing command: {e}"}

        response_json = json.dumps(response)
        server.send_message_to_all(response_json)
            
    else:
        logger.info('NOTIFICATION {} received from {}'.format(message, client))


def client_left(client, server):
    logger.info('Client left: {0}'.format(client))

server_notif = WebsocketServer(host=host, port=port, loglevel=logging.INFO)
server_notif.set_fn_new_client(new_client)
server_notif.set_fn_message_received(message_received)
server_notif.set_fn_client_left(client_left)
logger.info('The WebSocket server (NOTIFICATIONS) is up and running...')

# Run WebSocket server
server_notif.run_forever()
