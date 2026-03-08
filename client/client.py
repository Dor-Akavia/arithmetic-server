import json
import logging
import socket
import sys

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [CLIENT] %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


SERVER_HOST = "server"
SERVER_PORT = 9999

SUPPORTED_OPS = ["+", "-", "*", "/"]


# Verifies the user's number input.
def get_number(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  '{raw}' is not a valid number. Please try again.")


# Verifies the user's operation input.
def get_operation() -> str:
    while True:
        raw = input(f"Operation {SUPPORTED_OPS}: ").strip()
        if raw in SUPPORTED_OPS:
            return raw
        print(f"  '{raw}' is not supported. Choose from {SUPPORTED_OPS}.")

# Creates the request json, open a connection to the server and response a dict
def send_request(a: float, b: float, operation: str) -> dict:

    payload = json.dumps({"a": a, "b": b, "operation": operation}).encode("utf-8") 

    log.info("Connecting to server at %s:%s", SERVER_HOST, SERVER_PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        log.info("Sending request: %s %s %s", a, operation, b)
        sock.sendall(payload)

        # Bytes size limit, should be sufficent for small json
        raw_response = sock.recv(1024)

    return json.loads(raw_response.decode("utf-8"))


def main() -> None:
    log.info("Arithmetic Client started.")
    print("\n--- Arithmetic Calculator ---")
    print("Type Ctrl+C at any time to quit.\n")

    try:
        while True:
            a = get_number("Enter first number : ")
            b = get_number("Enter second number: ")
            op = get_operation()

            try:
                response = send_request(a, b, op)
            except ConnectionRefusedError:
                log.error(
                    "Could not connect to server at %s:%s.",
                    SERVER_HOST,
                    SERVER_PORT,
                )
                sys.exit(1)

            if "result" in response:
                log.info("Received result: %s", response["result"])
                print(f"\n  Result: {a} {op} {b} = {response['result']}\n")
            else:
                log.error("Server returned an error: %s", response.get("error"))
                print(f"\n  Error from server: {response.get('error')}\n")

            again = input("Calculate again? (y/n): ").strip().lower()
            if again != "y":
                break

    except KeyboardInterrupt:
        print("\nBye!")

    log.info("Client finished.")


if __name__ == "__main__":
    main()
