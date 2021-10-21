#!/usr/bin/env python3
import argparse
import sys
import socket
import logging

log = logging.getLogger(__name__)

ddp_version = "00030010"
port = 9302


def request_state(host):
    """
    Send a special HTTP request over UDP(!)
    Response should be something like "HTTP/1.1 620 Server Standby" or
    "HTTP/1.1 200 Ok"
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    msg = "SRCH * HTTP/1.1\n" "device-discovery-protocol-version:{}".format(ddp_version)
    try:
        log.debug("Sending:\n%s", msg)
        s.sendto(bytes(msg, "utf-8"), (host, port))
    except socket.error as e:
        log.error(e)
        return

    try:
        res_msg = s.recv(1024)
    except socket.timeout:
        log.debug("Timeout waiting for response from ps5")
        # Probably in transition between standby and on or vice versa
        res_msg = ""
    s.close()
    return str(res_msg)


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Query a PS5 for state. Prints ON/STANDBY/OFF (Unreachable host = OFF)"
    )
    p.add_argument("host")
    p.add_argument("-b", "--binary-mode", action="store_true", help="Report standby as OFF")
    args = p.parse_args()

    response = request_state(args.host) or ""

    if "200 Ok" in response:
        state = "ON"
    elif not args.binary_mode and "620 Server Standby" in response:
        state = "STANDBY"
    else:
        state = "OFF"

    print(state)
