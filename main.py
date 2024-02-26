import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Circle
from math import cos, sin, pi
from matplotlib.image import imread
from matplotlib.patches import Rectangle, RegularPolygon
import json

background_image = imread('./picture/map.PNG')
house_counter = 1
def draw_square():
    plt.figure(figsize=(10, 10))
    for i in range(3):
        plt.plot([i / 3, i / 3], [0, 1], 'k--')
        plt.plot([0, 1], [i / 3, i / 3], 'k--')
        

def draw_circle(x, y, radius):
    circle = Circle((x, y), radius=radius, fill=False, color='r')
    plt.gca().add_patch(circle)
    

def generate_nested_circles(num_circles):
    base_radius = 0.5
    x = 0.5
    y = 0.5
    plt.imshow(background_image, extent=[0, 1, 0, 1], aspect='auto', alpha=0.0)  # Afficher l'image de fond
    plt.axis('equal')
    plt.axis('off')
    
    for i in range(num_circles):
        radius = base_radius
        
        base_radius /= 1.7
        for _ in range(100):
            angle = random.uniform(0, 2 * 3.14159)
            shift_x = radius * 1.5 * random.uniform(0.1, 0.9) * cos(angle)
            shift_y = radius * 1.5 * random.uniform(0.1, 0.9) * sin(angle)
            new_x = x + shift_x
            new_y = y + shift_y
            if 0.2 <= new_x <= 0.8 and 0.2 <= new_y <= 0.8:
                x = new_x
                y = new_y
                break
        
        # Dessiner le cercle
        draw_circle(x, y, radius)
        
        # Dessiner l'espace extérieur du cercle en bleu
        xx, yy = np.meshgrid(np.linspace(0, 1, 100), np.linspace(0, 1, 100))
        d = np.sqrt((xx - x)**2 + (yy - y)**2)
        mask = d > radius
        plt.imshow(np.ones_like(xx)*mask, extent=[0, 1, 0, 1], aspect='auto', cmap='Blues', alpha=0.2, origin='lower')

        plt.savefig('./out/map_with_' + str(i) + '_circle.png', bbox_inches='tight')


def generate_houses(num_houses, map_width, map_height):
    house_locations = []  # Liste pour stocker les emplacements des maisons générées
    
    for _ in range(num_houses):
        while True:
            house_x = random.uniform(0, map_width)
            house_y = random.uniform(0, map_height)
            too_close = False
            
            # Vérification de la proximité des autres maisons
            for location in house_locations:
                if ((location[0] - house_x)**2 + (location[1] - house_y)**2)**0.5 < 0.05:
                    too_close = True
                    break
            
            # Si la nouvelle maison est trop proche, recommencer
            if too_close:
                continue
            
            # Ajouter l'emplacement de la nouvelle maison à la liste
            house_locations.append((house_x, house_y))
            break

    # Dessiner les maisons
    for i, (house_x, house_y) in enumerate(house_locations):
        draw_house(house_x, house_y, './picture/token_1.png', i + 1)
    
    return house_locations

def draw_house(x, y, image_path, house_number):
    house_width = 0.05
    house_height = 0.05
    image = imread(image_path)
    plt.imshow(image, extent=(x - house_width/2, x + house_width/2, y - house_height/2, y + house_height/2), alpha=1)
    plt.text(x, y, str(house_number), ha='center', va='center', color='black', fontsize=10)
    
def pick_house_tier():
    tiers = ['T1', 'T2', 'T3']
    probabilites = [0.5, 0.35, 0.25]
    tier_choisi = random.choices(tiers, weights=probabilites, k=1)[0]
    return tier_choisi

def pick_items(house_tier):
#"./data/common.txt"
#"./data/common_link.txt"
#"./data/uncommon.txt"
#"./data/uncommon_link.txt"
#"./data/rare.txt"
#"./data/rare_link.txt"
#"./data/very_rare.txt"
#"./data/very_rare_link.txt"
    objets = []
    if house_tier == 'T1':
        probabilites_rareté = [0.8, 0.15, 0.04, 0.01]  # Probabilités pour T1
    elif house_tier == 'T2':
        probabilites_rareté = [0.6, 0.3, 0.07, 0.03]  # Probabilités pour T2
    elif house_tier == 'T3':
        probabilites_rareté = [0.3, 0.4, 0.2, 0.1]  # Probabilités pour T3
    nombre_objets = random.randint(2, 6)
    for i in range(nombre_objets):
        rarete_choisie = random.choices(['commun', 'rare', 'tres rare', 'legendaire'], weights=probabilites_rareté, k=1)[0]
        objets.append({"id": i+1, "rarete": rarete_choisie})
    return objets

def generate_house_loot(house_nbr):
    loot_data = {}
    for i in range(house_nbr ):
        i = i + 1
        house_tier = pick_house_tier()
        items = pick_items(house_tier)
        loot_data[f"Maison_{i}"] = items

        with open("loot_data.json", "w") as json_file:
            json.dump(loot_data, json_file, indent=4)

def main():
    draw_square()
    plt.imshow(background_image, extent=[0, 1, 0, 1], aspect='auto', alpha=0.7)  
    house_nbr = random.randint(30, 50)
    generate_houses(house_nbr, 1, 1)  
    generate_house_loot(house_nbr)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('./out/map_no_circles.png', bbox_inches='tight')  # Enregistrer l'image sans les cercles
    exit()
    generate_nested_circles(5)


main()