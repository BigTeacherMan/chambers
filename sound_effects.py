import pygame
import random

pygame.mixer.init()

# The different channels that will be dedicated to playing specific sound effects
sound_channels = {
    "ambient_music_channel": pygame.mixer.Channel(0),
    "gui_sfx_channel": pygame.mixer.Channel(1),
    "game_sfx_channel": pygame.mixer.Channel(2),
}

# Nested Dictionary to store all sound effects in unique categories:
# 1. gun sounds
# 2. blood splatters
# 3. GUI interaction
sound_effects = {
    "revolver_collection": {
        "revolver_spin_sfx": pygame.mixer.Sound("sfx/revolver-spin.wav"),
        "revolver_reload_sfx": pygame.mixer.Sound("sfx/revolver-reload.wav"),
        "revolver_fire_empty_sfx": pygame.mixer.Sound("sfx/revolver-fire-empty.wav"),
        "revolver_fire_loaded_sfx": pygame.mixer.Sound("sfx/revolver-fire-loaded.wav"),
    },
    "blood_splatter_collection": {
        "blood_splatter_sfx": pygame.mixer.Sound("sfx/blood-splatter.wav"),
        "blood_splatter2_sfx": pygame.mixer.Sound("sfx/blood-splatter2.wav"),
        "blood_splatter3_sfx": pygame.mixer.Sound("sfx/blood-splatter3.wav"),
        "blood_splatter4_sfx": pygame.mixer.Sound("sfx/blood-splatter4.wav"),
        "blood_splatter5_sfx": pygame.mixer.Sound("sfx/blood-splatter5.wav"),
        "blood_splatter6_sfx": pygame.mixer.Sound("sfx/blood-splatter6.wav"),
        "blood_splatter7_sfx": pygame.mixer.Sound("sfx/blood-splatter7.wav"),
    },
    "GUI_Interact": {
        "mouse_hover_sfx": pygame.mixer.Sound("sfx/mouse-hover.wav"),
        "mouse_click_sfx": pygame.mixer.Sound("sfx/mouse-click.wav"),
    }
}


def play_revolver_sound_effect(collection, sound_effect):
    sound_effect_to_play = sound_effects.get(collection, {}).get(sound_effect)
    if sound_effect_to_play:
        sound_channels["game_sfx_channel"].queue(sound_effect)


def play_blood_splatter_sound_effect():
    random_sound_effect = random.choice(list(sound_effects["blood_splatter_collection"].keys()))
    sound_effect = sound_effects["blood_splatter_collection"][random_sound_effect]
    if sound_effect:
        sound_channels["game_sfx_channel"].play(sound_effect)


def play_mouse_click(collection, sound_effect):
    sound_effect_to_play = sound_effects.get(collection, {}).get(sound_effect)
    sound_effect_to_play.set_volume(0.2)
    if sound_effect_to_play:
        sound_channels["gui_sfx_channel"].play(sound_effect_to_play)
        while pygame.mixer.get_busy():  # Wait until the sound effect finishes playing
            pygame.time.delay(500)  # Add a small delay to avoid high CPU usage


def play_mouse_hover(collection, sound_effect):
    sound_effect_to_play = sound_effects.get(collection, {}).get(sound_effect)
    sound_effect_to_play.set_volume(0.075)
    if sound_effect_to_play:
        sound_channels["gui_sfx_channel"].play(sound_effect_to_play)




