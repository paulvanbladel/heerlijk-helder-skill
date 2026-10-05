#!/usr/bin/env python3
"""Deterministische structuurcontrole voor Nederlandse tekst (Heerlijk Helder).

Controleert alleen mechanische patronen. De linter bewijst niet dat een tekst
begrijpelijk is en vergelijkt geen origineel met een herschrijving. Nul
bevindingen betekent dat de ingebouwde patronen niets gevonden hebben.

Gebruik:
    python3 helder-lint.py BESTAND [BESTAND ...]
    python3 helder-lint.py --modus procedureel runbook.md
    python3 helder-lint.py --baseline 12 --advies SKILL.md
    python3 helder-lint.py --json tekst.md

Exitcode 0 als het aantal harde bevindingen <= baseline is, anders 1.
Alleen de Python-standaardbibliotheek. Werkt op Linux, macOS en Windows.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from dataclasses import dataclass, asdict
from typing import Iterable

ZIN_CAP = {"procedureel": 20, "beschrijvend": 25}

# Formulering 1 — ambtelijke en zwaarwichtige woorden met een gewoon alternatief.
STIJFWOORDEN = {
    "alsmede": "en, ook",
    "alvorens": "voordat",
    "bij dezen": "hierbij",
    "conform": "volgens",
    "derhalve": "dus",
    "desgevallend": "als dat zo is",
    "dient te": "moet",
    "dienen te": "moeten",
    "eveneens": "ook",
    "gelieve": "wilt u, kunt u",
    "hetwelk": "dat",
    "indien": "als",
    "ingeval": "als",
    "inzake": "over",
    "met het oog op": "voor",
    "middels": "met, door",
    "nopens": "over",
    "naar aanleiding van": "na, door",
    "met betrekking tot": "over",
    "in het kader van": "voor",
    "ten aanzien van": "over",
    "teneinde": "om",
    "te allen tijde": "altijd, op elk moment",
    "tevens": "ook, bovendien",
    "trachten": "proberen",
    "vermits": "omdat, want",
    "verzoeken": "vragen",
    "vigeren": "gelden",
    "woonachtig": "wonend",
    "werkzaam zijn te": "werken in",
    "reeds": "al",
    "zulks": "dat",
}

# Formulering 2 — redactionele afkortingen voluit schrijven.
AFKORTINGEN = {
    "d.w.z.": "dat wil zeggen",
    "i.p.v.": "in plaats van",
    "o.a.": "onder andere",
    "m.b.t.": "over",
    "n.a.v.": "na",
    "i.v.m.": "door, voor",
    "e.d.": "en dergelijke",
    "t.a.v.": "voor",
    "m.a.w.": "met andere woorden",
    "bv.": "bijvoorbeeld",
    "nl.": "namelijk",
}

# Formulering 3 — vage en wollige formuleringen zonder feit.
VAAGWOORDEN = [
    "eigenlijk",
    "in principe",
    "enigszins",
    "min of meer",
    "zo snel mogelijk",
    "op korte termijn",
    "in de nabije toekomst",
    "binnenkort",
    "geruime tijd",
    "diverse",
    "nodige",
    "adequate",
    "naadloos",
    "robuust",
    "krachtig",
    "state of the art",
]

# Contextafhankelijk: vraag om verduidelijking, maar niet elke treffer is vaag.
CONTEXT_VAAGWOORDEN = [
    "later", "vaak", "soms", "sommige", "mogelijk", "waarschijnlijk",
    "nogal", "veel", "weinig",
]

NEGATIES = ("niet", "geen", "nooit", "niets", "noch", "zonder")

# Formulering 4 — werkwoorden die een eindgroep vormen.
EINDGROEP = {
    "worden", "wordt", "werden", "werd", "zijn", "is", "was", "waren",
    "kunnen", "kan", "kon", "konden", "moeten", "moet", "moest", "moesten",
    "zullen", "zal", "zou", "zouden", "mogen", "mag", "mocht", "mochten",
    "hebben", "heeft", "had", "hadden", "worden.", "gaan", "gaat",
}

# Voltooid deelwoord: ge-vorm (ook met scheidbaar voorvoegsel), be-/ver-/ont-/
# her-/er-vorm, of -eerd. Een bewuste overschatting: de regel vuurt alleen
# binnen zes woorden na wordt/worden/werd/werden.
PARTICIPLE = re.compile(
    r"^(\w*ge\w+(d|t|en)|(be|ver|ont|her|er)\w+(d|t|en)|\w+eerde?)$",
    re.IGNORECASE,
)

# Formulering 3 — één woord per begrip; deze stammen rouleren het vaakst.
SYNONIEMGROEPEN = [
    ("controle", "nakijk", "verifi", "check"),
    ("instelling", "configurat", "setting"),
    ("uitvoer", "runn", "draai"),
    ("verwijder", "wiss", "delet"),
    ("aanmaak", "aanmak", "creëer", "creer", "opzett"),
    ("fout", "error", "storing"),
]

# Advies — leenwoorden met een gangbaar Nederlands equivalent.
LEENWOORDEN = {
    "implementeren": "invoeren, uitvoeren",
    "meeting": "vergadering, overleg",
    "policy": "beleid, aanpak",
    "desiderata": "wensen",
    "issue": "probleem, melding",
    "deadline": "uiterste datum",
    "feature": "functie",
    "update": "bijwerken, nieuwe versie",
}


@dataclass
class Bevinding:
    bestand: str
    regel: int
    kolom: int
    regelnaam: str
    bron: str
    bericht: str
    fragment: str
    hard: bool

    def tekst(self) -> str:
        soort = "" if self.hard else " [advies]"
        return (
            f"{self.bestand}:{self.regel}:{self.kolom} {self.regelnaam}{soort}: "
            f"{self.bericht} ({self.bron}) [{self.fragment}]"
        )


def strip_code(lines: list[str]) -> list[str]:
    """Vervang YAML-frontmatter, codeblokken, inline code en URL's door spaties.

    De regelnummering blijft intact: elke regel houdt zijn lengte.
    """
    uit: list[str] = []
    in_fence = False
    in_frontmatter = bool(lines) and lines[0].strip() == "---"
    for idx, line in enumerate(lines):
        if in_frontmatter:
            uit.append(" " * len(line))
            if idx > 0 and line.strip() == "---":
                in_frontmatter = False
            continue
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            uit.append(" " * len(line))
            continue
        if in_fence:
            uit.append(" " * len(line))
            continue
        schoon = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
        schoon = re.sub(r"https?://\S+", lambda m: " " * len(m.group(0)), schoon)
        uit.append(schoon)
    return uit


LIJST_MARKER = re.compile(r"^([-*+]|\d+[.)])\s+")


def is_lijstitem(kaal: str) -> bool:
    return bool(LIJST_MARKER.match(kaal))


def alineas(lines: list[str]) -> Iterable[list[tuple[int, str]]]:
    """Groepeer opeenvolgende tekstregels tot blokken.

    Koppen, tabelrijen en citaten tellen niet mee: die volgen andere regels.
    Elk lijstitem begint een nieuw blok, zodat twee opsommingstekens zonder punt
    niet tot één zin samensmelten.
    """
    blok: list[tuple[int, str]] = []
    for idx, line in enumerate(lines, start=1):
        kaal = line.strip()
        if not kaal or kaal.startswith(("#", "|", ">")):
            if blok:
                yield blok
                blok = []
            continue
        if is_lijstitem(kaal) and blok:
            yield blok
            blok = []
        blok.append((idx, LIJST_MARKER.sub("", kaal) if is_lijstitem(kaal) else kaal))
    if blok:
        yield blok


def zinnen(lines: list[str]) -> Iterable[tuple[int, int, str]]:
    """Lever (regelnummer, kolom, zin) op.

    Een zin die over meerdere regels loopt wordt samengevoegd en gemeld op de
    regel waar hij begint. Afkortingen breken de zin niet af.
    """
    for blok in alineas(lines):
        tekst = ""
        posities: list[tuple[int, int]] = []  # (regelnummer, kolom) per teken
        for regelnr, kaal in blok:
            if tekst:
                tekst += " "
                posities.append((regelnr, 1))
            for kolom, teken in enumerate(kaal, start=1):
                tekst += teken
                posities.append((regelnr, kolom))

        start = 0
        for m in re.finditer(r"[.!?](?=\s|$)", tekst):
            eind = m.end()
            kandidaat = tekst[start:eind]
            staart = kandidaat.rstrip()[-6:]
            if re.search(r"\b\w\.\w?\.$", staart) or re.search(r"\b\d+\.$", staart):
                continue
            if kandidaat.strip():
                offset = len(kandidaat) - len(kandidaat.lstrip())
                regelnr, kolom = posities[min(start + offset, len(posities) - 1)]
                yield regelnr, kolom, kandidaat.strip()
            start = eind
        rest = tekst[start:]
        if rest.strip():
            offset = len(rest) - len(rest.lstrip())
            regelnr, kolom = posities[min(start + offset, len(posities) - 1)]
            yield regelnr, kolom, rest.strip()


def woorden(zin: str) -> list[str]:
    return re.findall(r"[\w'’-]+", zin)


def _zoek(zin: str, naald: str) -> int:
    m = re.search(r"(?<!\w)" + re.escape(naald) + r"(?!\w)", zin, re.IGNORECASE)
    return m.start() + 1 if m else 0


def controleer_zin(
    bestand: str, regel: int, kolom: int, zin: str, cap: int, advies: bool
) -> list[Bevinding]:
    gevonden: list[Bevinding] = []
    low = zin.lower()

    def voeg_toe(naam, bron, bericht, fragment, offset, hard=True):
        gevonden.append(
            Bevinding(bestand, regel, kolom + max(offset - 1, 0), naam, bron,
                      bericht, fragment, hard)
        )

    for naald, beter in STIJFWOORDEN.items():
        pos = _zoek(zin, naald)
        if pos:
            voeg_toe("stijfwoord", "Formulering 1",
                     f"Ambtelijk woord. Schrijf: {beter}.", naald, pos)

    for naald, beter in AFKORTINGEN.items():
        if naald in low:
            voeg_toe("afkorting", "Formulering 2",
                     f"Schrijf de afkorting voluit: {beter}.", naald,
                     low.index(naald) + 1)

    for naald in VAAGWOORDEN:
        pos = _zoek(zin, naald)
        if pos:
            voeg_toe("vaag-woord", "Formulering 3",
                     "Vage formulering zonder feit. Noem het feit of schrap.",
                     naald, pos)

    ww = woorden(zin)
    if len(ww) > cap:
        voeg_toe("lange-zin", "Formulering 4",
                 f"Zin telt {len(ww)} woorden (max {cap}). Knip de zin op.",
                 f"{len(ww)} woorden", 1)

    # Lijdende vorm: worden/wordt/werd(en) gevolgd door een voltooid deelwoord.
    for m in re.finditer(r"\b(wordt|worden|werd|werden)\b", zin, re.IGNORECASE):
        staart = woorden(zin[m.end():])[:6]
        if any(PARTICIPLE.match(w) for w in staart):
            voeg_toe("lijdende-vorm", "Formulering 3",
                     "Lijdende vorm. Noem wie de handeling doet.",
                     m.group(0), m.start() + 1)
            break

    # Naamwoordstijl: "het aanvragen van", "bij het indienen van".
    for m in re.finditer(r"\b(het|bij het|voor het|na het|van het)\s+(\w+en)\s+van\b",
                         zin, re.IGNORECASE):
        voeg_toe("naamwoordstijl", "Formulering 3",
                 "Naamwoordstijl. Gebruik het werkwoord zelf.",
                 m.group(0), m.start() + 1)

    # Werkwoordsopeenhoping aan het zinseinde: "zou kunnen worden uitgevoerd".
    staart = woorden(zin)[-4:]
    reeks = 0
    for w in staart:
        if w.lower() in EINDGROEP or PARTICIPLE.match(w):
            reeks += 1
        else:
            reeks = 0
        if reeks >= 3:
            voeg_toe("werkwoordsgroep", "Formulering 4",
                     "Drie of meer werkwoorden op een rij. Herschrijf actief.",
                     " ".join(staart), 1)
            break

    aantal_negaties = sum(1 for w in ww if w.lower() in NEGATIES)
    if aantal_negaties >= 2:
        voeg_toe("negatiestapel", "Formulering 3",
                 f"{aantal_negaties} ontkenningen in één zin. Formuleer positief.",
                 " ".join(w for w in ww if w.lower() in NEGATIES), 1)

    pos = _zoek(zin, "men")
    if pos:
        voeg_toe("men-vorm", "Doelgroep 3",
                 "Spreek de lezer aan met u of je in plaats van 'men'.", "men", pos)

    for w in ww:
        if len(w) >= 25 and "-" not in w:
            voeg_toe("lange-samenstelling", "Formulering 1",
                     f"Samenstelling van {len(w)} tekens. Breek op met voorzetsels.",
                     w, _zoek(zin, w) or 1)

    if advies:
        for naald in CONTEXT_VAAGWOORDEN:
            pos = _zoek(zin, naald)
            if pos:
                voeg_toe("vaag-woord", "Formulering 3",
                         "Mogelijk vaag. Controleer of de lezer genoeg informatie krijgt.",
                         naald, pos, hard=False)
        for naald, beter in LEENWOORDEN.items():
            pos = _zoek(zin, naald)
            if pos:
                voeg_toe("leenwoord", "Formulering 1",
                         f"Nederlands alternatief bestaat: {beter}.", naald, pos,
                         hard=False)
        if ";" in zin:
            voeg_toe("puntkomma", "Formulering 4",
                     "Puntkomma. Maak er twee zinnen van.", ";",
                     zin.index(";") + 1, hard=False)

    return gevonden


def controleer_document(bestand: str, lines: list[str], alle_zinnen: list[tuple[int, int, str]]) -> list[Bevinding]:
    gevonden: list[Bevinding] = []
    volledig = " ".join(z for _, _, z in alle_zinnen).lower()

    for groep in SYNONIEMGROEPEN:
        aanwezig = [t for t in groep if re.search(r"(?<![a-z])" + t, volledig)]
        if len(aanwezig) >= 2:
            gevonden.append(
                Bevinding(bestand, 1, 1, "synoniemrotatie", "Formulering 3",
                          "Meerdere termen voor hetzelfde begrip. Kies er één.",
                          " / ".join(aanwezig), True)
            )

    # Structuur 6 — alinea's van meer dan zes zinnen. Opsommingen tellen niet mee.
    alinea_start, alinea_zinnen = None, 0
    for idx, line in enumerate(lines, start=1):
        kaal = line.strip()
        if kaal and not kaal.startswith(("#", "|", ">")) and not is_lijstitem(kaal):
            if alinea_start is None:
                alinea_start = idx
            alinea_zinnen += sum(1 for r, _, _ in alle_zinnen if r == idx)
        else:
            if alinea_start is not None and alinea_zinnen > 6:
                gevonden.append(
                    Bevinding(bestand, alinea_start, 1, "lange-alinea", "Structuur 6",
                              f"Alinea telt {alinea_zinnen} zinnen (max 6). Splits de alinea.",
                              f"{alinea_zinnen} zinnen", True)
                )
            alinea_start, alinea_zinnen = None, 0
    if alinea_start is not None and alinea_zinnen > 6:
        gevonden.append(
            Bevinding(bestand, alinea_start, 1, "lange-alinea", "Structuur 6",
                      f"Alinea telt {alinea_zinnen} zinnen (max 6). Splits de alinea.",
                      f"{alinea_zinnen} zinnen", True)
        )
    return gevonden


def lint(pad: pathlib.Path, modus: str, advies: bool) -> tuple[list[Bevinding], int]:
    ruwe = pad.read_text(encoding="utf-8").splitlines()
    lines = strip_code(ruwe)
    alle_zinnen = list(zinnen(lines))
    cap = ZIN_CAP[modus]
    gevonden: list[Bevinding] = []
    for regel, kolom, zin in alle_zinnen:
        gevonden.extend(controleer_zin(str(pad), regel, kolom, zin, cap, advies))
    gevonden.extend(controleer_document(str(pad), lines, alle_zinnen))
    gevonden.sort(key=lambda b: (b.regel, b.kolom, b.regelnaam))
    woordtotaal = sum(len(woorden(z)) for _, _, z in alle_zinnen)
    return gevonden, woordtotaal


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Structuurcontrole voor klare taal (Heerlijk Helder).")
    p.add_argument("bestanden", nargs="+", help="Markdown- of tekstbestanden.")
    p.add_argument("--modus", choices=sorted(ZIN_CAP), default="beschrijvend",
                   help="procedureel = 20 woorden per zin, beschrijvend = 25.")
    p.add_argument("--baseline", type=int, default=0,
                   help="Aantal harde bevindingen dat je aanvaardt zonder foutcode.")
    p.add_argument("--advies", action="store_true",
                   help="Toon ook adviesregels (leenwoorden, puntkomma).")
    p.add_argument("--json", action="store_true", help="Machineleesbare uitvoer.")
    args = p.parse_args(argv)

    alles: list[Bevinding] = []
    woordtotaal = 0
    for naam in args.bestanden:
        pad = pathlib.Path(naam)
        if not pad.is_file():
            print(f"Bestand niet gevonden: {naam}", file=sys.stderr)
            return 2
        bevindingen, telling = lint(pad, args.modus, args.advies)
        alles.extend(bevindingen)
        woordtotaal += telling

    hard = [b for b in alles if b.hard]
    if args.json:
        print(json.dumps({
            "bevindingen": [asdict(b) for b in alles],
            "hard": len(hard),
            "totaal": len(alles),
            "woorden": woordtotaal,
            "baseline": args.baseline,
        }, ensure_ascii=False, indent=2))
    else:
        for b in alles:
            print(b.tekst())
        dichtheid = (len(hard) / woordtotaal * 100) if woordtotaal else 0.0
        print(f"\n{len(alles)} bevindingen ({len(hard)} hard, baseline {args.baseline}), "
              f"{woordtotaal} woorden, {dichtheid:.1f} per 100 woorden")
        print("De linter controleert patronen, geen begrijpelijkheid. "
              "Nul bevindingen bewijst geen heldere tekst.")

    return 0 if len(hard) <= args.baseline else 1


if __name__ == "__main__":
    raise SystemExit(main())
