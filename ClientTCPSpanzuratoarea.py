import socket

def main():
    host = "127.0.0.1"  # Adresa IP a serverului
    port = 12345  # Portul pe care serverul ascultă

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Welcome to Hangman game by Dobra Stefania-Irina")
    name = input("Enter your name: ")
    client_socket.send(name.encode()
    )
    response = client_socket.recv(1024).decode()
    print(response)

    while True:
        data = client_socket.recv(1024).decode()
        if "hanged" in data or "Congratulations" in data:
            print(data)
            break

        print(data)

        guess = input("Enter your guess: ")
        client_socket.send(guess.encode())

    client_socket.close()

if __name__ == '__main__':
    main()
