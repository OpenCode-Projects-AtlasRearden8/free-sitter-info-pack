# STATUS — Free Sitter Info Pack

Last updated: 2026-10-27. State: working, tested, committed.

## What was built

A free, offline, printable sitter-packet project. Plain HTML/CSS sheets build to clean,
unbranded, US-Letter PDFs through one build script. There is no website, no signup, and
nothing online — print at home and leave the packet on the counter.

Deliverables in `printables/`:

| PDF | Pages | Covers |
| --- | --- | --- |
| `babysitter-packet.pdf` | 2 | Intro page + babysitter details sheet: emergency contacts, kids roster, routines, food & feeding, house quirks, door-lock notes |
| `pet-sitter-packet.pdf` | 2 | Intro page + pet sitter details sheet: emergency vet numbers, roster, feeding schedule, meds, potty/walks, house quirks, door-lock notes |
| `house-sitter-packet.pdf` | 2 | Intro page + house sitter details sheet: emergency contacts, check-in plan, mail/plants/bins, house quirks, door-lock notes |
| `treat-fairness-card.pdf` | 1 | Counter card with treat ground rules, bonus-treat log, and a daily fairness tally |
| `thank-you-certificate.pdf` | 1 | Certificate of Outstanding Sittering to fill in after the visit |

Each packet opens with a friendly "leave it on the counter" intro page, followed by the
one-page details sheet the original goal asked for. Official US helplines (911, Poison
Control 1-800-222-1222, ASPCA Pet Poison 888-426-4435) are pre-printed; all household
details are fill-in lines.

Project files:

- `sheets/` — 8 HTML sources + shared `styles.css` (open them in any text editor)
- `build.py` + `build.sh` — the one build script (WeasyPrint renders, pypdf stitches
  the two pages of each packet into one PDF)
- `tests/test_build.py` — the test suite
- `printables/` — the built, unbranded PDFs
- `README.md`, `LICENSE` (MIT, Asdale Dynamics, LLC)

## How to run it

```bash
pip install weasyprint pypdf     # the only requirements
./build.sh                       # rebuilds every PDF into printables/
python3 -m pytest tests/         # runs the full test suite
```

`./build.sh --out SOME_DIR` builds into a custom folder instead of `printables/`.

## Verification results

Run on 2026-10-27, from a clean `rm -rf printables` state:

- `./build.sh` — success. 5/5 PDFs built, each passing its internal page-count
  assertion (2/2/2/1/1 pages).
- `python3 -m pytest tests/` — **15 passed, 0 failed** in ~15 s.

What the tests verify:

1. All 8 HTML sheets are present, named consistently.
2. Every sheet individually renders to a valid PDF (`%PDF-` header, parseable by
   pypdf, extractable text, key sheet wording present).
3. The full CLI build produces exactly the 5 expected PDFs.
4. Each PDF has its exact expected page count and a neutral metadata title.
5. Packet page 1 is the intro ("leave this packet on the counter", correct variant)
   and page 2 is the matching details sheet.
6. The treat card contains ground rules + tally; the certificate contains its title
   and signature block.
7. All PDFs are unbranded: no "Asdale", "Dylan", or "Dynamics" in any text layer or
   metadata.
8. No secrets patterns in any source file.

Visual check: all 8 pages rendered to PNG and reviewed by eye — two-column layout on
the details sheets holds, fill-in lines are legible at print size, the card and
certificate are vertically centered on the page.

## Known gaps

- **US Letter only.** US Letter (612 x 792 pt) is hardcoded in `@page`; A4 users can
  change one line in `sheets/styles.css` (`size: letter` → `size: A4`).
- **English only.** Sheet copy is not translated or localized.
- **Hand-drawn testing only.** Tests validate PDF structure and text; they cannot
  judge aesthetics. Pages were visually reviewed once, not on every font platform.
- **Fill-in is on paper by design.** There is no PDF form-field/acroform version;
  the dotted lines are meant for pen.
- **No CI.** Nothing online, so there is no hosted test run; run
  `python3 -m pytest tests/` locally after any edit.
- **Fonts fall back.** The design names Nimbus/Palatino-esque stacks with generic
  serif/sans fallbacks; on a machine without those exact fonts the look shifts
  slightly but the layout and tests hold.

License: MIT, Copyright (c) 2026 Asdale Dynamics, LLC. Nothing here collects data,
talks to a server, or wraps printing in a signup.
