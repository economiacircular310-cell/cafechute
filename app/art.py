"""Arte generativo en SVG: el diente de león (símbolo de Chute) y curvas de nivel topográficas."""
from __future__ import annotations

import math
import random
from functools import lru_cache

from markupsafe import Markup


@lru_cache(maxsize=8)
def dandelion(seeds: int = 34, r: float = 46, cls: str = "dandelion") -> Markup:
    """Cabeza de diente de león: tallos radiales con un vilano en la punta."""
    rnd = random.Random(7)
    parts = []
    for i in range(seeds):
        a = 2 * math.pi * i / seeds + rnd.uniform(-0.05, 0.05)
        rr = r * rnd.uniform(0.86, 1.0)
        x, y = 50 + rr * math.cos(a), 50 + rr * math.sin(a)
        parts.append(f'<line x1="50" y1="50" x2="{x:.2f}" y2="{y:.2f}"/>')
        tuft = []
        for d in (-0.42, -0.21, 0, 0.21, 0.42):
            tx, ty = x + 7 * math.cos(a + d), y + 7 * math.sin(a + d)
            tuft.append(f"M{x:.2f} {y:.2f}L{tx:.2f} {ty:.2f}")
        parts.append(f'<path d="{" ".join(tuft)}"/>')
    return Markup(
        f'<svg class="{cls}" viewBox="-6 -6 112 112" aria-hidden="true" focusable="false">'
        f'<g fill="none" stroke="currentColor" stroke-width=".55" stroke-linecap="round">{"".join(parts)}</g>'
        '<circle cx="50" cy="50" r="3.2" fill="currentColor"/></svg>'
    )


@lru_cache(maxsize=4)
def topo(seed: int = 3, rings: int = 14, cls: str = "topo") -> Markup:
    """Curvas de nivel orgánicas (evocan el mapa de la finca)."""
    rnd = random.Random(seed)
    waves = [(k, rnd.uniform(0.04, 0.11), rnd.uniform(0, math.tau)) for k in (2, 3, 5)]
    paths = []
    for i in range(rings):
        base = 18 + i * 22
        pts = []
        for s in range(73):
            th = math.tau * s / 72
            rad = base * (1 + sum(amp * math.sin(k * th + ph + i * 0.18) for k, amp, ph in waves))
            pts.append((400 + rad * math.cos(th) * 1.35, 300 + rad * math.sin(th)))
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
        paths.append(f'<path d="{d}"/>')
    return Markup(
        f'<svg class="{cls}" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
        f'<g fill="none" stroke="currentColor" stroke-width="1">{"".join(paths)}</g></svg>'
    )


def harvest_ring(months_labels: list[str], harvest: list[int], current: int, today_label: str) -> Markup:
    """Anillo de 12 meses con los meses de cosecha resaltados y el mes actual marcado."""
    cx = cy = 160
    r_out, r_in = 140, 98
    segs = []
    for m in range(12):
        a0 = math.tau * m / 12 - math.pi / 2 + 0.012
        a1 = math.tau * (m + 1) / 12 - math.pi / 2 - 0.012
        p = [
            (cx + r_out * math.cos(a0), cy + r_out * math.sin(a0)),
            (cx + r_out * math.cos(a1), cy + r_out * math.sin(a1)),
            (cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)),
            (cx + r_in * math.cos(a0), cy + r_in * math.sin(a0)),
        ]
        d = (f"M{p[0][0]:.1f} {p[0][1]:.1f} A{r_out} {r_out} 0 0 1 {p[1][0]:.1f} {p[1][1]:.1f} "
             f"L{p[2][0]:.1f} {p[2][1]:.1f} A{r_in} {r_in} 0 0 0 {p[3][0]:.1f} {p[3][1]:.1f}Z")
        cls = "seg" + (" seg--harvest" if m + 1 in harvest else "") + (" seg--now" if m + 1 == current else "")
        am = (a0 + a1) / 2
        lx, ly = cx + (r_out + r_in) / 2 * math.cos(am), cy + (r_out + r_in) / 2 * math.sin(am)
        segs.append(f'<path class="{cls}" d="{d}"/>'
                    f'<text class="seg-label" x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="central">{months_labels[m]}</text>')
    am = math.tau * (current - 0.5) / 12 - math.pi / 2
    mx, my = cx + (r_out + 12) * math.cos(am), cy + (r_out + 12) * math.sin(am)
    marker = f'<circle class="ring-now" cx="{mx:.1f}" cy="{my:.1f}" r="6"/>'
    return Markup(
        f'<svg class="harvest-ring" viewBox="0 0 320 320" role="img" aria-label="{today_label}">'
        f'{"".join(segs)}{marker}</svg>'
    )
