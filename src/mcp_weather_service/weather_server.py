# TODO: use mcp.server.FastMCP
import logging
import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from weather_util import Weather
import json
from typing import Any, Sequence

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sse-mcp-weather-server")


class WeatherServer:
    def __init__(self):
        logger.debug("Initializing WeatherServer")
        self.app = Server("weather-mcp-server")
        self.setup_tools()

    def setup_tools(self):
        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="get_current_weather",
                    description="Get current weather and forecast for a location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "location_name": {
                                "type": "string",
                                "description": "The location to get the weather for"
                            }
                        },
                        "required": ["location_name"]
                    }
                )
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            if name != "get_current_weather":
                logger.error(f"Unknown tool: {name}")
                raise ValueError(f"Unknown tool: {name}")

            if not isinstance(arguments, dict) or "location_name" not in arguments:
                logger.error(f"Invalid weather arguments: {arguments} is not a 'dict'")
                raise ValueError(f"Invalid weather arguments: {arguments} is not a 'dict'")

            try:
                location_name = arguments["location_name"]
                logger.debug(f"Received weather request for location: {location_name}")
                weather = await Weather(locale='en', unit='imperial').get_forecast(location_name)
                logger.debug(f"Successfully received weather data for location")

                forecasts = []
                for forecast in weather.daily_forecasts:
                    forecasts.append({
                        'date': forecast.date.strftime('%Y-%m-%d'),
                        'high_temperature': forecast.highest_temperature,
                        'low_temperature': forecast.lowest_temperature
                    })

                weather_data = {
                    "currently": {
                        "current_temperature": weather.temperature,
                        "sky": weather.kind.emoji,
                        "feels_like": weather.feels_like,
                        "humidity": weather.humidity,
                        "wind_speed": weather.wind_speed,
                        "wind_direction": (weather.wind_direction.value + weather.wind_direction.emoji),
                        "visibility": weather.visibility,
                        "uv_index": weather.ultraviolet.index,
                        "description": weather.description,
                        "forecasts": forecasts
                    }
                }

                return [
                    TextContent(
                        type="text",
                        text=json.dumps(weather_data, indent=2)
                    )
                ]

            except Exception as e:
                logger.error(f"Error processing weather request: {str(e)}")
                raise RuntimeError(f"Weather API error: {str(e)}")


def create_app():
    weather_server = WeatherServer()
    sse = SseServerTransport("/weather")

    class HandleSSE:
        def __init__(self, sse, weather_server):
            self.sse = sse
            self.weather_server = weather_server

        async def __call__(self, scope, receive, send):
            async with self.sse.connect_sse(scope, receive, send) as streams:
                await self.weather_server.app.run(
                    streams[0],
                    streams[1],
                    self.weather_server.app.create_initialization_options()
                )

    class HandleMessages:
        def __init__(self, sse):
            self.sse = sse

        async def __call__(self, scope, receive, send):
            await self.sse.handle_post_message(scope, receive, send)

    routes = [
        Route("/sse", endpoint=HandleSSE(sse, weather_server), methods=["GET"]),
        Route("/weather", endpoint=HandleMessages(sse), methods=["POST"])
    ]

    return Starlette(routes=routes)


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=3001)
