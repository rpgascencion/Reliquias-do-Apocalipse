# -*- coding: utf-8 -*-
"""Conteúdo do livro As Relíquias do Apocalipse para os compêndios do módulo.
Tudo aqui é dado: o build_packs.py transforma em documentos do Foundry."""

MOD = "reliquias-do-apocalipse"

# ---------------------------------------------------------------- armas
# (nome, dano, pente, alcance, preco, espacos, empunhadura, descricao, extras)
ARMAS = [
    dict(nome="Pistola Arcana", dano="1d8", pente=6, alcance=("short", 0), area="", preco=250, espacos=1,
         empunhadura="leve", desc="Arma leve e prática, ideal para combates rápidos a curta distância. Possui 6 balas em seu carregador."),
    dict(nome="Escopeta Mística", dano="2d6", pente=3, alcance=("short", 0), area="Cone de 6m", preco=550, espacos=1,
         empunhadura="duas", desc="Devastadora em proximidade, dispara energia mágica concentrada; seu disparo atinge uma área cônica de 6m. Empunhada com duas mãos. Possui 3 balas em seu carregador."),
    dict(nome="Rifle Arcano", dano="1d12", pente=4, alcance=("m", 40), area="", preco=1000, espacos=2,
         empunhadura="duas", desc="Uma arma de duas mãos e precisa; necessita de +2 em Força para ser utilizada. <strong>Ignora metade da RD do alvo</strong> (aplique na mesa). Possui 4 balas em seu carregador."),
    dict(nome="Carabina de Rajada", dano="1d8", pente=9, alcance=("medium", 0), area="", preco=650, espacos=1,
         empunhadura="duas", desc="Uma arma de duas mãos que dispara em sucessão rápida, sacrificando precisão pela pressão ofensiva. Pode gastar <strong>+1 PM</strong> para efetuar um disparo em rajada de 3 tiros; cada disparo além do primeiro recebe –1 na Pontaria, sucessivamente. Possui 9 balas em seu carregador."),
    dict(nome="Arcanoblaster", dano="2d8", pente=3, alcance=("medium", 0), area="", preco=1250, espacos=2,
         empunhadura="duas", desc="Uma arma de duas mãos que dispara descargas mágicas devastadoras. Pode gastar <strong>+2 PM</strong> para um disparo concentrado, causando 1 dado de dano a mais e ignorando a RD do alvo nesse ataque. Possui 3 balas em seu carregador."),
]
REGRA_PENTE = "<p><strong>Recarga:</strong> ação de movimento + 1 PM (+1 PM a cada 3 níveis de aprimoramento). Proficiência: poder de combate Treinamento em Armas de Fogo Mágicas.</p>"

# ---------------------------------------------------------------- armaduras e escudos
# (nome, tipo T20, defesa, rd, penalidade, deslocamento, preco, espacos)
ARMADURAS = [
    ("Armadura Simples", "leve", 2, 1, 0, "9m", 20, 1),
    ("Armadura Média", "leve", 4, 3, -3, "9m", 40, 2),
    ("Armadura Completa", "pesada", 7, 5, -5, "-3m", 250, 5),
    ("Escudo Leve", "escudo", 1, 0, -1, "-", 5, 1),
    ("Escudo Pesado", "escudo", 2, 0, -2, "-", 15, 2),
]

# ---------------------------------------------------------------- forja
CUSTO_FORJA = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 400000]

# materiais: chave -> nome, lore, efeitos por categoria (texto do livro)
MATERIAIS = [
    ("aco-lunar", "Aço-Lunar", "Metal forjado sob a luz plena das luas gêmeas de Gudar, conduz magia com pureza quase divina.",
     "+1 de dano mágico (+1 adicional a cada 3 níveis); em +10, ignora resistência mágica.",
     "Resistência a um tipo de energia mágica (fogo, frio, elétrico, ácido, luz ou trevas) 5/10/15/20.",
     "Magias de energia pura causam +1 de dano por dado."),
    ("cristal-solar", "Cristal Solar", "Minerado nas dunas de Crystalis, o cristal armazena fragmentos do sol.",
     "Causa +1 de dano por fogo (+1 a cada 3 níveis).",
     "Resistência a frio 5/10/15/20.",
     "Magias de fogo causam +1d6 adicional em +7 e +2d6 em +10."),
    ("quitina-de-razza", "Quitina de Razza", "Proveniente de monstros ancestrais, vibra com energia primal.",
     "Ao rolar dano máximo, role novamente 1 dado.",
     "+1 Defesa (+1 a cada 3 níveis) e +2/+3/+4/+5 em Percepção.",
     "Magias com dano máximo repetem 1 dado."),
    ("aco-rubi", "Aço-Rubi", "Metal vítreo forjado em chamas dracônicas.",
     "Ignora 2/4/6/8 de RD.",
     "Chance de ignorar dano crítico 10%/25%/40%/50%.",
     "Magias ignoram RD e resistência equivalente a 5/10/15/20."),
    ("adamante-meteorico", "Adamante Meteórico", "Fragmento de estrelas caídas, pesado e poderoso.",
     "Aumenta o dano em 1 passo (+1 passo a cada 4 níveis).",
     "RD 2/4/6/8.",
     "Rerrola resultados 1 no dano."),
    ("madeira-de-crystalis", "Madeira de Crystalis", "Uma madeira negra e rígida, permeada por magia natural.",
     "Conta como mágica e reduz o custo de habilidades em –1 PM.",
     "Resistência à magia +2/+3/+4/+5.",
     "Resistência à magia +2/+3/+4/+5."),
    ("ferro-vivo", "Ferro Vivo", "Metal que pulsa como carne e se regenera em batalha.",
     "+1 de dano físico (+1 a cada 3 níveis). Em +10, recupera 1 PV por ataque bem-sucedido.",
     "Regenera 1 PV por rodada (+1 adicional a cada 3 níveis).",
     "Ao lançar magia de toque, recupera 1d4 PV."),
    ("sangrambaro", "Sangrâmbaro", "Madeira carmesim que se alimenta da vida e do sangue derramado.",
     "+1d4 de dano de sangramento (+1d4 a cada 3 níveis).",
     "Resistência a corte 5/10/15/20.",
     "Magias de necromancia ou sangue restauram 1d6 PV ao conjurador em +10."),
    ("aco-vulcanico", "Aço-Vulcânico", "Metal temperado em lava viva, usado por ferreiros de Talavaar.",
     "+1 de dano de fogo (+1 a cada 3 níveis); em +10, aplica queimadura.",
     "Resistência a fogo 5/10/15/20.",
     "Magias de fogo têm +1 CD e +1 dado de dano em +10."),
    ("ferro-etereo", "Ferro Etéreo", "Um minério instável entre o mundo físico e o espiritual.",
     "Ignora 10%/25%/50%/75% de cobertura e camuflagem.",
     "Concede visão no escuro e resistência espiritual 5/10/15/20.",
     "Magias aumentam o alcance em +5m a cada 3 níveis."),
    ("pedra-da-aurora", "Pedra da Aurora", "Cristal que reflete o amanhecer e canaliza energia cósmica.",
     "+1 no ataque (+1 a cada 3 níveis); em +10, causa cegueira (CD 15).",
     "+1 Defesa (+1 a cada 3 níveis) e resistência a luz 5/10/15/20.",
     "Magias de luz ou cura restauram +1d6 PV em +7 e +2d6 em +10."),
    ("coracao-de-leviata", "Coração de Leviatã", "Essência abissal condensada do sangue de criaturas marinhas antigas.",
     "+1d6 de dano de água (+1d6 a cada 3 níveis).",
     "Resistência a frio e eletricidade 5/10/15/20.",
     "Magias de água ou gelo restauram 1 PM por rodada quando causam dano."),
    ("prisma-onirico", "Prisma Onírico", "Fragmento cristalino nascido dos sonhos de Munir.",
     "Dano psíquico +1/+2/+3/+4; em +10, confunde o alvo (Vontade CD 15).",
     "Imunidade parcial a medo e ilusão (1/2/3/4 usos por descanso).",
     "Magias de ilusão e mente ganham +1 CD e +1d6 de dano mental em +10."),
    ("aco-draconico", "Aço-Dracônico", "Forjado com escamas dos Reis Dragões.",
     "+1 de dano físico (+1 a cada 3 níveis); em +10, ignora RD mágica.",
     "+1 Defesa (+1 a cada 3 níveis) e resistência elemental 5/10/15/20.",
     "Magias causam +1 de dano por dado e ignoram resistência elemental."),
    ("luz-estelar", "Luz Estelar", "Metal celestial vindo de meteoros sagrados.",
     "Dano radiante +1/+2/+3/+4; em +10, cega mortos-vivos por 1 rodada.",
     "RD contra trevas 5/10/15/20 e luz constante de 3m.",
     "Magias de luz ganham +2 CD e dissipam trevas mágicas."),
]

PERICIAS = ['Acrobacia (Des)', 'Adestramento (Pre)', 'Atletismo (For)', 'Atuação (Pre)', 'Cavalgar (Des)',
            'Conhecimento (Int)', 'Cura (Sab)', 'Diplomacia (Pre)', 'Enganação (Pre)', 'Fortitude (Vig)',
            'Furtividade (Des)', 'Guerra (Int)', 'Iniciativa (Des)', 'Intimidação (Pre)', 'Intuição (Sab)',
            'Investigação (Int)', 'Jogatina (Pre)', 'Ladinagem (Des)', 'Luta (For)', 'Misticismo (Int)',
            'Nobreza (Int)', 'Ofício (Int)', 'Percepção (Sab)', 'Pilotagem (Des)', 'Pontaria (Des)',
            'Reflexos (Des)', 'Religião (Sab)', 'Sobrevivência (Sab)', 'Vontade (Sab)']
