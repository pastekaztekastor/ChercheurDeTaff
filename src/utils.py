from datetime import datetime

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