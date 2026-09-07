# Proveniência e natureza dos dados

## Origem

As listas de 17 associações/cooperativas, 14 localidades do Distrito Federal e 35 produtos foram organizadas no trabalho acadêmico da disciplina Introdução à Inteligência Artificial (UnB, 2025/1).

As coordenadas são pontos centrais aproximados usados no experimento. Elas não representam necessariamente sede, unidade de atendimento ou endereço oficial de cada organização.

## Dados simulados

- A oferta de produtos por associação é gerada por `generate_association_products`.
- A semente padrão é `42`, garantindo a mesma saída em cada execução.
- Cada associação recebe de 5 a 10 produtos e todos os 35 produtos aparecem ao menos uma vez.
- As avaliações em `reviews.csv` são exemplos fictícios para exercitar o módulo colaborativo.

Esses registros não devem ser interpretados como catálogo, disponibilidade, avaliação ou vínculo institucional real.

## Sazonalidade

O arquivo `products.csv` reproduz o mapeamento didático do notebook entre produto e estação:

1. primavera
2. verão
3. outono
4. inverno

O mapeamento é simplificado e não substitui uma fonte agronômica.
