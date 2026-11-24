# The World in One Page — 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Tenguu0/news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Tenguu0/news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124)

A make.fun entry for
[news-image-20261124](https://make.fun/bounty/news-image-20261124):
a program that writes the world's news of Tuesday 24 November 2026 as
one newspaper front page — Iran's strikes on US bases in Bahrain and
the widening Gulf war, 15 dead in the Kyiv region as Ukraine's fifth
war winter begins, the COP31 climate collapse fallout, the world
court's historic Myanmar genocide ruling, the first Xi–Trump–Putin
trilateral in Shenzhen, and Alcaraz's first ATP Finals title — plus
a MEANWHILE strip (Amtrak derails in Louisiana, Waymo's freeway
pause, Sudan drone strikes, the Thai–Cambodia truce).

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

It writes `out/entry.png` (1024x1024 PNG). Python 3.12+, standard
library only — no network, no randomness, no clock, so every run
writes the same bytes.

## How it works

`entry.png` was composed by `build_page.py` (PIL + DejaVu fonts): a
newsprint masthead with the date in full, a picture-led lead (the
lead illustration is an AI-generated editorial image held in this
repo as `lead.webp`; every word on the page is typeset crisply by
PIL, never by the image model), flat pictograms for the other
stories, and a MEANWHILE strip. `main.py` is the entry program: it
copies the composed image to the output directory. The stories and
their sources are listed in `NEWS.md`.
