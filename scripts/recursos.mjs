/**
 * Energia Divina (ED) e Sanidade.
 * Os dois ficam nos recursos do próprio sistema (system.resources.ed / system.resources.sanidade),
 * então funcionam em barras de token, no consumo de itens ("Consumir: Atributo") e na ficha.
 * O máximo é calculado na preparação dos dados (não é gravado), e só o valor atual é salvo.
 */
import { MOD, cfg, elemento, ATRIBUTOS_MENTAIS } from "./config.mjs";
import { abrirDistribuicao } from "./atributos.mjs";

const num = (v, p = 0) => (Number.isFinite(Number(v)) ? Number(v) : p);

/** Atributo-chave da Bênção do ator (int, sab ou car). */
export function atributoBencao(actor) {
	const k = actor.getFlag?.(MOD, "atributoBencao");
	return ATRIBUTOS_MENTAIS[k] ? k : "sab";
}

/** Cálculo do máximo de Energia Divina, com o detalhamento para a dica da ficha. */
export function calcularED(actor) {
	const s = actor.system;
	const nivel = Math.max(1, num(s.attributes?.nivel?.value, 1));
	const atr = atributoBencao(actor);
	const valorAtr = num(s.atributos?.[atr]?.value);
	const inicial = Math.max(1, 1 + Math.floor(valorAtr / 2));
	const porNivel = nivel - 1;
	// classe principal: a de mais níveis; 4+ PM por nível dá +1 ED nos níveis ímpares a partir do 3º
	const classes = actor.items.filter((i) => i.type === "classe");
	const principal = classes.sort((a, b) => num(b.system.niveis) - num(a.system.niveis))[0];
	const pmNivel = num(principal?.system?.pmPorNivel);
	const impares = pmNivel >= 4 ? Math.floor((nivel - 1) / 2) : 0;
	const reservas = actor.items.filter((i) => {
		const t = i.getFlag?.(MOD, "tecnica");
		return i.type === "poder" && t?.passiva && !t?.marca;
	});
	const reservado = reservas.reduce((n, i) => n + num(i.getFlag(MOD, "tecnica")?.nivel), 0);
	const bonus = num(actor.getFlag?.(MOD, "edBonus"));
	const max = Math.max(0, inicial + porNivel + impares - reservado + bonus);
	return {
		max, nivel, atr, valorAtr, inicial, porNivel, impares, reservado, bonus, pmNivel, classe: principal?.name ?? "—",
		passivas: actor.items.filter((i) => i.type === "poder" && i.getFlag?.(MOD, "tecnica")?.passiva).length
	};
}

export function calcularSanidade(actor) {
	const s = actor.system;
	const nivel = Math.max(1, num(s.attributes?.nivel?.value, 1));
	const sab = num(s.atributos?.sab?.value);
	return { max: Math.max(0, 10 + sab + (nivel - 1) * (4 + sab)), nivel, sab };
}

function aplicarDerivados(actor) {
	if (actor.type !== "character") return;
	const res = (actor.system.resources ??= {});
	const ed = calcularED(actor);
	const san = calcularSanidade(actor);
	const fonte = actor._source?.system?.resources ?? {};
	const pega = (k, max) => (fonte[k] && Number.isFinite(Number(fonte[k].value)) ? Number(fonte[k].value) : max);
	res.ed = { ...(res.ed ?? {}), value: pega("ed", ed.max), max: ed.max, label: "Energia Divina" };
	res.sanidade = { ...(res.sanidade ?? {}), value: pega("sanidade", san.max), max: san.max, label: "Sanidade" };
}

/* ---------------- ficha do personagem ---------------- */

function liRecurso(id, titulo, valor, max, dica) {
	return `<li class="attribute rel-recurso rel-${id} flexcol" data-tooltip="${dica}">
		<h4 class="attribute-name box-title">${titulo}</h4>
		<div class="attribute-value multiple flexrow">
			<input type="number" data-dtype="Number" placeholder="0" name="system.resources.${id}.value" value="${valor}" max="${max}">
			<span class="sep">/</span>
			<input type="number" value="${max}" disabled>
		</div>
	</li>`;
}

function injetarFicha(app, html) {
	const actor = app.actor;
	if (!actor || actor.type !== "character") return;
	const raiz = elemento(html);
	if (!raiz || raiz.querySelector(".rel-recurso")) return;
	const editavel = app.isEditable;
	const ed = calcularED(actor);
	const san = calcularSanidade(actor);
	const r = actor.system.resources ?? {};
	const dicaED = [
		`<b>Energia Divina</b>`,
		`1º nível: 1 + ½ ${ATRIBUTOS_MENTAIS[ed.atr]} (${ed.valorAtr >= 0 ? "+" : ""}${ed.valorAtr}) = ${ed.inicial}`,
		`+1 por nível depois do 1º: +${ed.porNivel}`,
		`Classe ${ed.classe} (${ed.pmNivel} PM/nível)${ed.pmNivel >= 4 ? `: +${ed.impares} nos níveis ímpares` : ": sem bônus de ímpares"}`,
		ed.reservado ? `Passivas reservam: −${ed.reservado}` : "",
		ed.bonus ? `Bônus manual: ${ed.bonus > 0 ? "+" : ""}${ed.bonus}` : ""
	].filter(Boolean).join("<br>");
	const dicaSan = `<b>Sanidade</b><br>10 + Sabedoria no 1º nível, +4 + Sabedoria por nível.`;
	const lis = liRecurso("ed", "ED", r.ed?.value ?? ed.max, ed.max, dicaED.replace(/"/g, "&quot;"))
		+ liRecurso("sanidade", "Sanidade", r.sanidade?.value ?? san.max, san.max, dicaSan);

	// ao lado de PV/PM (ficha comum ou ficha em abas)
	const mana = raiz.querySelector("li.attribute.mana");
	if (mana) mana.insertAdjacentHTML("afterend", lis);
	else (raiz.querySelector(".sheet-body") ?? raiz).insertAdjacentHTML("afterbegin", `<ul class="attributes flexrow rel-recursos-solto">${lis}</ul>`);

	// barra do Relíquias: atributo da Bênção, bônus, descanso e distribuição
	const opts = Object.entries(ATRIBUTOS_MENTAIS).map(([k, v]) => `<option value="${k}" ${k === ed.atr ? "selected" : ""}>${v}</option>`).join("");
	const passivasAviso = ed.passivas > 3 ? `<span class="rel-aviso" data-tooltip="O livro permite no máximo 3 passivas da Bênção (contando a Marca).">⚠ ${ed.passivas} passivas</span>` : "";
	const barra = document.createElement("div");
	barra.className = "rel-barra flexrow";
	barra.innerHTML = `
		<span class="rel-barra-titulo">Relíquias</span>
		<label data-tooltip="Atributo-chave da Bênção (somente mentais). Define a ED inicial e a CD das Técnicas Divinas.">Bênção
			<select class="rel-atr-bencao" ${editavel ? "" : "disabled"}>${opts}</select></label>
		<label data-tooltip="CD das Técnicas Divinas = 10 + ½ nível + atributo-chave">CD <b>${10 + Math.floor(ed.nivel / 2) + ed.valorAtr}</b></label>
		<label data-tooltip="Bônus ou penalidade manual no máximo de ED (itens, Mestre etc.)">± ED
			<input type="number" class="rel-ed-bonus" value="${ed.bonus}" ${editavel ? "" : "disabled"}></label>
		${passivasAviso}
		<a class="rel-botao rel-descanso" data-tooltip="Recupera toda a Energia Divina"><i class="fa-solid fa-sun"></i></a>
		<a class="rel-botao rel-distribuir" data-tooltip="Distribuir atributos (regra do livro)"><i class="fa-solid fa-dice-d20"></i></a>`;
	const ancora = raiz.querySelector(".resources-main") ?? raiz.querySelector("li.rel-recurso")?.closest("ul");
	if (ancora) ancora.after(barra);

	if (!editavel) return;
	barra.querySelector(".rel-atr-bencao").addEventListener("change", (ev) => actor.setFlag(MOD, "atributoBencao", ev.currentTarget.value));
	barra.querySelector(".rel-ed-bonus").addEventListener("change", (ev) => actor.setFlag(MOD, "edBonus", Number(ev.currentTarget.value) || 0));
	barra.querySelector(".rel-descanso").addEventListener("click", async () => {
		await actor.update({ "system.resources.ed.value": calcularED(actor).max });
		ui.notifications.info(`${actor.name} recuperou toda a Energia Divina.`);
	});
	barra.querySelector(".rel-distribuir").addEventListener("click", () => abrirDistribuicao(actor));
}

/* ---------------- consumo de ED ---------------- */

/** Impede usar uma técnica sem ED suficiente (o sistema só deixaria de descontar). */
function protegerConsumo() {
	const proto = CONFIG.Item.documentClass?.prototype;
	if (!proto?._getUsageUpdates) return;
	const original = proto._getUsageUpdates;
	proto._getUsageUpdates = function (opts = {}) {
		try {
			const c = this.system?.consume;
			if (opts.consumeResource && c?.type === "attribute" && ["ed", "sanidade"].includes(c.target) && this.actor) {
				const atual = Number(this.actor.system.resources?.[c.target]?.value ?? 0);
				const custo = Number(c.amount ?? 0);
				if (custo > atual) {
					ui.notifications.warn(`${this.actor.name} não tem ${c.target === "ed" ? "Energia Divina" : "Sanidade"} suficiente para ${this.name} (precisa ${custo}, tem ${atual}).`);
					return false;
				}
			}
		} catch (e) { console.error(`${MOD} | consumo`, e); }
		return original.call(this, opts);
	};
}

export function iniciarRecursos() {
	if (!cfg("energiaDivina", true)) return;
	const proto = CONFIG.Actor.documentClass.prototype;
	const original = proto.prepareDerivedData;
	proto.prepareDerivedData = function (...args) {
		const r = original.apply(this, args);
		try { aplicarDerivados(this); } catch (e) { console.error(`${MOD} | ED/Sanidade`, e); }
		return r;
	};
	protegerConsumo();
	Hooks.on("renderActorSheet", injetarFicha);
}
