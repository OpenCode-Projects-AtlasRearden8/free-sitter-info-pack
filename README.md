# Free Sitter Info Pack

Free, printable packets for the person who saves your week: the **babysitter**, the
**pet sitter**, and the **house sitter**. Fill in one friendly page for each sitter, leave
the packet on the counter, and print a thank-you certificate for when the visit is over.

Everything here is plain HTML/CSS that builds to clean, unbranded, US-Letter PDFs with one
script. No accounts, no websites, no data collection — nothing online at all. Print at
home, hand out, done.

## What you get

Ready-to-print PDFs live in `printables/`:

| PDF | Pages | What it is |
| --- | --- | --- |
| `babysitter-packet.pdf` | 2 | Friendly intro + one-page details sheet: emergency contacts, kids roster, routines, food, house quirks, door-lock notes |
| `pet-sitter-packet.pdf` | 2 | Friendly intro + one-page details sheet: emergency vet numbers, the pet roster, feeding schedule, meds, potty/walks, quirks, locks |
| `house-sitter-packet.pdf` | 2 | Friendly intro + one-page details sheet: emergency contacts, check-in plan, mail/plants/bins, house quirks, door-lock notes |
| `treat-fairness-card.pdf` | 1 | The counter card that keeps kids (and pets) honest about treats, with ground rules and a daily tally |
| `thank-you-certificate.pdf` | 1 | A printable Certificate of Outstanding Sittering for after the visit |

Every packet opens with a warm "leave it on the counter" intro page you can hand to the
sitter as-is, then one page of fill-in fields that covers everything the original
goal promised: emergency contacts, routines, feeding schedules, house quirks,
and door-lock notes.

## How to use them

1. **Print.** US Letter, black and white is fine — the design is ink-friendly.
2. **Fill in together.** Ten minutes with the sitter beats an hour of guessing later.
   Everything the sitter needs ends up on one page.
3. **Leave it on the counter.** Seriously, that is the plan. The packet says so.
4. **Afterward,** print the thank-you certificate and fill in the sitter's name.
   Sitters frame these, and they are right to.

The official US helplines are pre-printed (911, Poison Control 1-800-222-1222, and
ASPCA Animal Poison Control 888-426-4435 for pets). Everything else is blank lines for
*your* house.

## Build it yourself

Requirements: Python 3.10+ with two packages:

```bash
pip install weasyprint pypdf
```

Then run the one build script from the project folder:

```bash
./build.sh
```

That converts every HTML/CSS sheet in `sheets/` into fresh, unbranded PDFs in
`printables/`. Something changed and you want a different output folder? Try
`./build.sh --out /tmp/new-printables`.

### Run the tests

The test suite builds every sheet and verifies each one produces a valid PDF with the
expected page count, plus checks that the PDFs stay unbranded and the sources contain no
secrets:

```bash
pip install pytest
python3 -m pytest tests/
```

## Edit your own copy

The sheets are plain HTML/CSS — no framework, no build system beyond one script:

```
sheets/
├── styles.css                 shared print styling (Letter page, form lines, cards)
├── intro-babysitting.html     "leave it on the counter" intro, babysit variant
├── babysitter.html            the one-page details sheet
├── intro-pet-sitter.html      intro, pet variant
├── pet-sitter.html            details sheet (feeding schedule lives here)
├── intro-house-sitter.html    intro, house variant
├── house-sitter.html          details sheet
├── treat-fairness-card.html   the counter card
└── thank-you-certificate.html the certificate
```

Each packet is built from two files: an intro page and a details sheet, stitched into one
two-page PDF. The important rule is **one page each**: if you edit a sheet, keep it to a
single Letter page — the tests will tell you if content overflows, because the build
fails loudly with a friendly message instead of shipping a surprise third page.

Colors, fonts, and line styles all live in `styles.css`. Fill-in lines are dotted so
handwriting fits.

## Where this fits

The Free Sitter Info Pack is a free printable from **Asdale Dynamics, LLC** — the
publishing home of Dylan Asdale's beginner-friendly AI guides (like *The Massive AI
Manual*) at dylanasdale.github.io. It follows the same spirit as everything there:
plain English, step by step, never condescending — and it works offline.

## Privacy

- Nothing is tracked, uploaded, or collected. There is no server at all.
- The PDFs are unbranded: no logos, no names, no links back here.
- Your filled-in details live on paper in your kitchen, where they belong.

## License

MIT — print it, share it, adapt it. See `LICENSE`.
