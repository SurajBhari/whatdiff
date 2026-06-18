# WhatDiff

A minimal webpage change-monitor. Run it on a schedule ([cron](https://en.wikipedia.org/wiki/Cron)) and it compares each configured page against its last-known state, reporting a line-by-line diff whenever something changes.

Use it to watch a product page, a news article, a blog post, a price, a "back in stock" label — anything on the web.

> **WIP:** this is a small work-in-progress script.

## Configure

Create `config.json` with one entry per page you want to watch:

```json
[
  {
    "url": "https://example.com",
    "selector": {
      "type": "id",
      "value": "idofelement",
      "count": 0
    }
  }
]
```

- `url` — the page to monitor.
- `selector.type` / `selector.value` — which element to track (e.g. an element `id`).
- `selector.count` — which match to use when the selector returns several (0-based).

## Run

```bash
pip install requests beautifulsoup4
python main.py
```

The first run records the current state into a `data/` folder; subsequent runs compare against it and print a unified diff of what changed. Schedule it with cron to monitor continuously, e.g.:

```cron
*/30 * * * * cd /path/to/whatdiff && python3 main.py
```
