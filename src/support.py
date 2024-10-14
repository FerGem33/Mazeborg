import pygame
from csv import reader
from os import walk


def import_csv_layout(path) -> list:
    """
    Imports the layout of the given CSV file and returns it.
    Parameters
    ----------
    path: str
    The path to the CSV file.
    """
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path) -> list:
    """
    Imports the images of the given folder and returns them as a list.
    Parameters
    ----------
    path: str
    The path to the CSV file.
    """
    surface_list = []
    for _, __, images in walk(path):
        for image in images:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list
