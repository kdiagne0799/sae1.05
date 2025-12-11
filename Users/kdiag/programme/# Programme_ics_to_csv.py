# Programme_ics_to_csv.py
# Objectif : lire un fichier .ics, extraire les événements et les écrire en pseudo-CSV

def convertir_evenement(evenement):
    uid = date = heure = duree = modalite = intitule = salles = profs = groupes = "vide"
    dtstart = dtend = None

    for ligne in evenement:
        ligne = ligne.strip()
        if ligne.startswith("UID:"):
            uid = ligne.split(":", 1)[1]
        elif ligne.startswith("DTSTART:"):
            dtstart = ligne.split(":", 1)[1]
            date = f"{dtstart[6:8]}-{dtstart[4:6]}-{dtstart[0:4]}"
            heure = f"{dtstart[9:11]}:{dtstart[11:13]}"
        elif ligne.startswith("DTEND:"):
            dtend = ligne.split(":", 1)[1]
            h1, m1 = int(dtstart[9:11]), int(dtstart[11:13])
            h2, m2 = int(dtend[9:11]), int(dtend[11:13])
            dh, dm = h2 - h1, m2 - m1
            duree = f"{dh:02}:{dm:02}"
        elif ligne.startswith("SUMMARY:"):
            intitule = ligne.split(":", 1)[1]
        elif ligne.startswith("LOCATION:"):
            salles = ligne.split(":", 1)[1]
        elif ligne.startswith("DESCRIPTION:"):
            desc = ligne.split(":", 1)[1]
            desc_parts = desc.split("\\n")
            groupes = desc_parts[1] if len(desc_parts) > 1 else "vide"
            profs = desc_parts[2] if len(desc_parts) > 2 else "vide"
            modalite = "TP" if "TP" in intitule else "CM"

    return f"{uid};{date};{heure};{duree};{modalite};{intitule};{salles};{profs};{groupes}"


# Lecture du fichier ICS
with open("mon_calendrier.ics", "r", encoding="utf-8") as fichier:
    lignes = fichier.readlines()

tableau = []
evenement = []

for ligne in lignes:
    if ligne.startswith("BEGIN:VEVENT"):
        evenement = []
    elif ligne.startswith("END:VEVENT"):
        tableau.append(convertir_evenement(evenement))
    else:
        evenement.append(ligne)

# Écriture du résultat dans un fichier CSV
with open("resultats.csv", "w", encoding="utf-8") as sortie:
    for ligne in tableau:
        sortie.write(ligne + "\n")

print("Extraction terminée. Résultats dans resultats.csv")