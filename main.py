# Import all modules and libraries necessary
import openai
import pygame
import random
import sys
import time

# Import all modules from other files in the game
from images import (Image, load_image, background_image_collection, gun_image_collection,
                    logo_image_collection, button_image_collection, color_palette, fade_in_out,
                    ImageCarousel)
from responses import alive_responses, dead_responses, next_turn_responses
from sound_effects import (play_mouse_click, play_blood_splatter_sound_effect, play_revolver_sound_effect,
                           sound_effects, play_mouse_hover, sound_channels)
from text import Text

# Initialize pygame and its mixer for sound effects
pygame.init()
pygame.mixer.init()

# Create the window for the game
window_width = 1280
window_height = 720
game_window = pygame.display.set_mode((window_width, window_height))

# Create the clock for frame rate
clock = pygame.time.Clock()
FPS = 120
clock.tick(FPS)

# The game name will now appear in the window
pygame.display.set_caption("Chambers")

back_button_path, back_button_rect = load_image(
    button_image_collection["go_back_button"]["image"],
    "topleft", 975, 580)
back_button_img = Image(back_button_path, back_button_rect, True, True,
                        True, False, None)

background_path, background_rect = load_image(background_image_collection["main_menu_background"]["image"],
                                              "topleft", 0, 0)
main_menu_background = Image(background_path, background_rect, False, False,
                             False, False, None)

icon_image = pygame.image.load(logo_image_collection["chambers_icon"]["image"])
pygame.display.set_icon(icon_image)


def wait_for_spacebar():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


def wait_for_mouseclick(rect_list, image_collection):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for rect, data in zip(rect_list, image_collection.values()):
                if rect.collidepoint(mouse_x, mouse_y):
                    play_mouse_click("GUI_Interact", "mouse_click_sfx")
                    if "menu_position" in data:
                        if data["menu_position"] == 1:
                            find_num_players()
                            return
                        elif data["menu_position"] == 2:
                            instructions_menu()
                            return
                        elif data["menu_position"] == 3:
                            settings_menu()
                            return
                        elif data["menu_position"] == 4:
                            pygame.quit()
                            sys.exit()
                        else:
                            return None


def check_mouse_hover(rect_list, image_collection, played):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for rect, data in zip(rect_list, image_collection.values()):
        if rect.collidepoint(mouse_x, mouse_y):
            if not played:
                play_mouse_hover("GUI_Interact", "mouse_hover_sfx")
            return True
    return False


def back_button(back_button_rect):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if back_button_rect.collidepoint(mouse_x, mouse_y):
                play_mouse_click("GUI_Interact", "mouse_click_sfx")
                main_menu_screen()


def main_menu_screen():
    # This list will store the rectangles of each image in the while loop below
    # The rectangles will then be used to determine where the mouse is clicking so
    # the proper event will trigger.
    main_menu_rects = []
    played = False

    while True:
        # Draws the main menu background using the load_image function
        # the Image class and the draw method within that class.
        # It is drawn first, so it is in the background.
        main_menu_background.draw(game_window, None, None, None,
                                  None, None, None, None)

        # Draws the logo image "Chambers" using the load_image function
        # the Image class and the draw method within that class.
        logo_path, logo_rect = load_image(logo_image_collection["chambers_logo"]["image"],
                                          "midtop", 640, 0)
        chambers_logo = Image(logo_path, logo_rect, False, False,
                              True, False, None)
        chambers_logo.draw(game_window, None, None, None,
                           None, None, 1)

        # Draws the Play button using the load_image function
        # the Image class and the draw method within that class.
        # Clicking play will start a new game and the user will pick the settings that determine
        # how the game is played
        play_path, play_rect = load_image(button_image_collection["play_button"]["image"],
                                          "center", 640, 280)
        play_button_img = Image(play_path, play_rect, True, True,
                                True, False, None)
        play_button_img.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                             color_palette["hushed_yellow"], 8, 1.15, 0, -10, 3)
        main_menu_rects.append(play_rect)

        # Draws the Instructions button using the load_image function
        # the Image class and the draw method within that class.
        # The instructions will show the user text descriptions on how to play the game
        instructions_path, instructions_rect = load_image(button_image_collection["instructions_button"]["image"],
                                                          "center", 640, 400)
        instructions_button_img = Image(instructions_path, instructions_rect, True, True,
                                        True, False, None)
        instructions_button_img.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                                     color_palette["hushed_yellow"], 8, 1.15, 0, -30, 3)
        main_menu_rects.append(instructions_rect)

        # Draws the Settings button using the load_image function
        # the Image class and the draw method within that class.
        # The settings will allow the user to change the overall volume of the game
        settings_path, settings_rect = load_image(button_image_collection["settings_button"]["image"],
                                                  "center", 640, 520)
        settings_button_img = Image(settings_path, settings_rect, True, True,
                                    True, False, None)
        settings_button_img.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                                 color_palette["hushed_yellow"], 8, 1.15, 0, -20, 3)
        main_menu_rects.append(settings_rect)

        # Draws the Quit button using the load_image function
        # the Image class and the draw method within that class.
        # The game will quit when it is clicked on... duh...
        quit_path, quit_rect = load_image(button_image_collection["quit_button"]["image"],
                                          "center", 640, 640)
        quit_button_img = Image(quit_path, quit_rect, True, True,
                                True, False, None)
        quit_button_img.draw(game_window, color_palette["russian_blue"], 6, color_palette["deep_blue"],
                             color_palette["hushed_yellow"], 8, 1.15, 0, -10, 2)
        main_menu_rects.append(quit_rect)

        played = check_mouse_hover(main_menu_rects, button_image_collection, played)
        wait_for_mouseclick(main_menu_rects, button_image_collection)

        pygame.display.update()
        pygame.display.flip()


def instructions_menu():
    played = False

    while True:
        game_window.fill((0, 0, 0))

        main_menu_background.draw(game_window, None, None, None,
                                  None, None, None, None)

        instructions_path, instructions_rect = load_image(
            button_image_collection["instructions_button"]["image"],
            "center", 640, 100)
        instructions_button_img2 = Image(instructions_path, instructions_rect, False, False,
                                         True, False, None)
        instructions_button_img2.draw(game_window, None, None, None,
                                      None, None, 1.25)

        back_button_img.draw(game_window, color_palette["midnight"], 6, color_palette["charcoal"],
                             color_palette["hushed_yellow"], 8, 1.15, None, -13, 3)

        back_button(back_button_rect)
        rect_list = [back_button_rect]
        played = check_mouse_hover(rect_list, button_image_collection, played)

        pygame.display.update()
        pygame.display.flip()


def settings_menu():
    played = False

    while True:
        game_window.fill((0, 0, 0))

        main_menu_background.draw(game_window, None, None, None,
                                  None, None, None, None)

        settings_path, settings_rect = load_image(button_image_collection["settings_button"]["image"],
                                                  "center", 640, 100)
        settings_button_img2 = Image(settings_path, settings_rect, False, False,
                                     True, False, None)
        settings_button_img2.draw(game_window, None, None, None,
                                  None, None, 1.25, None)

        back_button_img.draw(game_window, color_palette["midnight"], 6, color_palette["charcoal"],
                             color_palette["hushed_yellow"], 8, 1.15, None, -13, 3)

        back_button(back_button_rect)
        rect_list = [back_button_rect]
        played = check_mouse_hover(rect_list, button_image_collection, played)

        pygame.display.update()
        pygame.display.flip()


# Function that finds the number of players that will be playing the game
def find_num_players():
    while True:
        game_window.fill((0, 0, 0))

        num_players_text = Text("How Many Will Play?", 100, color_palette["silver"], 640, 500)
        num_players_text.find_center_position(window_width)
        num_players_text.render(game_window)

        gun_images = ImageCarousel(gun_image_collection, game_window, window_width, window_height)

        gun_images.draw_left_arrow()
        gun_images.draw_right_arrow()

        back_button_img.draw(game_window, color_palette["midnight"], 6, color_palette["charcoal"],
                             color_palette["hushed_yellow"], 8, 1.15, None, -13, 3)

        back_button(back_button_rect)

        pygame.display.update()
        pygame.display.flip()


"""
def find_chamber_size():

    num_images = len(gun_image_collection)
    image_width = pygame.image.load(gun_image_collection["gun_5_chambers"]["image"]).get_width()

    # Calculate the total width required to display all images
    total_width = num_images * image_width

    # Create a list to store the image rectangles
    image_rects = []

    chamber_size_text = Text("Select your Chamber Size", 52, (200, 200, 200), 0, 500)
    chamber_size_text.find_center_position(window_width)

    while True:
        game_window.fill((15, 15, 15))  # Fill the window with background color
        chamber_size_text.render(game_window)

        start_x = ((window_width - total_width) // 2) - 35

        for gun_image_data in gun_image_collection.values():
            chamber_size = gun_image_data["chamber_size"]
            gun_path = gun_image_data["image"]
            gun_image = pygame.image.load(gun_path)
            gun_rect = gun_image.get_rect(topleft=(start_x, 500))
            image_rects.append(gun_rect)  # Append each rect to the list
            center_x, center_y = gun_rect.center
            chamber_numbers = Text(str(chamber_size), 80, (200, 200, 200), center_x - 10, center_y - 30)

            gun_image = Image(gun_path, gun_rect, True,
                              True, True, True, chamber_numbers)
            gun_image.draw(game_window, (150, 150, 150), 10,
                           (50, 50, 50), (225, 225, 0),
                           12, 1.1, 100)

            start_x += (image_width + 35)

        pygame.display.update()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for rect, data in zip(image_rects, gun_image_collection.values()):
                    if rect.collidepoint(mouse_x, mouse_y):
                        play_mouse_click("GUI_Interact", "mouse_click_sfx")
                        chamber_size = data["chamber_size"]
                        return chamber_size

"""

if __name__ == "__main__":
    main_menu_screen()

    """
    #chamber_numbers = Text(str(chamber_size), 80, (200, 200, 200), center_x - 10, center_y - 30)
    gun_carousel = ImageCarousel(gun_image_collection, game_window, window_width, window_height,
                                 gun_image_collection["gun_5_chambers"]["image"])
    gun_carousel.display_carousel()
    """

"""
def take_turn(current_player, bullet_chamber, alive_players):
    # AI responses
    # player_response = generate_response(current_player, prompts)
    # print(player_response)
    player_response = next_turn_responses(current_player)
    print(player_response)
    time.sleep(2)


    def is_player_dead():
        if bullet_chamber == current_chamber:
            time.sleep(2)
            play_blood_splatter_sound_effect()
            print("BLAM!")
            time.sleep(2)
            print("Player", current_player, "is dead!")
            players_to_remove.append(current_player)
            time.sleep(2)
            last_player_dead = True
        else:
            time.sleep(2)
            play_revolver_sound_effect("revolver_collection", "revolver_fire_empty_sfx")
            print("WHEW!")
            time.sleep(2)
            print("Player", current_player, "is still alive!")
            time.sleep(2)
            alive_response = alive_responses(current_player)
            print(alive_response)
            last_player_dead = False
        return last_player_dead

    def spin_chamber():
        print("Player", current_player, "spins the chamber of the gun!")
        current_chamber = random.randint(1, bullet_chamber)
        play_revolver_sound_effect("revolver_collection", "revolver_spin_sfx")
        for _ in range(3):
            time.sleep(random.randint(1, 3))
            print(".")
        is_player_dead()

    def shoot_without_spinning():
        print("Player", current_player, "doesn't spin the chamber!")
        for _ in range(3):
            time.sleep(random.randint(1, 3))
            print(".")
        is_player_dead()

    def shoot_next_player():
        next_player = (current_player + 1) % alive_players
        print("Player", current_player, "takes aim at", next_player, "!")
        last_player_dead = True

        for _ in range(3):
            time.sleep(random.randint(1, 3))
            print(".")
        if bullet_chamber == current_chamber:
            time.sleep(2)
            play_blood_splatter_sound_effect()
            print("BLAM!")
            time.sleep(2)
            print("Player", current_player, "shot", next_player, "!")
            players_to_remove.append(next_player)
            time.sleep(2)

        else:
            time.sleep(2)
            play_revolver_sound_effect("revolver_collection", "revolver_fire_empty_sfx")
            print("WHEW!")
            time.sleep(2)
            print("Player", next_player, "is still alive!")
            time.sleep(2)
            print("Player", current_player, "must now die!")
            time.sleep(2)
            play_blood_splatter_sound_effect()
        return last_player_dead


def play_russian_roulette():
    alive_players = find_num_players()
    random.shuffle(alive_players)
    print(alive_players)
    bullet_chamber = random.randint(1, find_chamber_size())

    while len(alive_players) > 1:
        players_to_remove = []
        last_player_dead = False
        for current_player in alive_players:
            print("It is Player", str(current_player) + "'s turn!")
            if last_player_dead:
                play_revolver_sound_effect("revolver_collection", "revolver_reload_sfx")
            wait_for_spacebar()
            take_turn(current_player, bullet_chamber, alive_players)



            if bullet_chamber == current_chamber:
                time.sleep(2)
                play_blood_splatter_sound_effect()
                print("BLAM!")
                time.sleep(2)
                print("Player", current_player, "is dead!")
                players_to_remove.append(current_player)
                time.sleep(2)
                last_player_dead = True
            else:
                time.sleep(2)
                last_player_dead = False
                play_revolver_sound_effect("revolver_collection", "revolver_fire_empty_sfx")
                print("WHEW!")
                time.sleep(2)
                print("Player", current_player, "is still alive!")
                time.sleep(2)


# Remove dead players from the alive_players list after the iteration
for player_to_remove in players_to_remove:
    alive_players.remove(player_to_remove)

print("Game Over! Player", alive_players[0], "wins!")


"""
