"""
Librería de módulos reutilizables. Cada función devuelve un fragmento HTML
que se inserta como hijo directo de `.canvas` (flex column) -- por eso
componer un layout nuevo es solo concatenar módulos en el orden que
el composer decida, nada de coordenadas absolutas a mano.

Acabado (v2, tras comparar contra los 3 pósters de referencia):
  - los paneles se tintan por categoría en vez de quedar blancos planos
  - cada panel puede llevar título de sección con badge de color
  - los nodos aceptan icono
  - los conectores se dibujan con línea + punto, no con una flecha de texto
  - hay anotaciones laterales en gris y una fila de métricas grandes
  - los bloques se ajustan al contenido: nada de cajas que crecen vacías
"""

# tintes suaves por acento -- lo que en las referencias hace que un panel
# "pertenezca" a una categoría de un vistazo, sin leer el rótulo
TINTS = {
    "#D9661E": "rgba(217,102,30,0.07)",
    "#FF8A5B": "rgba(255,138,91,0.08)",
    "#3EE08C": "rgba(62,224,140,0.09)",
    "#2EE6F0": "rgba(46,230,240,0.08)",
    "#FFC53D": "rgba(255,197,61,0.10)",
}


def _tint(color):
    return TINTS.get(color, "rgba(46,230,240,0.07)")


SECTION_PALETTE = ["#D9661E", "#2EE6F0", "#3EE08C", "#FFC53D"]


def section_title(text, color="#2EE6F0", number=None):
    """Rótulo de panel con badge -- en las referencias cada bloque del póster
    está rotulado y numerado ("1 Agent loop", "2 Tool calling"), con un círculo
    de color propio por sección en vez de una barra uniforme; sin eso el
    lector tiene que deducir qué está mirando y todas las secciones se ven
    igual de importantes."""
    if number is not None:
        badge = (f'<span style="width:23px;height:23px;min-width:23px;border-radius:50%;background:{color};'
                  f'color:#fff;font-weight:900;font-size:12.5px;display:flex;align-items:center;'
                  f'justify-content:center;box-shadow:0 2px 6px {color}55">{number}</span>')
    else:
        badge = f'<span style="width:4px;height:17px;background:{color};border-radius:2px;display:inline-block"></span>'
    return (f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">'
            f'{badge}<span style="font-weight:800;font-size:15px;letter-spacing:.2px">{text}</span></div>')


def header(title, subtitle, tagline=None, kicker=None):
    kick = (f'<div style="font-size:12.5px;font-weight:800;letter-spacing:2.5px;'
            f'color:#D9661E;margin-bottom:8px">{kicker}</div>') if kicker else ""
    return f"""
<div style="flex:0 0 auto;display:flex;justify-content:space-between;align-items:flex-start;gap:20px">
  <div style="flex:1">
    {kick}
    <div style="font-size:41px;font-weight:800;line-height:1.1;letter-spacing:-1px">{title}</div>
    <div style="font-size:19px;color:var(--mut);margin-top:8px">{subtitle}</div>
  </div>
  {f'<div style="flex:0 0 250px;border-left:3px solid #D9661E;padding-left:14px;font-size:12.5px;color:var(--mut);line-height:1.45">{tagline}</div>' if tagline else ''}
</div>"""


def hub_network(center, satellites, grow=1, title=None, number=None, accent="#2EE6F0"):
    sats = "".join(
        f'<div class="box" style="padding:10px 12px;text-align:center;'
        f'background:{_tint("#2EE6F0")};border-color:rgba(46,230,240,.45)">'
        f'<div style="font-weight:700;font-size:13px">{s if isinstance(s,str) else s["name"]}</div></div>'
        for s in satellites
    )
    head = section_title(title, accent, number) if title else ""
    return f"""
<div style="flex:{grow};display:flex;flex-direction:column;justify-content:center">
  {head}
  <div style="display:flex;flex-direction:column;align-items:center;gap:14px">
    <div style="width:140px;height:140px;border-radius:50%;border:2px solid #2EE6F0;
      background:radial-gradient(circle at 50% 40%,#12507A,#0A2C4A 60%,#071C31 100%);color:#E8F4FB;
      display:flex;align-items:center;justify-content:center;text-align:center;font-weight:800;font-size:16px;
      box-shadow:0 0 28px rgba(46,230,240,.45)">{center}</div>
    <div style="display:grid;grid-template-columns:repeat({min(len(satellites),3)},1fr);gap:9px;width:100%">{sats}</div>
  </div>
</div>"""


def funnel(layers, grow=1, title=None, number=None, accent="#2EE6F0"):
    widths = [96, 82, 68, 54, 42]
    rows = ""
    for i, L in enumerate(layers):
        w = widths[min(i, len(widths) - 1)]
        c = L.get("color", "#2EE6F0")
        dashed = "border-style:dashed;" if L.get("future") else ""
        rows += f"""
<div style="align-self:center;width:{w}%;border:2px solid {c};{dashed}
  border-radius:14px;padding:11px 18px;text-align:center;position:relative;background:{_tint(c)}">
  <div class="tag" style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);
    background:{c};color:#09243B">{L.get('tag','')}</div>
  <div style="font-weight:800;font-size:17px;color:{c}">{L['name']}</div>
  <div style="font-size:12.5px;color:var(--mut);margin-top:3px">{L['desc']}</div>
</div>"""
    head = section_title(title, accent, number) if title else ""
    return f'<div style="flex:{grow};display:flex;flex-direction:column;justify-content:center;gap:12px">{head}{rows}</div>'


def timeline(stages, grow=1, title=None, number=None, accent="#2EE6F0"):
    rows = ""
    for s in stages:
        c = s.get("color", "#2EE6F0")
        rows += f"""
<div style="display:flex;gap:13px;align-items:stretch">
  <div style="width:64px;min-width:64px;border-radius:12px;background:{c};color:#09243B;
    display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:900">
    <div style="font-size:19px">{s['tag']}</div><div style="font-size:9.5px">{s['period']}</div></div>
  <div class="box" style="flex:1;padding:10px 15px;border-color:{c};background:{_tint(c)}">
    <div style="font-weight:800;font-size:16px">{s['name']}</div>
    <div style="font-size:12.5px;color:var(--mut)">{s['desc']}</div>
  </div>
</div>"""
    head = section_title(title, accent, number) if title else ""
    return f'<div style="flex:{grow};display:flex;flex-direction:column;justify-content:center;gap:9px">{head}{rows}</div>'


def compare2(left, right, grow=1, title=None, number=None, accent="#D9661E"):
    def side(d, color):
        items = "".join(
            f'<div style="display:flex;gap:9px;margin-top:13px;font-size:14px;line-height:1.5">'
            f'<span style="color:{color};font-weight:800">—</span><span>{it}</span></div>'
            for it in d["items"])
        icon = f'<span style="font-size:17px;margin-right:7px">{d["icon"]}</span>' if d.get("icon") else ""
        return f"""<div class="box" style="flex:1;border-color:{color};background:{_tint(color)};padding:16px 18px;
  display:flex;flex-direction:column;justify-content:center">
  <div style="font-weight:800;color:{color};font-size:19px;display:flex;align-items:center">{icon}{d['title']}</div>
  <div style="font-size:12px;font-weight:700;color:var(--mut);margin-top:3px;letter-spacing:.3px">{d.get('formula','')}</div>{items}</div>"""
    head = section_title(title, accent, number) if title else ""
    return (f'<div style="flex:{grow};display:flex;flex-direction:column;min-height:0">{head}'
            f'<div style="flex:1;display:flex;gap:13px;align-items:stretch">{side(left,"#D9661E")}{side(right,"#3EE08C")}</div></div>')


def compareN(options, grow=1, title=None, number=None, accent="#2EE6F0"):
    """Comparación de N alternativas nombradas, sin jerarquía entre ellas."""
    cols = ""
    palette = ["#2EE6F0", "#3EE08C", "#FFC53D", "#FF8A5B"]
    for i, o in enumerate(options):
        c = palette[i % len(palette)]
        items = "".join(
            f'<div style="display:flex;gap:7px;margin-top:9px;font-size:12.5px;line-height:1.4">'
            f'<span style="color:{c};font-weight:800">—</span><span>{it}</span></div>'
            for it in o["items"])
        cols += f"""<div class="box" style="flex:1;border-color:{c};background:{_tint(c)};padding:15px 16px">
  <div style="font-weight:800;color:{c};font-size:16px;line-height:1.25">{o['name']}</div>{items}</div>"""
    head = section_title(title, accent, number) if title else ""
    return (f'<div style="flex:{grow};display:flex;flex-direction:column;justify-content:center">{head}'
            f'<div style="display:flex;gap:10px;align-items:stretch">{cols}</div></div>')


def _connector(color="#2EE6F0", delay=0):
    """Conector dibujado: línea + punto. En los clips de referencia el punto
    sobre la ruta es justo lo que se anima -- una flecha de texto no da eso.
    animation-duration=1.5s es divisor de los 6s del loop final (ver 5.1 del
    skill) -- 4 ciclos exactos, cierra sin salto. El delay escalonado por
    conector es lo que da la sensación de pulso viajando por la cadena."""
    return (f'<div style="display:flex;align-items:center;min-width:26px;flex:0 0 26px">'
            f'<span style="height:2px;flex:1;background:{color};opacity:.55"></span>'
            f'<span style="width:7px;height:7px;border-radius:50%;background:{color};'
            f'box-shadow:0 0 7px {color};margin:0 -1px;animation:dotpulse 1.5s ease-in-out infinite;'
            f'animation-delay:{delay}s"></span>'
            f'<span style="height:2px;flex:1;background:{color};opacity:.55"></span></div>')


def cycle_flow(nodes, grow=1, title=None, color="#2EE6F0", number=None):
    """Ciclo cerrado de N nodos que se retroalimenta."""
    boxes = ""
    for i, n in enumerate(nodes):
        if i > 0:
            boxes += _connector(color, delay=round((i - 1) * 0.28, 2))
        icon = f'<div style="font-size:15px;margin-bottom:3px">{n["icon"]}</div>' if n.get("icon") else ""
        boxes += (
            f'<div class="box" style="flex:1 1 0;text-align:center;padding:10px 7px;'
            f'background:{_tint(color)};border-color:rgba(46,230,240,.4);'
            f'display:flex;flex-direction:column;justify-content:center">{icon}'
            f'<div style="font-weight:800;font-size:12.5px">{n["name"]}</div>'
            f'<div style="font-size:10.5px;color:var(--mut);margin-top:2px;line-height:1.3">{n.get("desc","")}</div></div>'
        )
    ret = (f'<div style="display:flex;align-items:center;gap:8px;margin-top:9px;justify-content:center">'
           f'<span style="height:1.5px;width:120px;background:#FFC53D;opacity:.5"></span>'
           f'<span style="font-size:12px;color:#B8860B;font-weight:700">↻ {nodes[-1]["name"]} '
           f'retroalimenta a {nodes[0]["name"]}</span>'
           f'<span style="height:1.5px;width:120px;background:#FFC53D;opacity:.5"></span></div>')
    head = section_title(title, color, number) if title else ""
    return (f'<div style="flex:{grow};display:flex;flex-direction:column;min-height:0">{head}'
            f'<div style="flex:1;display:flex;align-items:stretch">{boxes}</div>{ret}</div>')


def cards_grid(cards, grow=1, cols=3, title=None, number=None, accent="#3EE08C"):
    """Grilla de categorías del mismo peso, sin orden de lectura obligatorio."""
    palette = ["#D9661E", "#2EE6F0", "#3EE08C", "#FFC53D", "#FF8A5B", "#2EE6F0"]
    cells = ""
    for i, c in enumerate(cards):
        col = c.get("color", palette[i % len(palette)])
        cells += (
            f'<div class="box" style="padding:11px 13px;border-left:3px solid {col};background:{_tint(col)};'
            f'display:flex;flex-direction:column;justify-content:center">'
            f'<div style="display:flex;align-items:center;gap:7px">'
            f'<span style="font-size:15px">{c.get("icon","▸")}</span>'
            f'<span style="font-weight:800;font-size:13.5px">{c["title"]}</span></div>'
            f'<div style="font-size:11.5px;color:var(--mut);margin-top:4px;line-height:1.35">{c["desc"]}</div></div>'
        )
    head = section_title(title, accent, number) if title else ""
    return (f'<div style="flex:{grow};display:flex;flex-direction:column;min-height:0">{head}'
            f'<div style="flex:1;display:grid;grid-template-columns:repeat({cols},1fr);'
            f'grid-auto-rows:1fr;gap:9px">{cells}</div></div>')


def metrics_row(metrics, grow=0, title=None, number=None, accent="#FFC53D"):
    """Fila de números grandes -- las 3 referencias cierran con cifras así;
    es lo que convierte un diagrama explicativo en un argumento con evidencia."""
    cells = "".join(
        f'<div class="box" style="flex:1;text-align:center;padding:12px 10px;'
        f'border-color:{m.get("color","#2EE6F0")};background:{_tint(m.get("color","#2EE6F0"))}">'
        f'<div style="font-size:27px;font-weight:900;color:{m.get("color","#2EE6F0")};line-height:1;'
        f'animation:numberbreathe 3s ease-in-out infinite;animation-delay:{round(i*0.5,2)}s">{m["value"]}</div>'
        f'<div style="font-size:11px;color:var(--mut);margin-top:5px;line-height:1.3">{m["label"]}</div></div>'
        for i, m in enumerate(metrics)
    )
    head = section_title(title, accent, number) if title else ""
    return f'<div style="flex:0 0 auto">{head}<div style="display:flex;gap:9px">{cells}</div></div>'


def annotation(text, align="left"):
    """Nota al margen en gris -- en las referencias estas notas sueltas son
    buena parte de la densidad percibida y del tono de 'análisis', no de slide."""
    return (f'<div style="flex:0 0 auto;font-size:11.5px;color:var(--mut);font-style:italic;'
            f'text-align:{align};line-height:1.4;padding:0 4px">{text}</div>')


def roles_evolution(roles, caption, grow=0):
    chain = f'<span style="color:#2EE6F0;margin:0 9px;font-weight:800">→</span>'.join(
        f'<span style="font-weight:800">{r}</span>' for r in roles
    )
    return f"""<div class="box" style="flex:0 0 auto;text-align:center;padding:13px">
  <div style="font-size:15px">{chain}</div>
  <div style="font-size:11.5px;color:var(--mut);margin-top:5px">{caption}</div></div>"""


def insights(items, grow=1, title=None, number=None, accent="#2EE6F0"):
    rows = "".join(
        f'<div style="display:flex;gap:11px;margin-bottom:11px;font-size:13.5px;line-height:1.45">'
        f'<div style="min-width:22px;font-size:17px">{it["icon"]}</div><div>{it["text"]}</div></div>'
        for it in items
    )
    head = section_title(title, accent, number) if title else ""
    return f'<div class="box" style="flex:{grow};display:flex;flex-direction:column;justify-content:center;padding:15px 18px">{head}{rows}</div>'


def recapbar(chips, grow=0):
    body = '<span style="color:var(--mut);margin:0 7px">→</span>'.join(
        f'<span style="background:rgba(46,230,240,.16);padding:7px 14px;border-radius:16px;font-weight:700;font-size:13px">{c}</span>'
        for c in chips
    )
    return f'<div style="flex:0 0 auto;text-align:center;background:rgba(46,230,240,.06);border-radius:14px;padding:11px">{body}</div>'


def journey_bar(steps, color="#2EE6F0"):
    """Barra de trayecto horizontal que conecta las secciones del póster en
    una sola narrativa -- el hilo que las referencias cierran con una fila de
    hitos (Request -> Context -> Loop -> ... -> Reply sent) y que un póster de
    bloques sueltos, por bien tintado que esté, no sugiere por sí solo."""
    dots = ""
    for i, s in enumerate(steps):
        if i > 0:
            dots += (f'<span style="flex:1;height:2px;background:{color};opacity:.35;'
                      f'margin-top:-19px;min-width:8px"></span>')
        dots += (
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:5px;flex:0 0 auto">'
            f'<span style="width:10px;height:10px;border-radius:50%;background:{color};'
            f'box-shadow:0 0 6px {color}"></span>'
            f'<span style="font-size:10px;font-weight:700;color:var(--mut);white-space:nowrap">{s}</span></div>'
        )
    return (f'<div style="flex:0 0 auto;display:flex;align-items:flex-start;'
            f'justify-content:space-between;padding:2px 10px 0">{dots}</div>')


def footer(name, role, refs, cta, avatar_b64=None):
    """avatar_b64: foto de perfil real como marca de agua -- string base64 (sin
    el prefijo data:), o None para el placeholder sin foto. El footer es el
    'marco fijo' de marca: en tema balanceado queda como franja oscura ancla
    aunque el cuerpo del póster sea claro (clase m-footer-dark, ver theme.py)."""
    ref_html = "<br>".join(refs)
    avatar_html = (
        f'<img class="avatar" src="data:image/jpeg;base64,{avatar_b64}">' if avatar_b64
        else '<div class="avatar" style="background:rgba(46,230,240,.25)"></div>'
    )
    return f"""
<div class="m-footer-dark" style="flex:0 0 auto;border-top:1.5px solid rgba(46,230,240,.35);padding-top:12px;
  display:flex;align-items:center;gap:16px">
  <div style="flex:1.3;font-size:10.5px;color:var(--mut);border-right:1px solid rgba(46,230,240,.3);padding-right:14px">{ref_html}</div>
  <div style="flex:1;text-align:center;border-right:1px solid rgba(46,230,240,.3);display:flex;
    align-items:center;justify-content:center;gap:10px">
    {avatar_html}
    <div style="text-align:left">
      <div style="font-weight:700;font-size:19px">{name}</div>
      <div style="font-size:11px;letter-spacing:2px;color:var(--mut)">{role}</div>
    </div>
  </div>
  <div style="flex:1;text-align:center">
    <span style="background:linear-gradient(90deg,#FFB627,#FFD25E);color:#1A1300;font-weight:800;
      font-size:13px;padding:9px 16px;border-radius:22px">{cta}</span></div>
</div>"""
