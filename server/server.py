import json
import logging
import socket
import sys

from operations import OPERATIONS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [SERVER] %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


HOST = "0.0.0.0"   # Accept connections from any network interface
PORT = 9999         # Must match the port the client connects to
BUFFER_SIZE = 1024  # Max bytes to read per message


def handle_client(conn: socket.socket, addr: tuple) -> None:

    log.info("Connection accepted from %s:%s", addr[0], addr[1])

    with conn:
        raw = conn.recv(BUFFER_SIZE)
        if not raw:
            log.warning("Received empty request from %s — closing.", addr[0])
            return

        # Parse the json
        try:
            request = json.loads(raw.decode("utf-8"))
            a         = float(request["a"])
            b         = float(request["b"])
            op_symbol = request["operation"]
            log.info("Request: %s %s %s", a, op_symbol, b)
        except (json.JSONDecodeError, KeyError, ValueError) as exc:
            log.error("Bad request from %s: %s", addr[0], exc)
            send_response(conn, {"error": f"Bad request: {exc}"})
            return

        # Do the calculation
        operation = OPERATIONS.get(op_symbol)
        if operation is None:
            msg = f"Unknown operation '{op_symbol}'. Supported: {list(OPERATIONS)}"
            log.error(msg)
            send_response(conn, {"error": msg})
            return

        try:
            result = operation.calculate(a, b)
            log.info("Result: %s %s %s = %s", a, op_symbol, b, result)
            send_response(conn, {"result": result})
        except ValueError as exc:
            log.error("Calculation error: %s", exc)
            send_response(conn, {"error": str(exc)})


def send_response(conn: socket.socket, payload: dict) -> None:
    conn.sendall(json.dumps(payload).encode("utf-8"))


def run_server() -> None:
    # Create the listening socket and enter the accept loop
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()

        log.info("Server listening on %s:%s", HOST, PORT)
        log.info("Supported operations: %s", list(OPERATIONS.keys()))

        # Main accept loop — handles one client at a time.
        while True:
            conn, addr = server_sock.accept()
            handle_client(conn, addr)


if __name__ == "__main__":
    run_server()
