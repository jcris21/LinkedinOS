"""Paleta y envoltorio HTML compartidos por todos los módulos / arquetipos.

Dos temas, mismo marco fijo (header/footer siguen dando identidad de marca):
  - "dark"     -- el usado hasta ahora (fondo navy, texto claro)
  - "balanced" -- balance claro/oscuro: cuerpo del póster en tonos claros
                  (como el ejemplo real de +4200 likes), footer en navy
                  oscuro para anclar la identidad de marca entre posts.
"""

PALETTE = {
    "cyan": "#2EE6F0", "green": "#3EE08C", "gold": "#FFC53D",
    "ink": "#E8F4FB", "mut": "#9FB8CC", "bg0": "#0B2A45", "bg1": "#061527", "bg2": "#030B16",
}

BASE_CSS = """
* { box-sizing:border-box; margin:0; padding:0; }
body { width:1220px; height:1520px; overflow:hidden; position:relative;
  font-family:'Inter', Arial, sans-serif; color:%(ink)s; --mut:%(mut)s;
  background: radial-gradient(ellipse at 20%% 10%%, %(bg0)s 0%%, %(bg1)s 45%%, %(bg2)s 100%%);
  display:flex; align-items:center; justify-content:center; }
.canvas { width:1080px; height:1350px; position:relative; display:flex; flex-direction:column;
  padding:30px; gap:16px; }
.box { border-radius:18px; border:1.5px solid rgba(46,230,240,0.35);
  background:linear-gradient(160deg, rgba(16,58,92,0.55), rgba(8,28,48,0.65)); padding:18px 22px; }
.tag { display:inline-block; font-size:11px; font-weight:800; letter-spacing:0.5px; color:#fff;
  background:%(cyan)s; padding:3px 12px; border-radius:10px; }
.gapnote { position:absolute; right:30px; top:6px; font-size:10.5px; color:%(gold)s; font-weight:700;
  opacity:0.85; z-index:5; }
.mut { color:%(mut)s; }
.avatar { width:54px; height:54px; border-radius:50%%; object-fit:cover; flex:0 0 auto;
  border:2px solid rgba(46,230,240,0.6); }

/* duraciones divisoras de los 6s del loop final -- cierran sin salto (ver 5.1) */
@keyframes dotpulse { 0%%,100%% { transform:scale(1); opacity:.9; }
  50%% { transform:scale(1.9); opacity:1; box-shadow:0 0 14px currentColor; } }
@keyframes numberbreathe { 0%%,100%% { opacity:1; } 50%% { opacity:.72; } }
""" % PALETTE

# Overrides que balancean claro/oscuro: cuerpo claro (legible, como el
# ejemplo real de alto engagement), footer navy oscuro (marco fijo de marca).
BALANCED_CSS = """
body.theme-balanced { background:linear-gradient(160deg,#F7FAFD 0%,#EEF3F9 55%,#E6EDF6 100%) !important;
  color:#1B2A3D !important; --mut:#5B7083 !important; }
body.theme-balanced .box { background:#FFFFFF !important; border:1.5px solid rgba(20,60,100,0.16) !important;
  box-shadow:0 6px 22px rgba(20,45,80,0.08) !important; }
body.theme-balanced .m-footer-dark { background:#0B2A45 !important; border-radius:18px !important;
  padding:16px 22px !important; color:#E8F4FB !important; }
body.theme-balanced .m-footer-dark .mut { color:#9FB8CC !important; }
body.theme-balanced .avatar { border-color:#2EE6F0 !important; }
"""


def wrap(body_html, note=None, theme="dark"):
    note_html = f'<div class="gapnote">{note}</div>' if note else ""
    extra = BALANCED_CSS if theme == "balanced" else ""
    body_class = ' class="theme-balanced"' if theme == "balanced" else ""
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>{BASE_CSS}{extra}</style></head>
<body{body_class}>{note_html}<div class="canvas">{body_html}</div></body></html>"""
