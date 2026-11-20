# One Page of World News — Friday 20 November 2026

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Arifpratama19/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Arifpratama19/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

This is my entry for the make.fun bounty **"Sum up 20 November's world news in one image"**
(`news-image-20261120`). It is a small Python program that draws a
newspaper front page for Friday 20 November 2026 and saves it as a single
1024x1024 PNG. There are no photos and no downloaded assets: every pixel,
every letter and the PNG file itself are produced by code in `main.py`,
using only the Python standard library.

## What is on the page

The masthead names the day in a black bar — **FRIDAY 20 NOVEMBER 2026** —
so the picture says which day it sums up. The stories, all checked against
news reports from 20 November 2026:

- **Lead story — missiles rain on Kyiv hours after a peace summit.**
  Russia launched a massive overnight missile and drone attack on Ukraine
  lasting more than six hours. At least five people were killed (three in
  Kyiv, two in Lviv) and three bridges over the Dnipro were damaged. It
  came hours after Presidents Trump, Xi and Putin met in Shenzhen and
  signed a joint peace declaration. (CNN, OneTurn, The Hindu)
- **Markets — AI sell-off goes global.** The Nikkei fell 5.1%, the Kospi
  4.7%, Taiwan 6.6%, the S&P 500 2.0% and the Dow 2.2%. Anthropic closed
  up 17% at $97.17 on its Nasdaq debut, but that did not stop the slide.
  (Wall Street Journal, Tickmill, NordFX)
- **Justice — court: Myanmar committed genocide.** The World Court ruled
  Myanmar committed genocide against the Rohingya, by nine votes to six —
  the first such finding against a state by the court. (OneTurn, The Hindu)
- **Ukraine — UK pledges 1,000 drones for Ukraine.** Britain pledged more
  than 1,000 drones in a 260 million pound package, announced in Berlin.
  (AppiSToS)
- **Asia — North Korea fires missile to sea.** North Korea launched a
  ballistic missile towards the Sea of Japan, South Korea's military said.
  (The Munich Eye)
- **Middle East — Houthi missile hits Riyadh tower.** A Houthi missile
  damaged a skyscraper in Riyadh's financial district, including the
  sovereign wealth fund tower. (OneTurn, EIN Presswire)
- **Sport — Texans 26, Colts 3.** Houston beat Indianapolis on Thursday
  Night Football; C.J. Stroud threw three touchdown passes. (Sportradar,
  Yardbarker)
- **Also in the news —** Trump pardoned Pete Rose, the late baseball star;
  Spain held a general strike that hit ports and factories. (AppiSToS,
  The Munich Eye)

Nothing on the page is invented: every number and claim above comes from
one of the sources named, and anything I could not verify was left out.

## How to run it

Requires Python 3.12 or newer. No extra packages, no network access, no
input files.

```sh
python3 main.py
```

That writes the picture to `$MAKEFUN_OUTPUT_DIR/entry.png`, or to
`./output/entry.png` when that variable is not set. The run takes about
half a second. The output is fully deterministic — no randomness, no clock
— so running it twice gives a byte-identical file.

## Files

- `main.py` — the whole entry: a hand-written raster canvas, a hand-written
  5x7 bitmap font, the front-page layout, and a hand-written PNG encoder.
- `entry.png` — the finished picture, produced by running `main.py`.
- `README.md` — this file.
- `LICENSE` — MIT.

## License

MIT — see `LICENSE`.
