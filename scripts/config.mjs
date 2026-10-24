export const MOD = "reliquias-do-apocalipse";

/** Lê uma configuração sem quebrar se ela ainda não existir. */
export function cfg(chave, padrao) {
	try {
		return game.settings.get(MOD, chave);
	} catch {
		return padrao;
	}
}

/** Elemento DOM a partir do que o hook de renderização entregar (jQuery ou HTMLElement). */
export function elemento(html) {
	if (!html) return null;
	if (html instanceof HTMLElement) return html;
	return html[0] ?? null;
}

export const ATRIBUTOS_MENTAIS = { int: "Intelecto", sab: "Sabedoria", car: "Presença" };

export function registrarConfiguracoes() {
	const reg = (chave, dados) => game.settings.register(MOD, chave, { config: true, ...dados });

	reg("tema", {
		name: "Tema escuro do Relíquias",
		hint: "Cores escuras e a fonte do livro nas janelas, fichas, diários, chat e na barra lateral (inclusive no módulo T20 Sidebar). Vale só para você.",
		scope: "client", type: String, default: "escuro",
		choices: { escuro: "Ligado", desligado: "Desligado" },
		onChange: () => document.documentElement.dataset.reliquiasTema = cfg("tema", "escuro")
	});
	reg("fonteTitulos", {
		name: "Fonte do livro nos títulos",
		hint: "Usa a fonte Relíquias do Apocalipse nos títulos de janelas, fichas, diários e cartões do chat. O texto corrido continua numa fonte legível.",
		scope: "client", type: Boolean, default: true,
		onChange: (v) => document.documentElement.dataset.reliquiasFonte = v ? "sim" : "nao"
	});
	reg("nomesLivro", {
		name: "Nomes do livro para atributos e moeda",
		hint: "Constituição vira Vigor, Inteligência vira Intelecto, Carisma vira Presença e T$ vira M$ (Midares). Só muda os nomes na tela. Recarregue a página após mudar.",
		scope: "world", type: Boolean, default: true, requiresReload: true
	});
	reg("energiaDivina", {
		name: "Energia Divina e Sanidade na ficha",
		hint: "Mostra ED e Sanidade ao lado de PV e PM, com o máximo calculado pelas regras do livro.",
		scope: "world", type: Boolean, default: true, requiresReload: true
	});
	reg("criticoLivro", {
		name: "Crítico do livro (20 natural + d100)",
		hint: "No 20 natural de um ataque com arma, rola o d100 de confirmação no chat (25 ou menos confirma) e oferece o dano multiplicado pelo atributo de ataque.",
		scope: "world", type: Boolean, default: true
	});
	reg("pontosAtributos", {
		name: "Pontos para distribuir nos atributos",
		hint: "Regra do livro: todos começam com 1 em cada atributo e têm 6 pontos para distribuir.",
		scope: "world", type: Number, default: 6
	});
	reg("maxAtributoInicial", {
		name: "Valor máximo de um atributo na criação",
		scope: "world", type: Number, default: 3
	});
	reg("esconderMelhoriasT20", {
		name: "Esconder melhorias, materiais e encantos do T20",
		hint: "Nos itens, a aba Melhorias vira Forja: só aparecem a Forja de Gudar e os materiais do livro. Itens que já têm melhorias do T20 mantêm os efeitos.",
		scope: "world", type: Boolean, default: true
	});
	reg("forjaConsome", {
		name: "Forja: consumir pedras/ladrilhos e Midares",
		hint: "Ao aprimorar, procura a Pedra da Forja ou o Ladrilho da Proteção do nível no inventário e desconta os Midares. O Mestre sempre pode forjar sem cobrar.",
		scope: "world", type: Boolean, default: true
	});
}
