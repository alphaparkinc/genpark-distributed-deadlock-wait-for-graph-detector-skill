"""MCP Server wrapper for Distributed Deadlock Detector."""
import json
import sys
from client import DeadlockWaitForGraphDetector

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "detect_deadlock_cycles",
                    "description": "Detect lock dependency cycles in transaction Wait-For-Graphs and select minimal rollback cost victims",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "dependencies": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "from": {"type": "string"},
                                        "to": {"type": "string"},
                                        "cost": {"type": "number"}
                                    },
                                    "required": ["from", "to"]
                                }
                            }
                        },
                        "required": ["dependencies"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        args = req.get("params", {}).get("arguments", {})
        res = DeadlockWaitForGraphDetector.detect_deadlocks(args.get("dependencies", []))
        return {
            "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
        }
    return {}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            try:
                r = json.loads(line)
                out = handle_request(r)
                print(json.dumps(out), flush=True)
            except Exception as e:
                print(json.dumps({"error": str(e)}), flush=True)
