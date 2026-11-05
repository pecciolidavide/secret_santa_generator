# Secret Santa Generator

Kit per organizzare un Secret Santa con un sito statico (pensato per Netlify): ogni partecipante inserisce la propria password e vede a chi deve fare il regalo, insieme alla wishlist di quella persona. Serve solo Python 3, senza dipendenze.

## Come rifarlo ogni anno

1. **Copia questo kit** in una nuova cartella/repo, per esempio `secret_santa_2027`. Su GitHub: *Use this template* (la repo è un template), oppure `gh repo create secret_santa_2027 --template pecciolidavide/secret_santa_generator`.
2. **Crea i partecipanti**:
   ```bash
   python3 genera_pw.py
   ```
   Chiede nome e categoria di ognuno e crea `pw.csv` (con password casuali) e un file vuoto `wishlist/<Nome>.txt` per persona.
3. **Raccogli le wishlist**: apri ogni `wishlist/<Nome>.txt` e scrivi un'idea per riga (testo o link; le righe che iniziano con `#` sono ignorate). I link diventano cliccabili.
4. **Genera le pagine**:
   ```bash
   python3 script.py
   ```
   Scrive `abbinamenti.csv` e una pagina `public/<password>.html` per ciascuno.
5. **Pubblica `public/` su Netlify** (vedi sotto) e manda a ognuno l'indirizzo del sito e la sua password (la seconda colonna di `pw.csv`).

## Categorie

La categoria (lettera o sigla) serve a evitare che persone dello stesso gruppo, per esempio coppie o familiari, si regalino a vicenda. Lo script crea più liste con al massimo una persona per categoria e chiude ogni lista a cerchio: ognuno regala alla persona successiva. Senza categoria tutti finiscono in `SenzaCategoria`, quindi in un'unica catena.

Se una categoria è molto più numerosa delle altre, una lista può restare con meno di 3 persone: lo script stampa un avviso, perché una persona regalerebbe a se stessa o ci sarebbe uno scambio reciproco. In quel caso lancia `python3 script.py --nuovo` o cambia le categorie.

## Modificare una wishlist dopo la generazione

Modifica il file in `wishlist/` e rilancia `python3 script.py`: l'abbinamento salvato in `abbinamenti.csv` viene **riutilizzato**, quindi cambiano solo le pagine, non chi regala a chi. Per estrarre un abbinamento nuovo, `python3 script.py --nuovo`. Se `pw.csv` cambia (persone aggiunte o tolte), l'abbinamento viene rifatto da capo.

## Pubblicazione su Netlify

Il sito è la sola cartella `public/`. `pw.csv`, `abbinamenti.csv`, `wishlist/` e gli script restano fuori.

- **Da Git**: collega la repo a Netlify. `netlify.toml` imposta già `public` come publish directory e non serve nessun build command. Committa `public/` dopo aver lanciato lo script.
- **Manuale**: trascina `public/` su Netlify, oppure `netlify deploy --dir=public --prod`.

## Struttura

| File | Ruolo |
| --- | --- |
| `genera_pw.py` | Chiede i partecipanti, crea `pw.csv` e `wishlist/*.txt` |
| `script.py` | Abbina, salva `abbinamenti.csv`, genera le pagine in `public/` |
| `public/index.html` | Pagina d'ingresso con campo password |
| `public/<password>.html` | Pagina personale generata (nome del file = password) |
| `netlify.toml` | Imposta `public` come cartella pubblicata |
| `pw.csv`, `abbinamenti.csv`, `wishlist/` | Dati dell'anno, generati dagli script |

## Limiti di sicurezza

La protezione è solo l'oscurità del nome del file: chi conosce l'URL `.../<password>.html` vede l'abbinamento, e chi ha accesso alla repo vede tutto, `abbinamenti.csv` compreso. Va bene tra amici; usa password lunghe e casuali, quelle che genera lo script.
