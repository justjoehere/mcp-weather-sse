from . import weather_server
import asyncio

def main():
    asyncio.run(weather_server.main())

__all__ = ['main', 'weather_server']