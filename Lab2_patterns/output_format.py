import json
from models import Port, Ship, Container, HeavyContainer, RefrigeratedContainer, LiquidContainer

def _round2(x: float) -> float:
    return round(x + 1e-12, 2)

def build_output_dict(world) -> dict:
    result = {}
    for pid in sorted(world.ports.keys()):
        port: Port = world.ports[pid]
        pj = {}
        pj["lat"] = _round2(port.latitude)
        pj["lon"] = _round2(port.longitude)
        basic, heavy, refc, liq = [], [], [], []
        for c in port.containers:
            if isinstance(c, RefrigeratedContainer): refc.append(c.ID)
            elif isinstance(c, LiquidContainer):    liq.append(c.ID)
            elif isinstance(c, HeavyContainer):     heavy.append(c.ID)
            else:                                   basic.append(c.ID)
        for arr in (basic, heavy, refc, liq):
            arr.sort()
        pj["basic_container"] = basic
        pj["heavy_container"] = heavy
        pj["refrigerated_container"] = refc
        pj["liquid_container"] = liq
        ships_here = sorted(port.current, key=lambda s: s.ID)
        for s in ships_here:
            sj = {}
            sj["fuel_left"] = float(f"{s.fuel:.2f}")
            sb, sh, sr, sl = [], [], [], []
            for c in s.getCurrentContainers():
                if isinstance(c, RefrigeratedContainer): sr.append(c.ID)
                elif isinstance(c, LiquidContainer):    sl.append(c.ID)
                elif isinstance(c, HeavyContainer):     sh.append(c.ID)
                else:                                   sb.append(c.ID)
            sj["basic_container"] = sb
            sj["heavy_container"] = sh
            sj["liquid_container"] = sl
            sj["refrigerated_container"] = sr
            sj["visited_ports"] = s.visited_ports
            pj[f"ship_{s.ID}"] = sj
        result[f"Port {pid}"] = pj
    return result

def write_output_json(world, out_path: str):
    data = build_output_dict(world)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
