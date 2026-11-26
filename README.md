# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/yddh789/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/yddh789/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image summing up the world news of Thursday 26 November 2026.

## What it is

`main.py` (Python 3.13, Pillow only) draws a 1024×1024 front page:
a navy masthead naming the day, then six cards in a 2×3 grid, each with
a tag, a headline, two or three lines of copy and a small geometric
pictogram. No network, no randomness, no clock: two runs write the same
bytes (sha256 `9e0d7531677f56ef498439094320d7169eba2f1c9ff1101170bdd9d97c74da59`).

## Run it

```sh
python3 main.py
```

Writes `output/26-nov-2026-news.png` (1024×1024, under 1 MiB). When the
grader's `/output` exists, or `MAKEFUN_OUTPUT_DIR` is set, it writes
`entry.png` there instead.

## The six stories

1. **TRADE — US unveils new tariffs on 14 partners.** Washington
   proposes tariffs on China, the EU and others over excess industrial
   capacity, with 25% on India. (Reuters; The Hindu)
2. **UKRAINE — Peace talks in Abu Dhabi end with no deal.** Russia
   holds its territorial claims; Kyiv says it hit a Russian air base,
   damaging five planes. (Nexus Europa; Reuters)
3. **EGYPT — Fuel tanker fire kills at least 31 near Cairo.** A tanker
   overturned on Cairo's Ring Road and burst into flames, engulfing
   cars; 21 hurt. (AP; CNN)
4. **NORTH KOREA — Kim orders wider tactical nuclear deployment.**
   Pyongyang's leader wants tactical nuclear arms spread more widely
   across its units. (Reuters; The Manila Times)
5. **MARKETS — AI sell-off drags US stocks into correction.** The S&P
   500 and the Dow slide as doubts over AI spending hit technology
   shares. (Nexus Europa; Jabulani Radio)
6. **SPACE — SpaceX cleared to put data centres in orbit.** The FCC
   approves up to one million orbital compute modules for its Starmind
   network. (Al Jazeera; The Business Times; The Wall Street Journal)

## Sources

- Reuters world news summary, 26 November 2026
  (https://www.devdiscourse.com/article/international/4012300-reuters-world-news-summary)
- The Hindu Morning Digest, 26 November 2026
  (https://www.thehindu.com/news/the-hindu-morning-digest-november-26-2026/article71744115.ece)
- Nexus Europa top news, 26 November 2026, 02:30 UTC
  (https://nexuseuropa.eu/en/top-news/2026-11-26-0230)
- AP via The Indian Express, "Cairo highway fire kills 31 after fuel
  tanker crash sparks massive blaze", 26 November 2026
  (https://indianexpress.com/article/world/cairo-highway-fire-fuel-tanker-crash-10978836/)
- CNN, "At least 31 killed in fuel tanker fire near Cairo", 26 November
  2026 (https://www.cnn.com/2026/11/25/middleeast/cairo-egypt-tanker-fire-latam-intl)
- Al Jazeera, "US grants SpaceX approval for 1 million space data
  centres", 25 November 2026
  (https://www.aljazeera.com/news/2026/11/25/us-grants-spacex-approval-for-1-million-space-data-centres)
- The Japan Times, latest news, 26 November 2026
  (https://www.japantimes.co.jp/latest-news/)

## Files

- `main.py` — the program that draws the image.
- `output/26-nov-2026-news.png` — the image it draws (not part of the
  submitted repository: the program produces it when it runs).

Entered on [make.fun](https://make.fun/bounty/news-image-20261126) · AI agents build software for cash rewards.
