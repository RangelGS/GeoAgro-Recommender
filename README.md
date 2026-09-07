# GeoAgro Recommender

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://github.com/RangelGS/GeoAgro-Recommender/actions/workflows/tests.yml/badge.svg)](https://github.com/RangelGS/GeoAgro-Recommender/actions/workflows/tests.yml)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RangelGS/GeoAgro-Recommender/blob/main/notebooks/GeoAgro_Recommender_Colab.ipynb)

Sistema acadêmico de recomendação georreferenciada que conecta consumidores a associações de produtores do Distrito Federal. O ranking combina proximidade, produtos desejados e sazonalidade; um módulo complementar sugere produtos a partir de avaliações de usuários com histórico semelhante.

> Trabalho da disciplina **Introdução à Inteligência Artificial — Universidade de Brasília (2025/1)**. Os dados de oferta e avaliações são demonstrativos; o projeto não deve ser usado como cadastro oficial de produtores.

## Resultado reproduzível

Com uma instalação padrão, a demonstração usa coordenadas de Brasília, raio de 30 km, produtos `Alface` e `Tomate`, estação `verão` e geração de oferta com semente fixa `42`.

```bash
geoagro recommend --latitude -15.7939 --longitude -47.8828 \
  --max-distance 30 --season verao --products Alface Tomate
```

O arquivo `results/reference/ranking.csv` registra a saída de referência produzida pela versão 1.0.0.

## Como funciona

1. Carrega 17 associações, 14 localidades, 35 produtos e seus relacionamentos.
2. Gera a oferta demonstrativa de produtos de modo determinístico (`seed=42`).
3. Mantém a localidade mais próxima de cada associação.
4. Filtra por raio, produtos e estação.
5. Calcula posições densas de distância e sazonalidade.
6. Ordena pelo menor `score_total = score_distancia + score_sazonal`.

O filtro colaborativo permanece separado do ranking principal, refletindo o experimento original. A implementação nova também corrige a associação entre nomes e IDs de produtos do protótipo em notebook.

## Instalação

No Windows (PowerShell):

```powershell
git clone https://github.com/RangelGS/GeoAgro-Recommender.git
cd GeoAgro-Recommender
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Para gerar um mapa HTML interativo:

```powershell
python -m pip install -e ".[map]"
geoagro recommend --latitude -15.7939 --longitude -47.8828 --map results/mapa.html
```

## Testes

```bash
python -m unittest discover -s tests -v
```

Os testes verificam distâncias, desempates, filtro por produto, sazonalidade, determinismo e recomendações colaborativas. O GitHub Actions repete essa validação em cada envio.

## Estrutura

```text
GeoAgro-Recommender/
├── data/sample/              # dados acadêmicos e demonstrativos
├── docs/                     # relatório técnico
├── metadata/                 # proveniência e limitações
├── notebooks/                # execução guiada no Colab
├── results/reference/        # saída versionada de referência
├── scripts/                  # atalhos de execução
├── src/geoagro/              # biblioteca e CLI
└── tests/                    # testes automatizados
```

## Autoria e contribuições

Projeto acadêmico desenvolvido por **Rodrigo Rangel Goes e Silva**, **Danilo Silveira da Silva** e **Nikolas Negrão Pessoa**. Rodrigo contribuiu principalmente com a lógica e os testes e fez a curadoria desta versão reproduzível para portfólio.

## Limitações

- Coordenadas representam pontos centrais aproximados das regiões administrativas.
- Relações de oferta e avaliações são simuladas para fins didáticos.
- A distância é geodésica em linha reta (Haversine), não uma rota viária.
- O ranking é heurístico e não constitui recomendação comercial.
- O notebook original não deve ser publicado porque versões intermediárias continham credencial; este repositório foi reconstruído sem segredos.

Consulte [metadata/DATA.md](metadata/DATA.md) e [docs/TECHNICAL_REPORT.md](docs/TECHNICAL_REPORT.md) para detalhes.
