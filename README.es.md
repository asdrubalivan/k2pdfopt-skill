🇬🇧 [Read in English](README.md)

# k2pdfopt

Un skill de Claude Code que convierte libros PDF (escaneados o nativos) en
PDFs listos para Kindle y Kobo con
[k2pdfopt](https://www.willus.com/k2pdfopt/), y verifica el resultado
muestreando páginas renderizadas en vez de confiar a ciegas en la
conversión — o renderizarlas todas.

![Comparación de portada: escaneo original vs. Kindle en gris vs. Kobo Libra Colour a color](docs/screenshots/cover-comparison.png)
*Conversión real, mismo libro: escaneo de 2.9 MB / 140 páginas → salida
Kindle en escala de grises de 51.3 MB / 727 páginas (`-fs 18`) y salida
Kobo Libra Colour a color de 97.8 MB / 717 páginas (`-fs 22`). La foto de
portada y los logos de la editorial están difuminados aquí por derechos de
autor — el libro fuente no es nuestro para redistribuir; lo que importa es
el contraste gris/color, que sobrevive al difuminado.*

## El problema

Un PDF pensado para imprenta o escaneado de un libro físico no se lee bien
en un panel e-ink de 6-7": texto justificado diminuto, márgenes pensados
para hoja carta, y a veces imágenes de escaneo en JPEG2000 que no todos los
lectores decodifican. Tampoco alcanza con un solo comando de `k2pdfopt` —
hay que elegir el modo/perfil de dispositivo/DPI correctos para el
*dispositivo destino*, y en una salida reflow de 700+ páginas no hay forma
práctica de confirmar que nada se rompió sin abrir el libro completo.

## Qué hace el skill

1. **Resuelve el binario de k2pdfopt** — no existe fórmula de Homebrew para
   esto (ver abajo), así que es un paso real, no un formalismo.
2. **Inspecciona el PDF fuente** — cantidad de páginas, si tiene una capa de
   texto real o es un escaneo puro, si trae imágenes JPEG2000.
3. **Aplana escaneos JPEG2000 a JPEG** cuando hace falta — algunos builds de
   k2pdfopt no decodifican JP2 de forma confiable; poppler sí, así que se
   usa como paso previo en vez de arriesgarse a una corrupción silenciosa.
4. **Elige el/los dispositivo(s) destino** — Kindle, Kobo Libra, o ambos.
5. **Calibra ajustes de letra grande**, solo si se pide — el tamaño de
   fuente en puntos se ajusta por dispositivo (ver abajo por qué eso no es
   una constante), con un selector visual de tamaño opcional.
6. **Corre k2pdfopt en background**, en paralelo por dispositivo — un libro
   real tarda 60-150+ segundos, bastante más que el timeout típico de un
   comando en primer plano.
7. **Verifica el resultado con muestreo**, no renderizando el libro entero —
   ver la siguiente sección.
8. **Reporta** rutas de archivo, tamaños, cobertura de la muestra, y
   cualquier advertencia.

## Antes / después: texto reflowed

![Comparación de página de texto: escaneo denso original vs. texto grande reflowed en Kindle y Kobo](docs/screenshots/textpage-comparison.png)
*La misma idea, con una página de texto corrido: el original desperdicia
casi toda la página en márgenes alrededor de texto justificado pequeño;
ambas salidas lo reflowean en texto grande y bien espaciado, dimensionado
para su panel. Kindle y Kobo necesitaron `-fs` (tamaño de fuente en puntos)
**distintos** para llegar a la misma cantidad de líneas objetivo — un panel
más alto cabe más líneas con el mismo tamaño de fuente, algo que no es obvio
hasta que se mide. Ver
[`reference/decision-guide.md`](reference/decision-guide.md).*

## Cómo se verifica el resultado

Renderizar e inspeccionar cada página de un libro de 1500 páginas gastaría
una cantidad prohibitiva de tokens — y la mayoría de los defectos de
conversión (perfil de dispositivo equivocado, detección de columnas rota,
un tamaño de fuente demasiado chico) son *sistémicos*: aparecen en la
mayoría de las páginas, no en una sola al azar. Eso cambia la pregunta de
"estimar la tasa de defectos con precisión" (necesita cientos de muestras,
y el tamaño de la muestra *crece* con el libro) a "si un problema afecta al
menos P% de las páginas, ¿cuál es el mínimo de páginas que necesito revisar
para tener C% de probabilidad de detectarlo al menos una vez?" — lo cual
**no** crece con el largo del libro:

```
n = ceil( ln(1 - C) / ln(1 - P) )
```

Con los valores por defecto (C=95%, P=10%) son **~29 páginas**, sea el
libro de 40 páginas o de 1500. Las páginas muestreadas se agrupan en 1-3
"hojas de contacto" con etiquetas en vez de leerse una imagen a la vez, así
que revisar ~30 páginas cuesta un par de lecturas de imagen, no treinta.

**Trade-off honesto**: esto detecta problemas recurrentes/sistémicos, no
una página suelta rota en medio de un libro por lo demás correcto. Ese es
el costo deliberado de no renderizar todo — ver
[`reference/quality-checklist.md`](reference/quality-checklist.md) para el
checklist completo y la matemática.

## Requisitos / instalación

**No existe fórmula de Homebrew para k2pdfopt.** `brew install k2pdfopt`
siempre va a fallar — confirmado, no lo reintentes. Ver
[`reference/installation.md`](reference/installation.md) para las opciones
reales (un binario que ya se tenga, la build precompilada oficial, o
compilar desde fuente con dependencias provistas por Homebrew).

También hace falta `poppler-utils` (`pdfinfo`, `pdftoppm`, `pdfimages`,
`pdffonts`, `pdftotext`) y Python 3 con Pillow, ambos para las herramientas
de verificación propias del skill.

## Cómo se usa

Esto es un skill de [Claude Code](https://claude.com/claude-code), no un
CLI independiente. Se instala (por ejemplo, con un symlink de este
directorio dentro de `~/.claude/skills/`), y se activa cuando le pides a
Claude convertir, optimizar, reflowear, o achicar un PDF de un libro para
Kindle o Kobo, o cuando mencionas k2pdfopt explícitamente.

## Dispositivos soportados

| Destino | Enfoque |
|---|---|
| Kindle (clase Paperwhite/Voyage/Oasis) | Perfil integrado `kv` o `ko2`, o `-w/-h/-dpi` manual para calzar exacto con el panel |
| Kobo Libra (H2O / 2 / Colour) | Perfil integrado `kol`, o geometría manual — todavía no existe alias integrado para el panel Kaleido 3 de 1264×1680 del Kobo Libra Colour, confirmado durante las pruebas |

Cualquier panel para el que k2pdfopt no traiga un perfil se puede seguir
targeteando con geometría manual `-w -h -dpi` — ver
[`reference/decision-guide.md`](reference/decision-guide.md).

## Estructura del repo

```
SKILL.md                     el flujo de 8 pasos descrito arriba
reference/
  installation.md            cómo conseguir un binario de k2pdfopt
  decision-guide.md          flags confirmados: modo/dispositivo/calidad/letra grande
  quality-checklist.md       matemática del muestreo + checklist por página
  cli-reference.md           autogenerado del --help real del binario instalado
scripts/                     el toolset en tiempo de ejecución que invoca SKILL.md
docs/                        assets de este README y herramientas de mantenimiento
```

## Decisiones de diseño notables

- Las conversiones corren **en background, en paralelo por dispositivo** —
  confirmado que es necesario; una corrida de reflow a color/letra grande
  supera cómodamente un timeout de 120s en primer plano.
- `-mode` empaqueta un conjunto entero de flags (incluyendo dispositivo y
  orientación); todo lo que deba sobreescribirlo — `-dev`, `-ls-`, `-c`,
  `-fs` — tiene que ir *después* en la línea de comandos, o ganan en
  silencio los defaults del modo.
- `-mode fw`/`fp` vienen en orientación **landscape** por defecto,
  confirmado de la forma difícil — siempre acompañar con `-ls-` para
  lectura vertical normal.
- El JPEG2000 se pre-aplana vía poppler solo cuando la fuente es
  verdaderamente solo-imagen; aplanar una página con texto embebido real la
  destruiría.
- El tamaño de fuente de letra grande (`-fs`) se calibra empíricamente por
  libro *y* por dispositivo, nunca fijo — la cantidad de líneas depende de
  la densidad del libro fuente y de la altura del panel destino, confirmado
  que varía de forma significativa entre paneles Kindle/Kobo por lo demás
  parecidos.

## Limitaciones

- La verificación por muestreo es un umbral de confianza, no una garantía —
  una única página suelta rota puede pasar sin detectarse.
- La lista de dispositivos integrada de k2pdfopt es anterior al hardware
  reciente (Kindle Paperwhite 11ª gen, Kobo Libra 2/Colour no tienen alias
  integrado exacto); la geometría manual cierra la brecha pero no es
  perfecta al pixel de fábrica.
- Conseguir un binario nativo de Apple Silicon hoy implica tener uno ya, o
  compilar desde fuente — todavía no hay una distribución empaquetada para
  eso.

## Licencia

Todavía no hay archivo de licencia — pendiente.

## Créditos

Construido sobre [k2pdfopt](https://www.willus.com/k2pdfopt/) de Willus Wu.
