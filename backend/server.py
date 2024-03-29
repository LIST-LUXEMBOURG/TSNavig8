import logging
import json
import socket
import base64
import math
import datetime
from threading import Thread
from websocket_server import WebsocketServer
import subprocess
# Constants for header and data block sizes
HEADER_SIZE = 42
DATA_BLOCK_SIZE = 100
NUMBER_OF_BLOCKS = 12
TAIL_SIZE = 6
udp_host = '192.168.4.102'
udp_port = 6699
host = '10.150.2.48'
port = 8765
current_timestamp = -1
# Mapping of channel numbers to vertical angles
channel_vertical_angles = {
    16: 10, 32: 7, 14: 5, 30: 3.5, 31: 3, 7: 2.5, 12: 2, 23: 1.5,
    15: 1, 28: 0.5, 29: 0, 5: -0.5, 10: -1, 21: -1.5, 13: -2, 26: -2.5,
    27: -3, 3: -3.5, 8: -4, 19: -4.5, 11: -5, 24: -5.5, 25: -6, 1: -6.5,
    6: -7, 9: -8, 22: -9, 4: -10, 17: -11, 20: -12, 2: -13.5, 18: -16
}

# Initialize logger for notifications
logger = logging.getLogger('mylogger-notif')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('./logs/dgsec_sockets_notifications.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def parse_header(data):
    # Ensure the buffer size is correct
    if len(data) < HEADER_SIZE:
        raise ValueError("Incomplete header data")

    # Initialize an index for iterating through the data
    index = 0

    # Extract individual fields based on their lengths
    header_id = int.from_bytes(data[index:index+4], 'big')
    index += 4

    protocol_version = int.from_bytes(data[index:index+2], 'big')
    index += 2

    # Skipping 2 bytes for Resv
    index += 2

    top_board_count = int.from_bytes(data[index:index+4], 'big')
    index += 4

    bottom_board_count = int.from_bytes(data[index:index+4], 'big')
    index += 4

    # Skipping 1 byte for Resv
    index += 1

    range_resolution = data[index]  
    index += 1

    angle_pulse_interval = int.from_bytes(data[index:index+2], 'big')
    index += 2

    # Timestamp field
    # Interpret first 6 bytes as seconds
    seconds = int.from_bytes(data[index:index+6], 'big')

    # Interpret last 4 bytes as microseconds 
    microseconds = int.from_bytes(data[index+6:index+10], 'big')
    index += 10

    # Skipping 1 byte for Resv
    index += 1

    lidar_type = data[index]
    index += 1

    lidar_model = data[index]
    index += 1

    # Skipping 9 bytes for Resv
    index += 9

    # Create a dictionary with extracted header fields
    header_dict = {
        'Header ID': header_id,
        'Protocol Version': protocol_version,
        'Top Board Sending Packet Count': top_board_count,
        'Bottom Board Sending Packet Count': bottom_board_count,
        'Range Resolution': range_resolution,
        'Angle Pulse Interval Count': angle_pulse_interval,
        'Seconds': seconds,
        'Microseconds': microseconds,
        'LiDAR Type': lidar_type,
        'LiDAR Model': lidar_model,
    }
    
    return header_dict
def convert_distance(data_bytes):
    # Step 1: Convert distance value to a hexadecimal number
    hex_value = ''.join(format(byte, '02x') for byte in data_bytes)

    # Step 2: Convert to a 16-bit unsigned integer
    distance_decimal = int(hex_value, 16)

    # Step 3: Calculate according to the distances resolution (x0.25)
    distance_in_meters = distance_decimal * 0.25

    return distance_in_meters
    
def parse_data_blocks(data_blocks):
    parsed_blocks = []

    
    for i in range(0, len(data_blocks), 100):
        data_block = data_blocks[i:i + 100]
        # Ensure the buffer size is correct for each data block
        if len(data_block) < 100:
            print("Incomplete data block, skipping...")
            continue

        # Parse the 2-byte flag (Oxffee)
        flag = hex(int.from_bytes(data_block[0:2],'big')) #This has to be 0xffee
        #print(flag)
        # Parse the 2-byte azimuth value
        azimuth_dec = int.from_bytes(data_block[2:4],'big')
        azimuth_decimal = azimuth_dec / 100.0


        # Parse the 32 sets of 3-byte channel data
        channel_data = []
      
        for j in range(4, 100, 3):
            # Convert distance values using the new function
            distance_bytes = data_block[j:j+2]

            distance = convert_distance(distance_bytes)

            reflectivity = int.from_bytes(data_block[j+2:j+3], 'big')

            channel_data.append((distance, reflectivity))

        # Create a dictionary with extracted data block fields
        data_block_dict = {
            'Flag': flag,
            'Azimuth': azimuth_decimal,
            'Channel Data': channel_data,
        }

        parsed_blocks.append(data_block_dict)

    return parsed_blocks
def parse_udp_packet(data):
    global current_timestamp
    # Split the UDP packet into header, data blocks, and tail
    header_data = data[:HEADER_SIZE]
    data_block_data = data[HEADER_SIZE:-TAIL_SIZE]
    tail_data = data[-TAIL_SIZE:]

    # Parse header and data blocks
    header = parse_header(header_data)
    
    current_timestamp = header['Seconds'] + (header['Microseconds']/1000000)
    
    data_blocks = parse_data_blocks(data_block_data)

    return {'Header': header, 'Data Blocks': data_blocks, 'Tail': tail_data}
def convert_data_blocks_to_point_cloud(data_blocks):
    global channel_vertical_angles
    
    point_cloud = []

    for data_block in data_blocks:
        azimuth = math.radians(data_block['Azimuth'])  # Convert azimuth to radians
        channel_data = data_block['Channel Data']
        for j in range(len(channel_data)):
            distance, reflectivity = channel_data[j]
            channel_number = j + 1 
            vertical_angle =  channel_vertical_angles.get(channel_number, None)
            # print(vertical_angle)
            # Convert polar coordinates to Cartesian coordinates
            x = distance * math.cos(math.radians(vertical_angle)) * math.sin(azimuth)
            y = distance * math.cos(math.radians(vertical_angle)) * math.cos(azimuth)
            z = distance * math.sin(math.radians(vertical_angle))
            point_cloud.append([x, y, z, distance])
    return point_cloud

# UDP listener function
def start_udp_listener(udp_host, udp_port, logger, server_notif):
    global current_timestamp
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((udp_host, udp_port))
            logger.info(f"UDP server listening on {udp_host}:{udp_port}")
            sequence_cloud=[]
            start_time = current_timestamp
            threshold_time=0.1
            while True:
                data, addr = s.recvfrom(HEADER_SIZE + (DATA_BLOCK_SIZE * NUMBER_OF_BLOCKS) + TAIL_SIZE)  # Adjust buffer size as needed

                try:
                    lidar_data = parse_udp_packet(data)
                    point_cloud = convert_data_blocks_to_point_cloud(lidar_data['Data Blocks'])
                    sequence_cloud.extend(point_cloud)
                    elapsed_time = current_timestamp-start_time
                    if elapsed_time>=threshold_time:
                        # print(elapsed_time)
                    # Convert point cloud to JSON
                        json_point_cloud = json.dumps(sequence_cloud)
                        start_time=current_timestamp
                        sequence_cloud=[]

                        # Send UDP data as a notification to all connected clients
                        notification = {
                            "type": "udp_notification",
                            "point_cloud": json_point_cloud,
                            "addr": addr[0],
                            "port": addr[1]
                        }
                        # time.sleep(1)
                        # print(datetime.datetime.now().time())
                        server_notif.send_message_to_all(json.dumps(notification))

                except Exception as e:
                    logger.error(f"Error processing UDP data: {e}")

    except Exception as e:
        logger.error(f"Error in UDP listener: {e}")
        

# WebSocket server callbacks
def new_client(client, server):
    logger.info('A new client is registered for NOTIFICATIONS: %s', client)

# def message_received(client, server, message):
    # if message == "enable-tas":
    #     try:           
    #         subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/tas.json', '-n', '1'], check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
    # elif message == "config-tas":
    #     try:           
    #         subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/mtsn_demo/configs/test2-tas.json', '-n', '1'], check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
    # elif message == "enable-negative":
    #     try:           
    #         # subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/mtsn_demo/configs/test1-tas.json', '-n', '1'], check=True)

    #         subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/negative-tas.json', '-n', '1'], check=True)
    #         subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'config_traf_gen.py', '--port', '0', '-s', '1500', '-vtag', '1', '-p', '5', '-vid', '300', '-pr', '100'], check=True)
    #         subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'start_traf_gen.py', '--port', '0'], check=True)

    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
    # elif message == "disable-negative":
    #     try:           
    #         subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'stop_traf_gen.py', '--port', '0'], check=True)
    #         subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/disable-tas.json', '-n', '1'], check=True)

    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
    # elif message == "disable-tas":
    #     try:           
    #         subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/disable-tas.json', '-n', '1'], check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
    # elif message == "enable-noise":
    #     try:          
    #         # subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'config_traf_gen.py', '--port', '0', '-s', '1500', '-vtag', '1', '-p', '5', '-vid', '300', '-pr', '100'], check=True)
    #         subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'start_traf_gen.py', '--port', '0'], check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
    # # python3 start_traf_gen.py --port 0
    # elif message == "disable-noise":
    #     try:           
    #         subprocess.run(['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'stop_traf_gen.py', '--port', '0'], check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
    # elif message == "reset-tas":
    #     try:           
    #         subprocess.run(['ssh', 'relyum@192.168.4.64', '-t' ,'spt_qbv_config', '-w', '/usr/local/src/tsn_lidar/lidar_tas.json', '-n', '1'], check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")

    # elif "qbv_gate_parameters" in message:
    #     with open("tas.json", "w") as outfile:
    #         outfile.write(message)
    #     try:
    #         # scp sample.json relyum@192.168.4.64:/usr/local/src/tsn_lidar
    #         subprocess.run(['scp', 'tas.json', 'relyum@192.168.4.64:/usr/local/src/tsn_lidar'], check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
    # elif "--frame_size" in message:
    #     # print("Noise message: ", message.split(' '))
    #     try:          
    #         tmp = ['ssh', 'soc-e@192.168.4.66', '-t' ,'python3', 'config_traf_gen.py', '--port', '0', '-vtag', '1', '-vid', '300']
    #         tmp.extend(message.split(' '))
    #         subprocess.run(tmp, check=True)
    #     except subprocess.CalledProcessError as e:
    #         print(f"Error executing command: {e}")
            
    # else:
    #     logger.info('NOTIFICATION {} received from {}'.format(message, client))


def client_left(client, server):
    logger.info('Client left: {0}'.format(client))
# Initialize WebSocket server
server_notif = WebsocketServer(host=host, port=port, loglevel=logging.INFO)

# Start UDP listener in a separate thread
udp_thread = Thread(target=start_udp_listener, args=(udp_host, udp_port, logger, server_notif))
udp_thread.daemon = True
udp_thread.start()

# Set WebSocket server callbacks
server_notif.set_fn_new_client(new_client)
# server_notif.set_fn_message_received(message_received)
server_notif.set_fn_client_left(client_left)



logger.info('The WebSocket server (NOTIFICATIONS) is up and running...')

# Run WebSocket server
server_notif.run_forever()