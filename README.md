# OracleLuck MCP Server — 天啟好運玄學工具

**Remote MCP server** for Chinese metaphysics: daily almanac, BaZi (four pillars), I Ching, tarot, and a searchable knowledge base.

A **remote MCP server** exposing 5 tools over Streamable HTTP (JSON-RPC 2.0). No installation, no API key — just point your MCP client at the URL.

> 🌐 Website: https://www.oracleluck.com
> 📖 Docs: https://www.oracleluck.com/docs/mcp/
> 🔌 Endpoint: `https://www.oracleluck.com/mcp`

---

## Quick start

### Claude Desktop / Claude Code

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "oracleluck": {
      "url": "https://www.oracleluck.com/mcp"
    }
  }
}
```

### Cursor / other remote-MCP clients

```json
{
  "mcpServers": {
    "oracleluck": {
      "url": "https://www.oracleluck.com/mcp"
    }
  }
}
```

### cURL (verify it works)

```bash
curl -X POST https://www.oracleluck.com/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "curl", "version": "1.0"}
    }
  }'
```

Response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {"tools": {"listChanged": false}},
    "serverInfo": {"name": "oracleluck", "version": "1.1.0"}
  }
}
```

---

## Tools

### `get_almanac` — 黃曆查詢

Look up the Chinese almanac for any date: lunar date, year/month/day pillars, solar term, 建除十二神, 六曜, clash, wealth/joy/fortune directions, and lucky hours.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | string | — | Gregorian date `YYYY-MM-DD`. Defaults to today. |

<details>
<summary>Example response</summary>

```json
{
  "date": "2026-11-02",
  "weekday": "一",
  "lunar": "九月廿四",
  "year_gz": "丙午",
  "month_gz": "戊戌",
  "day_gz": "庚辰",
  "rokuyo": "友引",
  "jianchu": "破",
  "jianchu_type": "忌",
  "jianchu_text": "諸事不宜，可破屋壞垣",
  "cai_shen": "正東",
  "xi_shen": "西北",
  "fu_shen": "西南",
  "lucky_hours": [
    {"hour": "辰", "range": "07:00–09:00", "god": "青龍", "lucky": true}
  ]
}
```
</details>

---

### `get_bazi` — 四柱八字排盤

Compute the four pillars from a birth date/time, with ten gods, five-element distribution and day master.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `birth` | string | ✅ | Birth date `YYYY-MM-DD` |
| `time` | string | ✅ | Birth time `HH:MM` (24h) |
| `gender` | string | — | `男` or `女` |
| `name` | string | — | Optional name |

---

### `cast_hexagram` — 易經起卦

Cast a coin-method hexagram. Returns the six lines (yin/yang), upper/lower trigrams and moving line. **Does not include fortune-telling verdicts** — interpretation is left to the caller.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `question` | string | — | The question being asked (recorded only) |

---

### `get_tarot` — 塔羅牌牌義

Look up one of the 78 tarot cards: upright, reversed, love, career and advice.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `card` | string | ✅ | Card slug, e.g. `the-fool`, `ace-of-cups` |

---

### `search_knowledge` — 知識庫全文檢索

Full-text search across the knowledge base (1,400+ articles on Zi Wei, BaZi, I Ching, tarot, dream interpretation, almanac).

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | ✅ | Search query |
| `limit` | integer | — | Max results |

---

## What's behind it

The server is a thin layer over deterministic engines — **the data is computed, not generated**:

| Layer | Detail |
|---|---|
| Calendar | 1,096 days precomputed (2026-01-01 → 2028-12-31): lunar date, solar terms, year/month/day pillars, 六曜 |
| BaZi | Four pillars via standard 60-jiazi; optional true-solar-time correction for 42 cities |
| I Ching | All 64 hexagrams with judgement, line texts and structure |
| Tarot | All 78 cards, upright/reversed/love/career |
| Knowledge base | 3,100+ pages, Traditional Chinese, Simplified Chinese, English, Japanese |

---

## Content policy

OracleLuck is a **cultural reference and self-reflection tool**.

- We do **not** predict events, promise outcomes, or claim any supernatural efficacy.
- We do **not** provide medical, legal, or financial advice.
- Almanac auspicious/inauspicious classifications follow 建除十二神 only — a **simplified** model that may differ from a full 農民曆 (see [method note](https://www.oracleluck.com/method/)).
- Different almanac publishers disagree with each other; that is expected, not a bug.

---

## Technical notes

| Item | Value |
|---|---|
| Transport | Streamable HTTP (POST) |
| Protocol | JSON-RPC 2.0, MCP `2024-11-05` |
| Auth | None (public, read-only) |
| CORS | `Access-Control-Allow-Origin: *` |
| Rate limit | Fair use; please cache responses |

Supported methods: `initialize`, `tools/list`, `tools/call`, `ping`.

---

## Examples

- [`examples/curl.sh`](examples/curl.sh) — every tool via cURL
- [`examples/client.py`](examples/client.py) — minimal Python client (stdlib only)

---

## License

Code and examples in this repository: **MIT**.

The data served by the remote endpoint (almanac, BaZi, hexagrams, tarot texts, knowledge base) is © OracleLuck and provided for personal/reference use. Do not bulk-scrape or redistribute — see https://www.oracleluck.com/terms/

---

**天啟好運 OracleLuck** · https://www.oracleluck.com
