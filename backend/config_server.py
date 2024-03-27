import logging
import json
import socket
import math
from threading import Thread
from websocket_server import WebsocketServer
import subprocess

udp_host = '192.168.4.102'
udp_port = 6699
host = '10.150.2.48'
port = 7000

# Initialize logger for notifications
logger = logging.getLogger('mylogger-notif')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./logs/dgsec_sockets_notifications.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)   

# WebSocket server callbacks
def new_client(client, server):
    logger.info('A new client is registered for NOTIFICATIONS: %s', client)

def message_received(client, server, message):
    if message == "enable-tas":
        try:           
            subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/tas.json', '-n', '1'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    elif message == "enable-negative":
        try:           
            subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'stop_traf_gen.py', '--port', '0'], check=True)
            subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/negative-tas.json', '-n', '1'], check=True)
            subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'config_traf_gen.py', '--port', '0', '-s', '1500', '-vtag', '1', '-p', '5', '-vid', '300', '-pr', '100'], check=True)
            subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'start_traf_gen.py', '--port', '0'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    elif message == "disable-negative":
        try:           
            subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'stop_traf_gen.py', '--port', '0'], check=True)
            subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/disable-tas.json', '-n', '1'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    elif message == "disable-tas":
        try:           
            subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/disable-tas.json', '-n', '1'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    elif message == "enable-noise":
        try:          
            # subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'config_traf_gen.py', '--port', '0', '-s', '1500', '-vtag', '1', '-p', '5', '-vid', '300', '-pr', '100'], check=True)
            subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'start_traf_gen.py', '--port', '0'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    elif message == "disable-noise":
        try:           
            subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'stop_traf_gen.py', '--port', '0'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    elif message == "reset-tas":
        try:           
            subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/lidar_tas.json', '-n', '1'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

    elif "qbv_gate_parameters" in message:
        with open("tas.json", "w") as outfile:
            outfile.write(message)
        try:
            # scp sample.json relyum@192.168.4.64:/usr/local/src/tsn_lidar
            subprocess.run(['scp', 'tas.json', 'relyum@192.168.4.64:/usr/local/src/tsn_lidar'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
    elif "--frame_size" in message:
        # print("Noise message: ", message.split(' '))
        try:          
            tmp = ['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'config_traf_gen.py', '--port', '0', '-vtag', '1', '-vid', '300']
            tmp.extend(message.split(' '))
            subprocess.run(tmp, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            
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
