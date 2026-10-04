"""Tests voor scripts/helder-lint.py. Alleen standaardbibliotheek, geen netwerk.

Draai met:  python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

WORTEL = pathlib.Path(__file__).resolve().parent.parent
FIXTURES = WORTEL / "tests" / "fixtures"

_spec = importlib.util.spec_from_file_location("helder_lint", WORTEL / "scripts" / "helder-lint.py")
assert _spec and _spec.loader
lint_mod = importlib.util.module_from_spec(_spec)
# @dataclass zoekt de module in sys.modules; registreer hem vóór het uitvoeren.
sys.modules["helder_lint"] = lint_mod
_spec.loader.exec_module(lint_mod)


def namen(bevindingen) -> list[str]:
    return [b.regelnaam for b in bevindingen]


class TestFixtures(unittest.TestCase):
    def test_goede_tekst_geeft_geen_harde_bevinding(self):
        bevindingen, woorden = lint_mod.lint(FIXTURES / "goed.md", "beschrijvend", False)
        hard = [b for b in bevindingen if b.hard]
        self.assertEqual(hard, [], f"onverwachte bevindingen: {[b.tekst() for b in hard]}")
        self.assertGreater(woorden, 0)

    def test_slechte_tekst_raakt_elke_regel(self):
        bevindingen, _ = lint_mod.lint(FIXTURES / "slecht.md", "beschrijvend", False)
        gevonden = set(namen(bevindingen))
        verwacht = {
            "stijfwoord", "afkorting", "lange-zin", "lijdende-vorm",
            "naamwoordstijl", "werkwoordsgroep", "negatiestapel", "men-vorm",
            "lange-samenstelling", "synoniemrotatie",
        }
        self.assertTrue(verwacht.issubset(gevonden), f"ontbreekt: {verwacht - gevonden}")

    def test_codeblok_en_inline_code_worden_overgeslagen(self):
        bevindingen, _ = lint_mod.lint(FIXTURES / "slecht.md", "beschrijvend", False)
        regels_met_code = {24, 25, 26, 28}  # het bash-blok en de backtick-zin
        for b in bevindingen:
            self.assertNotIn(b.regel, regels_met_code,
                             f"bevinding in code: {b.tekst()}")


class TestRegels(unittest.TestCase):
    def check(self, tekst: str, modus: str = "beschrijvend", advies: bool = False):
        lines = lint_mod.strip_code(tekst.splitlines())
        uit = []
        for regel, kolom, zin in lint_mod.zinnen(lines):
            uit.extend(lint_mod.controleer_zin("t.md", regel, kolom, zin,
                                               lint_mod.ZIN_CAP[modus], advies))
        return namen(uit)

    def test_zinlengte_hangt_af_van_de_modus(self):
        zin = " ".join(["woord"] * 22) + "."
        self.assertNotIn("lange-zin", self.check(zin, "beschrijvend"))
        self.assertIn("lange-zin", self.check(zin, "procedureel"))

    def test_lijdende_vorm_herkent_deelwoord(self):
        self.assertIn("lijdende-vorm", self.check("De aanvraag wordt behandeld."))
        self.assertNotIn("lijdende-vorm", self.check("De dienst behandelt de aanvraag."))

    def test_actieve_zin_met_worden_is_geen_lijdende_vorm(self):
        self.assertNotIn("lijdende-vorm", self.check("De dagen worden korter."))

    def test_naamwoordstijl(self):
        self.assertIn("naamwoordstijl", self.check("Het indienen van het formulier duurt lang."))

    def test_werkwoordsgroep_van_drie(self):
        self.assertIn("werkwoordsgroep", self.check("De premie zou kunnen worden toegekend."))

    def test_negatiestapel_vanaf_twee(self):
        self.assertIn("negatiestapel", self.check("Het is niet uitgesloten dat u niet betaalt."))
        self.assertNotIn("negatiestapel", self.check("U betaalt niet."))

    def test_men_vorm(self):
        self.assertIn("men-vorm", self.check("Men moet het formulier invullen."))
        self.assertNotIn("men-vorm", self.check("De mensen vullen het formulier in."))

    def test_adviesregels_staan_standaard_uit(self):
        self.assertNotIn("leenwoord", self.check("We gaan dit implementeren."))
        self.assertIn("leenwoord", self.check("We gaan dit implementeren.", advies=True))

    def test_afkorting_breekt_de_zin_niet_af(self):
        lines = lint_mod.strip_code(["Stuur o.a. de bijlage mee en vul het formulier in."])
        self.assertEqual(len(list(lint_mod.zinnen(lines))), 1)

    def test_zin_over_meerdere_regels_wordt_samengevoegd(self):
        tekst = "Dit is een " + "heel " * 25 + "lange zin\ndie doorloopt op de tweede regel."
        self.assertIn("lange-zin", self.check(tekst))


class TestCli(unittest.TestCase):
    def test_exitcode_nul_bij_schone_tekst(self):
        self.assertEqual(lint_mod.main([str(FIXTURES / "goed.md")]), 0)

    def test_exitcode_een_bij_bevindingen(self):
        self.assertEqual(lint_mod.main([str(FIXTURES / "slecht.md")]), 1)

    def test_baseline_onderdrukt_de_foutcode(self):
        self.assertEqual(lint_mod.main(["--baseline", "999", str(FIXTURES / "slecht.md")]), 0)

    def test_onbekend_bestand_geeft_code_twee(self):
        self.assertEqual(lint_mod.main([str(FIXTURES / "bestaat-niet.md")]), 2)


if __name__ == "__main__":
    unittest.main()
