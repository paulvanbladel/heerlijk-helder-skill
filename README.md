# heerlijk-helder — klare taal in het Nederlands, als agentskill

Een skill die Nederlandse tekst herschrijft volgens **Heerlijk Helder**, de richtlijn
voor klare taal van Team Taaladvies van de Vlaamse overheid. Inclusief een
deterministische linter zonder afhankelijkheden.

De skill volgt het open **Agent Skills**-formaat: één `SKILL.md` met YAML-frontmatter,
plus bestanden onder `references/`, `scripts/` en `examples/`. Elke agent die dat
formaat leest, kan hem laden.

Dit is de Nederlandse tegenhanger van de ASD-STE100-skills voor het Engels. Er bestaat
geen Nederlandse ASD-STE100: deze skill past het principe toe (één woord per begrip,
actieve vorm, één instructie per zin, korte zinnen), niet een gecertificeerde norm.

## Wat de skill doet

1. Kiest een modus. **Procedureel** voor instructies, runbooks, foutmeldingen en
   UI-tekst (max 20 woorden per zin). **Beschrijvend** voor documentatie, nota's en
   verslagen (max 25).
2. Markeert overtredingen per zin, met verwijzing naar blok en nummer uit de brochure.
3. Herschrijft zonder een feit, voorwaarde of datum te laten vallen. Kost een kortere
   formulering precisie, dan blijft de langere staan en wordt de afweging gemeld.
4. Laat code, identifiers, commando's, geciteerde fouten en eigennamen ongemoeid.
5. Levert alleen de herschreven tekst. Vraag om "de diff" en je krijgt een tabel
   voor/na met regelverwijzingen.

## Installatie

Haal eerst de repo op:

```bash
git clone https://github.com/paulvanbladel/heerlijk-helder-skill
cd heerlijk-helder-skill
```

### ChatGPT

ChatGPT installeert een skill als zip-bestand. Maak die eerst:

```bash
cd .. && zip -r heerlijk-helder.zip heerlijk-helder-skill -x '*.git*'
```

Ga daarna in ChatGPT naar **Skills**, kies **Create**, en kies
**Upload from your computer**. Selecteer de zip. ChatGPT scant de skill en zet hem
daarna klaar.

Let op:

- Skills zijn er voor ChatGPT Business, Enterprise, Healthcare en Edu.
- Een beheerder kan uploaden afzetten in de werkruimte-instellingen.
- Persoonlijke skills synchroniseren niet tussen desktop en web.

### Claude

**Claude Code** leest skills uit een map. Zet de skill erin:

```bash
git clone https://github.com/paulvanbladel/heerlijk-helder-skill \
  ~/.claude/skills/heerlijk-helder
```

Wil je de skill alleen in één project? Gebruik dan `.claude/skills/heerlijk-helder`
in de projectmap.

**Claude op het web en in de app** werkt met een zip, net als ChatGPT. Maak de zip
zoals hierboven. Ga naar **Settings**, open **Capabilities**, kies **Skills** en
upload het bestand.

### Andere agents

Veel agents lezen skills uit een map op schijf. Kopieer de repo dan naar de skillmap
van je agent:

```bash
git clone https://github.com/paulvanbladel/heerlijk-helder-skill \
  <skillmap-van-je-agent>/heerlijk-helder
```

Leest je agent geen skills? Plak dan `SKILL.md` in de systeeminstructies en geef de
bestanden uit `references/` mee als bijlage.

## De linter

Alleen de Python-standaardbibliotheek, Python 3.9 of nieuwer, en geen netwerk.

```bash
python3 scripts/helder-lint.py tekst.md
python3 scripts/helder-lint.py --modus procedureel runbook.md
python3 scripts/helder-lint.py --advies --baseline 5 README.md
python3 scripts/helder-lint.py --json tekst.md
```

Hij controleert: stijfwoorden, redactionele afkortingen, zinslengte, lijdende vorm,
naamwoordstijl, werkwoordsgroepen van drie of meer, gestapelde ontkenningen, de
men-vorm, vage woorden, te lange samenstellingen, alinea's van meer dan zes zinnen en
synoniemrotatie. Met `--advies` komen leenwoorden en puntkomma's erbij.

Hij controleert **niet**: of de betekenis bewaard bleef, of de tekst begrijpelijk is,
of de toon klopt. Nul bevindingen betekent dat de ingebouwde patronen niets vonden.

Exitcode 0 onder de baseline, 1 erboven, 2 bij een onvindbaar bestand.

De repo lint zelf niet schoon: de regeltabellen citeren de patronen die ze verbieden.
Gemeten baselines: `SKILL.md` 13, `README.md` 8, `references/regels.md` 7,
`references/checklist.md` 4, `references/toepassingen.md` 2,
`references/woordenlijst.md` 0, `examples/voor-na.md` 8.

```bash
python3 scripts/helder-lint.py --baseline 13 SKILL.md
```

## Tests

```bash
python3 -m unittest discover -s tests
```

Zeventien tests, standaardbibliotheek, geen netwerk.

## Inhoud

| Pad | Inhoud |
|---|---|
| `SKILL.md` | de skill zelf: regels, werkwijze, valkuilen |
| `references/regels.md` | alle regels met de voorbeelden uit de brochure |
| `references/woordenlijst.md` | stijfwoord naar gewoon woord, naamwoordstijl, vage woorden |
| `references/checklist.md` | controlepas: mechanisch, telbaar, oordeel |
| `references/toepassingen.md` | foutmeldingen, runbooks, postmortems, prompts, UI |
| `examples/voor-na.md` | herschrijvingen met regelverwijzing |
| `scripts/helder-lint.py` | deterministische structuurcontrole |
| `tests/` | testsuite en fixtures |

## Bron en licentie

### Inhoudelijke bron

Gebaseerd op *Hou je taal Heerlijk Helder. Twintig tips voor een heldere taal en heldere
teksten*, Team Taaladvies, Departement Kanselarij en Bestuur, Vlaamse overheid, 2017
(depotnummer D/2017/3241/319). De brochure is vrij beschikbaar bij de Vlaamse overheid.
Deze repo herformuleert de richtlijnen voor agentgebruik en neemt een deel van de
voorbeelden over als illustratie.

### Afgeleid werk

De opzet van deze skill is overgenomen van twee bestaande ASD-STE100-skills voor het
Engels. Beide staan onder MIT; zie `NOTICE` voor de volledige vermeldingen.

- **`simple-english`**, een agentskill naar [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish)
  (MIT). Hiervan komen: de twee-modi-opzet, de volgorde van de werkwijze, de
  niet-aankomen-lijst, en de driedeling mechanisch/telbaar/oordeel in `checklist.md`.
  `references/toepassingen.md` is een bewerkte Nederlandse vertaling van hun
  `references/use-cases.md`, inclusief enkele voorbeelden (het postmortemvoorbeeld met
  de tijdstippen, de databasefoutmelding, de regel over *zou moeten* in prompts).
- **[danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill)** (MIT).
  Hiervan komt het idee van een deterministische linter naast de prose, met de vorm van
  de CLI (`--baseline`), het formaat van de samenvattingsregel, de disclaimerregel, de
  fixture-gestuurde tests, en de aanpak "de repo lint zelf niet schoon, hier is de
  gemeten baseline". De code van `helder-lint.py` is nieuw geschreven: de regels van
  die linter zijn Engels en niet overdraagbaar.

Nieuw in deze repo: alle Nederlandse regels en patronen, de woordenlijsten, de mapping
naar Doelgroep/Structuur/Formulering/Toetsing, de linterimplementatie, de testsuite en
de voorbeelden in `examples/voor-na.md`.

### Licentie

Code en tekst in deze repo: MIT. Zie `LICENSE` en `NOTICE`.

Voor spelling, grammatica en woordgebruik: taaltelefoon.be.
