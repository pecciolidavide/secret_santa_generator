"""
Passo 3: pubblica il contenuto di _build/<anno>/ nella repo secret_santa_<anno>.
Netlify serve solo la sottocartella public/ (lo dice netlify.toml).

Alla prima esecuzione inizializza git in _build/<anno>/ e collega (o crea, privata)
la repo su GitHub. Poi fa commit e push.

Uso:  python3 pubblica.py [--anno 2027]
"""
import datetime
import os
import subprocess
import sys

import common


def run(cmd, cwd, check=True, capture=False):
    r = subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=capture)
    return r.stdout.strip() if capture else r


def main():
    anno = common.parser("Pubblica _build/<anno>/ su GitHub.").parse_args().anno
    build = common.cartella_build(anno)
    if not os.path.exists(os.path.join(build, "public", "index.html")):
        sys.exit(f"{build} non contiene il sito: lancia prima script.py --anno {anno}.")

    repo = f"{common.OWNER}/{common.nome_repo(anno)}"
    if not os.path.isdir(os.path.join(build, ".git")):
        run(["git", "init", "-q", "-b", "main"], build)
        if subprocess.run(["gh", "repo", "view", repo], capture_output=True).returncode == 0:
            run(["git", "remote", "add", "origin", f"https://github.com/{repo}.git"], build)
            run(["git", "fetch", "-q", "origin"], build)
            run(["git", "reset", "-q", "origin/main"], build)  # tiene i file locali
            print(f"Collegata la repo esistente {repo}.")
        else:
            run(["gh", "repo", "create", repo, "--private", "--source", ".", "--remote", "origin"], build)
            print(f"Creata la repo privata {repo}.")

    run(["git", "add", "-A"], build)
    if run(["git", "status", "--porcelain"], build, capture=True):
        run(["git", "commit", "-q", "-m", f"Aggiornamento {datetime.date.today().isoformat()}"], build)
        print("Commit creato.")
    else:
        print("Nessuna modifica da committare.")
    run(["git", "push", "-q", "-u", "origin", "main"], build)
    print(f"Pubblicato su https://github.com/{repo}")


if __name__ == "__main__":
    main()
