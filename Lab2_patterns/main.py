import json
import sys

from models import (
    World, Port, Ship, Container,
    BasicContainer, HeavyContainer,
    RefrigeratedContainer, LiquidContainer
)
from output_format import write_output_json

def run(in_path: str, out_path: str):
    with open(in_path, "r", encoding="utf-8") as f:
        J = json.load(f)
    if "actions" not in J or not isinstance(J["actions"], list):
        print("No actions array in input")
        sys.exit(1)
    W = World()
    for a in J["actions"]:
        t = a.get("type", "")
        if t == "create_port":
            pid = int(a["id"])
            lat = float(a["lat"])
            lon = float(a["lon"])
            if pid not in W.ports:
                W.ports[pid] = Port(pid, lat, lon)
        elif t == "create_container":
            cid = int(a["id"])
            w   = int(a["weight"])
            kind = a.get("kind", "")
            if kind == "R":
                c = RefrigeratedContainer(cid, w)
            elif kind == "L":
                c = LiquidContainer(cid, w)
            else:
                c = BasicContainer(cid, w) if w <= 3000 else HeavyContainer(cid, w)
            W.containers[cid] = c
            if "at_port" in a:
                pid = int(a["at_port"])
                if pid in W.ports:
                    W.ports[pid].containers.append(c)
        elif t == "create_ship":
            sid = int(a["id"])
            pid = int(a["port"])
            totalW = int(a["totalW"])
            maxAll = int(a["maxAll"])
            maxH   = int(a["maxHeavy"])
            maxR   = int(a["maxRef"])
            maxL   = int(a["maxLiq"])
            base   = float(a["base"])
            start = W.ports.get(pid)
            W.ships[sid] = Ship(sid, start, totalW, maxAll, maxH, maxR, maxL, base)
        elif t == "load":
            sid = int(a["ship"]); cid = int(a["container"])
            if sid in W.ships and cid in W.containers:
                W.ships[sid].load(W.containers[cid])
        elif t == "unload":
            sid = int(a["ship"]); cid = int(a["container"])
            if sid in W.ships and cid in W.containers:
                W.ships[sid].unLoad(W.containers[cid])
        elif t == "refuel":
            sid = int(a["ship"]); amt = float(a["amount"])
            if sid in W.ships:
                W.ships[sid].reFuel(amt)
        elif t == "sail":
            sid = int(a["ship"]); pid = int(a["to_port"])
            if sid in W.ships and pid in W.ports:
                W.ships[sid].sailTo(W.ports[pid], W)
    write_output_json(W, out_path)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} input.json output.json")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])
