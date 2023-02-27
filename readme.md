
# Description d'une partition

Une partition est une succession de notes décrites dans un fichier texte, par exemple :
```
"note": {"date":0.02, "son": ["wav", "a"]}
"note": {"date":0.19, "son": ["wav", "e"]}
"note": {"date":0.31, "son": ["wav", "e"]}
```

## Note

De base, chaque note associe un son avec une date à laquelle il doit être produit. Par exemple `"note": {"date":0.19, "son": ["wav", "e"]}` joue le son du fichier audio `e.wav` à l'instant 0.19 (les dates sont en seconde).

Le format d'une note est:`"note": {"date":<date>, "son": [<format>, <nom>]}`
avec `<date>` l'instant en seconde auquel sera joué le son, `<format>` le format d'encodage du son (wav, mp3, etc.) et `<nom>` le nom du fichier son (sans l'extension).

## Effet

Il est possible d'ajouter un effet sur une note, par exemple `"note": {"date":0.19, "son": ["wav", "e"], "effet" = ["cut",0.12]}` coupe le son après 0.12s.

Trois effets sont actuellement prévus :
- superposition : superpose le sons sur le reste de le piste. Cet effet est appliqué par défaut (avec un _crossfade_ de 100 ms par défaut pour éviter les glitchs) et s'écrit `"effet" = ["supersposition"]`.
- coupe : coupe net le son après un certain délai. Cet effet s'écrit `"effet" = ["cut", <duree>]` avec `<duree>` le temps après lequel le son est stoppé. L'effet _cut_ peut se cumuler avec l'effet de superposition si les dates de démarrage du son recouvrent un autre son. Pour avoir deux sons distincts, il faut s'assurer que le son est terminé (coupé) avant la date à laquelle sera jouée le son suivant.
- fondu enchaîné : permet d'avoir une montée progressive d'un son puis sa réduction. Cet effet s'écrit
`"effet" = ["crossfade", <start>, <duration>, <end>]}` avec `<start>` la durée (en seconde) de la montée, attention la date à laquelle sera joué le son est décalée de cette durée (le son commencera donc à `date-start`), `<duration>` est la durée (en seconde) pendant lequel le son est joué à son volume normal, et `<end>` est la durée de la descente. Le son est coupé après une durée de `<start> + <duration> + <end>`

## Exemple
La partition suivante joue le son `sound1.wav` à la date 0s et coupe la piste au bout de 3s. Le son `sound2.wav` commence à la date 0.5s et est superposé (par défaut) à la piste. Le son `sound2.wav` est joué entièrement. Le son `sound3.mp3` démare à la date 2.0s (2.5-0.5) et monte en intensité pendant 0.5s (il sera donc à son niveau normal à la date 2.5s), puis reste constant pendant 1.5s et diminue sur 1s (il sera coupé à la date 5s).
```
"note": {"date":0, "son": ["wav", "sound1"], "effet":["cut", 3]}
"note": {"date":0.5, "son": ["wav", "sound2"]}
"note": {"date":2.5, "son": ["mp3", "sound3"], "effet":["crossfade", 0.5, 1.5, 1]}
```
```
          _______________________
sound1 : |                       |____________________
              ________________________________________
sound2 : ____|
                              ____________
sound3 : _________________////            \\\\\\\\\___
         0.0-0.5-1.0-1.5-2.0-2.5-3.0-3.5-4.0-4.5-5.0
```

## Stereo

Par défaut le son est en stereo avec la même puissance à droite et gauche. Il est possible de spécifier sur quel canal (doit ou gauche) est joué le son. Il suffit d'ajouter à la note un nouveau paramètre (s'il n'ets pas spécifié, le son est joué en stéréo avec la même puissance) : `"canal":["<param>"]`. Les paramètres possibles sont :

- stéréo : paramètre par défaut, le son est joué sur les deux canaux avec la même puissance. On écrit `"canal":["stereo"]`
- mono droite : le son est joué sur le canal droit. On écrit `"canal":["mono-droit"]`
- mono gauche : le son est joué sur le canal gauche. On écrit `"canal":["mono-gauche"]`
- mono aléatoire : le son est joué sur un unique canal. Le choix du canal est aléatoire. On écrit  `"canal":["mono-random"]`
- mono incrémental : le son est joué sur un unique canal. Le choix du canal alterne à chaque nouveau son avec ce paramètre. On écrit  `"canal":["mono-incremental"]`
- circulaire : le son passe d'un canal à un autre. On écrit `"canal":["circular", "<sens>", <duree>, ]` avec `<sens>` soit `left_to_right` pour que le son passe du canal gauche au canal droit, soit `right_to_left` pour l'inverse, et `<duree>` le temps en seconde pour que le son passe. Le son est coupé après cette durée.
- choix des canaux : un gain est appliqué au canal droit et gauche. On écrit `"canal":["gain", <left>, <right>]` avec `<left>`, respectivement `<right>`, le gain en dB appliqué sur le canal gauche, resp. le canal droit.

Attention le paramètre `effet` est appliqués avant `canal`.

## Génération de la bande sonore

Pour générer la bande sonore vous pouvez appeler le script pyhton `to_audio.py`, les options à passer sont :
- `-i <filename>` le fichier d'entrer de la partiion
- `-s <path>` le chemin vers le répertoire contenant les fichiers audio (s'il n'est pas renseigner les fichiers doivent être déposés au même niveau de le script)
- `-o <filename>` le fichier de sortie (par défaut `mashup.mp3`)
- `-d <duration>` durée en ms de la piste audio qui sera générée (par défaut la valeur est 0)

Par exemple
```python3 to_audio.py -i partition.txt -s ./sounds -o mySound.mp3 -d 10000```
transforme le fichier `partition.txt` en un fichier son `mySound.mp3` d'une durée de 10s et les fichiers audio sont dans le répertoire `./sounds`.
