/**
 * Tema escuro + fonte do livro, e os nomes do livro para atributos e moeda.
 * O tema é só CSS (styles/reliquias.css), ligado pelos atributos data-reliquias-* no <html>.
 * Com o módulo T20 Sidebar ativo, o tema troca as variáveis dele para a paleta do Relíquias.
 */
import { MOD, cfg } from "./config.mjs";

const NOMES = {
	AbilityCon: "Vigor", AbilityConAbbr: "Vig",
	AbilityInt: "Intelecto",
	AbilityCha: "Presença", AbilityChaAbbr: "Pre",
	CurrencySilver: "Midares", CurrencySilverAbbr: "M$"
};

/** O sistema pode já ter traduzido as listas do CONFIG: troca ali também (chaves "T20.*" ficam como estão). */
function corrigirConfig() {
	const T = CONFIG.T20;
	if (!T) return;
	const troca = (lista, k, v) => { if (T[lista] && typeof T[lista][k] === "string" && !T[lista][k].startsWith("T20.")) T[lista][k] = v; };
	troca("atributos", "con", "Vigor"); troca("atributos", "int", "Intelecto"); troca("atributos", "car", "Presença");
	troca("atributosAbr", "con", "Vig"); troca("atributosAbr", "car", "Pre");
}

export function iniciarTema() {
	const raiz = document.documentElement;
	raiz.dataset.reliquiasTema = cfg("tema", "escuro");
	raiz.dataset.reliquiasFonte = cfg("fonteTitulos", true) ? "sim" : "nao";

	Hooks.once("i18nInit", () => {
		if (!cfg("nomesLivro", true)) return;
		const t = game.i18n.translations?.T20;
		if (t) for (const [k, v] of Object.entries(NOMES)) if (k in t) t[k] = v;
		corrigirConfig();
	});
	Hooks.once("setup", () => { if (cfg("nomesLivro", true)) corrigirConfig(); });
	Hooks.once("ready", ligarEsquemaEscuro);
	Hooks.on("renderSettingsConfig", (app, html) => {
		// destaca as opções do módulo com a fonte do livro (só visual)
		const el = html instanceof HTMLElement ? html : html?.[0];
		el?.querySelector(`[data-category="${MOD}"], [data-tab="${MOD}"]`)?.classList.add("rel-config");
	});
}

/** Na primeira vez, liga o esquema de cores escuro do próprio Foundry (v13) para este jogador. Depois ele escolhe livremente. */
async function ligarEsquemaEscuro() {
	if (cfg("tema", "escuro") !== "escuro") return;
	const chave = `${MOD}.esquemaEscuroAplicado`;
	try {
		if (localStorage.getItem(chave)) return;
		const ui = foundry.utils.deepClone(game.settings.get("core", "uiConfig"));
		if (!ui?.colorScheme) return;
		localStorage.setItem(chave, "1");
		if (ui.colorScheme.applications === "dark" && ui.colorScheme.interface === "dark") return;
		ui.colorScheme.applications = "dark";
		ui.colorScheme.interface = "dark";
		await game.settings.set("core", "uiConfig", ui);
	} catch (e) {
		console.debug(`${MOD} | esquema escuro do Foundry não aplicado`, e);
	}
}
