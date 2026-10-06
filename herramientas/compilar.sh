#!/usr/bin/env bash
# Compila el trabajo final a PDF a partir de documentacion/.
#
# Uso:
#   herramientas/compilar.sh                  genera el LaTeX y compila el PDF
#   herramientas/compilar.sh --con-pendientes incluye los puntos sin respuesta (con la leyenda "Pendiente")
#   herramientas/compilar.sh --solo-latex     genera latex/generado/ sin compilar
#   herramientas/compilar.sh --limpiar        borra latex/build/
#
# Resultado: latex/build/main.pdf
# Requiere: pandoc, xelatex y latexmk.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOC="$RAIZ/documentacion"
LATEX="$RAIZ/latex"
GEN="$LATEX/generado"
BUILD="$LATEX/build"
FILTROS="$RAIZ/herramientas/latex"

CON_PENDIENTES=false
COMPILAR=true
for arg in "$@"; do
  case "$arg" in
    --con-pendientes) CON_PENDIENTES=true ;;
    --solo-latex) COMPILAR=false ;;
    --limpiar) rm -rf "$BUILD"; echo "Borrado $BUILD"; exit 0 ;;
    -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Opción desconocida: $arg (ver --help)" >&2; exit 1 ;;
  esac
done

for cmd in pandoc xelatex latexmk; do
  command -v "$cmd" >/dev/null || { echo "Falta '$cmd' en el PATH" >&2; exit 1; }
done

# Títulos de los capítulos y de los subtítulos intermedios, según la consigna
declare -A CAPITULOS=(
  [1]="Descripción General"
  [2]="Análisis estratégico"
  [3]="Análisis FODA"
  [4]="Segmentación"
  [5]="Plan de Acción"
  [6]="Plan de Marketing"
  [7]="Operaciones"
  [8]="Plan Financiero-Económico"
  [9]="Factibilidades"
  [10]="Aspectos Descriptivos de la Solución Tecnológica"
  [11]="Anexos"
)
declare -A INTERMEDIOS=(
  [2.1]="Análisis de Contexto"
  [2.2]="Análisis de la Competencia"
  [6.4]="Producto. Estrategia de Producto"
  [6.5]="Precio. Estrategia de Precio"
  [6.6]="Comunicaciones integradas de marketing"
  [6.7]="Distribución"
  [10.4]="Documento visión"
  [10.5]="Descripción Global del Producto"
)

# Convierte la sección "Respuesta" de un .md a LaTeX (vacío si el punto no se incluye)
convertir() {
  local archivo="$1"; shift
  pandoc "$archivo" -f markdown -t latex \
    --lua-filter="$FILTROS/respuesta.lua" \
    -M incluir_pendientes="$CON_PENDIENTES" "$@"
}

mkdir -p "$GEN"

# --- Carátula -------------------------------------------------------------------
pandoc "$DOC/00 - Preliminares/Carátula.md" -f markdown -t latex \
  --lua-filter="$FILTROS/caratula.lua" > "$GEN/caratula-datos.tex"

# --- Preliminares (siempre se incluyen) -------------------------------------------
{
  for nombre in "Ficha de seguimiento y revisión" "Descripción del documento"; do
    echo '\clearpage'
    convertir "$DOC/00 - Preliminares/$nombre.md" -M siempre_incluir=true
    echo
  done
} > "$GEN/preliminares.tex"

# --- Resumen ejecutivo y capítulos --------------------------------------------------
{
  resumen="$(convertir "$DOC/00 - Preliminares/A. Resumen Ejecutivo.md")"
  if [[ -n "$resumen" ]]; then
    echo '\clearpage'
    echo "$resumen"
    echo
  fi

  while IFS= read -r carpeta; do
    num="$(basename "$carpeta" | sed -E 's/^0*([0-9]+).*/\1/')"
    titulo_cap="${CAPITULOS[$num]:-$(basename "$carpeta" | sed -E 's/^[0-9]+ - //')}"
    capitulo_emitido=false
    declare -A intermedio_emitido=()

    while IFS= read -r archivo; do
      cuerpo="$(convertir "$archivo")"
      [[ -z "$cuerpo" ]] && continue

      if ! $capitulo_emitido; then
        echo "\\capitulo{$num $titulo_cap}"
        echo
        capitulo_emitido=true
      fi

      punto="$(basename "$archivo" | grep -oE '^[0-9]+(\.[0-9]+)*')"
      if [[ "$punto" =~ ^([0-9]+\.[0-9]+)\.[0-9]+ ]]; then
        padre="${BASH_REMATCH[1]}"
        if [[ -n "${INTERMEDIOS[$padre]:-}" && -z "${intermedio_emitido[$padre]:-}" ]]; then
          echo "\\subcapitulo{$padre ${INTERMEDIOS[$padre]}}"
          echo
          intermedio_emitido[$padre]=1
        fi
      fi

      echo "$cuerpo"
      echo
    done < <(find "$carpeta" -maxdepth 1 -type f -name '*.md' ! -name '_*' -printf '%f\n' | sort -V | sed "s|^|$carpeta/|")

    unset intermedio_emitido
  done < <(find "$DOC" -mindepth 1 -maxdepth 1 -type d -name '[0-9][0-9] - *' ! -name '00 - *' | sort -V)
} > "$GEN/contenido.tex"

echo "LaTeX generado en $GEN"
$COMPILAR || exit 0

# --- Compilación ---------------------------------------------------------------------
mkdir -p "$BUILD"
cd "$LATEX"
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="$BUILD" main.tex >"$BUILD/latexmk.log" 2>&1 || {
  echo "Error al compilar. Detalle en $BUILD/main.log:" >&2
  grep -E -A5 '^!' "$BUILD/main.log" | head -30 >&2 || tail -30 "$BUILD/latexmk.log" >&2
  exit 1
}
echo "PDF generado: $BUILD/main.pdf"
