---
name: heerlijk-helder
description: "Herschrijf Nederlandse tekst naar heldere, klare taal."
version: 0.1.0
author: Paul Van Bladel
license: MIT
platforms: [linux, macos, windows]
metadata:
  tags: [nederlands, klare-taal, heerlijk-helder, herschrijven, documentatie, toetsing]
  related_skills: [simple-english]
---

# Heerlijk Helder: klare taal in het Nederlands

Herschrijf Nederlandse tekst volgens Heerlijk Helder, de richtlijn voor klare taal van
Team Taaladvies van de Vlaamse overheid. De skill bewaart elk feit, elke voorwaarde en
elke beperking uit de brontekst. Als een kortere formulering precisie zou kosten, blijft
de langere staan en meld je de afweging.

Dit is de Nederlandse tegenhanger van `simple-english` (ASD-STE100). Pas er nooit twee
tegelijk toe op dezelfde tekst. Er bestaat geen Nederlandse ASD-STE100 en geen officieel
goedgekeurd woordenboek: deze skill past het principe toe, geen gecertificeerde norm.

## Wanneer gebruiken

- Nederlandse documentatie, README's, runbooks en procedures
- Foutmeldingen, UI-teksten en statusberichten in het Nederlands
- Mails, brieven en nota's aan klanten, collega's of management
- Postmortems en incidentverslagen
- Een tekst toetsen in plaats van herschrijven (controlemodus)

Niet gebruiken voor: Engelse tekst (gebruik `simple-english`), creatieve of wervende
copy, juridische teksten waarvan de formulering wettelijk vastligt, en citaten.

## Vereisten

Geen. De linter in `scripts/helder-lint.py` draait op Python 3.9 of nieuwer met alleen
de standaardbibliotheek.

## Modi

| Modus | Wanneer | Zinslengte |
|---|---|---|
| **Beschrijvend** (standaard) | documentatie, nota's, verslagen, mails | max 25 woorden |
| **Procedureel** | instructies, runbooks, foutmeldingen, UI-tekst | max 20 woorden |

Heerlijk Helder zegt alleen "niet te lang". De getallen komen uit de ASD-STE100-praktijk
en maken de regel toetsbaar. Noem de gekozen modus niet in de uitvoer.

## De regels

Vier blokken, zoals in de brochure *Hou je taal Heerlijk Helder* (Team Taaladvies, 2017).
Citeer regels als blok + nummer, bijvoorbeeld "Formulering 1". Verzin geen nummers:
zie `references/regels.md` voor de volledige lijst met voorbeelden.

### Doelgroep

1. Focus op wat de lezer wil of moet weten. Overschat de doelgroep niet.
2. Bepaal één kernboodschap en zet die vooraan.
3. Spreek de lezer rechtstreeks aan met *u* of *je*. Gebruik bij instructies de
   gebiedende wijs. Vervang *men* en *de gebruiker dient* door een directe aanspreking.
4. Kies een toon die bij de situatie past. Geen ambtelijke, juridische of
   gewichtige toon, en geen citaten uit regelgeving waar een gewone zin volstaat.

### Structuur

1. Groepeer wat bij elkaar hoort in duidelijke deelonderwerpen.
2. Geef elke tekst en rubriek een titel die de kernboodschap benoemt. Geen *Vraagje*,
   *Enquêteresultaten* of *Rapport*.
3. Maak de structuur zichtbaar met rubrieknummers, tussenkopjes en opsommingen.
4. Deel de tekst in alinea's van maximaal zes zinnen in.
5. Formuleer links betekenisvol. Nooit *meer informatie vindt u hier*.

### Formulering

1. Gebruik gewonemensentaal. Vervang stijfwoorden (`references/woordenlijst.md`).
   Breek samenstellingen van meer dan drie delen op met voorzetsels.
2. Schrijf redactionele afkortingen voluit. Introduceer een afkorting één keer
   met de volledige benaming erbij, tenzij ze algemeen bekend is.
3. Formuleer concreet. Noem wie wat doet, dus actief in plaats van lijdend. Vermijd
   naamwoordstijl (*het indienen van* → *dien in*). Formuleer positief: stapel geen
   ontkenningen. Gebruik consequent hetzelfde woord voor hetzelfde begrip.
4. Schrap wat overbodig is en knip lange zinnen op. Zet woorden die bij elkaar horen
   dicht bij elkaar: geen tangconstructies, geen werkwoordsgroep van drie of meer.

### Toetsing

1. Herschrijf. Een goede tekst ontstaat pas na meerdere versies.
2. Lees de tekst hardop na vanuit de positie van de lezer.
3. Werk de tekst af: spelling, taalfouten, leesbare opmaak.
4. Draai de linter en los elke harde bevinding op of verantwoord ze.

## Niet aankomen

Laat deze elementen letterlijk staan, ook als ze een regel breken:

- codeblokken, inline code, commando's, paden en bestandsnamen
- identifiers, functienamen, variabelen, foutcodes en logregels
- geciteerde foutmeldingen en letterlijke output
- eigennamen, productnamen en wettelijk vastgelegde formuleringen
- vakjargon dat de doelgroep dagelijks gebruikt — leg het uit in plaats van het te vervangen

## Werkwijze

1. **Bepaal de modus** en of elke passage procedureel of beschrijvend is. Procedures in
   de gebiedende wijs, beschrijvingen nooit in de gebiedende wijs. *Klaar als elke
   passage een label heeft.*
2. **Lees de brontekst.** Bij een bestand: lees het volledig in. Noteer elk feit, elke voorwaarde
   en elke datum. *Klaar als je de feitenlijst kunt opsommen.*
3. **Markeer de overtredingen** per zin, met blok en nummer. *Klaar als elke gemarkeerde
   zin een regelverwijzing heeft.*
4. **Herschrijf zin voor zin.** Laat geen feit vallen. Houd een kortere formulering tegen
   die precisie kost en meld die als afweging. *Klaar als de feitenlijst uit stap 2
   volledig terugkomt in de herschrijving.*
5. **Draai de linter** op het resultaat (zie Controleren). *Klaar als er geen harde
   bevindingen meer zijn, of elke overgebleven bevinding verantwoord is.*
6. **Schrijf terug.** Eén sectie: bewerk gericht. Hele tekst: schrijf het bestand opnieuw.
   *Klaar als het bestand op schijf staat en de niet-aankomen-lijst onaangeroerd is.*
7. **Lever alleen de herschreven tekst.** Geen inleiding, geen modusmelding, geen
   samenvatting van wijzigingen. Voeg één regel `Bewust ongewijzigd:` toe als je iets
   met opzet hebt laten staan.

Vraagt de gebruiker om het verschil ("toon de diff", "welke regels overtrad ik")?
Geef dan een tabel voor/na. Zet in elke rij de regelverwijzing erbij.

Vraagt de gebruiker om te **toetsen** in plaats van te herschrijven, meld dan per
overtreding: blok + nummer, het fragment, en een conforme herschrijving. Sluit af met:
"Deze controle is geen garantie op klare taal. De schrijver beslist."

## Controleren

Draai de deterministische linter in een shell:

```
python3 scripts/helder-lint.py tekst.md
python3 scripts/helder-lint.py --modus procedureel runbook.md
python3 scripts/helder-lint.py --advies --baseline 5 README.md
python3 scripts/helder-lint.py --json tekst.md
```

Exitcode 0 als het aantal harde bevindingen onder de baseline blijft, 1 erboven,
2 bij een onvindbaar bestand. Draai de testsuite met
`python3 -m unittest discover -s tests`.

Doe daarna de handmatige pas uit `references/checklist.md`. De linter dekt de
mechanische helft; de oordeelsregels blijven mensenwerk.

## Teksten van duizenden woorden

Een tekst boven ongeveer 2.000 woorden herschrijf je niet in één keer: de kwaliteit zakt
halverwege. Knip hem op langs zijn eigen koppen, in delen van ongeveer 2.000 woorden,
en behandel elk deel apart. Werk je met parallelle agents, geef elk deel dan dezelfde
harde eisen mee: zelfde koppen, zelfde volgorde, geen feit laten vallen.

Controleer na het samenvoegen mechanisch, niet op gevoel:

```
grep -c '^### ' bron.md resultaat.md
diff <(grep '^#' bron.md) <(grep '^#' resultaat.md)
```

Een lege sectie is de stille fout: een kop die blijft staan terwijl de tekst eronder
verdwenen is. Tel de tekens per sectie in plaats van het document door te lezen.

## Valkuilen

- **De linter bewijst niets.** Nul bevindingen betekent dat de ingebouwde patronen
  niets vonden, niet dat de tekst helder is. Hij vergelijkt ook geen origineel met
  een herschrijving en bewaakt de betekenis niet.
- **Het voltooid deelwoord wordt overschat.** De lijdende-vormregel herkent `be-`,
  `ver-`, `ont-`, `her-` en `ge-`-vormen met een ruim patroon en vuurt soms onterecht.
  Beoordeel elke melding.
- **Scheidbare werkwoorden zijn geen fout.** *Afsluiten*, *opstarten* en *uitvoeren*
  zijn normaal Nederlands. De Engelse phrasal-verb-regel uit ASD-STE100 geldt hier niet.
- **Kolomnummers schuiven** bij een zin die over meerdere regels loopt. Het
  regelnummer wijst naar het begin van de zin, de kolom is een benadering.
- **Deze tekst lint zelf niet schoon.** De regeltabellen citeren de patronen die ze
  verbieden en de "niet"-opsommingen stapelen ontkenningen. Draai
  `python3 scripts/helder-lint.py --baseline 13 SKILL.md` en lees de bevindingen als
  voorbeelden, niet als fouten.
- **Geen officieel keurmerk.** Voor een gecertificeerde beoordeling bestaat Wablieft;
  deze skill levert geen keurmerk.

## Bronnen

- *Hou je taal Heerlijk Helder. Twintig tips voor een heldere taal en heldere teksten*,
  Team Taaladvies, Departement Kanselarij en Bestuur, Vlaamse overheid, 2017
  (depotnummer D/2017/3241/319).
- Heerlijk Helder: `overheid.vlaanderen.be/communicatie/heerlijk-helder`
- Taaltelefoon (spelling, grammatica, woordgebruik): `taaltelefoon.be`
- Opzet afgeleid van de MIT-skills `simple-english` (AminBlg/SimpleEnglish) en
  `danyuchn/asd-ste100-skill`. Zie `NOTICE` in de repo.
