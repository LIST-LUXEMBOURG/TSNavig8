'''
  © 2024 - Luxembourg Institute of Science and Technology. All Rights Reserved
  This program is licensed under AGPL V3.0 License -  https://www.gnu.org/licenses/agpl-3.0.txt 
'''
import time
import psutil
import json
import logging
from threading import Thread
from websocket_server import WebsocketServer
from decouple import config

host = config('THROUGHPUT_SERVER_HOST')
port = config('THROUGHPUT_SERVER_PORT', cast=int)
eth_interface = config('THROUGHPUT_SERVER_ETH_INTERFACE')
vlan_eth_interface = config('THROUGHPUT_SERVER_VLAN_ETH_INTERFACE')
logger = logging.getLogger('mylogger-notif')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./logs/dgsec_sockets_notifications.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

server_notif = WebsocketServer(host=host, port=port, loglevel=logging.INFO)

def new_client(client, server):
    logger.info('A new client is registered for NOTIFICATIONS: %s', client)
    id_msg = {
        "type": "id_client",
        "id": client['id'],
        "addr": client['address'][0],
        "port": client['address'][1]
    }
    server.send_message_to_all(json.dumps(id_msg))

def update_data_and_send():
    global last_200, last_all
    my_net = psutil.net_io_counters(pernic=True)

    bytes_200 = my_net[vlan_eth_interface].bytes_recv
    bytes_all = my_net[eth_interface].bytes_recv

    new_200 = (bytes_200 - last_200) / 125000
    new_all = (bytes_all - last_all) / 125000

    data = {
        "type": "bandwidth_update",
        "last_200": new_200,
        "last_all": new_all
    }

    server_notif.send_message_to_all(json.dumps(data))

    last_200 = bytes_200
    last_all = bytes_all

def client_left(client, server):
    logger.info('Client left: {0}'.format(client))

server_notif.set_fn_new_client(new_client)
server_notif.set_fn_client_left(client_left)
logger.info('the websocket server (NOTIFICATIONS) is up and running...')

# Start the websocket server in a separate thread
server_thread = Thread(target=server_notif.run_forever)
server_thread.daemon = True
server_thread.start()

# Your existing code for updating bandwidth data
timestamps = []
mb_200 = []
mb_all = []

net = psutil.net_io_counters(pernic=True)

last_200 = net[vlan_eth_interface].bytes_recv
last_all = net[eth_interface].bytes_recv

while True:
    update_data_and_send()
    time.sleep(1)  # Adjust the interval as needed
