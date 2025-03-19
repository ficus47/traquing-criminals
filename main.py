import sherlock
import json
import os
import random
import threading

os.system("pip install sherlock")

# Liste de pseudos suspects de base
base_usernames = [
    "boylover", "girllover", "kidfan", "younglover",
    "babyfun", "childfriend", "pedo", "littlegirl", "littleboy",
    "toocute", "childplay", "kidworld", "sweetangel"
]

# Générer des variantes de pseudos
def generate_variants(username, count=5):
    """ Génère des variantes aléatoires d'un pseudo """
    variants = set()
    suffixes = ["123", "99", "01", "x", "xx", "_", "__", "pro", "real", "official"]
    
    while len(variants) < count:
        variant = username
        if random.random() > 0.5:
            variant += random.choice(suffixes)
        if random.random() > 0.3:
            variant = random.choice(["_", "", "-"]) + variant
        variants.add(variant)
    
    return list(variants)

# Générer toutes les variantes
suspect_usernames = []
for name in base_usernames:
    suspect_usernames.append(name)
    suspect_usernames.extend(generate_variants(name, count=3))  # Ajoute 3 variantes

# Dossier où stocker les résultats
results_dir = "sherlock_results"
os.makedirs(results_dir, exist_ok=True)

# Fonction pour exécuter Sherlock avec un pseudo
def run_sherlock(username):
    """ Lance Sherlock et sauvegarde les résultats JSON """
    output_file = f"{results_dir}/{username}.json"
    
    print(f"🔍 Recherche du pseudo : {username}")
    
    # Exécuter Sherlock en interne
    results = sherlock.sherlock(username, site_data_all=True)
    
    # Convertir les résultats en JSON
    output_data = {username: {}}
    for site, result in results.items():
        if result.get("status").startswith("FOUND"):
            output_data[username][site] = result.get("url_user")

    # Sauvegarde des résultats si des comptes ont été trouvés
    if output_data[username]:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)
        print(f"✅ Résultats enregistrés : {output_file}")
    else:
        print(f"❌ Aucun résultat pour {username}")

# Lancer la recherche avec multithreading
threads = []
for user in suspect_usernames:
    thread = threading.Thread(target=run_sherlock, args=(user,))
    threads.append(thread)
    thread.start()
    
# Attendre que tous les threads terminent
for thread in threads:
    thread.join()

print("\n🔎 Recherche terminée ! Vérifie le dossier 'sherlock_results'.")

