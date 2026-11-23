import sys, json
from playwright.sync_api import sync_playwright
import matcher, registry, composer, theme
from cases import CASES

# decisión humana simulada para esta corrida de prueba -- en producción esto
# es el gate B6/B4: la persona confirma, pide otra variante, o rechaza.
HUMAN_DECISIONS = {
    "roadmap": True,
    "jerarquia": True,
    "hub": True,       # 2da aprobación de H_hub_red -> debería promoverlo
    "topologias": None,  # no aplica: ningún arquetipo llega a proponerse con score suficiente
    "ciclo_agentico": False,  # A anota ~65 (recomendado con advertencia) pero se pierde
                               # el ciclo y la grilla -> el humano rechaza la propuesta
}

# tema visual por caso -- "balanced" = cuerpo claro + footer navy ancla
THEMES = {"ciclo_agentico": "balanced"}


def render_png(html_str, out_path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1220, "height": 1520}, device_scale_factor=1.6)
        page.set_content(html_str)
        page.wait_for_timeout(200)
        page.screenshot(path=out_path)
        b.close()


def run(case_id):
    case = CASES[case_id]
    signals, content = case["signals"], case["content"]

    result = matcher.propose(signals)
    print(f"\n{'='*70}\nCASO: {case_id}")
    print(matcher.explain(result))

    chosen_key = None
    notes = []

    if result["needs_composition"]:
        gaps = registry.recurring_gaps()
        parts, notes = composer.compose_custom(signals, content, gaps)
        chosen_key = None
        gap_labels = [c[0] for c in result["best"]["missing_required"] and [] or []]
        logged_gaps = [f"{case_id}:sin_arquetipo_de_catalogo"]
        registry.log_decision(case_id, result, None, human_confirmed=False, gaps=logged_gaps)
        print("\n🧩 COMPUESTO A MEDIDA (ningún arquetipo pasó el umbral):")
        for n in notes:
            print("   -", n)
    else:
        chosen_key = result["best"]["archetype"]
        confirmed = HUMAN_DECISIONS.get(case_id, True)
        if not confirmed:
            # el humano rechazó la propuesta -> se compone a medida igual,
            # aunque el score haya sido alto (gusto/contexto que el matcher no ve)
            gaps = registry.recurring_gaps()
            parts, notes = composer.compose_custom(signals, content, gaps)
            registry.log_decision(case_id, result, None, human_confirmed=False,
                                   gaps=[f"{case_id}:rechazado_por_humano"])
            print("\n🧩 Humano RECHAZÓ la propuesta -> se compone a medida igual.")
        else:
            parts = composer.assemble_known(chosen_key, content)
            registry.log_decision(case_id, result, chosen_key, human_confirmed=True)
            print(f"\n✅ Humano confirmó: {chosen_key}")
            if result["best"].get("learned"):
                rec, promoted = registry.bump_approval(chosen_key)
                print(f"   aprobaciones acumuladas: {rec['approvals']}"
                      + (" -> 🎖️ PROMOVIDO a arquetipo confiable" if promoted else ""))

    html_str = theme.wrap("".join(parts), theme=THEMES.get(case_id, "dark"))
    out = f"/home/claude/poster_test/system/out_{case_id}.html"
    with open(out, "w") as f:
        f.write(html_str)
    render_png(html_str, f"/home/claude/poster_test/system/out_{case_id}.png")
    print(f"   -> {out}.png")


if __name__ == "__main__":
    for cid in (sys.argv[1:] or list(CASES.keys())):
        run(cid)
