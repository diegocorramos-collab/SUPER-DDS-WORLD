# SUPER DDS WORLD v1.1 - Ranking Global

Pacote para GitHub Pages com ranking global baseado em `ranking.json`, GitHub Issues e GitHub Actions.

## Como funciona

1. O jogo lê `ranking.json` no mesmo site.
2. Ao clicar em **ENVIAR MEU RESULTADO**, o jogo abre uma nova Issue já preenchida.
3. O jogador precisa estar autenticado no GitHub e clicar em **Submit new issue**.
4. O workflow valida os campos, mantém o melhor resultado por nome e atualiza `ranking.json`.
5. A Issue recebe um retorno automático e é fechada.

## Configuração obrigatória no index.html

Localize `GLOBAL_RANKING_CONFIG` e altere:

```javascript
const GLOBAL_RANKING_CONFIG={
 owner:'SEU-USUARIO',
 repo:'SUPER-DDS-WORLD',
 branch:'main',
 rankingFile:'ranking.json',
 enabled:true
};
```

Substitua `SEU-USUARIO` pelo usuário ou organização do GitHub. Se o repositório tiver outro nome, altere `repo`.

## Publicação

1. Crie um repositório público.
2. Envie todo o conteúdo deste pacote para a branch `main`.
3. Em **Settings > Actions > General > Workflow permissions**, permita leitura e gravação.
4. Em **Settings > Pages**, publique a branch `main` pela pasta raiz.
5. Abra o jogo pela URL do GitHub Pages.

## Segurança e limitações

- Nenhum token é colocado no HTML.
- O usuário precisa de uma conta GitHub para registrar uma pontuação.
- Como o jogo roda no navegador, os valores ainda podem ser manipulados por um usuário técnico. Os limites do workflow reduzem dados inválidos, mas não provam que a partida foi legítima.
- O ranking mantém até 100 registros e exibe os 100 primeiros; a interface destaca os três primeiros e o jogador atual.
- Em caso de empate em pontuação, vence o menor tempo; depois, o maior número de moedas.

## Arquivos

- `index.html`: jogo com leitura e envio do ranking.
- `ranking.json`: base pública do ranking.
- `scripts/process_score.py`: validação, deduplicação e ordenação.
- `.github/workflows/ranking.yml`: automação.
