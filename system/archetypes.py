"""
Definición de arquetipos conocidos (incluye los aprendidos/promovidos).
Cada criterio es (señal, valor_esperado, puntos, obligatorio).
Si falta un criterio obligatorio, el score se capea en REQUIRED_CAP
aunque el resto matchee perfecto -- así nunca se "fuerza" un arquetipo
que le falta una pieza central.
"""

REQUIRED_CAP = 45  # score máximo posible si falta algo obligatorio

ARCHETYPES = {
    "A_proceso_mejora": {
        "label": "Proceso con mejora medible (antes/después + métricas)",
        "criteria": [
            ("structure_type", "sequence", 30, True),
            ("has_before_after", True, 30, True),
            ("has_metrics", True, 25, False),  # evidencia real (post SDLC->ADLC, +4k likes
                                                # sin panel de métricas) bajó esto de obligatorio a bono
            ("n_items", (3, 9), 10, False),
            ("has_hub_center", False, 5, False),
        ],
    },
    "B_jerarquia_capas": {
        "label": "Jerarquía de capas / taxonomía",
        "criteria": [
            ("structure_type", "hierarchy", 35, True),
            ("n_items", (3, 5), 20, True),
            ("has_recap_chain", True, 15, False),
            ("has_metrics", False, 10, False),
            ("has_before_after", False, 10, False),
            ("n_satellite_categories", (0, 0), 10, False),
        ],
    },
    "E_linea_tiempo": {
        "label": "Línea de tiempo / evolución",
        "criteria": [
            ("structure_type", "timeline", 35, True),
            ("has_dates", True, 25, True),
            ("has_roles_evolution", True, 20, False),
            ("has_recap_chain", True, 10, False),
            ("has_metrics", False, 10, False),
        ],
    },
    "H_hub_red": {
        "label": "Hub / red de categorías acopladas (aprendido)",
        "learned": True,          # no estaba en la librería original -- se agregó por composición
        "approvals": 1,            # ya tiene 1 aprobación humana (sesión anterior)
        "promoted": False,         # se promueve a "confiable" en 2 aprobaciones
        "criteria": [
            ("structure_type", "hub_network", 30, True),
            ("has_hub_center", True, 25, True),
            ("n_satellite_categories", (3, 6), 20, True),
            ("has_metrics", True, 10, False),
            ("has_roles_evolution", True, 10, False),
            ("has_before_after", True, 5, False),
        ],
    },
}

PROMOTION_THRESHOLD = 2  # aprobaciones humanas repetidas para considerarlo "confiable"
