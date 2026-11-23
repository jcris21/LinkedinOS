"""Grafo posicionado con rutas SVG reales y pulsos que viajan por ellas.

Esto es lo que separa un póster "apilado" de uno que se lee como un sistema:
los nodos se dimensionan por su contenido y se colocan en el lienzo, y lo que
los une son rutas con etiqueta y punta de flecha. El pulso NO late en su sitio
-- viaja por la ruta con `offset-path`, que es además la única forma que el
render frame-exacto puede controlar (SMIL / <animateMotion> no aparece en
document.getAnimations(), así que el capturador no lo podría pausar).
"""
import math

# tamaño del lienzo del grafo, en px, 1:1 con el viewBox del SVG para que el
# mismo string `d` sirva en el <path> y en el offset-path del pulso.
# El grafo es el héroe del póster: ocupa el grueso del canvas, como en los
# referentes -- un anillo chico rodeado de aire se lee como adorno, no como
# el argumento principal.
W, H = 752, 736
CX, CY, RX, RY = 376, 386, 268, 296


def _ellipse_pt(cx, cy, rx, ry, deg):
    r = math.radians(deg)
    return cx + rx * math.cos(r), cy + ry * math.sin(r)


def ring_layout(n, cx=CX, cy=CY, rx=RX, ry=RY, start_deg=-90):
    """Posiciones de n nodos repartidos en una elipse, empezando arriba."""
    step = 360.0 / n
    return [_ellipse_pt(cx, cy, rx, ry, start_deg + i * step) for i in range(n)]


def arc_path(cx, cy, rx, ry, a0, a1, gap=13, bulge=1.0):
    """Tramo de elipse entre dos ángulos, recortado `gap` grados en cada punta
    para no pegarse a las cajas. `bulge` abre la curva hacia afuera."""
    a0, a1 = a0 + gap, a1 - gap
    p0 = _ellipse_pt(cx, cy, rx * bulge, ry * bulge, a0)
    p1 = _ellipse_pt(cx, cy, rx * bulge, ry * bulge, a1)
    am = (a0 + a1) / 2.0
    # punto de control: empujado hacia afuera para que la curva siga el anillo
    k = 1.0 / math.cos(math.radians((a1 - a0) / 2.0))
    pm = _ellipse_pt(cx, cy, rx * bulge * k, ry * bulge * k, am)
    return (f"M {p0[0]:.1f} {p0[1]:.1f} Q {pm[0]:.1f} {pm[1]:.1f} "
            f"{p1[0]:.1f} {p1[1]:.1f}"), pm


def gate_block(question, yes, no, top=456):
    """Rombo de decisión con sus dos salidas -- el referente lo usa para marcar
    dónde el flujo deja de ser automático. Va dentro del anillo: el interior
    vacío de un grafo es el equivalente al aire muerto dentro de una caja."""
    return f"""<div class="gate" style="top:{top}px">
  <div class="gwrap">
    <div class="diamond"><span>{question}</span></div>
  </div>
  <div class="gouts">
    <div class="gout gyes"><b>Sí</b> · {yes}</div>
    <div class="gout gno"><b>No</b> · {no}</div>
  </div>
</div>"""


def ring_flow(nodes, center, loop_label, accent="#D9661E", close_accent="#2E9BD6",
              pulse_dur=3.0, gate=None, gate_edge=None, gate_center=(CX, 510)):
    """nodes: [{name, sub, icon}]  ·  center: {title, sub}  ·  loop_label: texto
    de la arista de cierre. Devuelve (html, css)."""
    n = len(nodes)
    cx, cy, rx, ry = CX, CY, RX, RY
    pts = ring_layout(n, cx, cy, rx, ry)
    step = 360.0 / n

    paths, labels, pulses, css = [], [], [], []
    for i in range(n):
        a0 = -90 + i * step
        a1 = a0 + step
        d, mid = arc_path(cx, cy, rx, ry, a0, a1)
        closing = (i == n - 1)
        col = close_accent if closing else accent
        dash = ' stroke-dasharray="7 5"' if closing else ""
        paths.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.2"'
                     f' opacity=".75"{dash} marker-end="url(#ah{"c" if closing else ""})"/>')
        lab = nodes[i].get("edge", "")
        if closing:
            lab = loop_label
        if lab:
            labels.append(
                f'<div class="elab" style="left:{mid[0]:.0f}px;top:{mid[1]:.0f}px;'
                f'border-color:{col}55;color:{col}">{lab}</div>')
        # pulso viajero: offset-path con el MISMO d del <path>
        cls = f"pl{i}"
        delay = round(i * (pulse_dur / n), 3)
        css.append(
            f'.{cls}{{offset-path:path("{d}");offset-rotate:0deg;'
            f'animation:travel {pulse_dur}s linear infinite;animation-delay:{delay}s;'
            f'background:{col};box-shadow:0 0 10px {col}}}')
        pulses.append(f'<div class="pulse {cls}"></div>')
        if gate_edge == i:
            # amarra el rombo a SU arista: un rombo suelto en el centro se lee
            # como adorno, no como una decisión que ocurre en un punto del flujo
            gx, gy = gate_center
            hw = 77  # medio ancho visual del rombo rotado
            sx = gx - hw if mid[0] < gx else gx + hw
            paths.append(f'<path d="M {sx} {gy} C {(sx+mid[0])/2:.0f} {gy:.0f} '
                         f'{(sx+mid[0])/2:.0f} {mid[1]:.0f} {mid[0]:.0f} {mid[1]:.0f}" '
                         f'fill="none" stroke="#A9BCCE" stroke-width="1.6" '
                         f'stroke-dasharray="5 5" opacity=".9"/>')

    boxes = ""
    for i, nd in enumerate(nodes):
        x, y = pts[i]
        boxes += f"""<div class="gnode" style="left:{x:.0f}px;top:{y:.0f}px">
  <span class="gbadge">{i+1}</span>
  <div class="gnhead"><span class="gicon">{nd['icon']}</span><span class="gntitle">{nd['name']}</span></div>
  <div class="gnsub">{nd['sub']}</div>
</div>"""

    html = f"""<div class="graph">
  <svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">
    <defs>
      <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
        <path d="M 0 1 L 9 5 L 0 9 z" fill="{accent}"/></marker>
      <marker id="ahc" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
        <path d="M 0 1 L 9 5 L 0 9 z" fill="{close_accent}"/></marker>
    </defs>
    {''.join(paths)}
  </svg>
  <div class="gcenter">
    <div class="gctitle">{center['title']}</div>
    <div class="gcsub">{center['sub']}</div>
  </div>
  {gate or ''}
  {''.join(labels)}
  {boxes}
  {''.join(pulses)}
</div>"""
    return html, "\n".join(css)


GRAPH_CSS = """
.graph { position:relative; width:%(W)spx; height:%(H)spx; flex:0 0 auto; }
.graph svg { position:absolute; left:0; top:0; }
.gnode { position:absolute; transform:translate(-50%%,-50%%); width:182px;
  background:#FFF; border:1.6px solid var(--nb); border-radius:13px;
  padding:11px 13px 10px; box-shadow:0 5px 16px rgba(18,42,70,.10); }
.gbadge { position:absolute; left:-10px; top:-11px; width:23px; height:23px; border-radius:50%%;
  background:#0E2A47; color:#fff; font-size:12px; font-weight:800;
  display:flex; align-items:center; justify-content:center; }
.gnhead { display:flex; align-items:center; gap:8px; }
.gicon { width:30px; height:30px; min-width:30px; border-radius:50%%; background:var(--nac);
  display:flex; align-items:center; justify-content:center; font-size:14px; }
.gntitle { font-weight:800; font-size:18.5px; letter-spacing:-.2px; line-height:1.1; }
.gnsub { font-family:'Anonymous Pro','DejaVu Sans Mono',monospace; font-size:13px;
  color:var(--mut); margin-top:5px; line-height:1.45; letter-spacing:-.1px; }
.gcenter { position:absolute; left:50%%; top:%(CY)spx; transform:translate(-50%%,-50%%);
  background:#0E2A47; color:#EAF4FB; border-radius:15px; padding:13px 24px; text-align:center;
  box-shadow:0 8px 26px rgba(14,42,71,.26); }
.gctitle { font-weight:800; font-size:25px; letter-spacing:-.4px; }
.gcsub { font-size:13px; color:#8FB0C9; margin-top:3px; letter-spacing:.2px; }
.elab { position:absolute; transform:translate(-50%%,-50%%); background:#FFF;
  border:1.3px solid; border-radius:11px; padding:3.5px 11px; font-size:13px;
  font-weight:700; white-space:nowrap; box-shadow:0 2px 7px rgba(18,42,70,.07); }
.pulse { position:absolute; left:0; top:0; width:10px; height:10px; border-radius:50%%;
  margin:-5px 0 0 -5px; }
.gate { position:absolute; left:50%%; transform:translateX(-50%%); display:flex;
  flex-direction:column; align-items:center; gap:13px; z-index:3; }
.gwrap { display:flex; justify-content:center; }
.diamond { width:108px; height:108px; transform:rotate(45deg); border-radius:15px;
  background:#FFF; border:1.8px solid #C9D7E6; display:flex; align-items:center;
  justify-content:center; box-shadow:0 5px 16px rgba(18,42,70,.09); }
.diamond span { transform:rotate(-45deg); font-weight:800; font-size:13.5px; text-align:center;
  line-height:1.2; width:95px; letter-spacing:-.2px; }
.gouts { display:flex; gap:9px; }
.gout { font-size:13.5px; border-radius:9px; padding:5px 11px; border:1.4px solid;
  background:#FFF; white-space:nowrap; font-weight:500; }
.gyes { border-color:#F0B86E; color:#A66414; }
.gno { border-color:#9BD9B8; color:#1B7A4F; }
@keyframes travel { 0%% { offset-distance:0%%; opacity:0; }
  12%% { opacity:1; } 88%% { opacity:1; } 100%% { offset-distance:100%%; opacity:0; } }
""" % {"W": W, "H": H, "CY": CY}
