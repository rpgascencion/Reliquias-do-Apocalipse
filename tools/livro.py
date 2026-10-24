# -*- coding: utf-8 -*-
"""Texto do livro As Relíquias do Apocalipse RPG (v2.4) em HTML, por capítulo e página de diário.
{{item:Nome}} vira um link @UUID para o item do compêndio; {{img:arquivo}} vira o caminho da imagem do módulo."""
from conteudo import ARMAS, ARMADURAS, CUSTO_FORJA, MATERIAIS, PERICIAS

def ul(*itens): return "<ul>" + "".join(f"<li>{i}</li>" for i in itens) + "</ul>"
def ol(*itens): return "<ol>" + "".join(f"<li>{i}</li>" for i in itens) + "</ol>"
def tabela(cab, linhas, cls="rel-tabela"):
    h = "".join(f"<th>{c}</th>" for c in cab)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>'
def M(n): return f"{n:,}".replace(",", ".")

ALC = {"short": "Curto", "medium": "Médio", "long": "Longo"}

CAPITULOS = []

# ------------------------------------------------------------------ capa
CAPITULOS.append(("As Relíquias do Apocalipse", [
    ("Capa", '<p style="text-align:center"><img src="{{img:capa-livro.webp}}" width="420"></p>'
             '<h2 style="text-align:center">Livro Básico de Regras</h2><p style="text-align:center">Criador: Gustavo (Joker)</p>'),
    ("Como usar este módulo", "<p>Este diário traz o livro inteiro. Os itens citados ficam nos compêndios da pasta <strong>Relíquias do Apocalipse</strong> e os nomes em destaque abrem o item.</p>"
     + ul("<strong>Energia Divina e Sanidade</strong>: aparecem no bloco <em>Relíquias</em> da ficha do personagem, com o máximo calculado automaticamente.",
          "<strong>Técnicas Divinas</strong>: são poderes do tipo <em>Distinção</em>. Na ficha do poder, o bloco <em>Técnica Divina</em> define o nível (0 a 5) e se é passiva; o custo em ED é cobrado ao usar.",
          "<strong>Distribuição de pontos</strong>: botão <em>Distribuir atributos</em> no bloco Relíquias da ficha.",
          "<strong>A Forja</strong>: na ficha de armas e armaduras, o bloco <em>Forja</em> sobe o nível do item (+1 a +10), aplica os bônus e as modificações.",
          "<strong>Crítico</strong>: no 20 natural o módulo rola o d100 de confirmação no chat (pode ser desligado nas configurações).")),
]))

# ------------------------------------------------------------------ criação de personagem
BENCAO = (
    "<p>Desde o selamento de Sakir, os deuses não podem mais agir diretamente em Midgard. Porém, os deuses selados deixaram fragmentos de suas almas com os mortais. "
    "Quando despertos em um escolhido — chamado de <strong>Arauto</strong> —, esses fragmentos manifestam-se como uma <strong>Bênção</strong>.</p>"
    "<p>Em termos de regras, uma Bênção funciona como uma <strong>Distinção</strong>, representando o vínculo eterno do personagem com o domínio de sua divindade patrona, mas com regras próprias de progressão adicional.</p>"
    "<h2>Características da Bênção</h2>"
    "<p>Todo personagem possui uma única Bênção ligada a ele, escolhida na criação de personagem (ou despertada em campanha, a critério do Mestre) e que <strong>não pode ser mudada</strong>.</p>"
    "<h3>1. Atributo-Chave da Bênção (Somente Atributos Mentais)</h3>"
    "<p>A conexão com o fragmento de um deus selado é um exercício de compreensão cósmica, devoção espiritual ou imposição de vontade. Por isso, <strong>somente atributos mentais — Intelecto, Sabedoria ou Presença — podem ser usados como Atributo-Chave</strong> de uma Bênção e de suas Técnicas Divinas.</p>"
    + ul("O Atributo-Chave é definido pelo domínio do deus que abençoa o Arauto (ou escolhido pelo jogador entre os três atributos mentais ao despertar a Bênção, de acordo com o conceito da sua fé).",
         "Esse atributo é utilizado para calcular sua reserva inicial de <strong>Energia Divina (ED)</strong> no 1º nível e a <strong>CD (Classe de Dificuldade)</strong> para resistir às suas Técnicas Divinas:")
    + '<p class="rel-formula"><strong>CD = 10 + ½ do Nível do Personagem + Atributo Mental da Técnica</strong><br><small>(metade do nível arredondada para baixo)</small></p>'
    "<h3>2. Marca da Bênção (1ª Passiva)</h3>"
    "<p>Assim como a <strong>Marca da Distinção</strong>, ao despertar sua Bênção no 1º nível, o Arauto recebe sua <strong>Marca da Bênção</strong>.</p>"
    + ul("Ela é uma habilidade <strong>passiva</strong> inicial e gratuita que representa o sinal divino na alma e no corpo do Arauto.",
         "<strong>Atenção:</strong> a Marca da Bênção <strong>conta como 1 das suas 3 habilidades passivas máximas</strong> permitidas pela Bênção.")
    + "<h3>3. Progressão de Poderes de Bênção (Técnicas Divinas)</h3>"
    "<p>A Bênção concede poderes <strong>adicionais</strong> à progressão normal da classe do personagem:</p>"
    + ul("<strong>Ganho Extra:</strong> no <strong>1º nível</strong> (além da Marca da Bênção) e a cada <strong>nível ímpar</strong> subsequente (3º, 5º, 7º, 9º etc.), o personagem desbloqueia gratuitamente uma nova <strong>Técnica Divina (Poder de Bênção)</strong>, elaborada em conjunto com o Mestre.",
         "<strong>Acúmulo Livre:</strong> as Técnicas Divinas e a Marca da Bênção <strong>não contam</strong> para o limite máximo de poderes de classe ou poderes gerais do personagem.",
         "<strong>Escalamento como Distinção:</strong> Técnicas Divinas podem possuir efeitos que melhoram conforme a quantidade total de Poderes daquela Bênção que o Arauto possui.")
    + "<h3>4. Limite de Habilidades Passivas (Máximo 3)</h3>"
    "<p>Para manter o equilíbrio e evitar o acúmulo excessivo de bônus permanentes, um Arauto pode possuir no máximo <strong>3 Habilidades Passivas</strong> vindas de sua Bênção ao longo de toda a sua progressão:</p>"
    + ol("<strong>Passiva I (Marca da Bênção):</strong> recebida automaticamente no 1º nível.",
         "<strong>Passiva II e Passiva III:</strong> podem ser escolhidas/criadas no lugar de uma Técnica Divina ativa em qualquer nível ímpar.")
    + "<p>Uma vez atingido o limite de <strong>3 passivas</strong>, todas as demais Técnicas Divinas adquiridas nos níveis ímpares seguintes devem obrigatoriamente ser <strong>habilidades ativas</strong>.</p>"
)
ED = (
    "<p>A <strong>Energia Divina (ED)</strong> é o recurso sagrado usado para ativar as Técnicas Divinas concedidas pelos deuses, separado dos Pontos de Mana (PM). Sua progressão é intencionalmente <strong>lenta e escassa</strong>, forçando o Arauto a ponderar o momento exato de manifestar seus milagres em combate.</p>"
    "<h3>Cálculo de Energia Divina (Progressão Reduzida)</h3>"
    "<p>Como o custo das técnicas é direto (1 para 1), a reserva de ED cresce de forma contida:</p>"
    + ul("<strong>No 1º Nível:</strong> você começa com <strong>ED = 1 + ½ do Atributo-Chave Mental</strong> (arredondado para baixo, mínimo de 1 ED inicial; o atributo é somado apenas no 1º nível).",
         "<strong>A cada nível subsequente (2º ao 20º):</strong> você recebe <strong>+1 ED por nível</strong>.",
         "<strong>Bônus de Classe/Mana:</strong> sempre que subir de nível, se a sua classe conceder <strong>4 ou mais Pontos de Mana (PM)</strong> básicos por nível, você recebe <strong>+1 ED adicional</strong> apenas nos <strong>níveis ímpares</strong> (3º, 5º, 7º etc.), refletindo sua maior afinidade espiritual.")
    + '<blockquote><p><strong>Exemplos de Progressão</strong></p>'
    + ul("<strong>Guerreiro da Fé (3 PM/nível, Sabedoria +2):</strong> começa no 1º nível com <strong>2 ED</strong> (1 + 1). Ganha +1 ED por nível, chegando ao 5º nível com <strong>6 ED</strong> e ao 10º nível com <strong>11 ED</strong>.",
         "<strong>Clérigo/Sábio Divino (5 PM/nível, Sabedoria +4):</strong> começa no 1º nível com <strong>3 ED</strong> (1 + 2). Ganha +1 ED nos níveis pares e +2 ED nos níveis ímpares, chegando ao 5º nível com <strong>9 ED</strong> e ao 10º nível com <strong>16 ED</strong>.")
    + "</blockquote>"
    "<h3>Custo 1 para 1 (Regra de Custo Direto)</h3>"
    "<p>As Técnicas Divinas são classificadas em níveis de <strong>0 a 5</strong>. O custo de ativação (ou de retenção, no caso de passivas) é de exatamente <strong>1 ED para cada nível da técnica</strong>:</p>"
    + tabela(["Nível da Técnica", "Custo de Ativação (Ativas)", "Redução no Máximo de ED (Passivas*)", "Acesso por Nível de Personagem"],
             [["Nível 0", "0 ED", "0 ED", "1º Nível"], ["Nível 1", "1 ED", "-1 ED Máximo", "1º Nível"], ["Nível 2", "2 ED", "-2 ED Máximo", "5º Nível"],
              ["Nível 3", "3 ED", "-3 ED Máximo", "9º Nível"], ["Nível 4", "4 ED", "-4 ED Máximo", "13º Nível"], ["Nível 5", "5 ED", "-5 ED Máximo", "17º Nível"]])
    + "<p><em>*Nota sobre Passivas: a <strong>Marca da Bênção</strong> é gratuita e não reduz seu ED máximo. A 2ª e a 3ª passivas reservam parte do seu ED máximo na proporção de <strong>1 para 1</strong> (1 ED por nível da passiva).</em></p>"
    + ul("<strong>Sustentação:</strong> técnicas sustentadas custam <strong>1 ED por rodada</strong> para serem mantidas ativas.")
)
TECNICAS = (
    "<p>As técnicas concedidas pelas bênçãos seguem a estrutura do Capítulo 9 – Criação de Técnicas do sistema Feiticeiros &amp; Maldições 2.0, adaptadas para refletir os domínios e a essência de cada deus.</p>"
    + ul("<strong>Efeitos:</strong> devem sempre remeter ao domínio do deus patrono.",
         "<strong>Balanceamento:</strong> segue a mesma lógica do Feiticeiros &amp; Maldições, mas integrado à progressão de Energia Divina descrita neste livro.")
    + "<p>Essas técnicas serão desenvolvidas em conjunto com os jogadores, com o Mestre supervisionando para manter equilíbrio e fidelidade ao tema da campanha.</p>"
    "<p>Modelos prontos ficam no compêndio <strong>Bênçãos e Técnicas</strong>: arraste para a ficha e ajuste o texto.</p>"
)
CAPITULOS.append(("Criação de Personagem", [
    ("Status", "<p>Nós usaremos um sistema de pontos parecido com o que a maioria dos RPGs usa, mas não teremos os números inteiros e sim apenas os modificadores. Os status presentes neste RPG são Força, Destreza, Vigor, Intelecto, Sabedoria e Presença.</p>"
               "<p>A distribuição de pontos será um pouco diferente da maioria dos RPGs: todos os jogadores começam com <strong>1 ponto em cada status</strong> e terão <strong>6 pontos para distribuir</strong> como quiser, porém um mesmo status inicialmente só poderá ser elevado a um <strong>máximo de 3</strong>. O nível mínimo de um mesmo status é <strong>-3</strong>, ou seja, pontos poderão ser retirados, diminuindo um status abaixo de 1.</p>"
               "<p><strong>OBS:</strong> ao retirar um ponto de um status que esteja em 1, o mesmo desce para -1 e não para 0.</p>"),
    ("Classe e Nível", "<p>Utilizaremos como base as classes do Tormenta20. Ao subir de nível, assim como no T20, pegamos um poder de classe — poderes esses que podem ser trocados por poderes do próprio T20 ou talentos de outros RPGs, que serão adaptados com o mestre. Nos níveis ímpares, o personagem desbloqueia um poder concedido da bênção, que será formulado junto do mestre.</p>"),
    ("Bênçãos e Energia Divina", BENCAO),
    ("Energia Divina (ED) e Custo de Técnicas", ED),
    ("Criação de Técnicas", TECNICAS),
]))

# ------------------------------------------------------------------ mecânicas
lin = [PERICIAS[i:i + 3] for i in range(0, len(PERICIAS), 3)]
lin[-1] += [""] * (3 - len(lin[-1]))
CAPITULOS.append(("Mecânicas de Jogo", [
    ("Base", "<p>Utilizaremos como base o sistema do Tormenta20 com algumas modificações e adaptações. Todas as mudanças e novas mecânicas estarão descritas neste documento.</p>"),
    ("Perícias", "<p>As perícias dentro de um RPG servem para definir o quão bom um personagem é executando certas ações, ou seja, para definir o sucesso de um personagem para, por exemplo, escalar uma parede. Toda perícia é determinada por um número, no qual faremos uma simples soma: caso você não seja treinado na perícia, a soma será metade do nível de personagem + atributo correspondente para tal perícia; caso seja treinado, você somará +2 nessa perícia, aumentando em +4 a partir do nível 7 e +6 a partir do nível 15. Cada classe possui algumas perícias que podem ser escolhidas; você também pode escolher um número de perícias igual ao seu Intelecto. As perícias presentes neste RPG são as mesmas do Tormenta20:</p>"
                 + tabela(["", "", ""], lin, "rel-tabela rel-pericias")),
    ("Atordoamento", "<p>Um ataque, um choque elétrico, uma queda ou outro dano podem incidentalmente atordoar um jogador por <strong>1d3 + 2 rodadas</strong> de combate. Atordoado, o jogador pode Bloquear ou Esquivar, mas não pode fazer mais nada. O mestre indica quando ocorre o atordoamento, talvez como resultado de um golpe especial ou acerto crítico. Ser atordoado pode ou não incluir a perda de pontos de vida.</p>"),
    ("Choque e Perda de Consciência", "<p>Se em um único ataque o jogador perder metade ou mais que seu total atual de pontos de vida, ele deve rolar um <strong>1d100</strong> e tirar um valor menor ou igual a <strong>Vig ×5</strong>; caso contrário, ficará inconsciente.</p>"
                                      "<p>Quando o jogador atingir 1 ponto de vida, ele ficará automaticamente inconsciente e não participará ativamente do jogo. Mesmo ainda estando vivo, o jogador só acordará quando seus pontos de vida chegarem a pelo menos 2.</p>"),
    ("Sanidade", "<p>A sanidade é o nível mental do jogador, o quanto ele aguenta presenciar situações traumatizantes. Quando esses pontos chegam ao fim, seu personagem fica louco e terá que ser acalmado por outro jogador com um teste de Diplomacia. O teste de sanidade é um teste de Vontade; caso enlouqueça e ninguém te salve, o personagem vira um PDM.</p>"
                 "<p>Para calcular quantos pontos de sanidade seu personagem possui:</p>"
                 + ul("<strong>Nível 1:</strong> 10 + Sabedoria", "<strong>A cada nível:</strong> 4 + Sabedoria")),
]))

# ------------------------------------------------------------------ combate
CAPITULOS.append(("Combate", [
    ("Ações", "<p>As ações são o que compõem um combate dentro de um RPG, e aqui temos estes tipos de ações: <strong>padrão, de movimento, livre, completa e bônus</strong>. Todo jogador tem direito a uma ação de movimento, uma ação padrão e uma ação bônus por turno. Cada ação tem sua utilidade durante um combate ou cena.</p>"
              + ul("<strong>Movimento:</strong> como o próprio nome já diz, são utilizadas para locomoção e, em alguns casos, podem ser usadas para conjurar magias, utilizar algumas perícias mais básicas, sacar sua arma, itens etc.",
                   "<strong>Padrão:</strong> utilizada para realizar ações mais complexas como atacar, utilizar perícias complexas etc. Pode também ser transformada em uma ação de movimento, fazendo com que se tenha 2 ações de movimento em uma rodada.",
                   "<strong>Completa:</strong> é a junção da ação de movimento com a padrão; normalmente é utilizada para ações muito complexas, como utilizar uma habilidade, uma magia mais poderosa, realizar um movimento muito difícil, entre outros.",
                   "<strong>Livre:</strong> pode ser usada a qualquer momento; normalmente a utilizamos para falar, mas, utilizando os equipamentos certos ou até mesmo fazendo seu devido treinamento, podemos utilizá-la para sacar a arma, pegar itens e, em casos mais raros, utilizar magias.",
                   "<strong>Bônus:</strong> pode ser utilizada uma vez por rodada, porém apenas algumas habilidades podem ser utilizadas nesta ação.")),
    ("Ataque e Defesa", "<p>Durante um combate, as mecânicas mais básicas são o ataque e a defesa. Um ataque deve ser feito durante uma ação padrão e, para determinar se tal ataque foi um sucesso, você deve rolar <strong>1d20 + Luta</strong> (perícia). O resultado dessa rolagem deve ser maior ou igual à armadura (Defesa) do alvo.</p>"
                        "<p>Se você for o alvo, pode utilizar uma <strong>reação</strong> — cada jogador possui uma reação por turno. As reações são:</p>"
                        + ul("<strong>Esquiva:</strong> somamos a perícia Reflexos na Defesa.", "<strong>Bloqueio:</strong> usamos a Fortitude como RD.",
                             "<strong>Contra-ataque:</strong> não somamos nem usamos nada; apenas esperamos que o atacante erre o ataque e, se isso acontecer, realizamos um golpe contra ele.")
                        + "<p>Você não pode usar a esquiva e o contra-ataque juntos.</p>"),
    ("Dano Crítico", "<p>O dano crítico será um pouco diferente, pois ele será realmente um divisor de águas durante uma batalha. Para que um acerto seja crítico, você precisa primeiramente que o dado de ataque seja um <strong>20 natural</strong> e, logo após, rolar um <strong>d100</strong>: se o resultado do d100 for igual ou menor que <strong>25</strong>, o acerto será crítico. O 20 natural apenas garante o acerto.</p>"
                     "<p>Assim que o ataque for determinado como crítico, você multiplicará o dano da arma pelo seu <strong>status respectivo de ataque</strong>.</p>"),
]))

# ------------------------------------------------------------------ equipamentos
armas_tab = tabela(["Arma", "Dano", "Pente", "Alcance", "Custo", "Espaços"],
                   [["{{item:%s}}" % a["nome"], a["dano"].upper(), f'{a["pente"]} Tiros',
                     ("Cone 6m" if a["area"] else (f'{a["alcance"][1]}m' if a["alcance"][0] == "m" else ALC[a["alcance"][0]])),
                     f'{M(a["preco"])} M$', str(a["espacos"])] for a in ARMAS])
arm_tab = tabela(["Armadura/Escudo", "Bônus de Defesa", "Redução de Dano", "Penalidade", "Deslocamento", "Custo", "Peso"],
                 [["{{item:%s}}" % n, f"+{d}", str(rd) if rd else "-", str(p) if p else "-", desl, f"{M(pr)} M$", str(e)] for n, t, d, rd, p, desl, pr, e in ARMADURAS])
CAPITULOS.append(("Equipamentos", [
    ("Inventário", "<p>Antes de falarmos sobre os equipamentos, temos que falar sobre onde vamos guardá-los: todo personagem consegue carregar até <strong>10× a sua Força</strong>. Cada personagem também possui alguns slots para equipar itens mágicos, assim como em MMORPGs. Esses itens se dividem em 3 categorias — <strong>Colar, Brinco e Anel</strong>: todos os personagens possuem 1 slot para colar, 1 par de brincos (que podem ser mesclados) e 2 slots de anel.</p>"),
    ("Sistema Monetário", "<p>Nesta parte iremos seguir um sistema muito conhecido em jogos: iremos conseguir dinheiro com base nos inimigos que derrotamos, e aqui esse dinheiro é chamado de <strong>Midar (M$)</strong>. Midares também vão ser concedidos aos personagens ao término de missões.</p>"
                          "<p><em>No Foundry, 1 Midar equivale a 1 T$ da ficha.</em></p>"),
    ("Armas", "<p>As armas são divididas em 4 categorias — simples, marciais, exóticas e balísticas —, o que as classifica pela facilidade de uso, e temos as divisões por propósito: de ataque corpo a corpo e a distância.</p>"
              + ul("<strong>Armas Simples:</strong> são armas fáceis de manejar; todos os personagens sabem usar essas armas.",
                   "<strong>Armas Marciais:</strong> são armas usadas especificamente por combatentes treinados.",
                   "<strong>Armas Exóticas:</strong> são armas complexas e difíceis de dominar, que exigem um treinamento muito específico.",
                   "<strong>Armas Balísticas:</strong> são armas à base de pólvora e/ou magia; são difíceis de manejar e não muito fabricadas.")
              + "<p>Dentro dessas classificações temos outras, descritas no livro do Tormenta20.</p>"
                "<h3>Passos de Dano</h3><p>1 – 1d2 – 1d3 – 1d4 – 1d6 – 1d8 – 1d10 – 1d12 + x</p><p>x = 1d4, 1d6, 1d8, 1d10, 1d12</p>"
                "<p>Dessa forma, quando o dano alcança 1d12, seu passo seguinte se torna a adição de 1d4, virando 1d12 + 1d4, e a progressão passa a valer para esse novo dado. Ao se tornar 1d12, repete-se a lógica adicionando +1d4. Para dados múltiplos segue-se a mesma lógica.</p>"
                "<p><strong>Ex.:</strong> 6d6, 6d8, 6d10, 6d12, 6d12 + 1d4, 6d12 + 1d6.</p><p>Dessa forma, a progressão segue uma escala controlável e viável matematicamente.</p>"),
    ("Novas Armas", "<h3>Armas de Fogo Arcanas</h3>"
                    "<p>As armas de fogo em Gudar são, na verdade, arcanas e alimentadas por magia. Cada arma possui uma quantia de balas em seu carregador, necessitando uma <strong>ação de movimento e 1 PM</strong> para recarregar; a cada 3 níveis de aprimoramento da arma, esse custo aumenta em +1.</p>"
                    "<p><strong>Treinamento em Armas de Fogo Mágicas</strong> – Poder de combate: você recebe proficiência em todas as armas de fogo arcanas.</p>"
                    + armas_tab
                    + "<h3>Características das Armas</h3>"
                    + "".join(f"<p><strong>{a['nome']}:</strong> {a['desc']}</p>" for a in ARMAS)),
    ("Armaduras e Escudos", "<p>Teremos 3 tipos de armaduras — simples, média e completa — e 2 tipos de escudo — leve e pesado.</p>" + arm_tab),
]))

# ------------------------------------------------------------------ a forja
custo_armas = ul(*[f"<strong>+{i + 1}:</strong> {{{{item:Pedra da Forja +{i + 1}}}}} + {M(c)} Midares" for i, c in enumerate(CUSTO_FORJA)])
custo_arm = ul(*[f"<strong>+{i + 1}:</strong> {{{{item:Ladrilho da Proteção +{i + 1}}}}} + {M(c)} Midares" for i, c in enumerate(CUSTO_FORJA)])
materiais_html = "".join(f"<h3>{{{{item:{n}}}}}</h3><p><em>{lore}</em></p>" + ul(f"<strong>Arma:</strong> {a}", f"<strong>Armadura:</strong> {ar}", f"<strong>Esotérico:</strong> {e}")
                         for k, n, lore, a, ar, e in MATERIAIS)
CAPITULOS.append(("A Forja", [
    ("Introdução", "<p>Desde os primórdios de Gudar, o fogo da criação molda não apenas mundos, mas também lâminas e escudos. As forjas são vistas como templos, e seus mestres, como sacerdotes que invocam o poder do metal e da chama. Não há arma que não carregue a alma de quem a empunha, nem armadura que não traga consigo as marcas do destino de seu dono.</p>"
                   "<p>Neste sistema, inspirado nas lendas de forjas cósmicas, cada guerreiro pode elevar suas armas e armaduras através do uso de pedras e ladrilhos especiais. O ato de forjar não é apenas trabalho de martelo e bigorna, mas um ritual que une sangue, suor e poder arcano.</p>"),
    ("Funcionamento", ul("Armas e armaduras podem ser aprimoradas até o nível <strong>+10</strong>.",
                         "Para cada aprimoramento, são necessários materiais especiais (Pedras da Forja ou Ladrilhos da Proteção) e a moeda de Gudar, os Midares.",
                         "O processo de aprimoramento deve ser realizado por um ferreiro ou artesão habilidoso, muitas vezes visto como mediador entre o mortal e a essência das chamas divinas.",
                         "A cada novo nível, o item não apenas se torna mais forte, mas também ganha ressonância com o espírito de seu portador, tornando-se uma extensão da própria alma.",
                         "<strong>A cada 3 níveis:</strong> armas sobem um passo de dano; armaduras recebem +2 de Defesa.",
                         "Cada arma/armadura pode ter <strong>1 modificação a cada 2 níveis</strong> e, no nível 0, pode escolher um material especial.")),
    ("Aprimoramentos", "<h3>Armas</h3><p><strong>Custo:</strong></p>" + custo_armas
                       + "<p><strong>Modificações:</strong></p>"
                       + ul("<strong>Cruel:</strong> +1 em dano (a cada 5 níveis aumenta +1).", "<strong>Certeira:</strong> +1 em ataque (a cada 5 níveis aumenta +1).",
                            "<strong>Precisa:</strong> +1 na margem de ameaça (máx. 2 vezes).", "<strong>Injeção Alquímica:</strong> libera efeitos de frascos alquímicos ao impacto.",
                            "<strong>Material Ancestral:</strong> feita de matéria rara.")
                       + "<h3>Armaduras</h3><p><strong>Custo:</strong></p>" + custo_arm
                       + "<p><strong>Modificações:</strong></p>"
                       + ul("<strong>Resistente:</strong> +1 na Defesa e +1 na penalidade (a cada 5 níveis aumenta +1).", "<strong>Leve:</strong> -1 na penalidade (a cada 5 níveis aumenta +1).",
                            "<strong>Fortificada:</strong> +1 em testes de resistência.", "<strong>Blindada:</strong> +1 de RD (a cada 5 níveis aumenta +1).",
                            "<strong>Resistência Elemental:</strong> +2 contra fogo, gelo, ácido, trevas etc.")),
    ("Armas de Fogo Arcanas", "<p>Aprimoramentos possíveis:</p>"
                              + ul("<strong>Mira Acoplada:</strong> recebe a capacidade de Mirar (só pode ser pego uma vez).",
                                   "<strong>Empunhadura:</strong> aumenta +1 em Pontaria se estiver segurando a arma com duas mãos (só pode ser pego uma vez).",
                                   "<strong>Coronha:</strong> Mirar se torna uma ação livre (só pode ser pego uma vez).",
                                   "<strong>Infusão Elemental:</strong> escolha 1 tipo de dano — fogo, frio, elétrico, ácido, luz ou trevas —; os disparos da arma passam a causar o tipo de dano escolhido em vez de balístico.",
                                   "<strong>Pente Estendido:</strong> aumenta a capacidade da arma em +2 (só pode ser pego uma vez).",
                                   "+1 em Pontaria enquanto estiver Mirando (a cada 5 níveis de arma aumenta 1).",
                                   "+1 no dano (a cada 5 níveis de arma aumenta 1).")
                              + "<p><strong>OBS — Mirar:</strong> não recebe penalidade ao atirar quando um aliado está adjacente ao seu alvo.</p>"),
    ("Runas", "<p>Cada arma aprimorada possui <strong>1 slot de Runa</strong>, um espaço místico capaz de abrigar um símbolo arcano que modifica seu poder. Runas podem ser encontradas em templos antigos, tumbas de heróis e como recompensas divinas.</p>"
              + ul("Uma arma pode receber apenas <strong>uma Runa por vez</strong>.",
                   "A cada 2 níveis de aprimoramento, o portador pode optar por <strong>reforçar sua Runa</strong> em vez de escolher um novo aprimoramento comum.",
                   "Runas funcionam como vínculos espirituais, e substituí-las exige um ritual especial em uma forja sagrada.")),
    ("Materiais Especiais", "<p>Além das Pedras da Forja e Ladrilhos da Proteção, existem materiais raros que podem ser usados para modificar armas e armaduras. Esses materiais são tesouros de Gudar, encontrados apenas em locais específicos ou obtidos em grandes jornadas. Cada um concede propriedades únicas ao equipamento que for trabalhado com ele.</p>"
                            "<p><strong>Importante:</strong> Materiais Ancestrais só podem ser aplicados uma única vez em cada item e apenas quando ele ainda está em nível 0. Após receber um material ancestral, o item carrega essa essência para sempre.</p>"
                            "<h3>Materiais e Refinamento</h3>"
                            + ul("Cada material especial confere um efeito único em armas, armaduras ou itens esotéricos.",
                                 "Os efeitos escalam com o nível do item, conforme o aprimoramento (+1/+4/+7/+10).",
                                 "Um item só pode ser forjado com um material especial.",
                                 "Refinadores lendários podem ultrapassar o limite de +10, a critério do Mestre.")
                            + "<p><strong>Escalonamento padrão dos efeitos:</strong></p>"
                            + ul("<strong>+1:</strong> efeito menor", "<strong>+4:</strong> efeito aprimorado", "<strong>+7:</strong> efeito superior", "<strong>+10:</strong> efeito lendário")
                            + materiais_html),
]))

# ------------------------------------------------------------------ mundo
CAPITULOS.append(("Criação do Mundo e História", [
    ("Prólogo", "<h3>Palavras Iniciais do Mestre</h3><p>Este tomo reúne as lendas, as verdades ocultas e os registros esquecidos do mundo de Gudar e dos Cinco Planos. Aqui estão escritos os ecos do princípio e do fim, as guerras dos deuses e dos mortais, e o legado do Rei de Paus, aquele que ousou selar o Nada.</p>"
                "<p>Que o leitor saiba: cada palavra é tanto revelação quanto véu. O que é mito e o que é verdade pertence ao olhar dos deuses — e ao destino dos heróis.</p>"),
    ("A Cosmologia e os Cinco Planos", "<h3>O Nada e a Criação</h3><p>No princípio, nada havia. O Nada reinava absoluto, estendendo-se em todas as direções, imutável e eterno. Mas então, no coração do vazio, uma fagulha brilhou. O cosmo nasceu. Dele emergiu <strong>Hannamori</strong>, a Deusa da Criação, cujo ser era luz e cujo passo fazia brotar cores onde antes só havia escuridão.</p>"
                                       "<p>Hannamori, em sua solidão, tomou fragmentos de seu núcleo e moldou dois filhos:</p>"
                                       + ul("<strong>Munir</strong>, esculpida na brancura de um buraco branco, feita de ordem e claridade.",
                                            "<strong>Sakir</strong>, gestado nas entranhas de um buraco negro, onde o Nada infiltrou-se em sua essência, contaminando-o.")
                                       + "<h3>Os Planos</h3><p>Para si e para seus filhos, Hannamori teceu os mundos:</p>"
                                       + ul("<strong>Asgard</strong>, o trono dos deuses.", "<strong>Midgard</strong>, o lar dos mortais.", "<strong>Campos Elísios</strong>, onde repousam as almas virtuosas.",
                                            "<strong>Jardim Pútrido</strong>, onde apodrecem as almas condenadas.", "<strong>Nidavellir</strong>, prisão feita do Nada, onde nem o tempo ousa caminhar.")),
    ("O Continente de Gudar", '<p style="text-align:center"><img src="{{img:mapa-gudar.webp}}" width="100%"></p>'
                              "<h3>Reino de Paus</h3><p>O maior e mais próspero dos reinos, marcado pela diversidade. Trolls, homens e fadas caminham lado a lado. Cada distrito possui líderes locais, mas todos servem sob o rei.</p><p><strong>Brasão:</strong> símbolo de Paus e um corvo.</p>"
                              "<h3>Reino de Morke</h3><p>Também chamado de Reino Obscuro. Tido como morto, mas guardado por segredos. Foi palco da maior batalha contra Sakir.</p><p><strong>Brasão:</strong> coração tribal corrompido.</p>"
                              "<h3>Reino de Crystalis</h3><p>Terra dos elfos e fadas, regida pela Rainha Arwen da Casa Crystalis. Magia em excesso transfigura plantas e animais em formas únicas.</p><p><strong>Brasão:</strong> espadas entrelaçadas por raízes.</p>"
                              "<h3>Reino de Talavaar</h3><p>Reino das forjas e das máquinas. Povos pequenos, mas de grande engenho, ergueram cidades nas montanhas e dominaram ciência e alquimia.</p><p><strong>Brasão:</strong> martelo sobre o símbolo de Ouros.</p>"),
    ("Os Contos Mortais", "<p>Nos livros de Midgard conta-se que Munir e Sakir moldaram estrelas e planetas, escreveram as leis da magia e criaram divindades menores. Mas Sakir, corrompido pelo Nada, tornou-se soberbo. Desejou ser mais forte que sua própria mãe.</p>"
                          "<p>Seguiu-se a <strong>Guerra dos Irmãos</strong>, onde deuses e mundos foram despedaçados. Após dois milênios de destruição, Sakir foi vencido e trancado em Nidavellir, enquanto os deuses se fecharam em Asgard, suas vozes distantes, suas bênçãos raras.</p>"
                          "<p>Fragmentos de Sakir e Munir cristalizaram-se em sete artefatos: as <strong>Relíquias do Apocalipse</strong>.</p>"
                          '<p style="text-align:center">?????????</p>'),
]))
