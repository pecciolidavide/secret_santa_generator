# Secret Santa Generator

Tutto il necessario per organizzare ogni anno un Secret Santa con un sito statico su Netlify: ogni partecipante inserisce la propria password e vede a chi deve fare il regalo, insieme alla wishlist di quella persona. Serve solo Python 3, senza dipendenze.

Questa repo contiene gli script e i **dati** di tutti gli anni (privata). Il sito generato finisce in `_build/<anno>/`, che è la working copy di una repo separata, `secret_santa_<anno>`, servita da Netlify.

```
secret_santa_generator/
├── genera_pw.py  script.py  pubblica.py  common.py
├── template/index.html        pagina d'ingresso (copiata nel sito)
├── anni/<anno>/               dati dell'anno: pw.csv, abbinamenti.csv, wishlist/
└── _build/<anno>/             sito generato = repo secret_santa_<anno> (ignorato da git qui)
```

Tutti gli script accettano `--anno AAAA` (default: anno corrente) e si possono lanciare da qualsiasi cartella.

## Flusso di lavoro

1. **Partecipanti**: `python3 genera_pw.py`
2. **Wishlist**: compila `anni/<anno>/wishlist/<Nome>.txt`.
3. **Genera il sito**: `python3 script.py`
4. **Pubblica**: `python3 pubblica.py`
5. Manda a ciascuno l'indirizzo Netlify e la sua password (seconda colonna di `anni/<anno>/pw.csv`).

Commit di `anni/<anno>/` in questa repo a fine lavoro, così i dati restano salvati.

## `genera_pw.py`

```bash
python3 genera_pw.py [--anno 2027]
```

Chiede nome e categoria di ogni partecipante (invio vuoto sul nome per terminare) e crea in `anni/<anno>/`:

- `pw.csv`, con una riga `Nome, Password, Categoria;` per persona e password casuali di 12 caratteri;
- `wishlist/<Nome>.txt`, un file con un commento d'istruzioni per ogni persona. Quelli già esistenti non vengono toccati.

Se `pw.csv` esiste già chiede conferma prima di sovrascriverlo. Servono almeno 3 partecipanti. I nomi non possono contenere `,` `;` `/` `\` né iniziare con un punto, e non possono essere doppi.

Se preferisci scrivere `pw.csv` a mano, il formato è:

```
Anna, x7Kq2mP9aZt4, A;
Bruno, Gd83LwQ1rVn2, A;
Chiara, uYe40TbHs6c1, B;
Dario, 2JfNx8WzKo5m;
```

La categoria è opzionale: chi non la ha finisce in `SenzaCategoria`.

## `script.py`

```bash
python3 script.py [--anno 2027] [--nuovo]
```

Legge `pw.csv` e `wishlist/`, abbina i partecipanti, salva l'abbinamento in `abbinamenti.csv` e scrive in `_build/<anno>/` `index.html` più una pagina `<password>.html` per ciascuno. Le pagine vecchie in `_build/<anno>/` vengono eliminate prima (la cartella `.git` no).

| Comando | Cosa succede |
| --- | --- |
| `python3 script.py` la prima volta | Estrae l'abbinamento, lo salva e genera il sito |
| `python3 script.py` con `abbinamenti.csv` presente | **Riutilizza** l'abbinamento e rigenera solo le pagine: serve dopo aver modificato una wishlist, senza cambiare chi regala a chi |
| `python3 script.py --nuovo` | Ignora `abbinamenti.csv`, estrae un abbinamento nuovo, lo salva e rigenera il sito |

Se `pw.csv` cambia (persone aggiunte o tolte), l'abbinamento salvato non corrisponde più e viene rifatto da capo, con un messaggio. Se manca `pw.csv` lo script si ferma.

### Come avviene l'abbinamento

1. Gli elenchi vengono mescolati.
2. Le persone sono distribuite in più liste, con **al massimo una persona per categoria** in ogni lista.
3. Ogni lista viene rimescolata e chiusa a cerchio: ognuno regala alla persona successiva, l'ultimo alla prima.

Nessuno regala quindi a qualcuno della propria categoria. Se una categoria è molto più numerosa delle altre, una lista può restare con meno di 3 persone: lo script stampa un avviso, perché qualcuno regalerebbe a se stesso o ci sarebbe uno scambio reciproco. In quel caso rilancia con `--nuovo` o cambia le categorie.

## Wishlist

Una per persona, in `anni/<anno>/wishlist/<Nome>.txt`: un'idea per riga, testo o link. Le righe vuote e quelle che iniziano con `#` sono ignorate, i link diventano cliccabili. Nella pagina di chi regala compare la wishlist del ricevente; se è vuota compare "Nessuna wishlist indicata".

## `pubblica.py`

```bash
python3 pubblica.py [--anno 2027]
```

Fa commit e push del contenuto di `_build/<anno>/` nella repo `secret_santa_<anno>` (l'account è in `common.py`, costante `OWNER`).

- **Prima volta in un anno**: inizializza git in `_build/<anno>/`, poi collega la repo se esiste già oppure la crea **privata** con `gh`.
- **Volte successive**: commit "Aggiornamento AAAA-MM-GG" (solo se ci sono modifiche) e push.

Richiede `gh` autenticato.

### Netlify

Collega la repo `secret_santa_<anno>` a Netlify una volta sola: nessun build command, e la root è già la cartella pubblicata. Ogni `pubblica.py` aggiorna il sito.

## Un nuovo anno

```bash
python3 genera_pw.py --anno 2027
# compila anni/2027/wishlist/
python3 script.py --anno 2027
python3 pubblica.py --anno 2027
```

## Limiti di sicurezza

La protezione è solo l'oscurità del nome del file: chi conosce l'URL `.../<password>.html` vede l'abbinamento. Chi ha accesso a questa repo vede tutto, `pw.csv` e `abbinamenti.csv` compresi, e la repo del sito contiene tutte le pagine. Va bene tra amici; tieni le repo private e usa password lunghe e casuali, come quelle generate da `genera_pw.py`.
