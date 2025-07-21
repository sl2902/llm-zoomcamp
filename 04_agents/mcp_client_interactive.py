"""
Interactive MCP client - lets you test individual commands
"""
import subprocess
import json
import sys
import threading
import queue

class InteractiveMCPClient:
    def __init__(self, server_script):
        self.server_process = subprocess.Popen(
            [sys.executable, server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        
        self.request_id = 0
        self.response_queue = queue.Queue()
        
        # Start background thread to read responses
        self.reader_thread = threading.Thread(target=self._read_responses)
        self.reader_thread.daemon = True
        self.reader_thread.start()
        
        # Initialize the connection
        self._initialize()
    
    def _read_responses(self):
        """Background thread to read server responses"""
        try:
            while True:
                line = self.server_process.stdout.readline()
                if not line:
                    break
                try:
                    response = json.loads(line.strip())
                    self.response_queue.put(response)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"Reader thread error: {e}")
    
    def send_message(self, message):
        """Send a message to the server"""
        json_str = json.dumps(message) + '\n'
        print(f"→ Sending: {json.dumps(message, indent=2)}")
        self.server_process.stdin.write(json_str)
        self.server_process.stdin.flush()
        
        # If this message has an ID, wait for response
        if 'id' in message:
            try:
                response = self.response_queue.get(timeout=5)
                print(f"← Received: {json.dumps(response, indent=2)}")
                return response
            except queue.Empty:
                print("⚠ No response received (timeout)")
                return None
        return None
    
    def _initialize(self):
        """Initialize the MCP connection"""
        self.request_id += 1
        init_response = self.send_message({
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "interactive-client", "version": "1.0.0"}
            }
        })
        
        # Send initialized notification
        self.send_message({
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        })
        
        print("✓ MCP client initialized successfully!")
        return init_response
    
    def list_tools(self):
        """List available tools"""
        self.request_id += 1
        return self.send_message({
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list"
        })
    
    def get_weather(self, city):
        """Get weather for a city"""
        self.request_id += 1
        return self.send_message({
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": "get_weather",
                "arguments": {"city": city}
            }
        })
    
    def set_weather(self, city, temperature):
        """Set weather for a city"""
        self.request_id += 1
        return self.send_message({
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": "set_weather",
                "arguments": {"city": city, "temp": temperature}
            }
        })
    
    def close(self):
        """Close the client connection"""
        self.server_process.terminate()
        self.server_process.wait()

def main():
    print("🌤️  Interactive MCP Weather Client")
    print("=" * 40)
    
    # Change this to your server file name
    client = InteractiveMCPClient('weather_server.py')
    
    try:
        while True:
            print("\nAvailable commands:")
            print("1. list - List available tools")
            print("2. get <city> - Get weather for city")
            print("3. set <city> <temp> - Set weather for city")
            print("4. quit - Exit")
            
            command = input("\nEnter command: ").strip().split()
            
            if not command:
                continue
            
            if command[0] == 'quit':
                break
            elif command[0] == 'list':
                client.list_tools()
            elif command[0] == 'get' and len(command) >= 2:
                city = ' '.join(command[1:])
                client.get_weather(city)
            elif command[0] == 'set' and len(command) >= 3:
                city = ' '.join(command[1:-1])
                try:
                    temp = float(command[-1])
                    client.set_weather(city, temp)
                except ValueError:
                    print("❌ Invalid temperature value")
            else:
                print("❌ Invalid command")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        client.close()

if __name__ == "__main__":
    main()