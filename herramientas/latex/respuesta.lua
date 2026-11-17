-- Filtro de pandoc: de un .md de documentacion/ deja solo la sección "## Respuesta",
-- precedida por un título armado con el frontmatter (punto + titulo).
--
-- Metadatos que lee (frontmatter del .md o -M en la línea de comandos):
--   punto, titulo, estado    → del frontmatter (estado "omitido": nunca se incluye)
--   incluir_pendientes=true  → incluye los puntos sin respuesta con la leyenda "Pendiente"
--   siempre_incluir=true     → incluye el punto aunque esté pendiente (preliminares)
--   id, nombre               → casos de uso (casos-de-uso/CU-*.md): el título es "id nombre",
--                              va por debajo de 10.5.3 y lleva la etiqueta id en minúsculas
--                              (para \pageref en el índice de casos de uso, 10.5.2)

local stringify = pandoc.utils.stringify

local function meta_str(meta, key)
  return meta[key] and stringify(meta[key]) or ""
end

local function meta_bool(meta, key)
  local v = meta[key]
  if v == nil then return false end
  if type(v) == "boolean" then return v end
  return stringify(v) == "true"
end

-- "1.1" → 2 (subsection), "2.1.1" → 3 (subsubsection); "A." o vacío → 1 (section)
local function nivel_de(punto)
  local partes = 0
  for _ in punto:gmatch("%d+") do partes = partes + 1 end
  if partes < 2 then return 1 end
  return math.min(partes, 4)
end

local function es_vacio(bloques)
  for _, b in ipairs(bloques) do
    if not (b.t == "RawBlock" and b.format == "html") then return false end
  end
  return true
end

-- Anchos exactos de columna: al escribir el markdown intermedio, pandoc ajusta las tablas a 72 caracteres
-- y agranda las columnas según su contenido, lo que deforma las proporciones de la fila separadora.
-- Escribirlas con un ancho de 1000 caracteres conserva la proporción exacta hasta el paso a LaTeX.
-- Se aplica a los casos de uso (frontmatter con `id`) y a los puntos con `anchos_exactos: true`;
-- en el resto se mantiene el ajuste al contenido, del que dependen las tablas de los capítulos anteriores.
local function tabla_con_anchos_exactos(tbl)
  if FORMAT ~= "markdown" then return nil end
  -- Si todas las columnas tienen el mismo ancho (p. ej., "| --- | --- |"), se deja que pandoc las ajuste al contenido.
  local primero, distintos = nil, false
  for _, spec in ipairs(tbl.colspecs) do
    local ancho = spec[2] or 0
    if ancho == 0 then return nil end
    primero = primero or ancho
    if math.abs(ancho - primero) > 1e-6 then distintos = true end
  end
  if not distintos then return nil end
  local md = pandoc.write(pandoc.Pandoc({ tbl }), "markdown-simple_tables-multiline_tables-pipe_tables",
    pandoc.WriterOptions({ columns = 1000 }))
  return pandoc.RawBlock("markdown", md)
end

function Pandoc(doc)
  local meta = doc.meta
  if meta.id or meta_bool(meta, "anchos_exactos") then
    doc.blocks = doc.blocks:walk({ Table = tabla_con_anchos_exactos })
  end
  local punto = meta_str(meta, "punto")
  local titulo = meta_str(meta, "titulo"):gsub("%.%s*$", "")
  local estado = meta_str(meta, "estado")

  -- Bloques posteriores al encabezado "Respuesta"
  local respuesta, dentro = {}, false
  for _, b in ipairs(doc.blocks) do
    if dentro then
      if not (b.t == "RawBlock" and b.format == "html") then
        table.insert(respuesta, b)
      end
    elseif b.t == "Header" and stringify(b.content) == "Respuesta" then
      dentro = true
    end
  end

  if estado == "omitido" then
    return pandoc.Pandoc({}, meta)
  end

  local pendiente = estado == "pendiente" or es_vacio(respuesta)
  if pendiente and not meta_bool(meta, "siempre_incluir") then
    if meta_bool(meta, "incluir_pendientes") then
      if es_vacio(respuesta) then
        respuesta = { pandoc.Para({ pandoc.Emph({ pandoc.Str("Pendiente.") }) }) }
      end
    else
      return pandoc.Pandoc({}, meta)
    end
  end

  local id_cu = meta_str(meta, "id")
  local etiqueta = ""
  local nivel = nivel_de(punto)
  if id_cu ~= "" then
    punto, titulo = id_cu, meta_str(meta, "nombre")
    etiqueta = id_cu:lower()
    nivel = 4
  end

  -- Los títulos internos de la respuesta quedan por debajo del título del punto
  for i, b in ipairs(respuesta) do
    if b.t == "Header" then
      b.level = math.min(nivel + b.level - 1, 5)
      b.classes:insert("unnumbered")
      respuesta[i] = b
    end
  end

  local texto = (punto ~= "" and (punto .. " ") or "") .. titulo
  local encabezado = pandoc.Header(nivel, pandoc.Inlines(texto), pandoc.Attr(etiqueta, { "unnumbered" }))
  table.insert(respuesta, 1, encabezado)

  return pandoc.Pandoc(respuesta, meta)
end

-- Las imágenes se buscan por nombre en documentacion/imagenes y en documentacion/imagenes/diagramas
-- (ver \graphicspath en main.tex). Los diagramas se enlazan en SVG (Obsidian los muestra) y en el PDF
-- se usa la versión .pdf que genera herramientas/diagramas.sh.
function Image(img)
  img.src = img.src:match("([^/]+)$"):gsub("%.svg$", ".pdf")
  return img
end
