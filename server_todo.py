import json
import socket

# This class represents a single todo item
class TodoItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

# This class represents a list of TodoItems
class TodoList:
    def __init__(self):
        self.items = []

    def add_item(self, title, description):
        item = TodoItem(title, description)
        self.items.append(item)

    def complete_item(self, index):
        if (index < 0 or index >= len(self.items)):
            raise IndexError("Invalid index")
        item = self.items[index]
        item.completed = True

    def count_items(self):
        return len(self.items)
    
    def display_items(self):
        result = ""
        for i, item in enumerate(self.items):
            status = "[ ]"
            if item.completed:
                status = "[x]"
            result += f"{i}. {status} {item.title}: {item.description}\n"
        return result
    
    def total_items_completas(self):
        contador = 0
        for i, item in enumerate(self.items):
            if not item.completed:
                contador = contador + 1
        return contador

host = 'localhost'
port = 1000
#1000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

todo_list = TodoList()

# Loop forever, waiting for client commands
while True:
    # Accept a connection
    print("Waiting for connection...")
    client_socket, address = server_socket.accept()
    print(f"Connected to {address}")

    # receive operation and numbers and make calculation
    command = client_socket.recv(1024).decode()
    print(f"Received command: {command}")
    choice, data = command.split("-")
    if choice == "1":
        title, description = data.split(",")
        todo_list.add_item(title, description)
        result = "Todo added."
    elif choice == "2":
        result = todo_list.display_items()
    elif choice == "3":
        index = int(data)
        todo_list.complete_item(index)
        result = "Todo completed."
    elif choice == "4":
        #index = int(data)
        n = todo_list.total_items_completas()
        print(f" -- Completed items:" + str(n))
        result = f"Completed items." + str(n)
    else:
        result = "Invalid command."
    print("Logging: " + result)
    client_socket.send(result.encode())
    client_socket.close()
