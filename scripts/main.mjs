/**
 * As Relíquias do Apocalipse (T20)
 * Módulo de ambientação para o sistema Tormenta20: livro, compêndios, Energia Divina, Sanidade,
 * Técnicas Divinas, distribuição de pontos, Forja de Gudar, crítico do livro e tema escuro.
 */
import { MOD, registrarConfiguracoes } from "./config.mjs";
import { iniciarRecursos } from "./recursos.mjs";
import { iniciarTecnicas } from "./tecnicas.mjs";
import { iniciarForja } from "./forja.mjs";
import { iniciarCritico } from "./critico.mjs";
import { iniciarTema } from "./tema.mjs";
import { abrirDistribuicao } from "./atributos.mjs";

Hooks.once("init", () => {
	registrarConfiguracoes();
	iniciarTema();
	console.log(`${MOD} | iniciado`);
});

Hooks.once("setup", () => {
	if (game.system.id !== "tormenta20") {
		console.warn(`${MOD} | este módulo foi feito para o sistema Tormenta20; nada foi ativado.`);
		return;
	}
	iniciarRecursos();
	iniciarTecnicas();
	iniciarForja();
	iniciarCritico();
});

Hooks.once("ready", async () => {
	const mod = game.modules.get(MOD);
	if (mod) mod.api = { abrirDistribuicao };
	await preencherCompendiosVazios();
});

/**
 * Rede de segurança: se um compêndio do módulo abrir vazio (arquivo de banco não carregou),
 * o Mestre recebe o conteúdo a partir dos JSON em /data. Se já tem conteúdo, nada é feito.
 */
async function preencherCompendiosVazios() {
	if (!game.user.isGM) return;
	const PACKS = { livro: "JournalEntry", equipamentos: "Item", forja: "Item", bencaos: "Item", reliquias: "Item" };
	for (const [nome, tipo] of Object.entries(PACKS)) {
		const pack = game.packs.get(`${MOD}.${nome}`);
		if (!pack || pack.index.size > 0) continue;
		try {
			const dados = await (await fetch(`modules/${MOD}/data/${nome}.json`)).json();
			const docs = dados.items ?? dados.journal ?? [];
			if (!docs.length) continue;
			const travado = pack.locked;
			if (travado) await pack.configure({ locked: false });
			const opts = { pack: pack.collection, keepId: true };
			if (dados.folders?.length) await Folder.createDocuments(dados.folders, opts);
			await getDocumentClass(tipo).createDocuments(docs, opts);
			if (travado) await pack.configure({ locked: true });
			console.log(`${MOD} | compêndio "${nome}" preenchido a partir de /data.`);
		} catch (err) {
			console.error(`${MOD} | falha ao preencher o compêndio "${nome}":`, err);
		}
	}
}
