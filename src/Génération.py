import json
import os
from datetime import datetime
from Entreprise import *
from Phase import *
from key import *

print("#### DÉMARAGE DE L'APPLICATION ####")

def write_to_log(fichier: str, level: int, message: str):
    fichier = f"/home/mathurin/Git/ChercheurDeTaff/var/{fichier}.log"
    log_levels = {
        1: "INFO",
        2: "WARNING",
        3: "ERROR"
    }
    if level not in log_levels:
        raise ValueError("Niveau de log non valide")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{log_levels[level]}] - {message}\n"
    with open(fichier, "a") as log_file:
        log_file.write(log_message)

# Chargement des fichier JSON et de leur contenu
write_to_log("statut", 2, f"#### DÉMARAGE DE L'APPLICATION ####")
json_entreprise = "data/entreprise.json"
write_to_log("statut", 1, f"Chargement de entreprise.json : '{json_entreprise}'")
json_phase = "data/phase.json"
write_to_log("statut", 1, f"Chargement de phase.json : '{json_phase}'")
objets_entreprise = loadJsonEntreprise(json_entreprise)
write_to_log("statut", 1, f"Chargement des objet de '{json_entreprise}' : {len(objets_entreprise)} objet(s) chargé(s)")
objets_phase = loadJsonPhase(json_phase)
write_to_log("statut", 1, f"Chargement des objet de '{json_phase}' : {len(objets_phase)} objet(s) chargé(s)")
liste_phase = [element.nom for element in objets_phase]
write_to_log("statut", 1, f"Récupération des différentes phase de récutement : {liste_phase}")

# Pour toute les entreprise qui ne sont pas en WAITING mode envoyer un mail si nécéssaire
time = datetime.today
print(" [  OK  ] - Démarage de la boucle infini")
while 1: 
    if (time != datetime.today):
        print(f" [  OK  ] - Acctualisation de mail - {datetime.today}")
        for e in objets_entreprise:
            if e.active:
                jours_ecoules, phase , nombre_mail_phase = time_since_last_email(e)
                print(jours_ecoules, phase , nombre_mail_phase)
                if jours_ecoules >= time_remaining_before_email(phase, nombre_mail_phase, objets_phase):
                    write_to_log("statut", 1, f"Envoie d'un mail à '{e.nom}' se référé au LOG interchange")
                    write_to_log("interchange", 1, f"Envoie d'un mail à l'entreprise '{e.nom}' en phase '{phase}' et avec {nombre_mail_phase} mail dans cette phase. Dernier mail le {e.historique_de_mail[len(e.historique_de_mail)-1].date} avec pour sujet : '{e.historique_de_mail[len(e.historique_de_mail)-1].sujet}'. Prochain mail dans {time_remaining_before_email(phase, nombre_mail_phase+1, objets_phase)}jours")
                    # TODO Ajout d'un mail a une liste d'envoie
                else:
                    write_to_log("statut", 1, f"Entreprise '{e.nom}' est active et le delais avant mail est de {time_remaining_before_email(phase, nombre_mail_phase, objets_phase)-jours_ecoules} jours.")
            else:
                write_to_log("statut", 1, f"Entreprise '{e.nom}' en attente d'information")
        time = datetime.today
    else:
        # TODO Check les mails arrivant. si un mail arrivent met le contact en active:false.
        a=0 # pour pas faire chier avec l'indentation
                
write_to_log("statut", 3, f"Sortie de la boucle principale")
print("#### FIN DU PROGRAMME ####")
