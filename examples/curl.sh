#!/usr/bin/env bash
# OracleLuck MCP server — cURL examples
# Endpoint: https://www.oracleluck.com/mcp
set -euo pipefail

MCP="https://www.oracleluck.com/mcp"
H1="Content-Type: application/json"
H2="Accept: application/json, text/event-stream"

echo "=== 1. initialize ==="
curl -s -X POST "$MCP" -H "$H1" -H "$H2" -d '{
  "jsonrpc": "2.0", "id": 1, "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "curl-example", "version": "1.0"}
  }
}' | head -c 400
echo; echo

echo "=== 2. tools/list ==="
curl -s -X POST "$MCP" -H "$H1" -H "$H2" -d '{
  "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
}' | head -c 600
echo; echo

echo "=== 3. get_almanac (today) ==="
curl -s -X POST "$MCP" -H "$H1" -H "$H2" -d '{
  "jsonrpc": "2.0", "id": 3, "method": "tools/call",
  "params": {"name": "get_almanac", "arguments": {}}
}' | head -c 500
echo; echo

echo "=== 4. get_almanac (specific date) ==="
curl -s -X POST "$MCP" -H "$H1" -H "$H2" -d '{
  "jsonrpc": "2.0", "id": 4, "method": "tools/call",
  "params": {"name": "get_almanac", "arguments": {"date": "2026-11-02"}}
}' | head -c 500
echo; echo

echo "=== 5. get_bazi ==="
curl -s -X POST "$MCP" -H "$H1" -H "$H2" -d '{
  "jsonrpc": "2.0", "id": 5, "method": "tools/call",
  "params": {"name": "get_bazi", "arguments": {
    "birth": "1990-05-15", "time": "14:30", "gender": "男"
  }}
}' | head -c 700
echo; echo

echo "=== 6. cast_hexagram ==="
curl -s -X POST "$MCP" -H "$H1" -H "$H2" -d '{
  "jsonrpc": "2.0", "id": 6, "method": "tools/call",
  "params": {"name": "cast_hexagram", "arguments": {"question": "Should I change jobs?"}}
}' | head -c 500
echo; echo

echo "=== 7. get_tarot ==="
curl -s -X POST "$MCP" -H "$H1" -H "$H2" -d '{
  "jsonrpc": "2.0", "id": 7, "method": "tools/call",
  "params": {"name": "get_tarot", "arguments": {"card": "the-fool"}}
}' | head -c 500
echo; echo

echo "=== 8. search_knowledge ==="
curl -s -X POST "$MCP" -H "$H1" -H "$H2" -d '{
  "jsonrpc": "2.0", "id": 8, "method": "tools/call",
  "params": {"name": "search_knowledge", "arguments": {"query": "紫微 天府", "limit": 3}}
}' | head -c 600
echo
