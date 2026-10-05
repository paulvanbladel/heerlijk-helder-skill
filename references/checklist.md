# Controlepas

Doe deze pas op elke versie voordat je ze oplevert. De checks staan van mechanisch naar
oordeel. De mechanische helft zit ook in `../scripts/helder-lint.py`; de rest is
mensenwerk.

## 1. Mechanisch (zoekbaar)

Zoek elk patroon. Beoordeel elke treffer buiten code en citaten; contextafhankelijke
woorden vragen om een afweging.

| Zoek op | Overtreding | Fix |
|---|---|---|
| men, de gebruiker dient | onpersoonlijke vorm (Doelgroep 3) | spreek de lezer aan met u of je |
| dienen te, gelieve, derhalve, vermits, indien, inzake, reeds, tevens, conform, middels, teneinde | stijfwoord (Formulering 1) | zie `woordenlijst.md` |
| d.w.z., i.p.v., o.a., m.b.t., n.a.v., i.v.m., e.d. | redactionele afkorting (Formulering 2) | voluit schrijven |
| wordt, worden, werd, werden + voltooid deelwoord | lijdende vorm (Formulering 3) | noem wie het doet |
| het ...en van, bij het ...en van | naamwoordstijl (Formulering 3) | gebruik het werkwoord |
| zou kunnen worden, had moeten zijn | werkwoordsgroep van drie (Formulering 4) | herschrijf actief |
| niet + geen in één zin | gestapelde ontkenning (Formulering 3) | formuleer positief |
| binnenkort, later, zo snel mogelijk, vaak, soms, sommige, mogelijk, waarschijnlijk, nogal, veel, weinig | mogelijk vaag woord (Formulering 3) | vraag welk tijdstip, aantal of welke waarschijnlijkheid bedoeld is |
| diverse, de nodige, in principe, robuust, naadloos | vaag woord (Formulering 3) | noem het getal, de datum of de naam |
| meer informatie vindt u hier | nietszeggende link (Structuur 7) | benoem de bestemming |

## 2. Telbaar

1. **Zinslengte.** Procedureel maximaal 20 woorden, beschrijvend maximaal 25.
   Een commando tussen backticks telt als één woord.
2. **Alinea.** Maximaal zes zinnen (Structuur 6). Wees ook zuinig met alinea's van
   één zin.
3. **Samenstellingen.** Meer dan drie delen of meer dan 25 tekens: opbreken met
   voorzetsels (Formulering 1).
4. **Instructies per zin.** Eén, tenzij de handelingen samenvallen.
5. **Titels.** Elke rubriek heeft een titel die de kernboodschap benoemt (Structuur 2).

## 3. Oordeel

6. **Classificatie.** Is elke passage ofwel procedureel ofwel beschrijvend? Procedures in
   de gebiedende wijs, beschrijvingen nooit in de gebiedende wijs.
7. **Doel.** Wat wil de schrijver bereiken (informeren, instrueren, overtuigen of
   motiveren)? Wat wil de lezer doen (kennis of een vaardigheid verwerven, een standpunt
   innemen of een beslissing nemen)? Past teksttype en volgorde bij beide doelen?
8. **Lijdende vorm.** Is de handelende persoon echt onbekend of onbelangrijk? Zo niet:
   actief maken.
9. **Voorwaarde vooraan.** Staat elke als-voorwaarde vóór het commando, met komma?
   *Als de build faalt, stop de pijplijn.*
10. **Eén woord per begrip.** Scan op controleren/nakijken/verifiëren,
   instellingen/configuratie, uitvoeren/runnen/draaien.
11. **Waarschuwingen.** Eerst de handeling of de voorwaarde, dan het risico.
12. **Volledigheid.** Staat elk feit, elke datum en elke voorwaarde uit het origineel
    nog in de herschrijving?
13. **Onaangeroerd.** Code, identifiers, commando's, geciteerde fouten en eigennamen
    zijn ongewijzigd.
14. **Toon.** Past de aanspreking (*u* of *je*) bij publiek en doel, zonder te gewichtig
    of te familiair te klinken?
15. **Leenwoorden.** Is er geen goed Nederlands alternatief, verschilt het alternatief
    in betekenis of gevoelswaarde, is het publiek anderstalig of specialistisch?
16. **Na publicatie.** Welke vragen stelt het contactcenter? Welke formuliervelden vullen
    dossierbehandelaars vaak fout in? Wat laten webstatistieken zien?

## 4. Rapporteren in controlemodus

Geef per overtreding: blok + nummer, het fragment, en een conforme herschrijving.
Citeer alleen regelnummers die in `regels.md` staan.

Sluit af met: "Deze controle is geen garantie op klare taal. De schrijver beslist."
