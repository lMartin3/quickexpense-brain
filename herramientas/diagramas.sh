#!/usr/bin/env bash
# Genera los diagramas de documentacion/imagenes/diagramas/*.puml en SVG (para Obsidian) y PDF (para LaTeX).
#
# Uso:
#   herramientas/diagramas.sh            genera todos los diagramas
#   herramientas/diagramas.sh nombre     genera solo nombre.puml
#
# Requiere: java, rsvg-convert y el jar de PlantUML (variable PLANTUML_JAR,
# por defecto ~/.local/share/plantuml/plantuml.jar).

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIR="$RAIZ/documentacion/imagenes/diagramas"
JAR="${PLANTUML_JAR:-$HOME/.local/share/plantuml/plantuml.jar}"

[[ -f "$JAR" ]] || { echo "No se encontró PlantUML en $JAR (definir PLANTUML_JAR)" >&2; exit 1; }
for cmd in java rsvg-convert; do
  command -v "$cmd" >/dev/null || { echo "Falta '$cmd' en el PATH" >&2; exit 1; }
done

if [[ $# -gt 0 ]]; then
  fuentes=("$DIR/${1%.puml}.puml")
else
  mapfile -t fuentes < <(find "$DIR" -maxdepth 1 -name '*.puml' ! -name '_*' | sort)
fi

for f in "${fuentes[@]}"; do
  base="${f%.puml}"
  java -jar "$JAR" -charset UTF-8 -tsvg "$f"
  rsvg-convert -f pdf -o "$base.pdf" "$base.svg"
  echo "Generado: ${base#$RAIZ/}.{svg,pdf}"
done
