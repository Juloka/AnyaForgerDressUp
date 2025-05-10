import pygame
import sys
# Initialize pygame
pygame.init()
# Window size & colors
WINDOW_SIZE = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)
LIGHT_GREEN = (150, 230, 150) # Colors found on Photoshop
DARK_GREEN = (50, 150, 50)
SELECT_GREEN = (100, 150, 255)
# Set up the game display window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame. display.set_caption("Anya Forger Dress Up Game")
# Load background image
background_image = None
try:
    background_image = pygame.image.load('AnyaBG.png')
    background_image = pygame.transform.scale(background_image, (WINDOW_SIZE, WINDOW_SIZE))
except pygame.error as e:
    print(f"Could not load background image: {e}")
# Function to load an image with error handling
def load_image(path, scale=None):
    try:
        image = pygame.image.load(path)
        if scale is not None:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        surf = pygame.Surface((100, 100))
        surf.fill((255, 0, 255))
        return surf
# Load character base
CHARACTER_SIZE = (WINDOW_SIZE, WINDOW_SIZE)
character_base = load_image('AnyaBase.png', CHARACTER_SIZE)
# Load clothing items
clothing_images = {}
# Categories and their options
categories = {
    "Hair": ["Normal", "School", "Bun", "Winter"],
    "Face": ["WakuWaku", "Determined", "Shocked", "Smuge"],
    "Clothes": ["School", "Blue", "Red", "Winter"],
    "Shoes": ["School", "Blue", "Red", "Winter"]
}
# Function to loading clothing images
def load_clothing_images():
    global clothing_images
    clothing_images = {}
    for category, options in categories.items():
        clothing_images[category] = []
        for option in options:
            filename = f"{category}/{option.lower()}.png"
            image = load_image(filename, CHARACTER_SIZE)
            clothing_images[category].append(image)
# For category selection buttons
def create_preview_buttons():
    preview_images = {}
    for category, options in categories.items():
        preview_size = 80
        preview_surf = pygame.Surface((preview_size, preview_size), pygame.SRCALPHA)
        preview_images[category] = preview_surf
    return preview_images
# Initial selections
current_selections = {
    "Hair": None,
    "Face": None,
    "Clothes": None,
    "Shoes": None
}
# Load clothing images
load_clothing_images()
category_previews = create_preview_buttons()
# Keep track of which catagory is active
active_category = "Hair"
# Create a button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_selected = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, DARK_GREEN, self.rect, 0)
        pygame.draw.rect(surface, color, pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4))
        if self.is_selected:
            pygame.draw.rect(surface, SELECT_GREEN, pygame.Rect(self.rect.x + 5, self.rect.y + 5, self.rect.width - 10, self.rect.height - 10), 2)
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_clicked):
        return self.rect.collidedict(mouse_pos) and mouse_clicked
# Create category buttons on the left side
category_buttons = {}
category_button_width = 250
category_button_height = 100
category_x = 20
category_y_start = WINDOW_SIZE // 4
for i, category in enumerate(categories.keys()):
    category_buttons[category] = Button(category_x, category_y_start + i * category_button_height, category_button_width, category_button_height, category, GREEN, LIGHT_GREEN)
    if category == active_category:
        category_buttons[category].is_selected = True
# Create option buttons on the right size
option_buttons = {}
option_button_width = 250
option_button_height = 100
option_x = 20
option_y_start = WINDOW_SIZE // 4
for category, options in categories.items():
    option_buttons[category] = []
    for i, option in enumerate(options):
        option_buttons[category].append(Button(option_x, option_y_start + i * option_button_height, option_button_width, option_button_height, option, GREEN, LIGHT_GREEN))
# Create a download button
download_button_width = 200
download_button_height = 60
download_button_x = WINDOW_SIZE // 2 - download_button_width // 2
download_button_y = WINDOW_SIZE - 120
download_button = Button(download_button_x, download_button_y, download_button_width, download_button_height, "Download Image", GREEN, LIGHT_GREEN)
# Function to update option buttons based on active category
def update_option_buttons():
    for category in categories:
        for i, button in enumerate(option_buttons[category]):
            if current_selections[category] == i:
                button.is_selected = True
            else:
                button.is_selected = False
# Create a character preview with clothing items
def draw_character():
    screen.blit(character_base, (0, 0))
    # Draw in the correct colthing order: Shoes, Clothes, Face, Hair
    if current_selections["Shoes"] is not None:
        screen.blit(clothing_images["Shoes"][current_selections["Shoes"]], (0, 0))
    if current_selections["Clothes"] is not None:
        screen.blit(clothing_images["Clothes"][current_selections["Clothes"]], (0, 0))
    if current_selections["Face"] is not None:
        screen.blit(clothing_images["Face"][current_selections["Face"]], (0, 0))
    if current_selections["Hair"] is not None:
        screen.blit(clothing_images["Hair"][current_selections["Hair"]], (0, 0))

def save_dressed_character():
    # Create a new surface with the same size as the character
    character_surface = pygame.Surface(CHARACTER_SIZE, pygame.SRCALPHA)
    # Show the base and selected clothing items onto the surface
    character_surface.blit(character_base, (0,0))
    if current_selections["Shoes"] is not None:
        character_surface.blit(clothing_images["Shoes"][current_selections["Shoes"]], (0, 0))
    if current_selections["Clothes"] is not None:
        character_surface.blit(clothing_images["Clothes"][current_selections["Clothes"]], (0, 0))
    if current_selections["Face"] is not None:
        character_surface.blit(clothing_images["Face"][current_selections["Face"]], (0, 0))
    if current_selections["Face"] is not None:
        character_surface.blit(clothing_images["Face"][current_selections["Face"]], (0, 0))
    # Create a filename (dressed_anya.png)
    filename = "dressed_anya.png"
    # Save the surface to a PNG file
    try:
        pygame.image.save(character_surface, filename)
        print(f"Character saved as {filename}")
    except pygame.error as e:
        print(f"Error saving image: {e}")

# Main game loop
def main():
    global active_category
    clock = pygame.time.Clock()
    # Load images before the main loop
    load_clothing_images()
    category_previews = create_preview_buttons()
    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        # Place the background
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        # Check for the download button
        if download_button.is_clicked(mouse_pos, mouse_clicked):
            save_dressed_character()
        # Check for the category button interactions
        for category, button in category_buttons.items():
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_clicked):
                active_category = category
                for c, b in category_buttons.items():
                    b.is_selected = (c == active_category)
        # Check for option button interactions (only for active category)
        for i, button in enumerate(option_buttons[active_category]):
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_clicked):
                current_selections[active_category] = 1
                update_option_buttons()
        # Draw character preview, category buttons (left side), option buttons
        # (right side), download button, title for options, and instructions
        draw_character()
        for button in category_buttons.values():
            button.draw(screen)
        for button in option_buttons.values():
            button.draw(screen)
        download_button.draw(screen)
        font = pygame.font.SysFont(None, 48)
        title_surface = font.render(f"Select {active_category}", True, BLACK)
        screen.blit(title_surface, (WINDOW_SIZE - 350, 20))
        instructions_font = pygame.font.SysFont(None, 36)
        instructions = "Help Anaya create an outfit! Choose a category on the right and then select an option on the left."
        instructions_surface = instructions_font.render(instructions, True, BLACK)
        screen.blit(instructions_surface, (WINDOW_SIZE // 2 - instructions_surface.get_width() // 2, WINDOW_SIZE - 50))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()