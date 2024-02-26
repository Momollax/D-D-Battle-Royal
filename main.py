import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Circle
from math import cos, sin, pi
from matplotlib.image import imread
from matplotlib.patches import Rectangle, RegularPolygon
import json
import os

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
    probabilites = [0.6, 0.25, 0.15]
    tier_choisi = random.choices(tiers, weights=probabilites, k=1)[0]
    return tier_choisi


def pick_items(house_tier):
    objets = []
    if house_tier == 'T1':
        probabilites_rareté = [0.6, 0.25, 0.1, 0.04, 0.01]  # Probabilités pour T1
    elif house_tier == 'T2':
        probabilites_rareté = [0.4, 0.3, 0.2, 0.07, 0.03]  # Probabilités pour T2
    elif house_tier == 'T3':
        probabilites_rareté = [0.2, 0.35, 0.25, 0.15, 0.05]  # Probabilités pour T3
    nombre_objets = random.randint(2, 6)
    for i in range(nombre_objets):
        rarete_choisie = random.choices(['common', 'uncommon', 'rare', 'very rare', 'legendary'], weights=probabilites_rareté, k=1)[0]
        
        with open("./data/objets.json", "r") as f:
            objets_disponibles = json.load(f)
        
        # Filtrer les objets en fonction de la rareté choisie
        objets_filtres = [objet for objet in objets_disponibles if objet["rarity"] == rarete_choisie]
        
        if objets_filtres:
            # Choisir aléatoirement un seul objet parmi les objets filtrés
            objet_choisi = random.choice(objets_filtres)
            objets.append({"id": i+1, "rarete": rarete_choisie, "item": objet_choisi})
    
    return objets

def generate_house_loot(house_nbr):
    for i in range(house_nbr):
        house_tier = pick_house_tier()
        items = pick_items(house_tier)  # Passer la liste des objets comme argument
        
        # Définir les probabilités en fonction du tier de la maison
        if house_tier == 'T1':
            enemy_probability = 0.1
            trap_probability = 0.15
        elif house_tier == 'T2':
            enemy_probability = 0.3
            trap_probability = 0.4
        elif house_tier == 'T3':
            enemy_probability = 0.4
            trap_probability = 0.5
        
        # Générer aléatoirement la présence d'ennemis, de pièges ou des deux en fonction des probabilités
        presence_enemy = random.choices([True, False], weights=[enemy_probability, 1 - enemy_probability], k=1)[0]
        presence_trap = random.choices([True, False], weights=[trap_probability, 1 - trap_probability], k=1)[0]
        
        if presence_enemy and presence_trap:
            loot_data = f"Maison_{i + 1}: {house_tier}\n"
            loot_data += "Ennemis présents\n"
            loot_data += "Pièges présents\n"
            loot_data += "\n"
        elif presence_enemy:
            loot_data = f"Maison_{i + 1}: {house_tier}\n"
            loot_data += "Ennemis présents\n"
            loot_data += "\n"
        elif presence_trap:
            loot_data = f"Maison_{i + 1}: {house_tier}\n"
            loot_data += "Pièges présents\n"
            loot_data += "\n"
        else:
            loot_data = f"Maison_{i + 1}: {house_tier}\n"
            loot_data += "Aucun ennemi ni piège\n"
            loot_data += "\n"
        
        # Ajouter les informations sur le butin dans le fichier texte
        for item in items:
            loot_data += f"    item ID: {item['id']}\n"
            loot_data += f"    Rarete: {item['rarete']}\n"
            loot_data += f"    Nom: {item['item']['name']}\n"
            loot_data += "\n"
        
        # Écrire les données dans un fichier texte
        with open(f"./out/maison{i + 1}_{house_tier}.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write(loot_data)

def clean_out_directory():
    directory = "./out"
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier {file_path}: {e}")

def main():
    clean_out_directory()
    draw_square()
    plt.imshow(background_image, extent=[0, 1, 0, 1], aspect='auto', alpha=0.7)  
    house_nbr = random.randint(30, 50)
    generate_houses(house_nbr, 1, 1)  
    generate_house_loot(house_nbr)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('./out/map_no_circles.png', bbox_inches='tight')  # Enregistrer l'image sans les cercles

    generate_nested_circles(5)


main()