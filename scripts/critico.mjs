/**
 * Dano crítico do livro: o 20 natural garante o acerto; para ser crítico, role 1d100 — 25 ou menos confirma.
 * Confirmado, o dano da arma é multiplicado pelo atributo de ataque (Força em Luta, Destreza em Pontaria...).
 * O módulo só acrescenta um cartão no chat; ele não muda as rolagens do sistema.
 */
import { MOD, cfg, elemento } from "./config.mjs";

function natural20(roll) {
	for (const d of roll?.dice ?? []) {
		if (d.faces !== 20) continue;
		const ativos = d.results.filter((r) => r.active !== false && !r.discarded);
		if (ativos.some((r) => r.result === 20)) return true;
	}
	return false;
}

function armaDaMensagem(message) {
	const html = document.createElement("div");
	html.innerHTML = message.content ?? "";
	const card = html.querySelector(".chat-card[data-item-id]");
	if (!card) return null;
	const actor = game.actors.get(card.dataset.actorId) ?? ChatMessage.getSpeakerActor(message.speaker);
	const item = actor?.items.get(card.dataset.itemId);
	if (!item || item.type !== "arma") return null;
	return { actor, item };
}

function atributoDoAtaque(actor, item) {
	const ataque = item.system.rolls?.find((r) => r.type === "ataque");
	const pericia = ataque?.parts?.[1]?.[0] || (item.system.proposito === "disparo" ? "pont" : "luta");
	const atr = ataque?.parts?.[1]?.[1] || actor.system.pericias?.[pericia]?.atributo || (pericia === "pont" ? "des" : "for");
	const valor = Number(actor.system.atributos?.[atr]?.value ?? 1);
	const nome = game.i18n.localize(CONFIG.T20?.atributos?.[atr] ?? atr);
	return { atr, nome, valor };
}

async function aoCriar(message) {
	if (!cfg("criticoLivro", true)) return;
	if (message.author?.id !== game.user.id && message.user?.id !== game.user.id) return;
	if (message.getFlag(MOD, "critico")) return;
	const rolls = message.rolls ?? [];
	const ataque = rolls.find((r) => (r.dice ?? []).some((d) => d.faces === 20));
	if (!ataque || !natural20(ataque)) return;
	const ref = armaDaMensagem(message);
	if (!ref) return;
	const { actor, item } = ref;
	const atr = atributoDoAtaque(actor, item);
	const mult = Math.max(1, atr.valor);
	const d100 = await new Roll("1d100").evaluate();
	const ok = d100.total <= 25;
	const dano = item.system.rolls?.find((r) => r.type === "dano");
	const formula = dano?.parts?.[0]?.[0] || "";
	const conteudo = `<div class="rel-critico ${ok ? "rel-ok" : "rel-falha"}">
		<h3>${ok ? "Crítico confirmado!" : "Sem crítico"}</h3>
		<p>20 natural com <b>${item.name}</b> — d100: <b>${d100.total}</b> ${ok ? "≤" : ">"} 25.</p>
		${ok ? `<p>Multiplique o dano da arma pelo atributo de ataque: <b>${atr.nome} ${atr.valor >= 0 ? "+" : ""}${atr.valor}</b> → <b>×${mult}</b>.</p>
		${formula ? `<button type="button" class="rel-dano-critico" data-formula="${formula}" data-mult="${mult}" data-tipo="${dano.parts[0][1] || ""}"><i class="fa-solid fa-burst"></i> Rolar dano da arma ×${mult}</button>` : ""}`
			: `<p>O 20 natural só garante o acerto: use o <b>dano normal</b> (o dobro automático do sistema não vale nesta regra).</p>`}
	</div>`;
	await ChatMessage.create({ speaker: message.speaker, content: conteudo, rolls: [d100], flags: { [MOD]: { critico: true } } });
}

function botoes(message, html) {
	const raiz = elemento(html);
	raiz?.querySelectorAll(".rel-dano-critico").forEach((b) => b.addEventListener("click", async (ev) => {
		ev.preventDefault();
		const { formula, mult, tipo } = ev.currentTarget.dataset;
		const r = await new Roll(`(${formula}) * ${mult}`).evaluate();
		r.toMessage({ speaker: message.speaker, flavor: `Dano crítico (×${mult})${tipo ? ` — ${tipo}` : ""}`, flags: { [MOD]: { critico: true } } });
	}));
}

export function iniciarCritico() {
	Hooks.on("createChatMessage", (m) => aoCriar(m).catch((e) => console.error(`${MOD} | crítico`, e)));
	if (game.release.generation >= 13) Hooks.on("renderChatMessageHTML", botoes);
	else Hooks.on("renderChatMessage", botoes);
}
