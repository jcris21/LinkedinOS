# LinkedinOS

Sistema de contenido automatizado de LinkedIn para posicionamiento como experto en IA
(Mid/Enterprise leaders): pipeline de skills + motor propio de pósters-diagrama animados.

## Documentación

- [`docs/linkedin-thought-leader-os-blueprint.md`](docs/linkedin-thought-leader-os-blueprint.md) —
  blueprint general del pipeline (A1→B7), qué es agente/skill/workflow y por qué.
- [`docs/linkedin-animated-post-builder-SKILL.md`](docs/linkedin-animated-post-builder-SKILL.md) —
  spec completa del componente B3: arquetipos de diagrama, matching determinístico
  copy↔arquetipo, motor de animación (`offset-path` + captura frame-exacta), y el
  flujo de extracción de paleta/componentes desde imágenes de referencia "maestras".

## `system/` — motor de render (código real, no las imágenes/videos generados)

| Archivo | Rol |
|---|---|
| `matcher.py` / `archetypes.py` / `registry.py` | Scoring determinístico copy↔arquetipo y registro de gaps/promociones |
| `composer.py` | Compone un layout desde módulos cuando ningún arquetipo califica; numera secciones y arma la barra de hitos |
| `modules.py` | Librería de bloques visuales reusables (header, hub, funnel, timeline, cards_grid, footer, etc.) |
| `graph.py` | Motor v3: layout de grafo en anillo con rutas SVG reales y pulsos animados vía CSS `offset-path` |
| `palette.py` | Vocabulario visual muestreado de referencias maestras: acentos, `pill_card`, `side_panel`, `journey` |
| `theme.py` | Temas `dark` / `balanced` |
| `cases.py` / `run_case.py` | Casos de prueba end-to-end por arquetipo |
| `build_ring.py` | Ensambla un póster completo usando `graph.py` + `palette.py` |
| `render_anim.py` | Captura frame-exacta (Playwright + Web Animations API) → Ken Burns (ffmpeg) |

Los outputs generados (`out_*.html/png`, `*_kenburns.mp4`) no se versionan — son
reproducibles corriendo `run_case.py` / `build_ring.py` + `render_anim.py`.

## Por qué `offset-path` y no SMIL

`render_anim.py` pausa todas las animaciones con `document.getAnimations()` para capturar
frames exactos antes de aplicar el Ken Burns. SMIL (`<animateMotion>`) no aparece en esa
API y por lo tanto no se puede pausar ni posicionar en un frame específico — por eso los
pulsos que viajan por los conectores usan CSS `offset-path`, que sí es controlable por
WAAPI.
