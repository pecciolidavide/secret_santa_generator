"""
Passo 1: chiede i partecipanti e crea, in anni/<anno>/:
  - pw.csv                  (Nome, Password, Categoria;)
  - wishlist/<Nome>.txt     (un file vuoto da compilare per ogni persona)

Uso:  python3 genera_pw.py [--anno 2027]
"""
import os
import secrets
import string

import common

FILE_OUTPUT = "pw.csv"
CARTELLA_WISHLIST = "wishlist"
LUNGHEZZA_PASSWORD = 12
ALFABETO = string.ascii_letters + string.digits

INTESTAZIONE_WISHLIST = """\
# Wishlist di {nome}
# Scrivi un'idea per riga (testo o link). Le righe che iniziano con # vengono ignorate.
"""


def genera_password(gia_usate):
    while True:
        pw = "".join(secrets.choice(ALFABETO) for _ in range(LUNGHEZZA_PASSWORD))
        if pw not in gia_usate:
            return pw


def chiedi_partecipanti():
    print("Inserisci i partecipanti, uno alla volta. Invio vuoto sul nome per terminare.")
    print("La categoria serve a evitare abbinamenti tra persone dello stesso gruppo")
    print("(es. coppie o familiari): chi ha la stessa categoria non si regala a vicenda.")
    print("Lasciala vuota se non serve.\n")
    persone = []
    while True:
        nome = input(f"Nome #{len(persone) + 1}: ").strip()
        if not nome:
            break
        if any(c in nome for c in ",;/\\") or nome.startswith("."):
            print("  Il nome non può contenere , ; / \\ né iniziare con un punto.")
            continue
        if any(p[0].lower() == nome.lower() for p in persone):
            print("  Nome già inserito.")
            continue
        categoria = input("  Categoria (opzionale): ").strip()
        if any(c in categoria for c in ",;"):
            print("  La categoria non può contenere virgole o punti e virgola.")
            continue
        persone.append((nome, categoria))
    return persone


def main():
    anno = common.parser("Crea pw.csv e le wishlist per un anno.").parse_args().anno
    dati = common.cartella_dati(anno)
    file_output = os.path.join(dati, FILE_OUTPUT)
    cartella_wishlist = os.path.join(dati, CARTELLA_WISHLIST)

    print(f"=== Secret Santa {anno} (dati in {dati}) ===\n")
    if os.path.exists(file_output):
        risposta = input(f"{file_output} esiste già e verrà sovrascritto. Continuare? [s/N] ")
        if risposta.strip().lower() != "s":
            print("Annullato.")
            return

    persone = chiedi_partecipanti()
    if len(persone) < 3:
        print("Servono almeno 3 partecipanti. Nessun file scritto.")
        return

    usate = set()
    righe = []
    for nome, categoria in persone:
        pw = genera_password(usate)
        usate.add(pw)
        # Senza categoria il campo viene omesso: lo script li metterà in 'SenzaCategoria'
        campi = [nome, pw] + ([categoria] if categoria else [])
        righe.append(", ".join(campi) + ";")

    os.makedirs(dati, exist_ok=True)
    with open(file_output, "w", encoding="utf-8") as f:
        f.write("\n".join(righe) + "\n")

    os.makedirs(cartella_wishlist, exist_ok=True)
    nuove = 0
    for nome, _ in persone:
        percorso = os.path.join(cartella_wishlist, f"{nome}.txt")
        if os.path.exists(percorso):  # non sovrascrivere liste già compilate
            continue
        with open(percorso, "w", encoding="utf-8") as f:
            f.write(INTESTAZIONE_WISHLIST.format(nome=nome))
        nuove += 1

    print(f"\nScritto {file_output} con {len(persone)} partecipanti.")
    print(f"Create {nuove} wishlist in {cartella_wishlist}/ (quelle già esistenti non sono state toccate).")


if __name__ == "__main__":
    main()
