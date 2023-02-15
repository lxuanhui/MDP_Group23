import pygame

def scale_image(image, scale):
    """Scale an image by a given factor."""
    size = round(image.get_width() * scale), round(image.get_height() * scale)
    return pygame.transform.scale(image, size)

def blit_rotate_center(screen,image,top_Left,angle):
    """Rotate an image while keeping its center and size."""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = top_Left).center)
    screen.blit(rotated_image, new_rect.topleft)