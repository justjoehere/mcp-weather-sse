# Introduction
This is a tutorial application for setting a Server-Sent Events (SSE) Model Context Protocol (MCP) Server.
This server returns weather information for a specified location.

This server demonstrates how to implement a simple MCP SSE server that can be integrated with AI agents.

## Features
- SSE-based MCP server implementation
- Real-time weather data retrieval
- Support for current conditions and forecasts
- Easy integration with AI agents through MCP

## Prerequisites
- Python 3.10 or later
- Node.js and NPM (for the MCP Inspector)
- Git (for version control)

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd mcp-weather-service
   ```

2. Run the setup script:
   ```bash
   scripts/setup.bat
   ```
   This will:
   - Create a Python virtual environment in `.venv`
   - Activate the virtual environment
   - Install all required dependencies

3. (Optional) Configure your IDE to use the Python interpreter from `.venv`

## Running the Server

There are several ways to run the server:

### Method 1: Direct Run (Preferred)
```bash
python src/mcp_weather_service/weather_server.py
```

### Method 2: Using Uvicorn
```bash
uvicorn mcp_weather_service.weather_server:app --host 127.0.0.1 --port 3001
```

### Method 3: Using Launch Script
```bash
scripts/launch.bat
```

## Verifying the Server

1. Check if the server is running:
   - Open your browser and navigate to `http://127.0.0.1:3001/sse`
   - You should see a response like:
     ```text
     event: endpoint
     data: /weather?session_id=f0c33285de5846d79a89f41212acfd75
     ```

2. Using the MCP Inspector:
   ```bash
   scripts/inspect.bat
   ```
   This launches the MCP Protocol Inspector, which allows you to:
   - Interact with the server directly
   - Test weather queries
   - Debug server responses
   - You MUST connect via `http://127.0.0.1:3001/sse` (use `127.0.0.1` instead of `localhost` especially on Windows!)

3. Using with a MCP Client
There is a gradio [MCP Client demo](https://github.com/justjoehere/mcp_gradio_client) that can be used to interact with this server.  See that projects' details to set it up
The entry for `config.json` for THAT project is:
```json
{
  "mcpServers": {
    "weather": {
      "type": "sse",
      "url": "http://127.0.0.1"
    }
  }
}

```

## Available Tools

### get_current_weather
Gets current weather and forecast for a specified location.

**Input Schema:**
```json
{
  "location_name": {
    "type": "string",
    "description": "The location to get the weather for"
  }
}
```

**Example Response:**
```json
{
  "currently": {
    "current_temperature": 72.5,
    "sky": "☀️",
    "feels_like": 74.2,
    "humidity": 65,
    "wind_speed": 8.5,
    "wind_direction": "NW↗️",
    "visibility": 10,
    "uv_index": 5,
    "description": "Clear skies",
    "forecasts": [
      {
        "date": "2024-12-05",
        "high_temperature": 75.8,
        "low_temperature": 62.4
      }
    ]
  }
}
```

## Development

### Virtual Environment
The project uses a Python virtual environment located in `.venv`. To activate it manually:
```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Unix/MacOS
```

### Adding Dependencies
1. Add new dependencies to `pyproject.toml`
2. Run `scripts/install_deps.bat` to install them

## Troubleshooting

### Common Issues

1. **Server Won't Start**
   - Verify Python version (3.10+)
   - Check if port 3001 is available
   - Ensure virtual environment is activated

2. **MCP Inspector Connection Failed**
   - Verify the server is running
   - Check the URL (should be http://127.0.0.1:3001/sse)
   - Ensure Node.js and NPM are installed

3. **Weather Data Not Returning**
   - Check internet connectivity
   - Verify location name format

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
