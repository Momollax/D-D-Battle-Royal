import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Circle
from math import cos, sin, pi
from matplotlib.image import imread
from matplotlib.patches import Rectangle, RegularPolygon
import json
import os

moyenne_player_level = 12

difficulty = moyenne_player_level

background_image = imread('./picture/map.PNG')
house_counter = 1

def read_monsters_from_file(file_path):
    with open(file_path, 'r') as file:
        monsters = json.load(file)
    return monsters

def draw_square():
    plt.figure(figsize=(10, 10))
    for i in range(4):
        plt.plot([i / 4, i / 4], [0, 1], 'k--', linewidth=0.4)
        plt.plot([0, 1], [i / 4, i / 4], 'k--', linewidth=0.4)
        
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
        for _ in range(1000):
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
    house_images = ['./picture/door1.PNG', './picture/door1.PNG', './picture/door3.PNG']

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
    probabilites = [0.5, 0.3, 0.2]
    tier_choisi = random.choices(tiers, weights=probabilites, k=1)[0]
    return tier_choisi


def pick_items(house_tier):
    objets = []
    if house_tier == 'T1':
        # Objets obligatoires pour T1

        # Probabilités pour les autres objets
        
        probabilites_rareté = [0.6, 0.25, 0.1, 0.04, 0.01]  # Probabilités pour T1
        min_objects = 3  # Nombre minimum d'objets pour T1
        max_objects = 7  # Nombre maximum d'objets pour T1
    elif house_tier == 'T2':
        # Objets obligatoires pour T2
  
        # Probabilités pour les autres objets
        probabilites_rareté = [0.4, 0.3, 0.2, 0.07, 0.03]  # Probabilités pour T2
        min_objects = 6  # Nombre minimum d'objets pour T2
        max_objects = 10  # Nombre maximum d'objets pour T2
    elif house_tier == 'T3':
        # Objets obligatoires pour T3

        # Probabilités pour les autres objets
        probabilites_rareté = [0.2, 0.35, 0.25, 0.15, 0.05]  # Probabilités pour T3
        min_objects = 10  # Nombre minimum d'objets pour T3
        max_objects = 20  # Nombre maximum d'objets pour T3
    
    # Générer un nombre aléatoire d'objets dans la plage correspondante au tier de la maison
    nombre_objets = random.randint(min_objects, max_objects)
    
    # Ajouter les autres objets aléatoirement
    for _ in range(nombre_objets - len(objets)):
        rarete_choisie = random.choices(['common', 'uncommon', 'rare', 'very rare', 'legendary'], weights=probabilites_rareté, k=1)[0]
        
        with open("./data/objets.json", "r") as f:
            objets_disponibles = json.load(f)
        
        # Filtrer les objets en fonction de la rareté choisie
        objets_filtres = [objet for objet in objets_disponibles if objet["rarity"] == rarete_choisie]
        
        if objets_filtres:
            # Choisir aléatoirement un seul objet parmi les objets filtrés
            objet_choisi = random.choice(objets_filtres)
            objets.append({"id": len(objets)+1, "rarete": rarete_choisie, "item": objet_choisi})
    
    return objets

def generate_rencontre(difficulty, house_tier):
    remaining_difficulty = difficulty
    if house_tier == "T2":
        remaining_difficulty = difficulty * 1.3
    if house_tier == "T3":
        remaining_difficulty = difficulty * 1.5

    selected_enemies = []
    monsters = read_monsters_from_file("./data/enemy_list.json")
    while remaining_difficulty > 0:
        random_enemy = random.choice(monsters)
        enemy_difficulty = float(list(random_enemy.values())[1])  # Convertir en float

        if remaining_difficulty >= enemy_difficulty:  # Ajout de la vérification
            selected_enemies.append(random_enemy)
            remaining_difficulty -= enemy_difficulty
        else:
            break  # Sortir de la boucle si remaining_difficulty est inférieur à enemy_difficulty
    sorted_enemies = sorted(selected_enemies, key=lambda x: float(list(x.values())[1]))
    return sorted_enemies

def calculate_trap_damage(house_tier, trap_type, modifier_number):
    # Charger les informations sur les pièges à partir du fichier JSON
    with open('./data/trap_list.json', 'r') as file:
        traps_info = json.load(file)

    # Vérifier si le tier de la maison est valide
    if house_tier not in traps_info:
        print("Attention: Tier de la maison invalide.")
        return None

    # Vérifier si le type de piège est valide
    matching_trap = next((trap for trap in traps_info[house_tier] if trap["name"] == trap_type), None)
    if not matching_trap:
        print("Attention: Type de piège invalide.")
        return None

    damage_modifier = matching_trap["damage"]

    # Ajouter le modificateur en fonction du nombre
    if 1 <= modifier_number <= 5:
        # Ne rien ajouter
        pass
    elif 6 <= modifier_number <= 9:
        damage_modifier += "+1d"
    elif 10 <= modifier_number <= 14:
        damage_modifier += "+2d"
    elif 15 <= modifier_number <= 20:
        damage_modifier += "+3d"
    else:
        print("Attention: Nombre invalide.")

    return damage_modifier

def choose_random_trap(house_tier):
    # Charger les informations sur les pièges à partir du fichier JSON
    with open('./data/trap_list.json', 'r') as file:
        traps_info = json.load(file)

    # Vérifier si le tier de la maison est valide
    if house_tier not in traps_info:
        print("Attention: Tier de la maison invalide.")
        return None

    # Choisir aléatoirement un piège en fonction des probabilités
    trap_type = random.choices([trap["name"] for trap in traps_info[house_tier]],
                               weights=[trap["probability"] for trap in traps_info[house_tier]], k=1)[0]

    return trap_type

def load_loot_config():
    with open('./data/armor_config.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def generer_armes(tier, data):
    armes_par_tier = list(data["armes"].keys())
    nombre_armes = data["tiers"][tier]["nombre_armes"]

    # Roll du modificateur en fonction des chances_drop
    modificateur_roll = random.choices(["+0", "+1", "+2", "+3"], data["tiers"][tier]["chances_drop"])[0]

    # Ajout du modificateur à chaque arme générée
    armes_generees = [f"{arme} {modificateur_roll}" for arme in random.sample(armes_par_tier, nombre_armes)]
    return armes_generees

def generer_armures(tier, data):
    armures_par_tier = data["armures"]
    chance_armure = data["tiers"][tier]["chance_armure"]

    # Roll du modificateur en fonction des chances_drop
    modificateur_roll = random.choices(["+0", "+1", "+2", "+3"], data["tiers"][tier]["chances_drop"])[0]

    if random.uniform(0, 1) <= chance_armure:
        # Ajout du modificateur à l'armure générée
        armure_generee = {**random.choice(armures_par_tier), "modificateur": modificateur_roll}
        return f"{armure_generee['nom']} {armure_generee['modificateur']}"
    else:
        return None

def generer_potions(tier):
    nombre_potions_heal = random.randint(2, 5)

    potions_generees_heal = []

    if tier == 'T1':
        probabilities_heal = [0.8, 0.2, 0.0]  # Probabilités pour T1
    elif tier == 'T2':
        probabilities_heal = [0.5, 0.45, 0.05]  # Probabilités pour T2
    elif tier == 'T3':
        probabilities_heal = [0.35, 0.55, 0.10]  # Probabilités pour T3

    potions_generees_heal = random.choices(['Mineur', 'Mageur', 'Superieur'], weights=probabilities_heal, k=nombre_potions_heal)

    return potions_generees_heal


def generate_house_loot(house_nbr):
    for i in range(house_nbr):
        house_tier = pick_house_tier()
        items = pick_items(house_tier)  # Passer la liste des objets comme argument
        data = load_loot_config()
        # Générer les armes et armures pour chaque maison
        armes = generer_armes(house_tier, data)
        armures = generer_armures(house_tier, data)
        potions = generer_potions(house_tier)
        # Définir les probabilités en fonction du tier de la maison
        if house_tier == 'T1':
            enemy_probability = 0.3
            trap_probability = 0.35
        elif house_tier == 'T2':
            enemy_probability = 0.40
            trap_probability = 0.45
        elif house_tier == 'T3':
            enemy_probability = 0.70
            trap_probability = 0.75
        
        # Générer aléatoirement la présence d'ennemis, de pièges ou des deux en fonction des probabilités
        presence_enemy = random.choices([True, False], weights=[enemy_probability, 1 - enemy_probability], k=1)[0]
        presence_trap = random.choices([True, False], weights=[trap_probability, 1 - trap_probability], k=1)[0]
        
        selected_enemies = []
        trap_type = ""
        trap_damage = ""

        if presence_enemy:
            selected_enemies = generate_rencontre(difficulty, house_tier)

        if presence_trap:
            trap_type = choose_random_trap(house_tier)
            trap_damage = calculate_trap_damage(house_tier, trap_type, difficulty)

        loot_data = f"Maison_{i + 1}: {house_tier}\n"

        if presence_enemy:
            loot_data += "Ennemis présents:\n"
            for enemy in selected_enemies:
                loot_data += f"    - {enemy['name']} (Difficulté: {enemy['difficulty']})\n"

        if presence_trap:
            loot_data += f"Piège présent: {trap_type} (Dégâts: {trap_damage})\n"

        loot_data += "Armes trouvées:\n"
        for arme in armes:
            loot_data += f"    - {arme}\n"

        loot_data += "Armures trouvées:\n"
        if armures:
            loot_data += f"    - {armures}\n"

        loot_data += "\n"
        for potion in potions:
            loot_data += f"    - {potion}\n"

        loot_data += "\n"
        # Ajouter les informations sur le butin dans le fichier texte
        for item in items:
            loot_data += f"    item ID: {item['id']}\n"
            loot_data += f"    Rarete: {item['rarete']}\n"
            loot_data += f"    Nom: {item['item']['name']}\n"
            loot_data += f"    Nom: {item['item']['url']}\n"
            loot_data += "\n"
        
        # Écrire les données dans un fichier texte avec l'encodage UTF-8
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
    house_nbr = random.randint(20, 30)
    generate_houses(house_nbr, 1, 1)  
    generate_house_loot(house_nbr)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('./out/map_no_circles.png', bbox_inches='tight')  # Enregistrer l'image sans les cercles

    generate_nested_circles(5)

main()

