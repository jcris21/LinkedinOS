"""Paleta y vocabulario visual medidos sobre los dos pósters maestros
(muestreo de color directo sobre los PNG, no a ojo).

Hallazgo que más cambia el resultado: su "oscuro" no es un navy desaturado
sino un índigo saturado (#001869 / #0C298C). Eso es lo que hace que el
póster se lea como marca y no como slide corporativa.
"""

INK       = "#0C298C"   # títulos
DEEP      = "#001869"   # barras oscuras, nodo ancla, footer
BODY      = "#2B3550"   # texto de cuerpo
MUT       = "#5F6B85"   # texto secundario
PAGE      = "#F5F6FA"   # fondo de página
BORDER    = "#C9CCD6"   # borde de tarjeta clara

# acentos con su tinte de relleno y su chip (tinte más saturado)
ACCENTS = {
    "orange": dict(line="#E07B1F", tint="#FFF8F2", chip="#FDE7D1"),
    "purple": dict(line="#7C5CE0", tint="#F8F5FF", chip="#E6DCFC"),
    "teal":   dict(line="#16A394", tint="#F2FBF9", chip="#D4F5EE"),
    "green":  dict(line="#5A9E26", tint="#F8FBF1", chip="#EEF7DC"),
    "blue":   dict(line="#3B6EF6", tint="#F5F8FF", chip="#D6DFFE"),
    "red":    dict(line="#E5484C", tint="#FCEBE4", chip="#F9D2D3"),
}


def a(name, key="line"):
    return ACCENTS[name][key]


def pill_card(num, icon, title, claim, body, take_icon, take_label, take_text, accent):
    """Anatomía de card del póster maestro: píldora de encabezado (badge +
    icono + título dentro de un contenedor tintado), línea de claim en
    negrita, cuerpo, separador punteado y línea de cierre con icono.
    Sin la píldora el encabezado flota y la card se lee como una lista."""
    A = ACCENTS[accent]
    return f"""<div class="scard" style="background:{A['tint']};border-color:{A['line']}44">
  <div class="spill" style="background:{A['chip']}">
    <span class="sbadge" style="background:{A['line']}">{num}</span>
    <span class="sico">{icon}</span>
    <span class="stitle" style="color:{A['line']}">{title}</span>
  </div>
  <div class="sclaim">{claim}</div>
  <div class="sbody">{body}</div>
  <div class="ssep"></div>
  <div class="stake"><span>{take_icon}</span><b>{take_label}:</b>&nbsp;{take_text}</div>
</div>"""


def side_panel(legend_icon, legend, items, accent="purple"):
    """Panel lateral de borde punteado con la píldora montada SOBRE el borde
    (tratamiento tipo fieldset/legend). En los dos pósters maestros es lo que
    ocupa el costado del diagrama y sube la densidad sin apretar el grafo."""
    A = ACCENTS[accent]
    rows = "".join(items)
    return f"""<div class="spanel" style="border-color:{A['line']}88;background:{A['tint']}">
  <div class="slegend" style="background:{A['tint']};border-color:{A['line']};color:{A['line']}">
    <span>{legend_icon}</span>{legend}</div>
  {rows}
</div>"""


def trap(title, text, accent="red"):
    A = ACCENTS[accent]
    return (f'<div class="trap"><div class="ttitle" style="color:{A["line"]}">'
            f'<span class="tx" style="background:{A["chip"]};color:{A["line"]}">✕</span>{title}</div>'
            f'<div class="ttext">{text}</div></div>')


def ok_pill(text, accent="green"):
    A = ACCENTS[accent]
    return (f'<div class="okpill" style="background:{A["chip"]};border-color:{A["line"]}66;'
            f'color:{A["line"]}">\u2713 {text}</div>')


def journey(steps):
    """Barra de hitos: línea con punta de flecha, puntos en el color de su
    sección y check verde al final -- en el póster maestro es el hilo que
    convierte secciones sueltas en un recorrido."""
    dots = ""
    for i, (label, accent) in enumerate(steps):
        last = i == len(steps) - 1
        col = ACCENTS[accent]["line"]
        if i:
            dots += '<span class="jline"></span>'
        inner = '<span class="jcheck">✓</span>' if last else ""
        dots += (f'<div class="jstep"><span class="jdot" style="background:{col}">{inner}</span>'
                 f'<span class="jlab">{label}</span></div>')
    return f'<div class="journey">{dots}<span class="jarrow">›</span></div>'


CSS = f"""
.scard {{ border:1.4px solid; border-radius:13px; padding:9px 11px 8px;
  display:flex; flex-direction:column; }}
.spill {{ display:inline-flex; align-items:center; gap:7px; border-radius:18px;
  padding:3.5px 12px 3.5px 4px; align-self:flex-start; }}
.sbadge {{ width:21px; height:21px; min-width:21px; border-radius:50%; color:#fff;
  font-size:11.5px; font-weight:800; display:flex; align-items:center; justify-content:center; }}
.sico {{ font-size:13px; }}
.stitle {{ font-weight:800; font-size:14px; letter-spacing:-.25px; }}
.sclaim {{ font-weight:800; font-size:13.5px; margin-top:7px; color:{BODY}; line-height:1.25; }}
.sbody {{ font-size:12.5px; color:{MUT}; margin-top:3px; line-height:1.35; }}
.ssep {{ border-top:1.4px dotted {BORDER}; margin:7px 0 6px; }}
.stake {{ font-size:11.5px; color:{MUT}; display:flex; align-items:baseline; gap:5px; line-height:1.3; }}
.stake b {{ color:{BODY}; }}

.spanel {{ position:relative; border:1.6px dashed; border-radius:14px;
  padding:19px 13px 12px; display:flex; flex-direction:column; gap:9px; }}
.slegend {{ position:absolute; top:-12px; left:13px; border:1.5px solid; border-radius:16px;
  padding:3px 12px; font-size:12.5px; font-weight:800; display:flex; align-items:center; gap:6px;
  letter-spacing:-.2px; }}
.trap {{ background:#FFF; border:1.3px solid {BORDER}; border-radius:10px; padding:7px 9px; }}
.ttitle {{ font-weight:800; font-size:12.5px; display:flex; align-items:center; gap:6px;
  letter-spacing:-.2px; line-height:1.2; }}
.tx {{ width:16px; height:16px; min-width:16px; border-radius:50%; font-size:10px; font-weight:900;
  display:flex; align-items:center; justify-content:center; }}
.ttext {{ font-size:11.5px; color:{MUT}; margin-top:4px; line-height:1.35; }}

.journey {{ display:flex; align-items:flex-start; gap:0; flex:0 0 auto; padding:0 4px; }}
.jstep {{ display:flex; flex-direction:column; align-items:center; gap:4px; flex:0 0 auto; }}
.jdot {{ width:13px; height:13px; border-radius:50%; display:flex; align-items:center;
  justify-content:center; color:#fff; font-size:8.5px; font-weight:900; }}
.jlab {{ font-size:11px; color:{MUT}; white-space:nowrap; font-weight:600; }}
.jline {{ flex:1; height:1.6px; background:{BORDER}; margin-top:5.7px; min-width:10px; }}
.jarrow {{ color:{BORDER}; font-size:17px; line-height:.75; margin-top:1px; font-weight:900; }}
"""
