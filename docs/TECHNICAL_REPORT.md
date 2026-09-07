# Relatório técnico

## Objetivo

O projeto investiga como combinar localização, preferência de produto e sazonalidade em um sistema simples de recomendação para agricultura familiar. A versão atual transforma o protótipo em notebook em uma biblioteca testável e executável por linha de comando.

## Pipeline

### 1. Preparação

Os CSVs representam associações, localidades, relacionamentos e produtos. A oferta demonstrativa é gerada com semente fixa. Essa mudança corrige a ausência de reprodutibilidade do experimento inicial.

### 2. Distância

A função de Haversine calcula a distância geodésica entre a coordenada do usuário e cada localidade. Para associações presentes em mais de uma região, somente a localidade mais próxima é mantida. Distâncias iguais recebem a mesma posição densa, começando em zero.

### 3. Produtos e sazonalidade

Se o usuário informa produtos, permanecem relações que contenham pelo menos um deles. Depois, contam-se os produtos relevantes disponíveis na estação escolhida. A maior contagem recebe `score_sazonal = 0`; empates recebem a mesma pontuação.

### 4. Ranking

O cálculo mantém a regra do notebook:

```text
score_total = score_distancia + score_sazonal
```

Quanto menor o valor, melhor a posição. Empates são ordenados por distância e sigla para garantir uma saída estável.

### 5. Colaboração

O módulo encontra usuários que avaliaram ao menos um produto também avaliado pelo usuário-alvo e sugere outros produtos desses usuários. Ele é complementar: suas avaliações não alteram o `score_total`. A refatoração corrige uma inconsistência do protótipo, que comparava nomes recomendados com IDs numéricos de produtos.

### 6. Mapa

Com a dependência opcional Folium, o comando gera um HTML com a posição informada e os pontos das associações ranqueadas. O mapa usa pontos centrais e não calcula rotas.

## Validação

Os testes automatizados cobrem:

- valores conhecidos da fórmula de Haversine;
- validação de coordenadas;
- carregamento e contagem das entidades;
- determinismo e cobertura da oferta simulada;
- combinação dos filtros;
- ordem e pontuação do ranking;
- recomendações colaborativas sem repetir item já visto.

## Reprodutibilidade e segurança

O repositório não depende de Google Drive, sessão Colab, API de geocodificação ou credencial do GitHub. Os notebooks antigos permanecem fora do projeto porque versões intermediárias continham um token. A credencial antiga deve ser revogada no GitHub mesmo sem ser publicada aqui.

## Responsabilidade autoral

O trabalho foi desenvolvido em equipe por Rodrigo Rangel Goes e Silva, Danilo Silveira da Silva e Nikolas Negrão Pessoa. Rodrigo contribuiu principalmente com a lógica e os testes e realizou a curadoria desta versão para portfólio.
