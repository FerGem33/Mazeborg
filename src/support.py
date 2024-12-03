import pygame
from json import load as json_load
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


def import_folder_dict(path) -> dict:
    """
    Imports the images of the given folder and returns them as a list.
    Parameters
    ----------
    path: str
    The path to the CSV file.
    """
    surface_dict = {}
    for _, __, images in walk(path):
        for image in images:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_dict[image] = image_surface
    return surface_dict


def load_icon(icon_path, size):
    """Loads and scales an icon image."""
    icon = pygame.image.load(f'assets/images/icons/{icon_path}').convert_alpha()
    return pygame.transform.scale(icon, size)


def load_level_list():
    with open('map/index.json', 'r') as file:
        data = json_load(file)

    names = []
    for level in data['levels']:
        names.append(level['name'])
    return names
