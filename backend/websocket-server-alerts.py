import logging
import json
from websocket_server import WebsocketServer
from decouple import config

# host = config("HOSTNAME")
# port = int(config("PORT_ALERT"))
host = '192.168.4.102'
port = 6699

logger = logging.getLogger('mylogger-alerts')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./logs/dgsec_sockets_alerts.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def new_client_for_alert(client, clients):
    logger.info('A new client is registered for ALERTS: %s', client)
    id_msg = {
        "type": "id_client",
        "id": client['id'],
        "addr": client['address'][0],
        "port": client['address'][1]
    }
    clients.send_message(client=client, msg=json.dumps(id_msg))


def alert_received(client, server, message):
    logger.info('ALERT {} received from {}'.format(message, client))
    for c in server.clients:
        if c['id'] != client['id']:
            server.send_message(client=c, msg=message)
            logger.info('send ALERT message %s to client %s', message, c)
        else:
            logger.info("client is the same that the receiver, so no message broadcast to him!")


def client_for_alert_left(client, server):
    server.clients.remove(client)
    logger.info('Client left: {0}'.format(client))


server_alert = WebsocketServer(host=host, port=port, loglevel=logging.INFO)
server_alert.set_fn_new_client(new_client_for_alert)
server_alert.set_fn_message_received(alert_received)
server_alert.set_fn_client_left(client_for_alert_left)
logger.info('the websocket server (ALERTS) is up and running...')
server_alert.run_forever()
