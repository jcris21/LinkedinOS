"""Póster de grafo con el lenguaje visual de los pósters maestros:
grafo a la izquierda + panel punteado a la derecha, paleta muestreada,
cards con píldora de encabezado y barra de hitos al cierre.
"""
import os
import graph as G
import palette as P
from cases import AUTHOR

AV = AUTHOR["avatar_b64"]

NODES = [
    dict(name="intent.md",      icon="\U0001F3AF", sub="qué construir\ny por qué",   edge="modela"),
    dict(name="spec.md",        icon="\U0001F4C4", sub="diseño\ny enfoque",          edge="descompone"),
    dict(name="plan.md",        icon="\U0001F5FA", sub="plan de\nimplementación",    edge="ejecuta"),
    dict(name="código + tests", icon="\U0001F4BB", sub="el diff\nverificable",       edge="audita"),
    dict(name="review",         icon="\U0001F50D", sub="aprobación\ny deploy",       edge="despliega"),
    dict(name="producción",     icon="\U0001F4E1", sub="incidente\no métrica",       edge=""),
]

CARDS = [
    (1, "\U0001F4DD", "Plan", "Diseño y requisitos convergen",
     "Dejan de ser dos etapas con un handoff en medio.",
     "\U0001F50E", "Señal", "una sola sesión produce intent y spec", "orange"),
    (2, "\U0001F4C1", "Build", "El contexto vive en archivos",
     "El conocimiento institucional sale de las cabezas.",
     "\U0001F50E", "Señal", "un agente nuevo arranca sin onboarding", "purple"),
    (3, "\U0001F9EA", "Test", "Evals continuas, no QA final",
     "La verificación corre con cada diff, no al cierre.",
     "⚠", "Trampa", "evals que solo miden el happy path", "teal"),
    (4, "\U0001F501", "Maintain", "La alerta escribe el intent",
     "Producción abre el siguiente ciclo por sí sola.",
     "\U0001F50E", "Señal", "el incidente llega como spec, no como ticket", "green"),
]

TRAPS = [
    P.trap("SDLC con un bot en medio",
           "Si una etapa sigue esperando a la anterior, no cambiaste de modelo."),
    P.trap("Medir solo el pico de la demo",
           "Ahí es donde el éxito cae de >80% a ≤38% en evolución continua."),
    P.trap("Saltarse la cadena por velocidad",
           "Ganas ritmo y pierdes el rastro que el incidente te va a pedir."),
    P.trap("Automatizar también la auditoría",
           "Auditar todo con el agente es tan frágil como no auditar nada."),
    P.ok_pill("cada commit deja el rastro que antes vivía en reuniones"),
]

METRICS = [
    ("-93%", "tiempo de diagnóstico de causa raíz", "green"),
    ("+200h", "ahorradas por mes en el mismo piloto", "blue"),
    ("≤38%", "éxito en evolución continua (EvoClaw)", "orange"),
]

JOURNEY = [("intent", "orange"), ("spec", "orange"), ("plan", "purple"),
           ("build", "purple"), ("review", "teal"), ("deploy", "blue"),
           ("producción", "green")]

REFS = ("Feng et al. (2026). Graph Engineering in the Era of LLM Agents. arXiv:2608.21156<br>"
        "Cao, Z. (2026). The End of Software Engineering. arXiv:2606.05608")

graph_html, graph_css = G.ring_flow(
    NODES,
    center=dict(title="El rastro de auditoría", sub="CADA ARTEFACTO QUEDA ESCRITO"),
    loop_label="retroalimenta",
    accent=P.a("orange"), close_accent=P.a("blue"),
    gate=G.gate_block("¿punto crítico?", "lo audita un humano", "deploy automático"),
    gate_edge=4,
)

cards_html = "".join(P.pill_card(*c) for c in CARDS)
panel_html = P.side_panel("⚠", "Las trampas", TRAPS, accent="red")
journey_html = P.journey(JOURNEY)
metrics_html = "".join(
    f'<div class="met" style="background:{P.a(c,"tint")};border-color:{P.a(c)}44">'
    f'<div class="mval" style="color:{P.a(c)};animation-delay:{round(i*0.5,2)}s">{v}</div>'
    f'<div class="mlab">{l}</div></div>'
    for i, (v, l, c) in enumerate(METRICS))

HTML = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ width:1220px; height:1520px; overflow:hidden;
  font-family:'Inter','Inter Display',sans-serif; color:{P.BODY}; --mut:{P.MUT};
  background:#DFE4EE; display:flex; align-items:center; justify-content:center; }}
.canvas {{ width:1080px; height:1350px; background:{P.PAGE};
  padding:26px 28px 24px; display:flex; flex-direction:column; gap:12px; position:relative; }}

.kick {{ font-family:'Inter Display',Inter,sans-serif; font-size:11.5px; font-weight:800;
  letter-spacing:2.6px; color:{P.a('orange')}; }}
h1 {{ font-family:'Inter Display',Inter,sans-serif; font-size:45px; font-weight:800;
  letter-spacing:-1.7px; line-height:1.02; margin-top:4px; color:{P.INK}; }}
.sub {{ font-size:17px; color:{P.MUT}; margin-top:5px; letter-spacing:-.2px; }}

.strip {{ display:flex; align-items:stretch; border:1.4px solid {P.BORDER}; border-radius:11px;
  background:#FFF; overflow:hidden; font-size:13px; flex:0 0 auto; }}
.scell {{ padding:8px 14px; display:flex; align-items:center; gap:7px; flex:0 0 auto;
  border-right:1.4px solid #E6EAF1; }}
.scell:last-child {{ border-right:none; }}
.stag {{ font-weight:800; font-size:11px; letter-spacing:.9px; text-transform:uppercase;
  padding:3px 10px; border-radius:7px; white-space:nowrap; }}

{G.GRAPH_CSS}
.gnode {{ --nb:{P.a('orange')}55; --nac:{P.a('orange','chip')}; }}
.gcenter {{ background:{P.DEEP} !important; }}

{P.CSS}

.mid {{ display:flex; gap:13px; flex:1; min-height:0; }}
.rail {{ flex:1; display:flex; flex-direction:column; gap:11px; min-height:0; }}
.spanel {{ flex:0 0 auto; }}

.cards {{ display:grid; grid-template-columns:repeat(4,1fr); gap:9px; flex:0 0 auto; }}

.mets {{ display:flex; flex-direction:column; gap:10px; flex:1; min-height:0; }}
.met {{ flex:1; border:1.4px solid; border-radius:11px; padding:10px 12px; text-align:center;
  display:flex; flex-direction:column; align-items:center; justify-content:center; }}
.mval {{ font-family:'Inter Display',Inter,sans-serif; font-size:34px; font-weight:800;
  letter-spacing:-1.2px; line-height:1; animation:breathe 3s ease-in-out infinite; }}
.mlab {{ font-size:12.5px; color:{P.MUT}; margin-top:5px; line-height:1.3; }}
@keyframes breathe {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.74; }} }}

.foot {{ background:{P.DEEP}; border-radius:12px; padding:12px 18px;
  display:flex; align-items:center; gap:15px; color:#E6ECFF; flex:0 0 auto; }}
.frefs {{ flex:1.25; font-size:11px; color:#9BA9D6; line-height:1.4;
  border-right:1px solid #1E327F; padding-right:14px; }}
.fme {{ flex:1; display:flex; align-items:center; justify-content:center; gap:10px;
  border-right:1px solid #1E327F; }}
.av {{ width:44px; height:44px; border-radius:50%; object-fit:cover; border:2px solid #6E86F5; }}
.fname {{ font-family:'Inter Display',Inter,sans-serif; font-weight:800; font-size:18.5px;
  letter-spacing:-.4px; }}
.frole {{ font-size:10.5px; letter-spacing:2px; color:#9BA9D6; margin-top:1px; }}
.fcta {{ flex:.95; text-align:center; }}
.fcta span {{ background:linear-gradient(92deg,#FFB627,#FFD35E); color:#20160A; font-weight:800;
  font-size:13.5px; padding:9px 16px; border-radius:20px; white-space:nowrap; }}

{graph_css}
</style></head>
<body><div class="canvas">

  <div>
    <div class="kick">INGENIERÍA AGÉNTICA</div>
    <h1>Del SDLC al Ciclo Agéntico</h1>
    <div class="sub">Seis artefactos, un solo ciclo: por qué el desarrollo deja de ser una línea</div>
  </div>

  <div class="strip">
    <div class="scell"><span class="stag" style="background:{P.a('orange','chip')};color:{P.a('orange')}">El contraste</span></div>
    <div class="scell" style="flex:1"><b>Antes:</b>&nbsp;requisitos → diseño → build → QA → release, en ese orden</div>
    <div class="scell" style="flex:1;background:{P.a('green','tint')}"><b>Ahora:</b>&nbsp;sin handoffs; el humano audita solo los puntos críticos</div>
  </div>

  <div class="mid">
    {graph_html}
    <div class="rail">
      {panel_html}
      <div class="mets">{metrics_html}</div>
    </div>
  </div>

  <div class="cards">{cards_html}</div>
  {journey_html}

  <div class="foot">
    <div class="frefs">{REFS}</div>
    <div class="fme">
      <img class="av" src="data:image/jpeg;base64,{AV}">
      <div><div class="fname">Christian Cobián</div><div class="frole">AI PRODUCT / SYSTEMS</div></div>
    </div>
    <div class="fcta"><span>Lee el análisis completo →</span></div>
  </div>

</div></body></html>"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out_ring.html")
with open(out, "w") as f:
    f.write(HTML)
print(out)
