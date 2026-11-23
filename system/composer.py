import modules as m

# títulos de sección por módulo -- el contenido puede sobrescribirlos vía
# content["titles"]; si no hay, se usa este default (las referencias rotulan
# todos sus paneles, y sin rótulo el lector tiene que deducir qué mira)
DEFAULT_TITLES = {
    "compare2": "El contraste",
    "compareN": "Las alternativas",
    "cycle_flow": "El ciclo",
    "cards_grid": "Fase por fase",
    "funnel": "Las capas",
    "timeline": "La línea de tiempo",
    "hub_network": "El sistema",
    "insights": "Hallazgos y advertencias",
    "metrics_row": "Los números",
}


def _title(content, key):
    return content.get("titles", {}).get(key, DEFAULT_TITLES.get(key))


class _Numbering:
    """Numera y colorea cada sección rotulada en orden de aparición -- es el
    badge con círculo de color + número que en la referencia 'AI Harness'
    hace que seis bloques iguales se lean como seis pasos de un sistema, en
    vez de seis cajas blancas sin jerarquía entre sí. Además guarda el título
    de cada sección para la journey_bar final."""
    def __init__(self):
        self.i = 0
        self.titles = []

    def next(self, title):
        color = m.SECTION_PALETTE[self.i % len(m.SECTION_PALETTE)]
        self.i += 1
        if title:
            self.titles.append(title)
        return self.i, color


def assemble_known(chosen_key, content):
    """Arma el HTML de un arquetipo YA conocido usando los módulos genéricos
    -- incluso los arquetipos 'de catálogo' pasan por la misma librería que
    usa el composer, para que todo el sistema sea una sola pieza auditable."""
    parts = [m.header(content["title"], content["subtitle"], content.get("tagline"),
                      content.get("kicker"))]
    num = _Numbering()

    if chosen_key == "A_proceso_mejora":
        t = _title(content, "compare2"); n, c = num.next(t)
        parts.append(m.compare2(content["left"], content["right"], grow=2, title=t, number=n, accent=c))
        t = _title(content, "insights"); n, c = num.next(t)
        parts.append(m.insights(content["metrics"], grow=1, title=t, number=n, accent=c))

    elif chosen_key == "B_jerarquia_capas":
        t = _title(content, "funnel"); n, c = num.next(t)
        parts.append(m.funnel(content["layers"], grow=3, title=t, number=n, accent=c))
        parts.append(m.recapbar(content["recap"]))

    elif chosen_key == "E_linea_tiempo":
        t = _title(content, "timeline"); n, c = num.next(t)
        parts.append(m.timeline(content["stages"], grow=3, title=t, number=n, accent=c))
        parts.append(m.recapbar(content["recap"]))

    elif chosen_key == "H_hub_red":
        t = _title(content, "hub_network"); n, c = num.next(t)
        parts.append(m.hub_network(content["hub_center"], content["satellites"], grow=2,
                                   title=t, number=n, accent=c))
        parts.append(m.roles_evolution(content["roles"], content["roles_caption"]))
        t = _title(content, "insights"); n, c = num.next(t)
        parts.append(m.insights(content["metrics"], grow=1, title=t, number=n, accent=c))

    if content.get("metrics_row"):
        t = _title(content, "metrics_row"); n, c = num.next(t)
        parts.append(m.metrics_row(content["metrics_row"], title=t, number=n, accent=c))
    if len(num.titles) >= 3:
        parts.append(m.journey_bar(num.titles))
    parts.append(m.footer(content["author"], content["role"], content["refs"], content["cta"],
                          content.get("avatar_b64")))
    return parts


def compose_custom(signals, content, recurring_gaps=None):
    """Sin arquetipo de catálogo con score suficiente (o humano rechazó):
    arma un layout propio a partir de la librería cruda de módulos, guiado
    por las señales reales del contenido -- y prioriza los gaps que vienen
    repitiéndose en el registro (si los hay)."""
    notes = []
    parts = [m.header(content["title"], content["subtitle"], content.get("tagline"),
                      content.get("kicker"))]
    num = _Numbering()

    if signals.get("has_named_alternatives"):
        t = _title(content, "compareN"); n, c = num.next(t)
        parts.append(m.compareN(content["alternatives"], grow=3, title=t, number=n, accent=c))
        notes.append("compareN: módulo nuevo para N alternativas sin jerarquía "
                      "(no existía en la librería -- A y B asumen 2 lados o niveles, "
                      "no N opciones paralelas)")
    elif signals.get("structure_type") == "hierarchy":
        t = _title(content, "funnel"); n, c = num.next(t)
        parts.append(m.funnel(content.get("layers", []), grow=3, title=t, number=n, accent=c))
    elif signals.get("structure_type") == "timeline":
        t = _title(content, "timeline"); n, c = num.next(t)
        parts.append(m.timeline(content.get("stages", []), grow=3, title=t, number=n, accent=c))
    elif signals.get("has_hub_center"):
        t = _title(content, "hub_network"); n, c = num.next(t)
        parts.append(m.hub_network(content.get("hub_center", ""), content.get("satellites", []),
                                   grow=2, title=t, number=n, accent=c))
    elif signals.get("structure_type") == "sequence" and content.get("left") and content.get("right"):
        t = _title(content, "compare2"); n, c = num.next(t)
        parts.append(m.compare2(content["left"], content["right"], grow=1.5,
                                title=t, number=n, accent=c))

    if content.get("annotation"):
        parts.append(m.annotation(content["annotation"]))

    if signals.get("has_cycle") and content.get("cycle_nodes"):
        t = _title(content, "cycle_flow"); n, c = num.next(t)
        parts.append(m.cycle_flow(content["cycle_nodes"], grow=0.8, title=t, number=n, color=c))
        notes.append("cycle_flow: módulo nuevo para un flujo cerrado que se retroalimenta "
                      "(ni jerarquía ni hub-con-centro -- A, B y H no lo cubren)")
    if signals.get("n_cards") and content.get("cards"):
        t = _title(content, "cards_grid"); n, c = num.next(t)
        parts.append(m.cards_grid(content["cards"], grow=1.6, title=t, number=n, accent=c))
        notes.append("cards_grid: módulo nuevo para categorías del mismo peso sin orden "
                      "de lectura obligatorio (insights asume una lista jerárquica de hallazgos)")

    if signals.get("has_roles_evolution") and content.get("roles"):
        parts.append(m.roles_evolution(content["roles"], content.get("roles_caption", "")))
    if signals.get("has_metrics") and content.get("metrics"):
        t = _title(content, "insights"); n, c = num.next(t)
        parts.append(m.insights(content["metrics"], grow=1, title=t, number=n, accent=c))
    if content.get("metrics_row"):
        t = _title(content, "metrics_row"); n, c = num.next(t)
        parts.append(m.metrics_row(content["metrics_row"], title=t, number=n, accent=c))
    if signals.get("has_recap_chain") and content.get("recap"):
        parts.append(m.recapbar(content["recap"]))

    if len(num.titles) >= 3:
        parts.append(m.journey_bar(num.titles))
    parts.append(m.footer(content["author"], content["role"], content["refs"], content["cta"],
                          content.get("avatar_b64")))

    if recurring_gaps:
        notes.append(f"gaps recurrentes en el registro considerados: {[g for g,_ in recurring_gaps]}")
    return parts, notes
