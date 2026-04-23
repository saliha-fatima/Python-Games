import socket
import pygame
import random
import threading

# Server-side code (to be run separately)
def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)
    server_socket.listen(5)

    print("Server started. Waiting for connections...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    player2_x, player2_y = 500, 100

    while True:
        try:
            # Receive player 1 position from the client
            data = client_socket.recv(1024)
            if data:
                player1_x, player1_y = eval(data.decode())

                # Simulate random movement for player 2
                player2_x += random.randint(-5, 5)
                player2_y += random.randint(-5, 5)

                # Boundary restrictions for player 2
                player2_x = max(0, min(player2_x, 640 - 50))  # Keep player 2 within screen width
                player2_y = max(0, min(player2_y, 480 - 50))  # Keep player 2 within screen height

                # Send player 2 position back to client
                client_socket.send(str((player2_x, player2_y)).encode())
        except Exception as e:
            print(f"Server error: {e}")
            break

    client_socket.close()
    server_socket.close()
    print("Server closed.")

# Client-side code (the main game)
def client_game():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8080)
    client_socket.connect(server_address)
    client_socket.settimeout(1.0)

    print("Connected to server. Waiting for game to start...")

    # Initialize Pygame
    pygame.init()

    # Set up the game screen
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set up the game title
    pygame.display.set_caption("Online Multiplayer Game")

    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Define player properties
    player_size = 50
    player_speed = 5

    # Define player positions
    player1_x, player1_y = 100, 100
    player2_x, player2_y = 500, 100

    # Define player scores
    player1_score = 0
    player2_score = 0

    # Game loop
    clock = pygame.time.Clock()
    game_over = False
    running = True  # Flag to indicate if the game is running

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit if the window is closed
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Quit if ESC key is pressed
                running = False

        # Get user input for player 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player1_y -= player_speed
        if keys[pygame.K_DOWN]:
            player1_y += player_speed
        if keys[pygame.K_LEFT]:
            player1_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player1_x += player_speed

        # Boundary restrictions for player 1
        player1_x = max(0, min(player1_x, screen_width - player_size))  # Keep player 1 within screen width
        player1_y = max(0, min(player1_y, screen_height - player_size))  # Keep player 1 within screen height

        # Send player 1's position to the server
        try:
            client_socket.send(str((player1_x, player1_y)).encode())
        except socket.error as e:
            print(f"Error sending data: {e}")
            running = False
            break

        # Receive player 2's position from the server
        try:
            data = client_socket.recv(1024)
            if data:
                player2_x, player2_y = eval(data.decode())
        except socket.timeout:
            pass
        except ConnectionAbortedError as e:
            print(f"Error: Connection aborted ({e})")
            running = False
            break

        # Check for collision between players
        if (player1_x < player2_x + player_size and player1_x + player_size > player2_x and
                player1_y < player2_y + player_size and player1_y + player_size > player2_y):
            game_over = True
            winner = 'Player 1' if player1_x > player2_x else 'Player 2'

        # Update scores if the game is over
        if game_over:
            if winner == 'Player 1':
                player1_score += 1
            else:
                player2_score += 1
            game_over = False

        # Render the game screen
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (player1_x, player1_y, player_size, player_size))
        pygame.draw.rect(screen, BLACK, (player2_x, player2_y, player_size, player_size))

        # Display the score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Player 1: {player1_score} | Player 2: {player2_score}", True, BLACK)
        screen.blit(text, (10, 10))

        if game_over:
            game_over_text = font.render(f"Game Over! {winner} Wins!", True, BLACK)
            screen.blit(game_over_text, (200, 200))

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Close Pygame and client socket when the loop ends
    pygame.quit()
    client_socket.close()
    print("Game closed.")

# Run the server in a separate thread
server_thread = threading.Thread(target=server)
server_thread.start()

# Start the game (client)
client_game()
