import socket
import random
import time

def main():
    host = "127.0.0.1"  # Adresa IP a serverului
    port = 12345  # Portul pe care serverul va asculta

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Serverul ascultă pe {host}:{port}")

    conn, addr = server_socket.accept()
    print(f"Conectat la {addr[0]}:{addr[1]}")

    print("Welcome to Hangman game by Dobra Stefania-Irina")
    name = conn.recv(1024).decode()
    conn.send(f"Hello {name}! Best of Luck!".encode())

    time.sleep(2)
    conn.send("The game is about to start!\nLet's play Hangman!".encode())
    time.sleep(3)

    words_to_guess = ["january", "border", "image", "film", "promise", "kids", "lungs", "doll", "rhyme", "damage", "plants"]
    word = random.choice(words_to_guess)
    length = len(word)
    count = 0
    display = '_' * length
    already_guessed = []

    while count < 5 and display != word:
        conn.send(f"{display} ({length} characters)\n".encode())

        correct_guess = False
        while not correct_guess:
            guess = conn.recv(1024).decode().strip()
            if len(guess) != 1 or not guess.isalpha():
                conn.send("Invalid Input, Try a letter".encode())
            elif guess in already_guessed:
                conn.send("Try another letter.".encode())
            else:
                break

        if guess in word:
            already_guessed.extend([guess])
            indexes = [i for i, letter in enumerate(word) if letter == guess]
            for index in indexes:
                display = display[:index] + guess + display[index + 1:]
                correct_guess = True
        else:
            count += 1

        remaining_attempts = 5 - count

        if display == word:
            conn.send(f"Congratulations! You have guessed the word correctly. The word was: {word}".encode())
        elif count == 5:
            conn.send(f"Wrong guess. You are hanged! The word was: {word}".encode())
        else:
            conn.send(f"Wrong guess. {remaining_attempts} guesses remaining\n".encode())

    conn.close()
    server_socket.close()

if __name__ == '__main__':
    main()
