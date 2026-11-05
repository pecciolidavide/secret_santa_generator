"""
Passo 2: legge pw.csv e wishlist/, abbina i partecipanti e genera in public/
una pagina <password>.html per ognuno.

L'abbinamento viene salvato in abbinamenti.csv: rilanciando lo script le pagine
vengono rigenerate (es. dopo aver modificato una wishlist) SENZA cambiare chi
regala a chi. Per estrarre un nuovo abbinamento usa:  python3 script.py --nuovo
"""
import csv
import html
import os
import random
import re
import sys

NOME_FILE_INPUT = "pw.csv"
FILE_ABBINAMENTI = "abbinamenti.csv"
CARTELLA_WISHLIST = "wishlist"
CARTELLA_OUTPUT = "public"  # cartella pubblicata su Netlify


def leggi_dati(percorso_file):
    """Legge un file con formato 'Nome, Password, Categoria;' e restituisce una lista di liste."""
    matrice = []
    with open(percorso_file, "r", encoding="utf-8") as f:
        for blocco in f.read().split(";"):
            riga = blocco.strip()
            if riga:
                matrice.append([item.strip() for item in riga.split(",")])
    return matrice


def organizza_per_categorie(matrice):
    """Distribuisce le persone in liste con al massimo una persona per categoria."""
    liste, categorie_per_lista = [], []
    for riga in matrice:
        nome = riga[0]
        categoria = riga[2] if len(riga) > 2 else "SenzaCategoria"
        for i in range(len(liste)):
            if categoria not in categorie_per_lista[i]:
                liste[i].append(nome)
                categorie_per_lista[i].add(categoria)
                break
        else:
            liste.append([nome])
            categorie_per_lista.append({categoria})
    return liste


def estrai_abbinamenti(persone):
    """Restituisce {donatore: ricevente}: ogni lista viene mescolata e chiusa a cerchio."""
    persone = random.sample(persone, len(persone))
    abbinamenti = {}
    for lista in organizza_per_categorie(persone):
        if len(lista) < 3:
            print(f"ATTENZIONE: lista con {len(lista)} persona/e {lista}: "
                  "qualcuno regala a se stesso o c'è uno scambio reciproco.")
        random.shuffle(lista)
        for i, donatore in enumerate(lista):
            abbinamenti[donatore] = lista[(i + 1) % len(lista)]
    return abbinamenti


def carica_abbinamenti(persone):
    """Legge abbinamenti.csv se esiste ed è coerente con pw.csv, altrimenti None."""
    if not os.path.exists(FILE_ABBINAMENTI):
        return None
    with open(FILE_ABBINAMENTI, newline="", encoding="utf-8") as f:
        abbinamenti = {r[0]: r[1] for r in csv.reader(f) if len(r) == 2}
    nomi = {p[0] for p in persone}
    if set(abbinamenti) != nomi or set(abbinamenti.values()) != nomi:
        print("abbinamenti.csv non corrisponde più a pw.csv: estraggo un nuovo abbinamento.")
        return None
    return abbinamenti


def salva_abbinamenti(abbinamenti):
    with open(FILE_ABBINAMENTI, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(abbinamenti.items())


def leggi_wishlist(nome):
    """Restituisce le righe di wishlist/<nome>.txt (senza vuote né commenti)."""
    percorso = os.path.join(CARTELLA_WISHLIST, f"{nome}.txt")
    if not os.path.exists(percorso):
        return []
    with open(percorso, encoding="utf-8") as f:
        return [r.strip() for r in f if r.strip() and not r.lstrip().startswith("#")]


def voce_html(testo):
    """Escape HTML e trasforma gli URL in link cliccabili."""
    esc = html.escape(testo)
    return re.sub(r'(https?://[^\s<]+)',
                  r'<a href="\1" target="_blank" rel="noopener">\1</a>', esc)


TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secret Santa</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f2f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        .card {
            background: white;
            padding: 2rem 3rem;
            margin: 1rem;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 32rem;
        }
        h1 { color: #333; font-weight: normal; font-size: 1.8rem; margin: 0; }
        .highlight { font-weight: bold; color: #007BFF; font-style: normal; }
        h2 { color: #555; font-weight: normal; font-size: 1.1rem; margin: 1.5rem 0 .5rem; }
        ul { text-align: left; color: #333; padding-left: 1.2rem; margin: 0; overflow-wrap: anywhere; }
        .vuota { color: #888; font-style: italic; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Ciao %%DONATORE%%, tu devi fare il regalo a <em class="highlight">%%RICEVENTE%%</em></h1>
        <h2>Idee dalla sua wishlist</h2>
%%WISHLIST%%
    </div>
</body>
</html>"""


def scrivi_html(nome_file, donatore, ricevente, idee):
    if idee:
        wishlist = "        <ul>\n" + "\n".join(f"            <li>{voce_html(i)}</li>" for i in idee) + "\n        </ul>"
    else:
        wishlist = '        <p class="vuota">Nessuna wishlist indicata: libera fantasia!</p>'
    pagina = (TEMPLATE.replace("%%DONATORE%%", html.escape(donatore))
                      .replace("%%RICEVENTE%%", html.escape(ricevente))
                      .replace("%%WISHLIST%%", wishlist))
    os.makedirs(CARTELLA_OUTPUT, exist_ok=True)
    with open(os.path.join(CARTELLA_OUTPUT, f"{nome_file}.html"), "w", encoding="utf-8") as f:
        f.write(pagina)


def main():
    try:
        persone = leggi_dati(NOME_FILE_INPUT)
    except FileNotFoundError:
        sys.exit(f"Errore: '{NOME_FILE_INPUT}' non esiste. Lancia prima genera_pw.py.")

    abbinamenti = None if "--nuovo" in sys.argv else carica_abbinamenti(persone)
    if abbinamenti is None:
        abbinamenti = estrai_abbinamenti(persone)
        salva_abbinamenti(abbinamenti)
        print(f"Nuovo abbinamento salvato in {FILE_ABBINAMENTI}.")
    else:
        print(f"Abbinamento esistente riutilizzato da {FILE_ABBINAMENTI}.")

    for nome, password, *_ in persone:
        ricevente = abbinamenti[nome]
        scrivi_html(password, nome, ricevente, leggi_wishlist(ricevente))
    print(f"Generate {len(persone)} pagine in {CARTELLA_OUTPUT}/.")


if __name__ == "__main__":
    main()
