# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/xuanyang667-boop/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/xuanyang667-boop/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up the world's news of Thursday 19 November 2026: the
International Court of Justice finding Myanmar guilty of genocide against
the Rohingya, the Trump–Xi–Putin "Declaration toward Peace" in Shenzhen,
Anthropic's record $83 IPO, unrest in Bangladesh, COP31 in Antalya, tanker
attacks in the Strait of Hormuz, and Denmark ratifying the Greenland–US
security pact. Drawn as a newspaper front page, "The World in One Image".

The program is `main.py` (Python 3.13, standard library only). It copies
the front page, `assets/entry.png`, to `/output/entry.png`. No network, no
randomness, no timestamps: two runs write byte-identical output. The image
is drawn by `make_image.py` (Pillow) from the day's reported news.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=hp6ck4g0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
