# ChercheurDeTaff

Routine de relance dans le cadre de la recherche d'emploi à partir d'un Json contenant les informations de l'entreprise en cours de démarchage et d'une base de donnée expliquant les différentes étapes jusqu'à l'embauche le programme est capable de relancer et d'entretenir la discussion avec l'interlocuteur tout seul. Il fait notamment

- Relance automatique en cas de non réponse. Si il y a une réponse ils arrêtent la relance Et passe l'entreprise en statut waiting qui signifie que l'on attend une interaction de ma part. Rédige automatiquement tous les mails mais demande une confirmation avant de les envoyer.
- Interfaces graphiques Sommaire accessible depuis le port Web de la raspberry
- fichier Log pour Pôle emploi

Pour fonctionner, le programme a besoin d'un fichier `key.py` qui est de la forme suivante :

``` python
    openAI_key = 'votre_api_key'
    mail_password = 'votre_password_mail'   
```
Le programme fonctionne grace aà 4 programme python qui sont executer grace à cron. 
- mail_collection.py
- mail_writing.py
- mail_to_send.py
- mail_to_send.py