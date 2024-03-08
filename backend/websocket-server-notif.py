import logging
import json
import uuid
from websocket_server import WebsocketServer
from decouple import config

host = '192.168.4.102'
port = 6699

logger = logging.getLogger('mylogger-notif')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./logs/dgsec_sockets_notifications.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# When a client connects to the server
# Generate a unique ID and store this ID with the client type [1= REQ LUX, 2= AUTH LUX]
def new_client(client, clients):
    logger.info('A new client is registered for NOTIFICATIONS: %s', client)
    id_msg = {
        "type": "id_client",
        "id": client['id'],
        "addr": client['address'][0],
        "port": client['address'][1]
    }
    clients.send_message(client=client, msg=json.dumps(id_msg))


def message_received(client, server, message):
    logger.info('NOTIFICATION {} received from {}'.format(message, client))
    for c in server.clients:
        # print(p)
        if c['id'] != client['id']:
            server.send_message(client=c, msg=message)
            logger.info('send NOTIFICATION message %s to client %s', message, c)
        else:
            logger.info("client is the same that the receiver, so no message broadcast to him!")


def client_left(client, server):
    server.clients.remove(client)
    logger.info('Client left: {0}'.format(client))


server_notif = WebsocketServer(host=host, port=port, loglevel=logging.INFO)
server_notif.set_fn_new_client(new_client)
server_notif.set_fn_message_received(message_received)
server_notif.set_fn_client_left(client_left)
logger.info('the websocket server (NOTIFICATIONS) is up and running...')
server_notif.run_forever()
