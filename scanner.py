import argparse
import asyncio
import ipaddress
import sys
from typing import List, Tuple

DEFAULT_TIMEOUT = 0.5
DEFAULT_CONCURRENCY = 200

BANNER = """
Ethical Port Scanner (TCP connect scan)
- Use ONLY on systems u own or have explicit permission to test.
- This tool is designed with safety defaults (localhost-first, opt-in for remote).
"""

def parse_ports(port_str: str) -> List[int]:
    ports: List[int] = []
    parts = [p.strip() for p in port_str.split(",") if p.strip()]
    for part in parts:
        if "-" in part:
            a, b = part.split("-", 1)
            start, end = int(a), int(b)
            if start > end:
                start, end = end, start
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    for p in ports:
        if p < 1 or p > 65535:
            raise ValueError(f"Invalid port: {p}")
    return sorted(set(ports))

def is_private_or_localhost(host: str) -> bool:
    try:
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        return False

async def check_port(host: str, port: int, timeout: float, sem: asyncio.Semaphore) -> Tuple[int, str]:
    async with sem:
        try:
            conn = asyncio.open_connection(host, port)
            reader, writer = await asyncio.wait_for(conn, timeout=timeout)
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            return port, "open"
        except (asyncio.TimeoutError, ConnectionRefusedError):
            return port, "closed"
        except OSError:
            return port, "filtered"
        except Exception:
            return port, "error"

async def run_scan(host: str, ports: List[int], timeout: float, concurrency: int) -> List[Tuple[int, str]]:
    sem = asyncio.Semaphore(concurrency)
    tasks = [check_port(host, p, timeout, sem) for p in ports]
    results = await asyncio.gather(*tasks)
    return sorted(results, key=lambda x: x[0])

def main() -> int:
    parser = argparse.ArgumentParser(description="Ethical TCP connect port scanner (permission-only).")
    parser.add_argument("--host", default="127.0.0.1", help="Target host (default: 127.0.0.1)")
    parser.add_argument(
        "--ports", default="1-1024",
        help="Ports to scan, e.g. '22,80,443' or '1-1024' (default: 1-1024)"
    )
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help=f"Timeout seconds (default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY, help=f"Max concurrent connections (default: {DEFAULT_CONCURRENCY})")
    parser.add_argument("--open-only", action="store_true", help="Print only open ports")
    parser.add_argument(
        "--acknowledge",
        action="store_true",
        help="Acknowledge you have explicit permission to scan this target (required for non-local targets)."
    )
    args = parser.parse_args()

    print(BANNER.strip())

    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print(f"[!] Port parse error: {e}", file=sys.stderr)
        return 2

    if not is_private_or_localhost(args.host):
        if not args.acknowledge:
            print(
                "\n[!] Refusing to scan non-local / hostname target without --acknowledge.\n"
                "    This is a safety feature. Use ONLY with explicit permission.\n"
                "    Example (with permission): python scanner.py --host example.com --ports 80,443 --acknowledge\n",
                file=sys.stderr
            )
            return 3

    if args.concurrency > 2000:
        print("[!] Concurrency too high for an ethical default. Please keep it <= 2000.", file=sys.stderr)
        return 4
    if args.timeout < 0.1:
        print("[!] Timeout too low. Please keep it >= 0.1s.", file=sys.stderr)
        return 5

    print(f"\nTarget: {args.host}")
    print(f"Ports : {ports[0]}-{ports[-1]} ({len(ports)} ports)")
    print(f"Timeout: {args.timeout}s, Concurrency: {args.concurrency}\n")

    results = asyncio.run(run_scan(args.host, ports, args.timeout, args.concurrency))

    open_ports = [p for p, status in results if status == "open"]
    for port, status in results:
        if args.open_only and status != "open":
            continue
        print(f"{port:5d}/tcp  {status}")

    print("\nSummary:")
    print(f"  Open ports: {len(open_ports)}")
    if open_ports:
        print(f"  {open_ports}")

    return 0

if __name__ == "__main__":

    raise SystemExit(main())
