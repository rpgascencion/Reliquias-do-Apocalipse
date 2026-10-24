/**
 * A Forja de Gudar: aprimoramento +1 a +10 de armas e armaduras, modificações (1 a cada 2 níveis),
 * material especial (só no nível 0) e slot de Runa.
 * O bloco "Forja" fica na aba Melhorias da ficha do item. Os bônus viram efeitos do próprio item,
 * no mesmo formato das melhorias do sistema, e são recalculados a cada mudança.
 */
import { MOD, cfg, elemento } from "./config.mjs";

const CUSTO = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 400000];
const f3 = (n) => Math.floor(n / 3), f4 = (n) => Math.floor(n / 4), f5 = (n) => Math.floor(n / 5);
const faixa = (n) => (n >= 10 ? 3 : n >= 7 ? 2 : n >= 4 ? 1 : 0);
const DEF = "system.attributes.defesa.bonus", PDA = "system.attributes.defesa.pda";
const RD = (t) => `system.tracos.resistencias.${t}.bonus`;

/* ---------------- dados ---------------- */
/** Modificações. cat: arma | fogo (só armas de fogo) | armadura. fx(n, item) devolve {arma:[...], armadura:[...]} de mudanças. */
export const MODS = {
	cruel: { cat: "arma", nome: "Cruel", txt: "+1 em dano (+1 a cada 5 níveis).", fx: (n) => ({ arma: [["dano", 1 + f5(n)]] }) },
	certeira: { cat: "arma", nome: "Certeira", txt: "+1 em ataque (+1 a cada 5 níveis).", fx: (n) => ({ arma: [["ataque", 1 + f5(n)]] }) },
	precisa: { cat: "arma", nome: "Precisa", max: 2, txt: "+1 na margem de ameaça (máx. 2 vezes).", fx: () => ({ arma: [["criticoM", -1]] }) },
	injecao: { cat: "arma", nome: "Injeção Alquímica", txt: "Libera efeitos de frascos alquímicos ao impacto (à mão)." },
	mira: { cat: "fogo", nome: "Mira Acoplada", max: 1, txt: "Recebe a capacidade de Mirar: não sofre penalidade ao atirar com aliado adjacente ao alvo (à mão)." },
	empunhadura: { cat: "fogo", nome: "Empunhadura", max: 1, txt: "+1 em Pontaria segurando com duas mãos (automático em armas de duas mãos).",
		fx: (n, item) => (item.system.empunhadura === "duas" ? { arma: [["ataque", 1]] } : {}) },
	coronha: { cat: "fogo", nome: "Coronha", max: 1, txt: "Mirar se torna uma ação livre (à mão)." },
	infusao: { cat: "fogo", nome: "Infusão Elemental", max: 1, txt: "Os disparos passam a causar o tipo de dano escolhido (fogo, frio, elétrico, ácido, luz ou trevas). Troque o tipo na rolagem de dano da arma." },
	pente: { cat: "fogo", nome: "Pente Estendido", max: 1, txt: "Capacidade do pente +2." },
	mirando: { cat: "fogo", nome: "+1 em Pontaria Mirando", txt: "+1 em Pontaria enquanto estiver Mirando (+1 a cada 5 níveis da arma; à mão)." },
	danofogo: { cat: "fogo", nome: "+1 no Dano", txt: "+1 no dano (+1 a cada 5 níveis da arma).", fx: (n) => ({ arma: [["dano", 1 + f5(n)]] }) },
	resistente: { cat: "armadura", nome: "Resistente", txt: "+1 na Defesa e +1 na penalidade (+1 a cada 5 níveis).", fx: (n) => ({ armadura: [[DEF, 1 + f5(n)], [PDA, 1 + f5(n)]] }) },
	leve: { cat: "armadura", nome: "Leve", txt: "-1 na penalidade (+1 a cada 5 níveis).", fx: (n) => ({ armadura: [[PDA, -(1 + f5(n))]] }) },
	fortificada: { cat: "armadura", nome: "Fortificada", txt: "+1 em testes de resistência.", fx: () => ({ armadura: [["system.modificadores.pericias.resistencia", 1]] }) },
	blindada: { cat: "armadura", nome: "Blindada", txt: "+1 de RD (+1 a cada 5 níveis).", fx: (n) => ({ armadura: [[RD("dano"), 1 + f5(n)]] }) },
	elemental: { cat: "armadura", nome: "Resistência Elemental", txt: "+2 de resistência contra fogo, frio, ácido e trevas.",
		fx: () => ({ armadura: ["fogo", "frio", "acido", "trevas"].map((t) => [RD(t), 2]) }) }
};

const T4 = (v) => (n) => v[faixa(n)];
/** Materiais: efeitos automáticos por categoria; o texto completo fica no item do compêndio. */
export const MATERIAIS = {
	"aco-lunar": { nome: "Aço-Lunar", arma: (n) => [["dano", 1 + f3(n)]], manual: "Em +10 a arma ignora resistência mágica. Armadura: escolha a energia (resistência 5/10/15/20) e aplique à mão. Esotérico: +1 de dano por dado em magias de energia pura." },
	"cristal-solar": { nome: "Cristal Solar", arma: (n) => [["dano", 1 + f3(n)]], armadura: (n) => [[RD("frio"), T4([5, 10, 15, 20])(n)]], manual: "Esotérico: magias de fogo +1d6 em +7 e +2d6 em +10." },
	"quitina-de-razza": { nome: "Quitina de Razza", armadura: (n) => [[DEF, 1 + f3(n)], ["system.pericias.perc.bonus", T4([2, 3, 4, 5])(n)]], manual: "Arma: ao rolar dano máximo, role novamente 1 dado. Esotérico: magias com dano máximo repetem 1 dado." },
	"aco-rubi": { nome: "Aço-Rubi", arma: (n) => [["ignoraRD", T4([2, 4, 6, 8])(n)]], esoterico: (n) => [["ignoraRD", T4([5, 10, 15, 20])(n)]], manual: "Armadura: chance de ignorar dano crítico 10%/25%/40%/50%." },
	"adamante-meteorico": { nome: "Adamante Meteórico", arma: (n) => [["passos", 1 + f4(n), 0]], armadura: (n) => [[RD("dano"), T4([2, 4, 6, 8])(n)]], manual: "Esotérico: rerrola resultados 1 no dano." },
	"madeira-de-crystalis": { nome: "Madeira de Crystalis", custoArma: -1, manual: "Conta como mágica. Armadura/Esotérico: resistência à magia +2/+3/+4/+5." },
	"ferro-vivo": { nome: "Ferro Vivo", arma: (n) => [["dano", 1 + f3(n)]], manual: "Em +10 a arma recupera 1 PV por ataque bem-sucedido. Armadura: regenera 1 PV por rodada (+1 a cada 3 níveis). Esotérico: magia de toque recupera 1d4 PV." },
	"sangrambaro": { nome: "Sangrâmbaro", arma: (n) => [["dano", `${1 + f3(n)}d4`]], armadura: (n) => [[RD("corte"), T4([5, 10, 15, 20])(n)]], manual: "Esotérico: magias de necromancia ou sangue restauram 1d6 PV ao conjurador em +10." },
	"aco-vulcanico": { nome: "Aço-Vulcânico", arma: (n) => [["dano", 1 + f3(n)]], armadura: (n) => [[RD("fogo"), T4([5, 10, 15, 20])(n)]], manual: "Em +10 a arma aplica queimadura. Esotérico: magias de fogo +1 CD e +1 dado de dano em +10." },
	"ferro-etereo": { nome: "Ferro Etéreo", manual: "Arma: ignora 10%/25%/50%/75% de cobertura e camuflagem. Armadura: visão no escuro e resistência espiritual 5/10/15/20. Esotérico: +5m de alcance a cada 3 níveis." },
	"pedra-da-aurora": { nome: "Pedra da Aurora", arma: (n) => [["ataque", 1 + f3(n)]], armadura: (n) => [[DEF, 1 + f3(n)], [RD("luz"), T4([5, 10, 15, 20])(n)]], manual: "Em +10 a arma causa cegueira (CD 15). Esotérico: magias de luz ou cura +1d6 PV em +7 e +2d6 em +10." },
	"coracao-de-leviata": { nome: "Coração de Leviatã", arma: (n) => [["dano", `${1 + f3(n)}d6`]], armadura: (n) => [[RD("frio"), T4([5, 10, 15, 20])(n)], [RD("eletricidade"), T4([5, 10, 15, 20])(n)]], manual: "Esotérico: magias de água ou gelo restauram 1 PM por rodada quando causam dano." },
	"prisma-onirico": { nome: "Prisma Onírico", arma: (n) => [["dano", T4([1, 2, 3, 4])(n)]], manual: "Dano psíquico; em +10 confunde o alvo (Vontade CD 15). Armadura: imunidade parcial a medo e ilusão (1/2/3/4 usos por descanso). Esotérico: ilusão e mente +1 CD e +1d6 em +10." },
	"aco-draconico": { nome: "Aço-Dracônico", arma: (n) => [["dano", 1 + f3(n)]], armadura: (n) => [[DEF, 1 + f3(n)], ...["fogo", "frio", "eletricidade", "acido"].map((t) => [RD(t), T4([5, 10, 15, 20])(n)])], manual: "Em +10 a arma ignora RD mágica. Esotérico: +1 de dano por dado e ignora resistência elemental." },
	"luz-estelar": { nome: "Luz Estelar", arma: (n) => [["dano", T4([1, 2, 3, 4])(n)]], armadura: (n) => [[RD("trevas"), T4([5, 10, 15, 20])(n)]], manual: "Dano radiante; em +10 cega mortos-vivos por 1 rodada. Armadura: luz constante de 3m. Esotérico: magias de luz +2 CD e dissipam trevas mágicas." }
};

/* ---------------- estado ---------------- */
export function categoria(item) {
	if (item.type === "arma") return "arma";
	if (item.type === "equipamento") {
		if (["leve", "pesada", "escudo"].includes(item.system.tipo)) return "armadura";
		if (item.system.tipo === "esoterico") return "esoterico";
	}
	return null;
}
const ehFogo = (item) => item.type === "arma" && (item.system.proficiencia === "fogo" || item.getFlag(MOD, "armaFogoArcana"));
function estado(item) {
	const f = item.getFlag(MOD, "forja") ?? {};
	return { nivel: Number(f.nivel) || 0, material: f.material || "", mods: Array.isArray(f.mods) ? [...f.mods] : [], runa: f.runa ?? null, reforcos: Number(f.reforcos) || 0 };
}
const slotsTotais = (e) => Math.floor(e.nivel / 2);
const slotsLivres = (e) => slotsTotais(e) - e.mods.length - e.reforcos;

/* ---------------- efeitos ---------------- */
const TIPO = { 0: "custom", 2: "add", 5: "override" };
const mudanca = ([key, value, mode = 2]) => ({ key, value: String(value), mode, type: TIPO[mode] ?? "add", priority: null });

function montarEfeitos(item, e) {
	const cat = categoria(item);
	const n = e.nivel;
	const efeitos = [];
	const base = (nome, changes, { onuse, transfer, spell, custo } = {}) => ({
		name: nome, img: item.img, type: "base", description: "", disabled: false, transfer: !!transfer, origin: item.uuid,
		changes: changes.map(mudanca),
		system: { onuse: !!onuse, abilityUse: { automatic: !!onuse, types: onuse ? [spell ? "spell" : "self"] : [], names: [], aumenta: false, custo: custo ?? null, description: "" } },
		flags: { [MOD]: { forja: true }, tormenta20: { onuse: !!onuse, durationScene: false, self: !!onuse && !spell, ...(spell ? { spell: true } : {}), ...(custo ? { custo: String(custo) } : {}) } }
	});
	if (cat === "arma") {
		const ch = [];
		if (f3(n)) ch.push(["passos", f3(n), 0]);
		for (const k of e.mods) { const fx = MODS[k]?.fx?.(n, item); if (fx?.arma) ch.push(...fx.arma); }
		const m = MATERIAIS[e.material];
		if (m?.arma) ch.push(...m.arma(n));
		if (ch.length) efeitos.push(base(`Forja +${n}${m ? ` · ${m.nome}` : ""}`, ch, { onuse: true }));
		if (m?.custoArma) efeitos.push(base(`${m.nome}: −1 PM nas habilidades da arma`, [], { onuse: true, custo: m.custoArma }));
	} else if (cat === "armadura") {
		const ch = [];
		if (f3(n)) ch.push([DEF, 2 * f3(n)]);
		for (const k of e.mods) { const fx = MODS[k]?.fx?.(n, item); if (fx?.armadura) ch.push(...fx.armadura); }
		const m = MATERIAIS[e.material];
		if (m?.armadura) ch.push(...m.armadura(n));
		if (ch.length) efeitos.push(base(`Forja +${n}${m ? ` · ${m.nome}` : ""}`, ch, { transfer: true }));
	} else if (cat === "esoterico") {
		const m = MATERIAIS[e.material];
		if (m?.esoterico) efeitos.push(base(`${m.nome} (esotérico)`, m.esoterico(n), { onuse: true, transfer: true, spell: true }));
	}
	return efeitos;
}

async function aplicar(item, e) {
	await item.setFlag(MOD, "forja", e);
	const velhos = item.effects.filter((ef) => ef.getFlag(MOD, "forja")).map((ef) => ef.id);
	if (velhos.length) await item.deleteEmbeddedDocuments("ActiveEffect", velhos);
	const novos = montarEfeitos(item, e);
	if (novos.length) await item.createEmbeddedDocuments("ActiveEffect", novos);
	// o sistema só recalcula os rótulos do item (ataque, dano) quando o personagem é preparado de novo
	item.actor?.reset();
	item.sheet?.rendered && item.sheet.render(false);
	item.actor?.sheet?.rendered && item.actor.sheet.render(false);
}

/* ---------------- custos ---------------- */
function acharMaterial(actor, item, nivel) {
	const tipo = categoria(item) === "arma" ? "arma" : "armadura";
	const nome = tipo === "arma" ? `Pedra da Forja +${nivel}` : `Ladrilho da Proteção +${nivel}`;
	return actor?.items.find((i) => {
		const f = i.getFlag(MOD, "forja");
		return (f && Number(f.nivel) === nivel && f.tipo === tipo) || i.name === nome;
	}) ?? null;
}

async function cobrar(actor, coisas) {
	const { pedra, midares, material } = coisas;
	if (pedra) {
		const q = Number(pedra.system.qtd ?? 1);
		if (q > 1) await pedra.update({ "system.qtd": q - 1 }); else await pedra.delete();
	}
	if (material) {
		const q = Number(material.system.qtd ?? 1);
		if (q > 1) await material.update({ "system.qtd": q - 1 }); else await material.delete();
	}
	if (midares) await actor.update({ "system.dinheiro.tp": Number(actor.system.dinheiro?.tp ?? 0) - midares });
}

/* ---------------- ações ---------------- */
const DialogV2 = () => foundry.applications.api.DialogV2;
const confirmar = (titulo, conteudo) => DialogV2().confirm({ window: { title: titulo }, content: conteudo, classes: ["reliquias", "rel-dialogo"], rejectClose: false });

async function aprimorar(item) {
	const e = estado(item);
	if (e.nivel >= 10 && !game.user.isGM) return ui.notifications.warn("O limite é +10. Refinadores lendários podem ultrapassá-lo, a critério do Mestre.");
	const prox = e.nivel + 1;
	const midares = CUSTO[Math.min(prox, 10) - 1];
	const actor = item.actor;
	const cobra = cfg("forjaConsome", true) && actor;
	const pedra = cobra ? acharMaterial(actor, item, prox) : null;
	const dinheiro = Number(actor?.system.dinheiro?.tp ?? 0);
	const nomeMat = categoria(item) === "arma" ? `Pedra da Forja +${prox}` : `Ladrilho da Proteção +${prox}`;
	const falta = cobra && (!pedra || dinheiro < midares);
	let linhas = `<p>Levar <b>${item.name}</b> ao nível <b>+${prox}</b>.</p>`;
	if (cobra) linhas += `<ul><li>${nomeMat}: ${pedra ? "✔ no inventário" : "<b>✘ não encontrado</b>"}</li><li>${midares.toLocaleString("pt-BR")} Midares: ${dinheiro >= midares ? "✔" : `<b>✘ só tem ${dinheiro.toLocaleString("pt-BR")}</b>`}</li></ul>`;
	else linhas += `<p>Custo do livro: ${nomeMat} + ${midares.toLocaleString("pt-BR")} Midares (cobrança desligada).</p>`;
	if (falta && !game.user.isGM) return ui.notifications.warn(`Falta material ou dinheiro para forjar ${item.name} +${prox}.`);
	if (falta) linhas += `<p><i>Como Mestre, você pode forjar mesmo assim (nada é cobrado).</i></p>`;
	if (!(await confirmar("A Forja de Gudar", linhas))) return;
	if (cobra && !falta) await cobrar(actor, { pedra, midares });
	e.nivel = prox;
	await aplicar(item, e);
	ChatMessage.create({ speaker: ChatMessage.getSpeaker({ actor }), content: `<div class="rel-chat-forja"><b>A Forja de Gudar</b><br>${item.name} foi aprimorada para <b>+${prox}</b>.${prox % 3 === 0 ? (categoria(item) === "arma" ? " O dano sobe um passo." : " +2 de Defesa.") : ""}${prox % 2 === 0 ? " Uma nova modificação está disponível." : ""}</div>` });
}

async function rebaixar(item) {
	const e = estado(item);
	if (e.nivel <= 0) return;
	if (!(await confirmar("A Forja de Gudar", `<p>Baixar ${item.name} para +${e.nivel - 1}? Nada é devolvido. Modificações que não couberem mais serão removidas.</p>`))) return;
	e.nivel -= 1;
	while (slotsLivres(e) < 0) { if (e.reforcos) e.reforcos--; else e.mods.pop(); }
	await aplicar(item, e);
}

async function escolherModificacao(item) {
	const e = estado(item);
	if (slotsLivres(e) <= 0) return ui.notifications.warn("Não há espaço para modificação: uma a cada 2 níveis.");
	const cat = categoria(item);
	const disponiveis = Object.entries(MODS).filter(([k, m]) => {
		if (m.cat === "fogo" && !ehFogo(item)) return false;
		if (m.cat !== "fogo" && m.cat !== cat) return false;
		const vezes = e.mods.filter((x) => x === k).length;
		return !m.max || vezes < m.max;
	});
	const opcoes = disponiveis.map(([k, m]) => `<option value="${k}">${m.nome} — ${m.txt}</option>`).join("");
	const runaOpt = cat === "arma" && e.runa ? `<option value="__reforco">Reforçar a Runa (${e.runa.nome})</option>` : "";
	const k = await DialogV2().prompt({
		window: { title: "Nova modificação" }, classes: ["reliquias", "rel-dialogo"],
		content: `<div class="form-group"><select name="mod" style="width:100%">${runaOpt}${opcoes}</select></div>`,
		ok: { label: "Adicionar", callback: (ev, btn) => btn.form.elements.mod.value }, rejectClose: false
	});
	if (!k) return;
	if (k === "__reforco") e.reforcos += 1; else e.mods.push(k);
	await aplicar(item, e);
}

async function removerModificacao(item, idx) {
	const e = estado(item);
	if (idx === "reforco") e.reforcos = Math.max(0, e.reforcos - 1); else e.mods.splice(Number(idx), 1);
	await aplicar(item, e);
}

async function escolherMaterial(item) {
	const e = estado(item);
	if (e.material) return;
	if (e.nivel > 0 && !game.user.isGM) return ui.notifications.warn("Materiais ancestrais só podem ser aplicados em itens de nível 0.");
	const actor = item.actor;
	const opcoes = Object.entries(MATERIAIS).map(([k, m]) => {
		const tem = actor?.items.find((i) => i.getFlag(MOD, "material") === k || i.name === m.nome);
		return `<option value="${k}">${m.nome}${actor ? (tem ? " (no inventário)" : "") : ""}</option>`;
	}).join("");
	const k = await DialogV2().prompt({
		window: { title: "Material especial" }, classes: ["reliquias", "rel-dialogo"],
		content: `<p>O material só pode ser aplicado uma vez e fica para sempre no item.</p><div class="form-group"><select name="mat" style="width:100%">${opcoes}</select></div>`,
		ok: { label: "Aplicar", callback: (ev, btn) => btn.form.elements.mat.value }, rejectClose: false
	});
	if (!k) return;
	const mat = actor?.items.find((i) => i.getFlag(MOD, "material") === k || i.name === MATERIAIS[k].nome);
	if (cfg("forjaConsome", true) && actor && !mat && !game.user.isGM) return ui.notifications.warn(`${MATERIAIS[k].nome} não está no inventário.`);
	if (cfg("forjaConsome", true) && mat) await cobrar(actor, { material: mat });
	e.material = k;
	await aplicar(item, e);
}

async function removerMaterial(item) {
	if (!game.user.isGM) return;
	const e = estado(item);
	if (!(await confirmar("Material especial", "<p>Remover o material deste item? (só o Mestre pode)</p>"))) return;
	e.material = "";
	await aplicar(item, e);
}

/* ---------------- bloco na ficha ---------------- */
function injetar(app, html) {
	const item = app.item ?? app.document;
	if (!item) return;
	const cat = categoria(item);
	if (!cat) return;
	const raiz = elemento(html);
	const aba = raiz?.querySelector('.tab.enhancements[data-tab="enhancements"]');
	if (!aba || aba.querySelector(".rel-forja")) return;
	const e = estado(item);
	const ed = app.isEditable;
	const m = MATERIAIS[e.material];
	const fogo = ehFogo(item);
	const linhasMods = e.mods.map((k, i) => `<li><b>${MODS[k]?.nome ?? k}</b> <span class="notes">${MODS[k]?.txt ?? ""}</span>${ed ? ` <a class="rel-del-mod" data-idx="${i}" data-tooltip="Remover"><i class="fa-solid fa-trash"></i></a>` : ""}</li>`).join("")
		+ (e.reforcos ? `<li><b>Runa reforçada ×${e.reforcos}</b>${ed ? ` <a class="rel-del-mod" data-idx="reforco"><i class="fa-solid fa-trash"></i></a>` : ""}</li>` : "");
	const proxCusto = e.nivel < 10 ? `${cat === "arma" ? "Pedra da Forja" : "Ladrilho da Proteção"} +${e.nivel + 1} + ${CUSTO[e.nivel].toLocaleString("pt-BR")} M$` : "nível máximo";
	const automatico = cat === "arma"
		? [f3(e.nivel) ? `+${f3(e.nivel)} passo(s) de dano` : "", fogo ? `Recarga: ação de movimento + ${1 + f3(e.nivel)} PM` : ""].filter(Boolean).join(" · ")
		: cat === "armadura" ? (f3(e.nivel) ? `+${2 * f3(e.nivel)} de Defesa` : "") : "";
	const bloco = document.createElement("fieldset");
	bloco.className = "rel-forja rel-bloco";
	bloco.innerHTML = `
		<legend>A Forja de Gudar</legend>
		${cat !== "esoterico" ? `
		<div class="rel-forja-nivel flexrow">
			<span class="rel-forja-num">+${e.nivel}</span>
			<div class="rel-forja-info"><div>Próximo: ${proxCusto}</div><div class="notes">${automatico || "A cada 3 níveis: armas sobem um passo de dano; armaduras +2 de Defesa."}</div></div>
			${ed ? `<button type="button" class="rel-aprimorar" ${e.nivel >= 10 && !game.user.isGM ? "disabled" : ""}><i class="fa-solid fa-hammer"></i> Aprimorar</button>
			${game.user.isGM && e.nivel > 0 ? `<button type="button" class="rel-rebaixar" data-tooltip="Baixar um nível (Mestre)"><i class="fa-solid fa-arrow-down"></i></button>` : ""}` : ""}
		</div>
		<h4>Modificações <span class="notes">(${e.mods.length + e.reforcos}/${slotsTotais(e)} — uma a cada 2 níveis)</span></h4>
		<ul class="rel-forja-mods">${linhasMods || `<li class="notes">Nenhuma.</li>`}</ul>
		${ed && slotsLivres(e) > 0 ? `<button type="button" class="rel-add-mod"><i class="fa-solid fa-plus"></i> Adicionar modificação</button>` : ""}` : ""}
		<h4>Material especial</h4>
		${m ? `<p><b>${m.nome}</b>${game.user.isGM && ed ? ` <a class="rel-del-mat" data-tooltip="Remover (Mestre)"><i class="fa-solid fa-trash"></i></a>` : ""}<br><span class="notes">À mão: ${m.manual}</span></p>`
			: `<p class="notes">Nenhum. Só pode ser aplicado com o item em nível 0.</p>${ed && (e.nivel === 0 || game.user.isGM) ? `<button type="button" class="rel-add-mat"><i class="fa-solid fa-gem"></i> Aplicar material</button>` : ""}`}
		${cat === "arma" && e.nivel >= 1 ? `
		<h4>Runa</h4>
		<div class="rel-runa" data-tooltip="Arraste uma runa (item) para cá">${e.runa ? `<img src="${e.runa.img}" width="28" height="28"> <a class="rel-abrir-runa">${e.runa.nome}</a>${ed ? ` <a class="rel-del-runa"><i class="fa-solid fa-trash"></i></a>` : ""}` : `<span class="notes">Slot de Runa vazio — arraste uma runa para cá.</span>`}</div>` : ""}`;
	aba.prepend(bloco);
	const on = (sel, fn) => bloco.querySelectorAll(sel).forEach((el) => el.addEventListener("click", (ev) => { ev.preventDefault(); ev.stopPropagation(); fn(ev.currentTarget); }));
	on(".rel-abrir-runa", () => fromUuid(e.runa?.uuid).then((d) => d?.sheet?.render(true)));
	if (!ed) return;
	on(".rel-aprimorar", () => aprimorar(item));
	on(".rel-rebaixar", () => rebaixar(item));
	on(".rel-add-mod", () => escolherModificacao(item));
	on(".rel-del-mod", (el) => removerModificacao(item, el.dataset.idx));
	on(".rel-add-mat", () => escolherMaterial(item));
	on(".rel-del-mat", () => removerMaterial(item));
	on(".rel-del-runa", async () => { const s = estado(item); s.runa = null; s.reforcos = 0; await aplicar(item, s); });
	const runa = bloco.querySelector(".rel-runa");
	runa?.addEventListener("dragover", (ev) => ev.preventDefault());
	runa?.addEventListener("drop", async (ev) => {
		ev.preventDefault(); ev.stopPropagation();
		let dados; try { dados = JSON.parse(ev.dataTransfer.getData("text/plain")); } catch { return; }
		if (dados?.type !== "Item") return;
		const doc = await fromUuid(dados.uuid);
		if (!doc || doc.id === item.id) return;
		const s = estado(item);
		s.runa = { nome: doc.name, uuid: doc.uuid, img: doc.img };
		await aplicar(item, s);
	});
}

export function iniciarForja() {
	Hooks.on("renderItemSheet", injetar);
}
