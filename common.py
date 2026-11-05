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


def cartella_build(anno):
    """Tutto l'anno: dati (pw.csv, abbinamenti.csv, wishlist/), public/ e netlify.toml.
    È la working copy della repo di pubblicazione."""
    return os.path.join(RADICE, "_build", str(anno))


def cartella_public(anno):
    """Il solo sito pubblicato da Netlify."""
    return os.path.join(cartella_build(anno), "public")


def nome_repo(anno):
    return f"secret_santa_{anno}"
