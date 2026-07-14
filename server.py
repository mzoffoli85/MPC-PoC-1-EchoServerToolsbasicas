"""PoC 1 - MCP Echo Server: 3 tools basicas sobre transporte stdio."""

import logging
import sys

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("poc1-echo-server")

mcp = FastMCP(name="poc1-echo-server")


@mcp.tool()
def echo(message: str) -> str:
    """Devuelve el mismo mensaje recibido, sin modificaciones."""
    logger.info("echo llamado con message=%r", message)
    return message


@mcp.tool()
def add(a: float, b: float) -> float:
    """Suma dos numeros y devuelve el resultado."""
    logger.info("add llamado con a=%r b=%r", a, b)
    return a + b


@mcp.tool()
def reverse(text: str) -> str:
    """Invierte el orden de los caracteres de un string."""
    logger.info("reverse llamado con text=%r", text)
    return text[::-1]


if __name__ == "__main__":
    logger.info("Iniciando poc1-echo-server sobre stdio")
    mcp.run(transport="stdio")
