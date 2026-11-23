"""English-language variant of build_ring.py — same engine, same layout,
translated copy. Every pipeline run produces one ES asset and one EN asset
from the same underlying data; this file is the EN side of that pair.
"""
import os
import graph as G
import palette as P
from cases import AUTHOR

AV = AUTHOR["avatar_b64"]

NODES = [
    dict(name="intent.md",      icon="\U0001F3AF", sub="what to build\nand why",     edge="models"),
    dict(name="spec.md",        icon="\U0001F4C4", sub="design\nand approach",       edge="breaks down"),
    dict(name="plan.md",        icon="\U0001F5FA", sub="implementation\nplan",       edge="executes"),
    dict(name="code + tests",   icon="\U0001F4BB", sub="the verifiable\ndiff",       edge="audits"),
    dict(name="review",         icon="\U0001F50D", sub="approval\nand deploy",       edge="deploys"),
    dict(name="production",     icon="\U0001F4E1", sub="incident\nor metric",        edge=""),
]

CARDS = [
    (1, "\U0001F4DD", "Plan", "Design and requirements converge",
     "They stop being two stages with a handoff in between.",
     "\U0001F50E", "Signal", "a single session produces intent and spec", "orange"),
    (2, "\U0001F4C1", "Build", "Context lives in files",
     "Institutional knowledge leaves people's heads.",
     "\U0001F50E", "Signal", "a new agent starts with no onboarding", "purple"),
    (3, "\U0001F9EA", "Test", "Continuous evals, not final QA",
     "Verification runs with every diff, not at the end.",
     "⚠", "Trap", "evals that only measure the happy path", "teal"),
    (4, "\U0001F501", "Maintain", "The alert writes the intent",
     "Production opens the next cycle on its own.",
     "\U0001F50E", "Signal", "the incident arrives as a spec, not a ticket", "green"),
]

TRAPS = [
    P.trap("SDLC with a bot in the middle",
           "If one stage still waits on the previous one, you haven't changed models."),
    P.trap("Measuring only the demo peak",
           "That's where success drops from >80% to ≤38% under continuous evolution."),
    P.trap("Skipping the chain for speed",
           "You gain pace and lose the trail the incident will demand."),
    P.trap("Automating the audit too",
           "Having the agent audit everything is as fragile as auditing nothing."),
    P.ok_pill("every commit leaves the trail that used to live in meetings"),
]

METRICS = [
    ("-93%", "root-cause diagnosis time", "green"),
    ("+200h", "saved per month in the same pilot", "blue"),
    ("≤38%", "success rate under continuous evolution (EvoClaw)", "orange"),
]

JOURNEY = [("intent", "orange"), ("spec", "orange"), ("plan", "purple"),
           ("build", "purple"), ("review", "teal"), ("deploy", "blue"),
           ("production", "green")]

REFS = ("Feng et al. (2026). Graph Engineering in the Era of LLM Agents. arXiv:2608.21156<br>"
        "Cao, Z. (2026). The End of Software Engineering. arXiv:2606.05608")

graph_html, graph_css = G.ring_flow(
    NODES,
    center=dict(title="The audit trail", sub="EVERY ARTIFACT GETS WRITTEN DOWN"),
    loop_label="feeds back",
    accent=P.a("orange"), close_accent=P.a("blue"),
    gate=G.gate_block("critical point?", "a human audits it", "automatic deploy",
                      yes_label="Yes", no_label="No"),
    gate_edge=4,
)

cards_html = "".join(P.pill_card(*c) for c in CARDS)
panel_html = P.side_panel("⚠", "The traps", TRAPS, accent="red")
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
    <div class="kick">AGENTIC ENGINEERING</div>
    <h1>From SDLC to the Agentic Cycle</h1>
    <div class="sub">Six artifacts, one cycle: why development stops being a line</div>
  </div>

  <div class="strip">
    <div class="scell"><span class="stag" style="background:{P.a('orange','chip')};color:{P.a('orange')}">The contrast</span></div>
    <div class="scell" style="flex:1"><b>Before:</b>&nbsp;requirements → design → build → QA → release, in that order</div>
    <div class="scell" style="flex:1;background:{P.a('green','tint')}"><b>Now:</b>&nbsp;no handoffs; the human only audits the critical points</div>
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
    <div class="fcta"><span>Read the full analysis →</span></div>
  </div>

</div></body></html>"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out_ring_en.html")
with open(out, "w") as f:
    f.write(HTML)
print(out)
