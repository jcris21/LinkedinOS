---
name: linkedin-animated-post-builder
description: Convierte un copy/hook ganador (de linkedin-hook-copywriter) en un póster técnico denso (título+subtítulo y byline/CTA fijos, cuerpo con un diagrama cuyo arquetipo —proceso con mejora, jerarquía de capas, comparación, árbol de decisión, línea de tiempo— se elige según la forma de la información del insight) y lo exporta como MP4 en loop con encuadre fijo (sin zoom/pan de cámara) y la animación viviendo en los elementos del propio diagrama, replicando el formato de infográficos técnicos que circulan como "video" en LinkedIn. No genera video creativo escena por escena — el movimiento es determinístico (ffmpeg + CSS), el valor está en el diagrama.
---

# linkedin-animated-post-builder

## Qué hace
Toma un insight técnico (copy + pilar + documentación de soporte) y lo convierte en un **póster informativo de una sola pantalla**: un marco fijo (título + subtítulo + byline/CTA, ver 1.1) con un **cuerpo cuyo arquetipo de diagrama se elige según la forma de la información** (ver 1.3 — proceso con mejora medible, jerarquía de capas, comparación de alternativas, árbol de decisión, o línea de tiempo), lo renderiza en alta resolución, y lo exporta como MP4 en loop con **encuadre de cámara fijo** — el movimiento vive adentro del diagrama (pulsos viajando por las rutas, glow respirando, cards encendiéndose en secuencia), no en la cámara — el mismo formato que usan creadores de IA B2B en LinkedIn para que un infográfico estático se distribuya como video nativo.

> **Nota de historial de diseño:** las primeras versiones de este skill sí aplicaban Ken Burns (zoom/pan lento de cámara sobre el póster completo). Se retiró por feedback explícito de Cris — el zoom/pan hacía que toda la publicación se sintiera "flotando", y eso competía con la lectura del contenido. El encuadre fijo + animación interna es el comportamiento por defecto desde esta versión (ver 5).

**Nota de referencia:** el formato (estructura del póster + tipo de movimiento) está basado en un ejemplo que Cris compartió de un post real de LinkedIn. Este skill replica el **formato**, nunca el contenido ni el diagrama específico de ese post — cada pieza que genera debe ser un diagrama original sobre el pilar/insight de Cris, no una copia del ejemplo.

## Cuándo se activa
- Como paso B3 del pipeline `linkedin-thought-leader-os`, después de que `linkedin-hook-copywriter` entrega título + subtítulo + ángulo técnico (ver nota de interfaz abajo).
- Suelto, cuando Cris ya tiene un insight/diagrama en mente y solo quiere el export animado.

## Inputs requeridos
| Input | Fuente | Obligatorio |
|---|---|---|
| Título + subtítulo del póster | B2 `linkedin-hook-copywriter` (ver nota de interfaz) | Sí |
| Insight técnico a diagramar (el "cómo funciona") | Cris / pilar de contenido | Sí |
| Claims/datos de soporte (si hay panel de métricas) | Cris, con fuente citable | Solo si se incluye panel de métricas |
| Brand kit (paleta, tipografía, logo, foto/handle para byline) | A2 `linkedin-brand-kit` | Sí |

> **Nota de interfaz con B2:** para este formato, `linkedin-hook-copywriter` ya no solo escribe el copy del post — también debe entregar: (1) título del póster, (2) subtítulo, (3) 2-4 bullets o pasos que estructuran el diagrama, y (4) el copy corto que acompaña el post en el feed (el texto que va *fuera* del video). Dado que B3 entrega ES+EN por regla (ver 7), B2 debe entregar estos 4 elementos **en ambos idiomas** (o el insight en bruto suficientemente claro para que B3 traduzca sin perder precisión técnica). Esto hay que ajustarlo en el spec de B2 cuando se formalice.

---

## 1. Anatomía del póster: marco fijo + arquetipo de cuerpo variable

Con dos ejemplos de referencia ya es visible el patrón: **el marco es constante, el cuerpo no.** El cuerpo cambia de estructura según la forma de la información del insight (y de la documentación de soporte que la respalda) — forzar siempre el mismo layout de flujo+comparación+métricas produciría diagramas forzados en temas que no son "un proceso que mejora" (como el ejemplo 2, que es una taxonomía de capas, no un proceso con antes/después).

### 1.1 Marco fijo (igual en todo póster, es lo que da identidad de marca)

```
┌─────────────────────────────────────────────┐
│          TÍTULO — gancho de 1-2 líneas        │
│   subtítulo — reformulación / mapa del        │
│   argumento (ej. "A → B → C" o 3 términos)    │
├─────────────────────────────────────────────┤
│                                               │
│         [ CUERPO — arquetipo variable,        │
│           ver 1.3 ]                           │
│                                               │
├─────────────────────────────────────────────┤
│  [foto] Nombre · "Sígueme para más sobre IA"  │
└─────────────────────────────────────────────┘
```
- **Header:** título corto y afirmativo (a veces una lista de 2-4 términos clave, a veces una promesa directa) + subtítulo que reformula el argumento completo en una línea (frecuentemente como cadena "X → Y → Z").
- **Footer:** foto real de Cris (marca de agua circular, no un ícono genérico) + nombre + CTA de follow — siempre presente, es lo que convierte alcance en seguidores. Implementado en `system/modules.py::footer(avatar_b64=...)`, con la foto embebida como base64 para que el HTML quede autocontenido.
- **Color-coding consistente** (regla transversal a cualquier arquetipo): cada categoría/capa/rama del diagrama tiene un color fijo, y ese mismo color se usa en el texto explicativo asociado (leyenda, panel, bullet) — es lo que hace que un diagrama denso se lea rápido sin esfuerzo.

**Dos temas, mismo marco** (`system/theme.py`, parámetro `theme="dark" | "balanced"`):
- `dark` — fondo navy, texto claro (el usado en los primeros 4 pósters de prueba).
- `balanced` — **balance claro/oscuro**: el cuerpo del póster pasa a paneles claros/blancos (más legible, calca el tratamiento del ejemplo real de +4200 likes que vimos en tema claro), y el **footer se mantiene como franja navy oscura** — ese anclaje es intencional: aunque el cuerpo cambie de tema post a post, el footer oscuro + la foto + el color de marca siguen dando la misma identidad reconocible en el feed. El color-coding (naranja/verde/cian/dorado) se mantiene igual en ambos temas porque ya tenía suficiente contraste sobre blanco.

### 1.2 Paso previo: modelar la información antes de elegir layout

Antes de maquetar nada, extraer del insight + documentación de soporte:
- ¿Cuáles son las entidades/categorías/pasos involucrados?
- ¿Cómo se relacionan entre sí — es una secuencia (A pasa a B pasa a C), una jerarquía (A contiene/refina a B), una disyuntiva (A o B, dependiendo de X), o una comparación (A vs. B, sin que uno dependa del otro)?
- ¿Hay una mejora medible o un resultado numérico que mostrar, o el valor es puramente explicativo/taxonómico?

Esa forma de la información es la que determina el arquetipo — no al revés.

### 1.3 Librería de arquetipos de cuerpo (seleccionar uno por post)

| Arquetipo | Cuándo usarlo | Elementos típicos | Evidencia |
|---|---|---|---|
| **A — Proceso con mejora medible** | El insight es "así se hace tradicionalmente vs. así se hace mejor", con un resultado cuantificable | Diagrama de flujo/swimlanes central + panel de contraste "antes/después" + panel de métricas | Clip de referencia 1 |
| **B — Jerarquía de capas / taxonomía** | El insight es una relación de conceptos en capas o niveles que se refinan entre sí (ej. "3 tipos de grafo que se alimentan uno al otro") | Embudo o stack de capas con color por nivel + columna lateral explicativa (1 bloque de texto por capa) + línea de tiempo/anotación lateral opcional + barra de recapitulación lineal al final | Clip de referencia 2 |
| **C — Comparación de alternativas (sin jerarquía)** | El insight es "opción A vs. B vs. C", ninguna deriva de otra | Columnas lado a lado, un color por opción, checklist de criterios debajo de cada una | Extrapolado — sin ejemplo de referencia todavía |
| **D — Framework / árbol de decisión** | El insight es una regla para decidir entre caminos ("si pasa X, hacé A; si pasa Y, hacé B") | Diamantes de decisión con ramas etiquetadas, termina en acciones concretas | Extrapolado — sin ejemplo de referencia todavía |
| **E — Evolución / línea de tiempo** | El insight describe cómo algo cambió o maduró en el tiempo | Eventos ordenados horizontalmente, cada uno con mini-explicación y fecha/hito | ✅ Validado — probado con el roadmap de 4 etapas (paper 2), score 100/100 contra su propia definición |
| **H — Hub / red de categorías acopladas** (aprendido, no estaba en el diseño original) | El insight es "un núcleo coordina/organiza N categorías satélite relacionadas entre sí, sin que una contenga a la otra" (ej. grafo multiagente con 5 subsistemas) | Nodo central con glow + N cajas satélite alrededor + franja de roles humanos + panel de hallazgos/métricas | ✅ Validado y **promovido** — 2 aprobaciones humanas (template dark original + reconfirmación con el matcher), ver 1.5 |

> C y D siguen siendo extrapolación sin caso real todavía. A, B, E y H ya están validados con contenido real de los dos papers de prueba. H nació de una composición manual (no estaba en el diseño original) y se promovió a arquetipo de catálogo tras su segunda aprobación — así es como se espera que crezca la librería en producción: por uso real, no por diseño anticipado.

### 1.5 Matching determinístico copy↔arquetipo, confirmación humana y composición propia

El riesgo de una librería de arquetipos cerrada es forzar contenido real dentro de un molde que no le queda — o, al revés, no tener nunca un camino para que aparezca un layout genuinamente nuevo cuando ninguno encaja. Este paso resuelve ambos problemas con tres piezas, todas deterministas y auditables (el LLM solo extrae señales; el score y la decisión los calcula código fijo):

**a) Extracción de señales (LLM) → score por arquetipo (código).**
El LLM lee el copy + la fuente documental y produce un JSON de señales de forma de la información (`structure_type`, `has_hub_center`, `has_before_after`, `has_metrics`, `has_dates`, `has_roles_evolution`, `n_items`, `has_named_alternatives`, etc. — ver `system/cases.py` para el esquema completo). Un scorer fijo (`system/matcher.py`) compara esas señales contra los criterios de cada arquetipo (`system/archetypes.py`) y devuelve, por cada uno: el score 0-100, qué señales cubre, y — crítico para la justificación — qué requisito obligatorio le falta si no califica. Nunca se "fuerza" un arquetipo al que le falta una pieza central: si falta algo marcado como obligatorio, el score queda capeado en 45 aunque el resto encaje perfecto.

**b) Umbrales de decisión.**
| Score del mejor arquetipo | Acción |
|---|---|
| ≥ 75 | Se recomienda directamente, con la justificación de qué cubre |
| 55–74 | Se recomienda con advertencia explícita de qué se pierde, mostrando la alternativa |
| < 55, o el humano rechaza la propuesta | Se compone un layout propio (ver c) |

**c) Composición propia + registro de gaps (`system/registry.py`, `system/composer.py`).**
Cuando nada califica, el sistema no intenta adaptar a la fuerza el arquetipo con mejor score: arma un layout nuevo a partir de la **librería cruda de módulos** (`system/modules.py` — header, hub, funnel, timeline, compare2, compareN, cycle_flow, cards_grid, roles, insights, recapbar, footer), seleccionando los que de verdad corresponden a las señales presentes. Cada rechazo/composición se loguea en un registro persistente (`registry.json`) junto con qué señal quedó sin cubrir. Ese registro cumple dos funciones:
1. **Prioriza gaps recurrentes** — si la misma señal no cubierta aparece seguido, el composer la prioriza en la próxima composición en vez de ignorarla de nuevo.
2. **Promueve composiciones repetidas a arquetipos de catálogo** — una composición que se aprueba 2 veces pasa a `promoted: true` y entra al pool de matching normal (así nació el arquetipo H de la tabla 1.3).

**Casos probados end-to-end:**
- "3 topologías de equipos de agentes sin jerarquía entre ellas" (cadena / routing-supervisor / fan-out-fan-in, paper 1) no calificó contra ningún arquetipo existente (mejor score 45, con "estructura de jerarquía" como requisito faltante) → el composer construyó un módulo nuevo, `compareN` (comparación N-way sin jerarquía, que no existía porque A y B asumen 2 lados o niveles fijos), y lo registró como gap.
- Un tercer ejemplo real de LinkedIn ("From SDLC to ADLC", +4200 likes, +250 comentarios — mismo patrón de póster técnico pero en tema claro, confirmando que el patrón no depende del tema de color) expuso dos formas que la librería no tenía: un **ciclo cerrado que se retroalimenta** (no es jerarquía ni hub-con-centro) y una **grilla de categorías del mismo peso sin orden de lectura** (distinta de `insights`, que es una lista jerárquica de hallazgos). Se agregaron `cycle_flow` y `cards_grid` a la librería de módulos. Ese mismo ejemplo real también mostró que un antes/después de proceso sin panel de métricas igual puede funcionar muy bien — por eso `has_metrics` pasó de obligatorio a bono en el arquetipo A. Al testear con contenido propio sobre esa misma forma (comparación SDLC-vs-agéntico + ciclo de artefactos + grilla de 6 fases), A anotó 65 (recomendado con advertencia) pero el humano lo rechazó porque la propuesta no capturaba el ciclo ni la grilla → el composer unió `compare2` + `cycle_flow` + `cards_grid` en un solo póster por primera vez, sin overflow ni espacio muerto.
- Un cuarto ejemplo real ("What Is an AI Harness?", formato tutorial de 6 secciones numeradas) confirmó, tras comparar nuestro propio output ya pulido contra esa referencia, un gap de jerarquía visual: el sistema tintaba cada panel por categoría pero **todas las secciones competían por la misma atención** (mismo acento cian, sin numerar) y el póster no tenía ningún elemento que uniera el argumento de principio a fin — la referencia cierra justo con eso, una barra de hitos horizontal. Se agregaron el badge numerado circular (`section_title(..., number=i)`, rotando colores por `SECTION_PALETTE`) y el módulo `journey_bar()`, ambos aplicados automáticamente por el composer vía un contador (`_Numbering`) en vez de requerir que cada caso los pida a mano.

### 1.6 Checklist de acabado (derivada de comparar contra las 3 referencias)

Al comparar frame a frame los pósters generados contra los tres ejemplos reales, los gaps no estaban en la estructura sino en el **acabado**. Esta es la checklist que cierra cada uno — todos implementados en `system/modules.py`:

| Gap detectado | Qué hacen las referencias | Regla que lo cierra |
|---|---|---|
| Aire muerto entre bloques | Nunca hay huecos: los paneles se estiran y el contenido se centra **dentro** de la caja | Módulos de bloque usan `flex:1` + `min-height:0` en el wrapper y `justify-content:center` dentro de cada caja. Un hueco entre cajas se lee como error de maquetado; un panel grande con su contenido centrado se lee como decisión |
| Paneles blancos planos | Cada panel lleva un tinte suave de su color de categoría | `TINTS[]` por acento — el tinte es lo que hace que un panel "pertenezca" a una categoría de un vistazo, sin leer el rótulo |
| Bloques sin rótulo | Todo panel está rotulado ("The Artifact Chain", "Evaluation Result") | `section_title(texto, color)` — barra de color + título, en todo módulo |
| Flechas `→` de texto | Conector dibujado con un punto sobre la ruta | `_connector()` — línea + punto con glow. Además es el elemento que después se anima (ver 5.1); una flecha de texto no permite eso |
| Nodos sin icono | Un icono por nodo, dentro de la caja | `icon` opcional en cycle_flow, cards_grid, compare2 |
| Sin anotaciones | Notas sueltas en gris/cursiva al lado de los elementos | `annotation()` — buena parte de la densidad percibida y del tono de análisis (vs. tono de slide) viene de ahí |
| Sin cifras de cierre | Las 3 referencias cierran con números grandes (80, 17%, 98%) | `metrics_row()` — es lo que convierte un diagrama explicativo en un argumento con evidencia |
| Header plano | Kicker de categoría en versalitas + título + subtítulo + nota lateral | `header(kicker=..., tagline=...)` |
| Secciones sin jerarquía entre sí (todas con el mismo tinte cian) | Cada sección numerada con un círculo de color propio y rotado — da la lectura de "pasos de un sistema" en vez de "cajas sueltas" | `section_title(..., number=i)` con `SECTION_PALETTE` rotando por sección; el composer numera automáticamente vía `_Numbering` |
| Sin hilo que una las secciones del póster | Una barra de hitos conecta el argumento completo de punta a punta, no solo dentro de cada panel | `journey_bar(titulos_de_seccion)` — se agrega automáticamente cuando el póster tiene 3+ secciones rotuladas, justo antes del footer |
| Texto de card ilegible a escala de feed | El póster se renderiza grande (~1080px) pero se ve en el feed a ~480-500px de ancho — un texto que se ve bien en el canvas de render se lee diminuto publicado | Subir el tamaño base de fuente de títulos/cuerpo de card en `graph.py`/módulos equivalentes, y acortar el copy del cuerpo si el texto más grande no entra, en vez de reducir la fuente para que entre |

**Regla de densidad:** las referencias meten ~40 elementos de información por póster; un layout con ~15 se ve vacío por más que esté bien alineado. Si el contenido no alcanza para llenar el canvas, el problema es el contenido, no el layout — antes de estirar cajas, agregar bullets, una anotación o una fila de métricas.

### 1.4 Elementos no negociables (universales, en cualquier arquetipo)
1. Título + subtítulo que reformula el argumento completo (header del marco fijo).
2. Un diagrama técnico real — con color-coding consistente entre diagrama y texto explicativo — nunca solo iconos decorativos.
3. Byline con foto + nombre + CTA de follow (footer del marco fijo).
4. Algún elemento de cierre/recapitulación visual del argumento completo (su forma varía por arquetipo: panel de métricas en A, barra lineal en B, etc.) — ambos ejemplos lo tienen, aunque con contenido distinto.

## 2. Especificaciones técnicas de salida

| Parámetro | Valor |
|---|---|
| Formato final | MP4, H.264 |
| Resolución del póster base (render estático) | 1350×1890px (se renderiza ~1.4x más grande que el frame final para dejar margen de zoom) |
| Resolución del video de salida | 1080×1512px (ratio ≈ 4:5.6, equivalente al ejemplo) — o 1080×1350 (4:5 estándar) si se prioriza consistencia con el resto del feed |
| Duración del loop | 5-8s (el ejemplo usa ~4.8s) |
| Movimiento | Encuadre de cámara **fijo** (sin zoom ni pan) — el movimiento vive en los elementos del diagrama (pulsos, glow, secuencia de cards), no en la cámara |
| Audio | Ninguno (autoplay de LinkedIn va sin sonido — todo el contenido ya está en el texto quemado del póster) |
| Texto | Debe ser legible a ~480px de ancho (tamaño real de render en el feed móvil) — nada de texto menor a ~22px efectivos en el póster base |

### 2.1 Por qué MP4 (no GIF) para loop infinito sin click

Pregunta recurrente: para que la persona NO tenga que hacer click y el póster entre en bucle infinito apenas aparece en el feed, hay dos formatos que logran eso en LinkedIn — pero con una diferencia de robustez importante:

| Formato | ¿Autoplay + loop sin click? | Límite que lo rompe |
|---|---|---|
| **MP4 subido como video, <15s** | Sí — se comporta igual que un GIF animado, en loop continuo | Ninguno relevante para nuestro caso (nuestros clips son de 5-8s, muy por debajo del límite) |
| GIF subido como imagen (no por el ícono de video) | Sí, también autoplay+loop sin click | Se congela en el primer frame si pesa más de 5MB o supera ~400 frames — un riesgo real para un diagrama denso con gradientes (los GIF comprimen mal ese tipo de contenido) |

**Por eso el skill ya elige MP4 por default**: a 5-8s de duración estamos cómodamente bajo el umbral de 15s que garantiza el loop automático, y no hay riesgo de que el formato falle silenciosamente por peso de archivo como sí le pasa al GIF con contenido rico en gradientes/glow. El GIF-como-imagen queda como alternativa solo si algún día se necesita publicar sin pasar por el flujo de video (ej. en un comentario, donde LinkedIn solo soporta GIF vía su propio buscador GIPHY, no archivo propio).

## 3. Paso a paso

1. **Modelar la información** (1.2): extraer entidades/categorías/pasos del insight + documentación de soporte, y cómo se relacionan (secuencia, jerarquía, disyuntiva, comparación).
2. **Elegir el arquetipo de cuerpo** (1.3) según esa forma de la información — no por default ni por el último post usado.
3. **Mapear el contenido al arquetipo**: título + subtítulo (marco fijo) + los elementos específicos del arquetipo elegido, con color-coding consistente entre diagrama y texto.
4. **Verificar exactitud técnica** — si el diagrama describe un concepto real (una arquitectura, un patrón, una técnica), no inventar pasos ni cifras; marcar explícitamente cualquier cifra de ejemplo como ilustrativa si no viene de un dato real de Cris.
5. **Maquetar el póster** en el motor de render elegido (ver decisión abajo), aplicando el brand kit (A2): paleta, tipografía, logo, foto de byline.
6. **Exportar el póster estático** en alta resolución (PNG, 1350×1890 o equivalente).
7. **Capturar la animación interna frame-exacta** con Playwright + WAAPI y componer el MP4 con ffmpeg, encuadre de cámara fijo (sin zoom/pan), loop sin salto visible.
8. **QA de legibilidad**: revisar el título/subtítulo y los paneles a tamaño de feed móvil (~480px) antes de pasar a `linkedin-post-qa-brand-check`.
9. **Generar la segunda variante de idioma** (ver 7): mismo data/layout, copy traducido — nunca se entrega un solo idioma.
10. **Entregar** ambos MP4 + ambos PNG estáticos (útiles como fallback o para carrusel) + alt-text + metadata, por idioma.

## 4. Motor de render del póster — decisión

| Opción | Cuándo usarla |
|---|---|
| **HTML/CSS + captura de pantalla (Playwright/headless)** *(recomendada por defecto)* | Layout denso y variable (cajas + conectores + paneles) que cambia de contenido cada semana. Totalmente scripteable → es la única opción que se automatiza de punta a punta sin intervención manual en una herramienta de diseño. |
| **Figma** (`generate_diagram` / `use_figma`) | Cuando Cris quiere un archivo maestro editable para retocar a mano o reusar como plantilla de equipo. |
| **Canva** (`generate-design-structured`) | Para variantes rápidas o si se prefiere mantener todo dentro del ecosistema de brand templates de Canva. |

**No se usa RunComfy para este formato** — no hay generación de imagen/video creativo involucrada; el "movimiento" es 100% determinístico sobre un render estático, así que un motor generativo de video no aporta nada aquí y sí introduce variabilidad innecesaria.

## 5. Encuadre fijo + animación interna, en términos simples (para quien lo automatice en n8n/ffmpeg)

**Por qué se retiró el Ken Burns (zoom/pan de cámara):** las primeras versiones aplicaban un zoom/pan lento y continuo sobre el póster completo. Feedback explícito de Cris: ese movimiento de cámara hacía que toda la publicación se sintiera "flotando" — competía con la lectura, en vez de ayudarla. Desde esta versión, **el encuadre de cámara es fijo por defecto**; todo el movimiento vive dentro del diagrama (ver 5.1).

- `render_anim.py` ya no aplica `zoompan` con zoom/pan — los parámetros `amp` (amplitud de zoom) y `pan` (desplazamiento vertical) tienen default `0`, así que el crop queda centrado y estático en todos los frames.
- El lienzo sigue teniendo margen de sangrado (1220×1520 para un frame de 1080×1350) porque el fondo decorativo se extiende al margen — eso es independiente del Ken Burns, es solo para que el crop final no corte el fondo contra el borde.
- Si alguna vez se necesita el movimiento de cámara de nuevo (por ejemplo, para un formato distinto), `render_anim.py` lo sigue soportando pasando `amp`/`pan` explícitos en la llamada — pero ya no es el comportamiento por defecto de ningún caso nuevo.
- Output a 24-30fps, 5-8s — eso no cambió.

### 5.1 Motor de movimiento — animación real del diagrama (validado con template dark)

Con la cámara fija, todo el "sentido de vida" del póster viene de **animaciones CSS** con duraciones divisoras del loop (1s, 1.5s, 2s, 3s, 6s), para que el loop cierre sin salto:
  - líneas punteadas que fluyen (`stroke-dashoffset`)
  - pulsos de luz que viajan por los conectores (`offset-path`, del nodo central a cada satélite, de entradas al hub y del hub a los resultados)
  - glow del nodo central (respiración de 3s)
  - **encendido en secuencia** de las tarjetas narrativas (01→02→03, roles humanos), cada una 1/3 del loop — guía la lectura del ojo
- `render_anim.py` pausa todas las animaciones con la Web Animations API, fija el tiempo de cada frame (`currentTime`), captura 150 frames (6s × 25fps) y recién después compone el MP4 con ffmpeg (crop fijo, sin zoom/pan). Resultado determinístico: el mismo HTML produce exactamente el mismo video.

### 5.2 Motor de movimiento v3 — grafo en anillo con rutas SVG reales y pulsos viajando por el trazo (`system/graph.py`)

Feedback sobre un cuarto clip de referencia ("Agent Development Lifecycle", E2.mp4) señaló que la v2 todavía no alcanzaba: los pulsos parecían "respirar" en el lugar en vez de viajar dentro del flujo, y había demasiado espacio entre el texto y sus contenedores. Diagnóstico cuantitativo (no visual): se acumularon las diferencias de píxel entre frames consecutivos del clip de referencia en una sola imagen ("mapa de movimiento") — reveló que lo que de verdad se mueve son puntos de luz recorriendo rutas SVG reales entre nodos, con una cola/trail visible, no un dot pulsando sobre un conector fijo.

- **`graph.py`** reemplaza el layout de fila completa por un **layout en anillo** (`ring_layout`): N nodos distribuidos en una elipse, con arcos SVG reales (`arc_path`) conectando nodos adyacentes, marcadores de flecha y píldoras de etiqueta por arista.
- Los pulsos viajan con **CSS `offset-path`** sobre el `d` real del arco (`ring_flow()`), elegido deliberadamente **en vez de SMIL `<animateMotion>`**: SMIL no aparece en `document.getAnimations()`, así que `render_anim.py` no puede pausarlo ni fijarle `currentTime` — rompería el pipeline de captura frame-exacta. `offset-path` sí es controlable por WAAPI.
- Soporta un **nodo de decisión** (`gate_block`, rombo) conectado al anillo por una ruta punteada adicional atada a una arista específica (`gate_edge`), para narrativas con un punto de control humano explícito.
- QA de esta versión: mapa de movimiento propio comparado contra el de la referencia (mismo patrón de "cola" visible); diff de píxeles entre el primer y el último frame del loop (~2.6/255 de media → loop sin salto); diff entre frames 0 y 20 (~80k píxeles con cambio de intensidad >40 → confirma que los pulsos viajan, no solo parpadean).

### 5.3 Paleta y componentes por muestreo directo de referencias "maestras" (`system/palette.py`)

Cuando Cris comparte una imagen de referencia como "diseño maestro", no se estima la paleta a ojo — se **muestrea por píxel** (`PIL.Image` + `collections.Counter` sobre recortes de la imagen) para extraer los hex reales. Esto corrigió un error de percepción: el tono oscuro de marca de las referencias es **índigo saturado** (`#001869` / `#0C298C`), no navy desaturado.

`palette.py` encapsula ese vocabulario visual una vez extraído:
- `ACCENTS` — 6 acentos con línea/tinte/chip (naranja, morado, teal, verde, azul, rojo).
- `pill_card()` — card con píldora de encabezado (badge + ícono + título dentro de un contenedor tintado), claim en negrita, cuerpo, separador punteado y línea de cierre con ícono ("Señal:", "Trampa:").
- `side_panel()` — panel de borde punteado con una píldora de leyenda montada sobre el borde superior (tratamiento tipo fieldset), para listas de advertencias/trampas.
- `journey()` — barra de hitos con puntos coloreados por etapa, línea conectora, flecha final y check en el último paso.

**Nota técnica recurrente:** cualquier bloque de CSS embebido en un string de Python con `%`-formatting rompe si tiene `%` literales (`border-radius:50%`) sin escapar como `%%`. Ya pasó dos veces en este proyecto (`theme.py` y `palette.py`) — la salida es escribir el bloque como f-string con `{{`/`}}` para las llaves literales, o escapar `%%` consistentemente si se mantiene `%`-formatting.

## 6. Guardrails

- El diagrama debe ser **original de Cris** — nunca una reproducción del diagrama/contenido de otro creador, aunque el formato esté inspirado en un ejemplo ajeno.
- Ninguna cifra en el panel de métricas sin respaldo real; si es ilustrativa, se marca como tal.
- Nunca queda texto por debajo de ~22px efectivos a tamaño de render final (pierde legibilidad en mobile).
- El byline + CTA de follow es obligatorio en todo póster — es lo que convierte alcance en seguidores.
- El zoom nunca recorta ningún elemento del diagrama fuera de cuadro en ningún punto del loop — se verifica en el frame de máximo zoom.

## 7. Formato de salida (handoff a B4)

**Regla de idioma (no negociable, vigente desde esta versión):** cada ejecución del
pipeline produce **dos activos del mismo post** — uno en español y uno en inglés —,
nunca solo uno. Ambos comparten `post_id`, arquetipo, data y layout; lo único que
cambia es el copy (título, subtítulo, textos de nodos/cards/panel, CTA) y cualquier
etiqueta de UI embebida en un módulo (ej. el rombo de decisión de `graph.py` usa
`yes_label`/`no_label` parametrizables — antes tenía "Sí"/"No" quemados, lo cual
rompía la variante en inglés; ver nota técnica abajo). Convención de nombre de
archivo: sufijo `_es` / `_en` antes de la extensión (`post_<id>_es.mp4`,
`post_<id>_en.mp4`).

```yaml
post_id: <referencia al copy de B2>
variantes:
  es:
    poster_estatico: poster_<id>_es.png   # 1350x1890, alta resolución
    archivo_principal: post_<id>_es.mp4   # 1080x1512 (o 1080x1350), H.264, 5-8s, encuadre fijo + animación interna
    alt_text: "<descripción del diagrama y su conclusión principal, en español>"
  en:
    poster_estatico: poster_<id>_en.png
    archivo_principal: post_<id>_en.mp4
    alt_text: "<same description, in English>"
arquetipo_elegido: A | B | C | D | E | H | custom   # ver 1.3/1.5 — "custom" = compuesto desde módulos
match_score: <0-100, del scorer determinístico — ver 1.5>
match_justificacion: "<qué señales cubre el arquetipo elegido, qué se pierde si aplica>"
confirmado_por_humano: true | false
gaps_registrados: [<señales no cubiertas, si se compuso un layout propio>]
diagrama_outline: [titulo, subtitulo, elementos_especificos_del_arquetipo]
fuentes_documentales: [<papers, docs o datos usados para modelar la información>]
motor_usado: html_screenshot | figma | canva
nota_para_qa: "<riesgos, cifras ilustrativas marcadas, etc.>"
```

**Nota técnica — texto embebido en módulos, no solo en el contenido:** cualquier
módulo nuevo en `modules.py`/`graph.py`/`palette.py` que incluya una palabra o
etiqueta de interfaz fija (como "Sí"/"No", "Antes"/"Ahora") debe recibir esa palabra
como parámetro con default en español, nunca hardcodeada — si no, la variante en
inglés sale con texto mezclado. Es el mismo tipo de gap que el escape de `%` en CSS:
un detalle de implementación que solo aparece al generar la segunda variante, no la
primera.

## 8. Condición de parada
Entrega el MP4 + PNG + metadata **de ambas variantes de idioma (ES + EN)** a `linkedin-post-qa-brand-check` y termina. No decide aprobación ni publica.

---

## Fuente de este formato
Análisis de frames de un clip de referencia que Cris compartió (post real de LinkedIn, formato "póster técnico + Ken Burns"), no de una fuente escrita — documentado aquí para trazabilidad del diseño del skill.
