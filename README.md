# wireproto

Protótipo de geração de wireframes com abordagem **skeleton-first**.

## Objetivo

Gerar layouts estruturais antes da renderização visual.

```text
prompt -> semantic layout plan -> layout generator -> constraints -> LayoutGraph JSON -> SVG renderer
```

A fonte da verdade é o `LayoutGraph` em JSON; SVG é apenas a visualização.

## Rodar

```bash
python -m wireproto.cli "dashboard financeiro com sidebar, cards, gráfico e tabela"
```

Saídas: `output/layout.json` e `output/wireframe.svg`.

## Próximos passos

- gerador condicionado por LLM/Transformer
- dataset de layouts com hierarquia e bounding boxes
- Layout Transformer/Layout Diffusion
- scoring de overlap, alinhamento, densidade e hierarquia
- exportação HTML/Figma
