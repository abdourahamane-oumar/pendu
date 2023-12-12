import pygame
import sys
from button import Button
import random

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/image/Background.png")

keys = pygame.key.get_pressed()

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
remaining_attempts = 6
correct_letters = []
selected_letters = []
incorrect_letters = []
secret_word = ""
keys = pygame.key.get_pressed()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = police(100).render("LE PENDU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/image/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=police(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/image/insere Rect.png"), pos=(640, 400), 
                            text_input="INSERER", font=police(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/image/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=police(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    inserer()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def inserer():
    new_word = ""
    input_active = False
    input_rect = pygame.Rect(500, 350, 300, 50)
    input_color = pygame.Color('lightskyblue3')
    font = pygame.font.Font(None, 36)

    OPTIONS_BACK = Button(image=None, pos=(640, 460),
                          text_input="BACK", font=police(75), base_color="Black", hovering_color="Green")
    OPTIONS_SAVE = Button(image=None, pos=(640, 550),
                          text_input="SAVE", font=police(75), base_color="Black", hovering_color="Green")

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = police(25).render("Insérer un nouveau mot dans la liste!", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                elif OPTIONS_SAVE.checkForInput(OPTIONS_MOUSE_POS):
                    if new_word:
                        with open("mots.txt", "a") as file:
                            file.write(new_word + "\n")
                            print(f"Mot ajouté : {new_word}")
                        new_word = ''  # Réinitialiser le mot après l'enregistrement

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    new_word = new_word[:-1]
                else:
                    new_word += event.unicode

        pygame.draw.rect(SCREEN, input_color, input_rect, 2)
        text_surface = font.render(new_word, True, (0, 0, 0))
        width = max(200, text_surface.get_width() + 10)
        input_rect.w = width
        SCREEN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        OPTIONS_SAVE.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_SAVE.update(SCREEN)

        pygame.display.update()

def play():
    global remaining_attempts, correct_letters, incorrect_letters, selected_letters, secret_word

    réglage_inserer()
    PLAY_BACK = Button(image=None, pos=(640, 550),
                      text_input="BACK", font=police(75), base_color="White", hovering_color="Green")

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        # Vérifier si une touche du clavier est pressée
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_a, pygame.K_z + 1):
                    letter = chr(event.key)
                    if letter not in selected_letters:
                        selected_letters.append(letter)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        # Afficher les images du pendu
        pendu_images = [pygame.image.load(f"assets/image/{i}.png") for i in range(7)]
        print(remaining_attempts)
        print(len(pendu_images))

        # Vérifier si le joueur a gagné ou perdu
        if set(correct_letters) == set(secret_word):
            win_image = pygame.image.load("assets/image/win.png")
            SCREEN.blit(win_image, (50, 10))
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

        if 0 <= (7 - remaining_attempts) < len(pendu_images):
            current_pendu_image = pendu_images[7 - remaining_attempts]
            fail_image = pygame.image.load("assets/image/fail.png")
            SCREEN.blit(current_pendu_image, (50, 50))
            PLAY_BACK.changeColor(PLAY_MOUSE_POS)
            PLAY_BACK.update(SCREEN)

    
        # Afficher les lettres de l'alphabet
        letter_font = police(35)
        for i, letter in enumerate(alphabet):
            x = 50 + i * 50
            y = 500
            letter_text = letter_font.render(letter, True, "black")
            letter_rect = letter_text.get_rect(center=(x, y))

        # Vérifier si la lettre est correcte
        for letter in selected_letters:
            if letter in secret_word:
                correct_letters.append(letter)
                selected_letters.remove(letter)
            elif letter not in incorrect_letters:
                incorrect_letters.append(letter)
                remaining_attempts -= 1

        # Afficher le mot caché avec toutes les lettres correctes
        hidden_word = "".join([letter if letter in correct_letters else "_" for letter in secret_word])
        WORD_TEXT = police(45).render(hidden_word, True, "black")
        WORD_RECT = WORD_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(WORD_TEXT, (640 - WORD_RECT.width // 2, 260))

        # Afficher les lettres incorrectes
        incorrect_text = police(25).render("Lettre incorrect: {remaining_attempts} " + " ".join(incorrect_letters), True, "black")
        incorrect_rect = incorrect_text.get_rect(center=(640, 400))
        SCREEN.blit(incorrect_text, incorrect_rect)

        # Afficher le nombre d'essais restants
        ATTEMPTS_TEXT = police(25).render(f"Essai: {remaining_attempts}", True, "black")
        ATTEMPTS_RECT = ATTEMPTS_TEXT.get_rect(center=(640, 450))
        SCREEN.blit(ATTEMPTS_TEXT, ATTEMPTS_RECT)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        pygame.display.update()

def police(size):
    return pygame.font.Font("assets/image/font.ttf", size)

def réglage_play():

    with open("mots.txt", "r") as file:
        words = file.read().splitlines()

    chosen_word = random.choice(words)
    print("Chosen secret word:", chosen_word)  
    return chosen_word

def réglage_inserer():
    global remaining_attempts, correct_letters, selected_letters, secret_word

    remaining_attempts = 7
    correct_letters = []
    selected_letters = []
    secret_word = réglage_play()

main_menu()