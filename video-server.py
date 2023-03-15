import cv2
import socket
import pickle
import struct

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
# host_ip = socket.gethostbyname(host_name)
host_ip = '10.203.178.120'
print('Host IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

# Bind the socket to a public host and a port
server_socket.bind(socket_address)

# Listen for incoming connections
server_socket.listen(5)

print('Waiting for client...')
while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Client connected:', client_address)

    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Set the video dimensions
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Send the video dimensions to the client
    client_socket.send(struct.pack("I", frame_width))
    client_socket.send(struct.pack("I", frame_height))

    # Start streaming the video
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        frame_resize = cv2.resize(frame, (640,360))

        # Convert the frame to a byte string
        data = pickle.dumps(frame_resize)

        # Send the frame size to the client
        client_socket.send(struct.pack("I", len(data)))

        # Send the frame to the client
        client_socket.send(data)
