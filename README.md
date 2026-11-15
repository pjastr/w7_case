# Wykład 7 – kody ze slajdów jako projekt PyCharm

Przykłady z wykładu 7 (testowanie w oparciu o tablice decyzyjne) jako uporządkowany projekt testów:
reguły biznesowe i pomocnicze funkcje w `src/`, testy w `tests/`, przykłady do uruchamiania ręcznie
w `examples/`. Kod (nazwy, komentarze) jest po angielsku, jak w ćwiczeniach. Identyfikatory SklepTO
(`#wartosc`, `#karta`, `dostawa-kurier`, komunikaty) są częścią aplikacji i zostają po polsku.

Część testów nie potrzebuje przeglądarki (reguły z tablic decyzyjnych w czystym Pythonie), część
sprawdza kalkulator SklepTO przez Selenium (znacznik `ui`).

## Struktura

```text
w7_case/
├── pyproject.toml          # pytest: testpaths, pythonpath = src, znacznik ui, xfail_strict
├── requirements.txt        # przypięte wersje: selenium, pytest, pytest-html, allpairspy
├── .gitignore              # .venv, cache, reports/, .idea
├── src/
│   ├── rules/                    # reguły i tablice – bez przeglądarki
│   │   ├── discount.py           # rabat z podręcznika: karta, kwota > 1000 zł, zakupy ≤ 30 dni
│   │   ├── scholarship.py        # przykład 1: stypendia (Decimal zamiast float)
│   │   ├── decision_table.py     # „–” (DONT_CARE), full_table(), expand(), check_minimised()
│   │   └── pairwise.py           # uncovered_pairs() – które pary wartości nie są pokryte
│   └── webtests/                 # Selenium i kalkulator SklepTO
│       ├── config.py             # SKLEPTO_URL, SELENIUM_WEB_URL, headless(), WINDOW_SIZE, TIMEOUT
│       ├── browser.py            # create_driver() – te same opcje dla wszystkich testów
│       ├── locators.py           # CalculatorPage, WebFormPage – lokalizatory w jednym miejscu
│       ├── calculator.py         # klasa Calculator (open, fill, calculate, result), calculator_url()
│       ├── calculator_tables.py  # tablice kalkulatora jako dane: R1–R8, E1–E5
│       └── assertions.py         # check_actions() – wszystkie różnice akcji naraz
├── tests/
│   ├── conftest.py               # --headless, driver (session), calculator, zrzut przy porażce
│   ├── test_discount_rule.py     # tablica jako lista krotek, ids, pytest.param, pełna tablica, AWB
│   ├── test_minimization.py      # połowienie, „–”, luki i nakładanie, ryzyko minimalizacji
│   ├── test_scholarship.py       # przykład 1: TC1–TC7
│   ├── test_pairwise.py          # 4 testy dla 3 warunków, allpairspy (4 × 3 wartości)
│   ├── test_check_actions.py     # check_actions() – raport wszystkich różnic
│   ├── test_form_controls.py     # pole tekstowe, checkbox, radio, select, wysłanie i czekanie   (ui)
│   ├── test_calculator_table.py  # pełna tablica kalkulatora R1–R8 przez formularz               (ui)
│   ├── test_delivery.py          # wpisy rozszerzone: sposób dostawy E1–E5                       (ui)
│   ├── test_threshold_bva.py     # AWB progu 200,00 zł i zakresu wartości                       (ui)
│   ├── test_discount_code.py     # klasy kodu rabatowego                                         (ui)
│   └── test_get_vs_ui.py         # te same reguły przez adres GET + pomiar czasu UI / URL        (ui)
└── examples/                     # uruchamiane ręcznie, nie są zbierane przez python -m pytest
    ├── generate_full_table.py          # itertools.product: połowienie i drzewo 2 × 3 × 2
    ├── pairwise_allpairspy.py          # allpairspy: 4 parametry × 3 wartości
    ├── failing_rule_demo.py            # „Który wiersz tablicy padł?” + xfail przy regule
    └── anti_pattern_copied_oracle.py   # antywzorzec: wyrocznia skopiowana z implementacji
```

## Przygotowanie SklepTO

1. XAMPP: **Start** przy Apache i MySQL.
2. Folder aplikacji `sklepto` (z materiałów do zajęć) skopiowany do `xampp\htdocs\sklepto`.
3. `http://localhost/sklepto/kalkulator.php` otwiera kalkulator. Inny port: zmienna `SKLEPTO_URL` (niżej).

Kalkulator nie zapisuje nic w bazie – testy nie resetują danych. Test listy rozwijanej korzysta
ze strony Selenium Web Form (`https://www.selenium.dev/selenium/web/web-form.html`), więc wymaga internetu.

## Otwarcie w PyCharm

1. **File ▸ Open…** → folder `w7_case` → *Trust Project*.
2. **Settings ▸ Python ▸ Interpreter ▸ Add Interpreter ▸ Add Local Interpreter**:
   *Virtualenv*, nowe `.venv` w folderze projektu, Python 3.14.
3. Terminal PyCharm (PowerShell): `pip install -r requirements.txt`
4. **Settings ▸ Tools ▸ Python Integrated Tools**: *Default test runner* = **pytest**.
5. Prawy klik na `src` ▸ **Mark Directory as ▸ Sources Root**,
   na `tests` ▸ **Mark Directory as ▸ Test Sources Root**.

Sterownika nie trzeba instalować – pobiera go Selenium Manager.

## Uruchomienie

Polecenia dla terminala PyCharm (PowerShell), z folderu `w7_case`. Kopiuj je z bloku poniżej:
podgląd Markdown w tabelach potrafi zamienić cudzysłów na `&quot;`.

```powershell
# wszystkie testy (90 testów, ok. 30 s)
python -m pytest

# tylko testy bez przeglądarki (reguły, minimalizacja, pairwise) – ułamek sekundy
python -m pytest -m "not ui"

# tylko testy z przeglądarką
python -m pytest -m ui

# bez okna przeglądarki – w nagłówku wyniku: "headless: yes"
python -m pytest --headless

# jedna reguła tablicy (diagnoza)
python -m pytest -k R3 -v

# raport HTML (wtyczka pytest-html) – plik report.html w folderze projektu
python -m pytest --html=report.html --self-contained-html

# czasy UI i URL – wydruk z testu (-rP pokazuje print zaliczonych testów)
python -m pytest tests/test_get_vs_ui.py -rP

# inny port XAMPP
$env:SKLEPTO_URL = "http://localhost:8080/sklepto"
python -m pytest
```

Przykłady z `examples/` uruchamia się ręcznie, każdy osobno:

```powershell
python examples/generate_full_table.py
python examples/pairwise_allpairspy.py
python -m pytest examples/failing_rule_demo.py -v
python -m pytest examples/anti_pattern_copied_oracle.py -v
```

Zmienna ustawiona w terminalu działa **tylko** dla poleceń wpisanych w tym terminalu.
Testy uruchamiane zieloną strzałką PyCharm jej nie widzą – tam:

- **Run ▸ Edit Configurations…** ▸ konfiguracja pytest ▸ *Additional Arguments*: `--headless`
  albo *Environment variables*: `HEADLESS=1`
- dla wszystkich nowych konfiguracji: **Edit configuration templates…** ▸ *Python tests* ▸ *pytest* – to samo

Zmienne środowiskowe projektu: `SKLEPTO_URL`, `SELENIUM_WEB_URL`, `HEADLESS` (`1` = bez okna),
`WINDOW_SIZE`, `TIMEOUT`.

## Kolejność omawiania plików (zgodnie z wykładem)

Na wykładzie warto mieć otwarte obok siebie slajdy i PyCharm. Kolejność kroków = kolejność slajdów.

### Blok 1 – Tablice decyzyjne: podstawy

| Krok | Slajdy | Plik / test | Co pokazać |
|---|---|---|---|
| 1 | Reguła biznesowa = implikacja, budowa tablicy, przykład: rabat w sklepie | `src/rules/discount.py` | trzy warunki i jedna akcja; każda gałąź `if` = reguła z tablicy |
| 2 | Przykład wpisów rozszerzonych | `src/webtests/calculator_tables.py` (`DELIVERY_TABLE`), `tests/test_delivery.py` | sposób dostawy = jeden warunek z trzema wartościami |

### Blok 2 – Kombinacje warunków

| Krok | Slajdy | Plik / test | Co pokazać |
|---|---|---|---|
| 3 | Ile jest kolumn?, systematyczne wypełnianie, drzewo kombinacji | `examples/generate_full_table.py` | uruchomić: wzór T/N „połowienia” i 12 liści drzewa |
| 4 | Pojęcie: iloczyn kartezjański | `src/rules/decision_table.py` (`full_table`), `test_minimization.py::test_full_table_halving_order` | `itertools.product` generuje **warunki** |

### Blok 3 – Minimalizacja tablicy

| Krok | Slajdy | Plik / test | Co pokazać |
|---|---|---|---|
| 5 | Minimalizacja krok po kroku, kontrola poprawności, kontrola w kodzie | `src/rules/decision_table.py` (`DONT_CARE`, `expand`, `check_minimised`), `tests/test_minimization.py` | „–” rozwija się na 2 kolumny; luka i nakładanie wykrywane automatycznie |
| 6 | Minimalizacja – ryzyko | `test_minimization.py::test_implementation_agrees_with_every_hidden_column` | sprawdzamy **każdą** kolumnę ukrytą za „–” |

### Blok 4 – Pokrycie i przypadki testowe

| Krok | Slajdy | Plik / test | Co pokazać |
|---|---|---|---|
| 7 | Przypadki testowe – rabaty, łączenie z EP i AWB | `tests/test_discount_rule.py` (`test_full_table`, `test_amount_threshold_bva`) | warunki z `product`, akcje ręcznie; granica 1000,00 / 1000,01 |
| 8 | Przykład: próg darmowej dostawy, ile testów łącznie? | `tests/test_threshold_bva.py` | 199,99 / 200,00 / 200,01 i przecinek; próg bez karty |
| 9 | Pojęcie: liczby zmiennoprzecinkowe i zaokrąglanie | `src/webtests/calculator_tables.py` (kwoty jako tekst), `src/rules/scholarship.py` (`Decimal`) | dlaczego oczekiwane kwoty są napisami |

### Blok 5 – Przykłady rozpisane

| Krok | Slajdy | Plik / test | Co pokazać |
|---|---|---|---|
| 10 | Przykład 1: stypendium – tablica i dane z AWB | `src/rules/scholarship.py`, `tests/test_scholarship.py` | TC1–TC7 z id kolumn (`TC2-S2` …) |
| 11 | Przykład 3: kalkulator SklepTO – wymagania | `src/webtests/calculator_tables.py` (`FULL_TABLE`) | pełna tablica R1–R8 jako dane; komentarz T/N przy każdej kolumnie |

### Blok 6 – Alternatywy przy wielu warunkach

| Krok | Slajdy | Plik / test | Co pokazać |
|---|---|---|---|
| 12 | Pojęcie: operatory logiczne, grafy przyczynowo-skutkowe | `src/rules/discount.py` | `and` / `or` w regułach |
| 13 | Pairwise – przykład, pojęcie: jak sprawdzić pokrycie par | `src/rules/pairwise.py`, `tests/test_pairwise.py` | 4 testy pokrywają wszystkie pary, ale pomijają (T,T,N) |
| 14 | Pairwise – narzędzia | `examples/pairwise_allpairspy.py` | uruchomić: 9 testów zamiast 81 |

### Blok 7 – Implementacja w pytest

| Krok | Slajdy | Plik / test | Co pokazać |
|---|---|---|---|
| 15 | Tablica jako lista krotek, test parametryzowany | `tests/test_discount_rule.py` (`DISCOUNT_TABLE`, `test_discount`) | kolumna tablicy = krotka; `ids` = numery kolumn |
| 16 | pytest.param – identyfikator przy danych | `test_discount_rule.py` (`DISCOUNT_PARAMS`), `examples/failing_rule_demo.py` | id obok danych; `xfail` przy jednej regule |
| 17 | Który wiersz tablicy padł?, raport z testów, wtyczki | `examples/failing_rule_demo.py`; `--html`, `-rf`, `-k R3` | uruchomić: `test_discount[R3]` FAILED, raport HTML |
| 18 | Asercja wielu akcji | `tests/test_calculator_table.py` | jedna asercja na krotce (rabat, dostawa, kwota) |
| 19 | Wiele akcji – zbieranie niezgodności, pojęcie: `!r` | `src/webtests/assertions.py`, `tests/test_check_actions.py`, `tests/test_delivery.py` | wszystkie różnice w jednym komunikacie |
| 20 | Wyrocznia: nie kopiuj logiki, pojęcie: wyrocznia testowa | `examples/anti_pattern_copied_oracle.py` | uruchomić: kopia wzoru przechodzi, test z wymagań wykrywa błąd |

### Blok 8 – Selenium: kontrolki formularza

| Krok | Slajdy | Plik / test | Co pokazać |
|---|---|---|---|
| 21 | Pole tekstowe, checkbox, radio, kontrolki w konsoli | `tests/test_form_controls.py` (`test_text_field_…`, `test_checkbox_…`, `test_radio_group`) | `clear()`, `is_selected()`, `:checked`; stan po przeładowaniu |
| 22 | Lista rozwijana (select), lista w konsoli | `test_form_controls.py::test_select_on_web_form`, `src/webtests/locators.py` (`WebFormPage`) | `Select`, `first_selected_option` |
| 23 | Wysłanie formularza i oczekiwanie | `test_form_controls.py::test_submit_and_wait_for_new_page` | `staleness_of` – czekanie na nową stronę |
| 24 | Klasa pomocnicza, pojęcie: interfejs płynny | `src/webtests/calculator.py`, fixture `calculator` w `tests/conftest.py` | `open().fill().calculate()`; metody zwracają `self` |
| 25 | Test przez UI czy przez URL?, adres w DevTools, pomiar czasu | `calculator.py` (`calculator_url`), `tests/test_get_vs_ui.py` | te same wyniki, ok. 10 razy szybciej przez adres |
| 26 | Typowe błędy | `reports/screenshots/` (po nieudanym teście UI) | zrzut ekranu przy porażce |

## Dobre praktyki zastosowane w projekcie

| Praktyka | Gdzie |
|---|---|
| Układ `src/` + `tests/`; przykłady i antywzorce poza zbieranymi testami | struktura, `pyproject.toml` |
| Reguły biznesowe testowane **bez przeglądarki**; UI tylko dla kalkulatora | `src/rules/`, znacznik `ui` |
| Tablica decyzyjna jako **dane**; kolumna = krotka z komentarzem T/N; id = numer kolumny | `calculator_tables.py`, `test_discount_rule.py` |
| Akcje oczekiwane wpisane ręcznie z wymagań; `itertools.product` tylko dla warunków | `calculator_tables.py`, `test_discount_rule.py` |
| Kwoty jako tekst (dokładnie to, co pokazuje strona); `Decimal` przy liczeniu w teście | `calculator_tables.py`, `scholarship.py` |
| Automatyczna kontrola minimalizacji (2ⁿ) i sprawdzenie kolumn ukrytych za „–” | `decision_table.py`, `test_minimization.py` |
| Wszystkie akcje reguły w jednej asercji (krotka) lub z raportem wszystkich różnic | `test_calculator_table.py`, `assertions.py` |
| Formularz obsługiwany w jednym miejscu (klasa pomocnicza, interfejs płynny) | `calculator.py` |
| Lokalizatory jako stałe; nazwy po angielsku, wartości z aplikacji | `locators.py` |
| Po wysłaniu formularza czekamy na nową stronę (`staleness_of`) | `Calculator.calculate()` |
| Adres GET budowany przez `urlencode()` – bez ręcznego sklejania | `calculator_url()` |
| Jedna przeglądarka na przebieg (`session`) – kalkulator nie przechowuje stanu | `tests/conftest.py` |
| Zrzut przy porażce testu UI: `reports/screenshots/<test>.png` | `tests/conftest.py` |

## Pojęcia nowe względem wcześniejszych wykładów – gdzie są w kodzie

| Pojęcie | Slajd | W projekcie |
|---|---|---|
| iloczyn kartezjański, `itertools.product` | Pojęcie: iloczyn kartezjański | `decision_table.full_table`, `examples/generate_full_table.py` |
| „–” (*don't care*), rozwijanie reguły, kontrola 2ⁿ | Kontrola minimalizacji w kodzie | `decision_table.expand`, `check_minimised` |
| liczby zmiennoprzecinkowe, zaokrąglanie, `Decimal` | Pojęcie: liczby zmiennoprzecinkowe i zaokrąglanie | `scholarship.py`, kwoty jako tekst |
| operatory ORAZ / LUB / NIE, prawo De Morgana | Pojęcie: operatory logiczne | `discount.py` |
| tablica pokrywająca, `itertools.combinations` | Pojęcie: jak sprawdzić pokrycie par? | `pairwise.uncovered_pairs`, `test_pairwise.py` |
| wtyczka pytest, opcje `-r`, `-k` a znaczniki | Pojęcie: wtyczki i opcje raportu pytest | `requirements.txt` (pytest-html), `pyproject.toml` (`-ra`) |
| porównanie krotek, `!r`, lista z warunkiem | Pojęcie: porównanie krotek, `!r` i lista z warunkiem | `assertions.check_actions` |
| wyrocznia testowa | Pojęcie: wyrocznia testowa | `calculator_tables.py`, `test_ui_and_url_give_the_same_results` |
| interfejs płynny (`return self`) | Pojęcie: interfejs płynny | `calculator.py` |
| `time.perf_counter`, `*_` przy rozpakowaniu | UI czy URL – pomiar czasu | `test_get_vs_ui.py` |
| znacznik (*marker*) i wybór `-m` | – (README) | `pytestmark = pytest.mark.ui`, `pyproject.toml` |

## Uwagi

- **`-m "not ui"`** – tu cudzysłów jest potrzebny (wyrażenie ze spacją). Kopiuj polecenie z bloku
  kodu, nie z tabeli.
- **`itertools.product` w `parametrize`** – od pytest 9 przekazanie iteratora jest przestarzałe
  (ostrzeżenie `PytestRemovedIn10Warning`); dlatego w kodzie jest `list(product(…))`.
- **`-k` dopasowuje też znaczniki** – `-k param` wybierze każdy test z `@pytest.mark.parametrize`.
  Do wyboru jednego pliku lub funkcji lepiej podać ścieżkę: `tests/test_discount_rule.py::test_discount`.
- **Selenium Web Form** jest na stronie selenium.dev – bez internetu `test_select_on_web_form` nie
  przejdzie; inny adres: zmienna `SELENIUM_WEB_URL`.
- **Czas UI i URL** zależy od komputera; wydruk pokazuje `-rP` (przy sprawdzaniu: ok. 6 s i 0,6 s).

Sprawdzone na: Python 3.13, Selenium 4.49.0, pytest 9.1.1, pytest-html 4.2.0, allpairspy 2.5.1,
Chrome 153, SklepTO 1.0 (PHP 8.3 + MariaDB 10.11).
