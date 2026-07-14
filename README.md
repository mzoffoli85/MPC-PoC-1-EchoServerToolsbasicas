# PoC 1 — MCP Echo Server (Tools básicas sobre stdio)

Primera PoC de una serie de 5 para aprender **MCP (Model Context Protocol)** en profundidad. Server MCP en Python que expone 3 tools simples sobre transporte **stdio**, pensado para validar el handshake completo `initialize` → negociación de capabilities → `tools/list` → `tools/call` contra Claude Desktop / Claude Code.

Spec completa de la PoC: [`POC1_MCP_ECHO_SERVER.md`](POC1_MCP_ECHO_SERVER.md).

## Tools expuestas

| Tool      | Input                  | Output              | Propósito didáctico                    |
|-----------|-------------------------|----------------------|------------------------------------------|
| `echo`    | `message: str`          | el mismo string      | Validar ida y vuelta trivial             |
| `add`     | `a: float`, `b: float`  | la suma              | Validar tipado de inputs y coerción      |
| `reverse` | `text: str`             | el string invertido  | Validar manejo de strings no triviales   |

Implementadas como funciones síncronas y puras (sin efectos secundarios) usando la API moderna `FastMCP` del SDK `mcp` (decorador `@mcp.tool()`).

## Instalar dependencias

Con `uv` (preferido):

```bash
uv sync
```

Con `venv` + `pip`:

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -e .
```

## Registrar el server en Claude Desktop

Editar `claude_desktop_config.json` (en Windows: `%APPDATA%\Claude\claude_desktop_config.json`) y agregar:

```json
{
  "mcpServers": {
    "poc1-echo-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\PoC\\MCP\\MPC-PoC-1-EchoServerToolsbasicas",
        "python",
        "server.py"
      ]
    }
  }
}
```

Si preferís usar el intérprete de un venv en vez de `uv`, reemplazá `command`/`args` por la ruta absoluta al `python.exe` del venv y `["C:\\PoC\\MCP\\MPC-PoC-1-EchoServerToolsbasicas\\server.py"]`.

Reiniciar Claude Desktop para que detecte el nuevo server.

## Probar cada tool

Frases de ejemplo para gatillar cada tool desde el chat de Claude Desktop:

- **echo**: "Usá la tool echo para repetir el mensaje 'hola mundo'"
- **add**: "Sumá 15.5 y 22.3 usando la tool add"
- **reverse**: "Invertí el string 'MCP' con la tool reverse"

También podés correr el server directo para validar que arranca sin errores:

```bash
python server.py
```

Va a quedar esperando input JSON-RPC por stdin (comportamiento normal); `Ctrl+C` para salir.

## Ver los logs de stderr (debug del handshake)

Todo el logging va a **stderr** (nunca a stdout, que es el canal del protocolo). Claude Desktop guarda los logs de cada MCP server en:

```
%APPDATA%\Claude\logs\mcp-server-poc1-echo-server.log
```

Ahí se ve el `initialize`, la negociación de capabilities y cada `tools/call` con sus argumentos, gracias al logging agregado en `server.py`.

## Qué aprendí

- El SDK `mcp` moderno resuelve casi todo con `FastMCP` + `@mcp.tool()`: el schema de inputs se genera solo a partir de los type hints, sin tocar JSON Schema a mano.
- El canal stdout está reservado 100% para JSON-RPC — cualquier `print()` o log mal dirigido rompe el protocolo; todo el logging tiene que ir a stderr explícitamente.
- El handshake (`initialize` → `tools/list` → `tools/call`) es visible y depurable en los logs de Claude Desktop, lo cual hace mucho más fácil diagnosticar problemas de conexión que "adivinar" desde el lado del cliente.
- Correr el server standalone (`python server.py`) antes de registrarlo en Claude Desktop ahorra un ciclo completo de debugging: si arranca limpio ahí, el problema de conexión está en la config, no en el código.

## Siguiente en la serie

**PoC 2** — Resource Provider: exponer Google Sheets como Resources leíbles vía MCP.
