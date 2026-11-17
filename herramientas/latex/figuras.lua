-- Filtros que se aplican en el paso final a LaTeX.
--
-- Figuras apaisadas: una imagen con la clase .apaisada, por ejemplo
--   ![Diagrama de componentes](../imagenes/diagramas/componentes.svg){.apaisada}
-- se ubica sola en una página, rotada 90°, para aprovechar el alto de la hoja.

function Figure(fig)
  local img
  fig.content:walk({ Image = function(i) img = i end })
  if not (img and img.classes:includes("apaisada")) then return nil end
  local inlines = pandoc.utils.blocks_to_inlines(fig.caption.long)
  local caption = pandoc.write(pandoc.Pandoc({ pandoc.Plain(inlines) }), "latex"):gsub("%s+$", "")
  return pandoc.RawBlock("latex", table.concat({
    "\\begin{sidewaysfigure}",
    "\\centering",
    "\\includegraphics[width=\\textheight,height=0.92\\textwidth,keepaspectratio]{" .. img.src .. "}",
    "\\caption{" .. caption .. "}",
    "\\end{sidewaysfigure}",
  }, "\n"))
end

-- Código dentro de tablas: se escribe con \path (paquete url/xurl) para que los nombres largos,
-- como default_chatbot_workspace_id, puedan cortarse al final de la línea en vez de desbordar la celda.
local function codigo_cortable(c)
  if c.text:find("[{}]") then return nil end
  return pandoc.RawInline("latex", "\\path{" .. c.text .. "}")
end

function Table(t)
  return t:walk({ Code = codigo_cortable })
end
