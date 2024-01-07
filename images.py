import pygame
from sound_effects import play_mouse_click
from text import Text

color_palette = {
    "silver": (203, 211, 219),
    "russian_blue": (122, 143, 159),
    "midnight": (46, 55, 67),
    "charcoal": (37, 39, 43),
    "hazy_blue": (70, 96, 132),
    "deep_blue": (7, 15, 45),
    "razzmatazz": (231, 14, 90),
    "hushed_yellow": (225, 225, 0),
}

# Individualized nested dictionaries that contain the associated images for each category
gun_image_collection = {
    "gun_5_chambers": {
        "image": "images/gun_chamber_5.png",
        "chamber_size": 5,
    },
    "gun_6_chambers": {
        "image": "images/gun_chamber_6.png",
        "chamber_size": 6,
    },
    "gun_7_chambers": {
        "image": "images/gun_chamber_7.png",
        "chamber_size": 7,
    },
}

logo_image_collection = {
    "chambers_logo": {
        "image": "images/chambers_title.png",
    },
    "chambers_icon": {
        "image": "images/chambers_icon.png",
    },
}

button_image_collection = {
    "play_button": {
        "image": "images/play_button.png",
        "menu_position": 1,
    },
    "instructions_button": {
        "image": "images/instructions_button.png",
        "menu_position": 2,
    },
    "settings_button": {
        "image": "images/settings_button.png",
        "menu_position": 3,
    },
    "quit_button": {
        "image": "images/quit_button.png",
        "menu_position": 4,
    },
    "go_back_button": {
        "image": "images/go_back_button.png",
    },
    "left_arrow": {
        "image": "images/left_arrow.png",
    },
    "right_arrow": {
        "image": "images/right_arrow.png",
    }
}

background_image_collection = {
    "main_menu_background": {
        "image": "images/main_menu_background.png"
    },
}


class Image:
    def __init__(self, image_path, rect, can_hover, has_border, scalable, has_opacity, text):
        self.image_path = image_path
        self.rect = rect
        self.can_hover = can_hover
        self.has_border = has_border
        self.scalable = scalable
        self.has_opacity = has_opacity
        self.text = text
        self.hovered = False
        self.original_image = pygame.image.load(image_path)
        self.modified_image = self.original_image.copy()

    def draw(self, game_window, border_color=(0, 0, 0), border_width=0,
             background_color=(0, 0, 0), hover_color=(0, 0, 0), hover_width=0,
             scale=0.0, opacity=0, polygon_angle=0, polygon_angle2=0):

        if self.has_border:
            bordered_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            bordered_surface.fill(border_color)

            points1 = [(0, 0), (0, self.rect.height), (self.rect.width, 0)]
            points2 = [(self.rect.width, self.rect.height), (self.rect.width, polygon_angle2),
                       (polygon_angle, self.rect.height)]

            # Create a darker shade for the bottom and right borders
            darker_color = (max(0, border_color[0] - 50), max(0, border_color[1] - 50), max(0, border_color[2] - 50))

            # Fill the bottom and right sides with the darker shade
            pygame.draw.polygon(bordered_surface, border_color, points1)
            pygame.draw.polygon(bordered_surface, darker_color, points2)

            inner_surface = pygame.Surface((self.rect.width - border_width * 2, self.rect.height - border_width * 2))
            inner_surface.fill(background_color)
            bordered_surface.blit(inner_surface, (border_width, border_width))

            game_window.blit(bordered_surface, self.rect.topleft)

        self.check_hover(self.can_hover)

        if self.hovered and self.can_hover:

            # This code draws the actual hover border when the images are hovered over.
            pygame.draw.rect(game_window, hover_color, self.rect, hover_width)

            if self.scalable:
                scaled_width = int(self.original_image.get_width() * scale)
                scaled_height = int(self.original_image.get_height() * scale)
                scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

                if self.has_opacity:
                    scaled_image.set_alpha(opacity)
                    scaled_rect = scaled_image.get_rect()
                    scaled_rect.center = self.rect.center
                    game_window.blit(scaled_image, scaled_rect.topleft)
                else:
                    scaled_rect = scaled_image.get_rect()
                    scaled_rect.center = self.rect.center
                    game_window.blit(scaled_image, scaled_rect.topleft)

                if self.text:
                    self.text.render(game_window)

        elif self.scalable and not self.can_hover:
            scaled_width = int(self.original_image.get_width() * scale)
            scaled_height = int(self.original_image.get_height() * scale)
            scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))

            scaled_rect = scaled_image.get_rect()
            scaled_rect.center = self.rect.center
            game_window.blit(scaled_image, scaled_rect.topleft)

        else:
            game_window.blit(self.original_image, self.rect.topleft)

    def check_hover(self, can_hover):
        if can_hover:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.hovered = self.rect.collidepoint(mouse_x, mouse_y)


def load_image(path, rect_location, x_pos=0, y_pos=0):
    image = pygame.image.load(path)
    image_rect = image.get_rect(**{rect_location: (x_pos, y_pos)})
    return path, image_rect


def fade_in_out(window_width, window_height, game_window):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    alpha_value = 255
    fade_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)

    while alpha_value >= 0:
        fade_surface.fill((0, 0, 0, alpha_value))
        game_window.blit(fade_surface, (0, 0))

        pygame.display.update()
        pygame.time.delay(50)
        alpha_value -= 3


def create_alpha_mask(image_path):
    image = pygame.image.load(image_path)
    image.convert_alpha()

    alpha_mask = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    alpha_mask.fill((0, 0, 0))

    for x in range(image.get_width()):
        for y in range(image.get_height()):
            alpha = image.get_at((x, y))[3]
            alpha_mask.set_at((x, y), (0, 0, 0, alpha))

    return alpha_mask


class ImageCarousel:
    def __init__(self, image_collection, window, window_width, window_height):
        self.images = image_collection
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.starting_image = 0
        self.images = []
        self.image_rects = []

        for key, image_data in image_collection.items():
            image_path = image_data["image"]
            loaded_image = pygame.image.load(image_path).convert_alpha()
            self.images.append(loaded_image)

    # def draw_carousel(self):
    #     for gun_image_data in gun_image_collection.values():
    #         chamber_size = gun_image_data["chamber_size"]
    #         gun_path = gun_image_data["image"]
    #         gun_image = pygame.image.load(gun_path)
    #         gun_rect = gun_image.get_rect(topleft=(start_x, 500))
    #         image_rects.append(gun_rect)  # Append each rect to the list
    #         center_x, center_y = gun_rect.center
    #         chamber_numbers = Text(str(chamber_size), 80, (200, 200, 200), center_x - 10, center_y - 30)
    #
    #         gun_image = Image(gun_path, gun_rect, True,
    #                           True, True, True, chamber_numbers)
    #         gun_image.draw(self.window, (150, 150, 150), 10,
    #                        (50, 50, 50), (225, 225, 0),
    #                        12, 1.1, 100)
    #
    #         start_x += (image_width + 35)
    #
    #     pygame.display.update()
    #     pygame.display.flip()


    def draw_left_arrow(self):
        left_arrow_path, left_arrow_rect = load_image(button_image_collection["left_arrow"]["image"],
                                                      "center", 240, 400)

        left_arrow = Image(left_arrow_path, left_arrow_rect, True, False,
                           True, False, None)

        left_arrow.draw(self.window, None, 6, None,
                        color_palette["hushed_yellow"], 8, 1.15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if left_arrow_rect.collidepoint(mouse_x, mouse_y):
                    play_mouse_click("GUI_Interact", "mouse_click_sfx")

    def draw_right_arrow(self):
        right_arrow_path, right_arrow_rect = load_image(button_image_collection["right_arrow"]["image"],
                                                        "center", 1040, 400)
        right_arrow = Image(right_arrow_path, right_arrow_rect, True, False,
                            True, False, None)

        right_arrow.draw(self.window, None, 6, None,
                         color_palette["hushed_yellow"], 8, 1.15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if right_arrow_rect.collidepoint(mouse_x, mouse_y):
                    play_mouse_click("GUI_Interact", "mouse_click_sfx")

