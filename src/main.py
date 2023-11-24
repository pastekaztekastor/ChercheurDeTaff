import json
import os
from datetime import datetime
from flask import Flask
from Entreprise import *
from WaitingMail import *
from Phase import *
from key import *

import imaplib
import email
from email.header import decode_header
import time

proofreading = True # TODO faire un meilleur système

print("#### DÉMARAGE DE L'APPLICATION ####")

def write_to_log(fichier: str, level: int, message: str):
    fichier = f"var/{fichier}.log"
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

# Lancement dy serveur flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


# Chargement des fichier JSON et de leur contenu
write_to_log("statut", 2, f"#### DÉMARAGE DE L'APPLICATION ####")

json_entreprise     = "data/entreprise.json"
write_to_log("statut", 1, f"Chargement de entreprise.json : '{json_entreprise}'")
json_phase          = "data/phase.json"
write_to_log("statut", 1, f"Chargement de phase.json : '{json_phase}'")
json_waitingMail    = "data/waitingMail.json"
write_to_log("statut", 1, f"Chargement de waitingMail.json : '{json_waitingMail}'")

objets_entreprise   = loadJsonEntreprise(json_entreprise)
write_to_log("statut", 1, f"Chargement des objet de '{json_entreprise}' : {len(objets_entreprise)} objet(s) chargé(s)")
objets_phase        = loadJsonPhase(json_phase)
write_to_log("statut", 1, f"Chargement des objet de '{json_phase}' : {len(objets_phase)} objet(s) chargé(s)")
objets_waitingMail  = loadJsonPhase(json_waitingMail)
write_to_log("statut", 1, f"Chargement des objet de '{json_waitingMail}' : {len(objets_waitingMail)} objet(s) chargé(s)")

liste_phase         = [element.nom for element in objets_phase]
write_to_log("statut", 1, f"Récupération des différentes phase de récutement : {liste_phase}")

time = datetime.today

# Paramètres de connexion au serveur SMTP et connection
imap_server = 'imap.mail.me.com'
imap_port = 993  # Port IMAP SSL
# Les informations confidentiel tel que le mot de passe et mon adresse mail sont dans le fichier key.py
try:
    mail = imaplib.IMAP4_SSL(imap_server, imap_port)
    mail.login(sender_email, mail_password)
    write_to_log("statut", 1, f"Connection SMPT érablie {mail.check}")
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
        elif (proofreading) :
            # TODO Fonction qui récupère la liste et la check machinalement 
            # server.sendmail(sender_email, receiver_email, message.as_string())
            a=0 # pour pas faire chier avec l'indentation
        else:
            mail.select('inbox')  # Sélectionne la boîte de réception
            # Recherche des e-mails non lus
            status, messages = mail.search(None, 'UNSEEN')
            if status == 'OK':
                for num in messages[0].split():
                    status, data = mail.fetch(num, '(RFC822)')
                    if status == 'OK':
                        # Parse les données de l'e-mail
                        message = email.message_from_bytes(data[0][1])
                        subject = decode_header(message['Subject'])[0][0]
                        sender = decode_header(message['From'])[0][0]
                        is_answer, entreprise_nom = mail_is_answer(objets_entreprise, sender)
                        if is_answer :
                            for e in objets_entreprise:
                                if e.nom == entreprise_nom:
                                    e.active = False
    mail.logout()  # Fermeture de la connexion au serveur

except Exception as e:
    write_to_log("statut", 3, f"Connection au serveur : {e}")       
    
write_to_log("statut", 1, f"Déconection du serveur")
write_to_log("statut", 3, f"Sortie de la boucle principale")
print("#### FIN DU PROGRAMME ####")
