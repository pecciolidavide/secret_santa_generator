"""Percorsi e opzioni condivise da genera_pw.py, script.py e pubblica.py."""
import argparse
import datetime
import os

OWNER = "pecciolidavide"          # account GitHub delle repo di pubblicazione
RADICE = os.path.dirname(os.path.abspath(__file__))


def parser(descrizione):
    p = argparse.ArgumentParser(description=descrizione)
    p.add_argument("--anno", type=int, default=datetime.date.today().year,
                   help="anno del Secret Santa (default: anno corrente)")
    return p


def cartella_dati(anno):
    """Dati dell'anno (privati): pw.csv, abbinamenti.csv, wishlist/."""
    return os.path.join(RADICE, "anni", str(anno))


def cartella_build(anno):
    """Sito generato: è anche la working copy della repo di pubblicazione."""
    return os.path.join(RADICE, "_build", str(anno))


def nome_repo(anno):
    return f"secret_santa_{anno}"
