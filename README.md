# As Relíquias do Apocalipse (T20)

Módulo de ambientação para **Foundry VTT v13** com o sistema **Tormenta20**. Ele roda por cima do sistema, sem modificá-lo: as atualizações do T20 continuam funcionando.

## Instalação
No Foundry, **Add-on Modules → Install Module** e cole o manifesto:

```
https://raw.githubusercontent.com/rpgascencion/Reliquias-do-Apocalipse/main/module.json
```

## Compêndios (pasta "Relíquias do Apocalipse")
- **Relíquias: Livro Básico**: o livro inteiro em diários (Criação de Personagem, Mecânicas, Combate, Equipamentos, A Forja, Criação do Mundo e História), com o mapa de Gudar e links para os itens.
- **Relíquias: Armas e Armaduras**: Pistola Arcana, Escopeta Mística, Rifle Arcano, Carabina de Rajada, Arcanoblaster, Armaduras Simples/Média/Completa, Escudos Leve/Pesado.
- **Relíquias: Forja e Materiais**: Pedras da Forja +1 a +10, Ladrilhos da Proteção +1 a +10 e os 15 materiais especiais.
- **Relíquias: Bênçãos e Técnicas**: modelos de Bênção, Marca da Bênção, Técnicas Divinas ativas (nível 0 a 5) e passivas (nível 1 a 5).
- **Relíquias: Itens do Mestre** (só o Mestre vê): relíquias, runas e magias do mundo da campanha.

## Regras automatizadas
- **Energia Divina (ED)** e **Sanidade**: aparecem ao lado de PV e PM. O máximo é calculado: ED = 1 + ½ atributo-chave no 1º nível, +1 por nível, +1 nos níveis ímpares se a classe principal dá 4+ PM por nível, menos as passivas reservadas. Sanidade = 10 + Sab no 1º nível, +4 + Sab por nível. Ficam em `system.resources.ed` e `system.resources.sanidade` (servem para barras de token).
- **Barra Relíquias** na ficha: atributo-chave da Bênção (Int, Sab ou Pre), CD das Técnicas, bônus manual de ED, descanso (recupera ED) e **Distribuir atributos**.
- **Técnicas Divinas**: na ficha de um poder, aba Detalhes, bloco *Técnica Divina*: nível 0 a 5 e tipo (ativa, passiva ou Marca da Bênção). As ativas descontam a ED ao usar; sem ED suficiente o uso é bloqueado. Passivas reservam ED do máximo.
- **Distribuição de pontos do livro**: todos começam com 1, 6 pontos, máximo 3, mínimo -3, e de 1 se desce direto para -1.
- **A Forja de Gudar**: na aba Melhorias de armas, armaduras e escudos. Aprimora de +1 a +10 consumindo a pedra/ladrilho do nível e os Midares, aplica +1 passo de dano (armas) ou +2 de Defesa (armaduras) a cada 3 níveis, libera 1 modificação a cada 2 níveis, aplica o material especial (só no nível 0) com efeitos que escalam em +1/+4/+7/+10 e tem o slot de Runa (arraste o item da runa).
- **Crítico do livro**: no 20 natural de um ataque com arma, o módulo rola o d100 de confirmação (25 ou menos) e oferece o botão de dano da arma multiplicado pelo atributo de ataque.
- **Tema escuro** com a fonte do livro nos títulos; a barra lateral (T20 Sidebar) fica em cinza e roxo com a fonte do livro.
- **Melhorias, materiais e encantos do T20 escondidos** nos itens: a aba vira **Forja** (pode desligar nas configurações). Os nomes do livro (Vigor, Intelecto, Presença, M$) podem ser desligados.

Tudo pode ser ligado ou desligado em **Configurações → Configurar módulos → As Relíquias do Apocalipse**.

## O que continua manual
Efeitos que dependem da cena: Mirar, Coronha, Pente Estendido, Infusão Elemental (troque o tipo de dano na rolagem), Injeção Alquímica, efeitos de +10 dos materiais, resistências escolhidas, chance de ignorar crítico, ataques de rajada e disparo concentrado (PM extra), recarga das armas de fogo.

## Desenvolvimento
Os compêndios são gerados por `python3 tools/build_packs.py` a partir de `tools/conteudo.py` e `tools/livro.py`. Os JSON em `data/` servem de reserva: se um compêndio abrir vazio, o Mestre o preenche automaticamente ao entrar.

Fonte "Relíquias do Apocalipse" do autor; fonte de apoio Trade Winds (SIL Open Font License, ver `fonts/TradeWinds-OFL.txt`).
