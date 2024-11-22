import pygame
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Activity Manager")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 150, 255)

# Fonts
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 28)

# Paths
USERS_DIR = "users"
os.makedirs(USERS_DIR, exist_ok=True)


# Helper functions for JSON handling
def load_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open(file_path, "w") as file:
            json.dump([], file)
        return []


def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def user_exists(username):
    return os.path.exists(os.path.join(USERS_DIR, username))


def create_user(username, password):
    user_dir = os.path.join(USERS_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    with open(os.path.join(user_dir, "password.json"), "w") as file:
        json.dump({"password": password}, file)
    for file in ["activities.json", "events.json", "budget.json"]:
        with open(os.path.join(user_dir, file), "w") as f:
            json.dump([], f)


def authenticate_user(username, password):
    if not user_exists(username):
        return False
    with open(os.path.join(USERS_DIR, username, "password.json"), "r") as file:
        data = json.load(file)
        return data.get("password") == password


# Draw text helper
def draw_text(text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))
    if center:
        text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Input box class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = FONT.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = BLUE if self.active else GRAY
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.txt_surface = FONT.render(self.text, True, BLACK)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

    def clear(self):
        self.text = ""
        self.txt_surface = FONT.render(self.text, True, BLACK)


# Main loop
def main():
    clock = pygame.time.Clock()
    input_username = InputBox(300, 200, 200, 40)
    input_password = InputBox(300, 260, 200, 40)
    active_screen = "login"
    message = ""
    current_user = None

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            input_username.handle_event(event)
            input_password.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if active_screen == "login":
                    username = input_username.text
                    password = input_password.text
                    if authenticate_user(username, password):
                        message = "Login successful!"
                        current_user = username
                        active_screen = "dashboard"
                    else:
                        message = "Invalid username or password."
                elif active_screen == "signup":
                    username = input_username.text
                    password = input_password.text
                    if not username or not password:
                        message = "Fields cannot be empty!"
                    elif user_exists(username):
                        message = "User already exists!"
                    else:
                        create_user(username, password)
                        message = "Account created! Log in now."
                        active_screen = "login"

        if active_screen == "login":
            draw_text("Login", FONT, BLACK, WIDTH // 2, 100, center=True)
            input_username.draw(screen)
            input_password.draw(screen)
            draw_text("Press Enter to Login", SMALL_FONT, BLACK, WIDTH // 2, 320, center=True)
            draw_text(message, SMALL_FONT, BLACK, WIDTH // 2, 360, center=True)
        elif active_screen == "signup":
            draw_text("Sign Up", FONT, BLACK, WIDTH // 2, 100, center=True)
            input_username.draw(screen)
            input_password.draw(screen)
            draw_text("Press Enter to Sign Up", SMALL_FONT, BLACK, WIDTH // 2, 320, center=True)
            draw_text(message, SMALL_FONT, BLACK, WIDTH // 2, 360, center=True)
        elif active_screen == "dashboard":
            draw_text(f"Welcome, {current_user}!", FONT, BLACK, WIDTH // 2, HEIGHT // 2, center=True)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
