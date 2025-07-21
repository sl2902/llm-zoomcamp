import subprocess
import json

# Start the MCP server (replace with the actual command)
proc = subprocess.Popen(
    ["fastmcp", "run", "weather_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

def send_message(proc, message):
    raw = json.dumps(message)
    content = f"Content-Length: {len(raw)}\r\n\r\n{raw}"
    proc.stdin.write(content)
    proc.stdin.flush()

def read_response(proc):
    # Read headers
    headers = ""
    while True:
        line = proc.stdout.readline()
        if line == "\r\n" or line == "\n":
            break
        headers += line

    # Get content length
    content_length = 0
    for header in headers.splitlines():
        if header.lower().startswith("content-length:"):
            content_length = int(header.split(":")[1].strip())

    # Read the body
    body = proc.stdout.read(content_length)
    return json.loads(body)

# Step 1: Initialize
init_message = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
        "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
}

send_message(proc, init_message)
print("Initialize response:", read_response(proc))

# Step 2: Notify Initialized
initialized_notify = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
send_message(proc, initialized_notify)

# Step 3: List Tools
tools_list = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
}
send_message(proc, tools_list)
print("Tools list:", read_response(proc))

# Step 4: Call a tool (like get_weather)
call_weather = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "get_weather",
        "arguments": {
            "city": "Berlin"
        }
    }
}
send_message(proc, call_weather)
print("Weather response:", read_response(proc))
