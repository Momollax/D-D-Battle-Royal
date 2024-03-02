import json
import random

def load_loot_config():
    with open('../data/armor_config.json', 'r', encoding='utf-8') as file:
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

tier = "T2"
data = load_loot_config()
armes_generees = generer_armes(tier, data)
armures_generees = generer_armures(tier, data)

print("Armes:")
for arme in armes_generees:
    print("-", arme)

print("Armures:")
if armures_generees:
    print("-", armures_generees)
else:
    print("- Aucune armure générée")