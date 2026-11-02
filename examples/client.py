#!/usr/bin/env python3
"""Minimal OracleLuck MCP client — stdlib only, no dependencies.

Usage:
    python3 client.py                    # run all demos
    python3 client.py almanac 2026-11-02 # almanac for a date
    python3 client.py bazi 1990-05-15 14:30
    python3 client.py tarot the-fool
    python3 client.py search "紫微"
"""
import json
import sys
import urllib.request

MCP_URL = "https://www.oracleluck.com/mcp"
_id = 0


def rpc(method, params=None):
    """Send one JSON-RPC request to the MCP endpoint."""
    global _id
    _id += 1
    payload = {"jsonrpc": "2.0", "id": _id, "method": method, "params": params or {}}
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": "oracleluck-mcp-example/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def call_tool(name, arguments):
    """Call a tool and return its parsed text payload."""
    res = rpc("tools/call", {"name": name, "arguments": arguments})
    content = res.get("result", {}).get("content") or []
    for c in content:
        if c.get("type") == "text":
            txt = c.get("text") or ""
            try:
                return json.loads(txt)
            except json.JSONDecodeError:
                return txt
    return res


def main():
    # 1) handshake
    init = rpc("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "python-example", "version": "1.0"},
    })
    info = init.get("result", {}).get("serverInfo", {})
    print("server:", info.get("name"), "v" + str(info.get("version")))
    print()

    # 2) list tools
    tools = rpc("tools/list").get("result", {}).get("tools") or []
    print("tools (%d):" % len(tools))
    for t in tools:
        print("  -", t["name"], "—", (t.get("description") or "")[:60])
    print()

    # 3) CLI mode
    args = sys.argv[1:]
    if args:
        cmd = args[0]
        if cmd == "almanac":
            d = args[1] if len(args) > 1 else None
            out = call_tool("get_almanac", {"date": d} if d else {})
        elif cmd == "bazi":
            out = call_tool("get_bazi", {
                "birth": args[1], "time": args[2],
                "gender": args[3] if len(args) > 3 else "男",
            })
        elif cmd == "tarot":
            out = call_tool("get_tarot", {"card": args[1]})
        elif cmd == "search":
            out = call_tool("search_knowledge", {"query": args[1], "limit": 3})
        elif cmd == "hexagram":
            out = call_tool("cast_hexagram", {"question": " ".join(args[1:])})
        else:
            print("unknown command:", cmd)
            return 1
        print(json.dumps(out, ensure_ascii=False, indent=2)[:2000])
        return 0

    # 4) demo: almanac for today
    print("=== get_almanac (today) ===")
    a = call_tool("get_almanac", {})
    if isinstance(a, dict):
        print("  date:   ", a.get("date"), a.get("weekday"))
        print("  lunar:  ", a.get("lunar"))
        print("  pillar: ", a.get("year_gz"), a.get("month_gz"), a.get("day_gz"))
        print("  jianchu:", a.get("jianchu"), a.get("jianchu_text"))
        print("  wealth: ", a.get("cai_shen"))
    print()

    print("=== get_bazi ===")
    b = call_tool("get_bazi", {"birth": "1990-05-15", "time": "14:30", "gender": "男"})
    if isinstance(b, dict):
        for k, v in (b.get("pillars") or {}).items():
            print("  %s: %s" % (k, v.get("ganzhi")))
        print("  day master:", (b.get("day_master") or {}).get("stem"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
