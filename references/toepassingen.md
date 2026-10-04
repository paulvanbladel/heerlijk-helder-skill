# Toepassingen in IT- en bedrijfsteksten

Heerlijk Helder is geschreven voor overheidscommunicatie. Dezelfde regels werken overal
waar een misverstand geld of tijd kost. Per geval: de modus en de aanpassing.

## Foutmeldingen en CLI-uitvoer

Modus: procedureel. Het hoogste rendement. Een foutmelding is een instructie aan iemand
die om 2 uur 's nachts gewekt is.

Patroon: wat ging er mis (verleden tijd), wat is de oorzaak, wat moet de lezer doen.

> **Liever niet:** Er is helaas iets misgegaan bij het tot stand brengen van een
> verbinding. Gelieve na te gaan of uw gegevens correct geconfigureerd zijn.
>
> **Maar wel:** De verbinding met de database is mislukt. Het wachtwoord van gebruiker
> `app` klopt niet. Stel `DB_PASSWORD` in en probeer opnieuw.

## Runbooks en procedures

Modus: procedureel. Elke stap in de gebiedende wijs, één handeling per stap, voorwaarde
vooraan. Waarschuwing vóór de stap: eerst de handeling, dan het risico. De limiet van 20
woorden geldt hard; een operator onder tijdsdruk leest elke zin één keer.

## Incidentverslagen en postmortems

Modus: beschrijvend. Gebruik de onvoltooid verleden tijd en noem tijdstippen.

> **Liever niet:** We hebben vastgesteld dat een probleem mogelijk impact gehad heeft op
> de toegang van sommige gebruikers.
>
> **Maar wel:** Tussen 14.02 en 14.31 uur faalde 12% van de aanvragen. Een deploy om
> 14.00 uur verwijderde de cache-opwarming.

Heerlijk Helder verbiedt verbloemende formuleringen (Formulering 3). Het verslag noemt
wat bekend is en schrijft "onbekend" voor de rest. Dat leest eerlijker omdat het dat is.

## Commits en pull requests

Modus: gebiedende wijs in de titel, beschrijvend in de tekst. Schrap *deze PR heeft tot
doel*. Pas de woordenlijst en de limiet van 25 woorden toe op de tekst.

## Releasenotes en changelogs

Modus: beschrijvend. Eén wijziging per regel, één zin waar het kan. Breekt iets: eerst
de handeling, dan de uitleg. *Pas uw aanroepen aan naar `v2/users`. Het veld `name` is
gesplitst in `first_name` en `last_name`.*

## Mails en nota's aan management

Modus: beschrijvend. Kernboodschap in de eerste alinea (Doelgroep 2). Een
onderwerpregel die de boodschap benoemt, geen *Vraagje* of *Update* (Structuur 2). Geen
gestapelde slagen om de arm: noem het cijfer of zeg dat je het niet weet.

## Instructies voor AI-agents (prompts, AGENTS.md, skills)

Modus: procedureel. Een systeemprompt is een procedure die gelezen wordt door iemand die
geen vraag kan stellen.

- Eén instructie per zin maakt elke regel los citeerbaar en moeilijk half te volgen.
- Eén woord per begrip voorkomt dat het model *controleren*, *nakijken* en *verifiëren*
  als drie verschillende handelingen leest.
- Voorwaarde vooraan: *Als de build faalt, stop* werkt beter dan een voorwaarde achteraan.
- Geen *zou moeten*: een model leest dat als optioneel. Schrijf *moet*, of schrap de regel.

## UI-teksten en lege toestanden

Modus: procedureel, harde lengtelimieten. Knoppen en labels zijn namen en blijven staan.
De lopende tekst volgt de regels: *Nog geen projecten. Maak een project aan om te starten.*

## Vertaling en lokalisatie

Modus: beschrijvend, streng. Eén betekenis per woord en volledige zinnen halen de meeste
dubbelzinnigheid uit een brontekst. Dat verlaagt de kost en de foutenlast van een
vertaling, ook van een machinevertaling.
