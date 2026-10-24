/**
 * Técnicas Divinas: poderes do tipo Distinção com nível 0 a 5.
 * - Ativas: custam 1 ED por nível, descontado ao usar (sem ED suficiente, o uso é bloqueado).
 * - Passivas: reservam 1 ED por nível do máximo (a Marca da Bênção é gratuita).
 * O bloco "Técnica Divina" aparece na aba Detalhes da ficha do poder.
 */
import { MOD, elemento } from "./config.mjs";

const ACESSO = { 0: 1, 1: 1, 2: 5, 3: 9, 4: 13, 5: 17 };

export function dadosTecnica(item) {
	return item?.getFlag?.(MOD, "tecnica") ?? null;
}

async function salvar(item, t) {
	const upd = { [`flags.${MOD}.tecnica`]: t };
	if (t) {
		upd["system.tipo"] = "distincao";
		if (t.passiva) upd["system.ativacao.execucao"] = "passive";
		else if (item.system.ativacao?.execucao === "passive") upd["system.ativacao.execucao"] = "action";
	}
	await item.update(upd);
}

/** Cobra a ED das técnicas ativas ao usar (o sistema não tem consumo para poderes). */
function cobrarAoUsar() {
	const proto = CONFIG.Item.documentClass?.prototype;
	if (!proto?.roll) return;
	const original = proto.roll;
	proto.roll = async function (...args) {
		const t = this.type === "poder" ? dadosTecnica(this) : null;
		const custo = t && !t.passiva ? Number(t.nivel) || 0 : 0;
		const actor = this.actor;
		if (custo > 0 && actor) {
			const atual = Number(actor.system.resources?.ed?.value ?? 0);
			if (atual < custo) {
				ui.notifications.warn(`${actor.name} não tem Energia Divina suficiente para ${this.name} (precisa ${custo}, tem ${atual}).`);
				return null;
			}
			const r = await original.apply(this, args);
			if (r) await actor.update({ "system.resources.ed.value": atual - custo });
			return r;
		}
		return original.apply(this, args);
	};
}

function injetarItem(app, html) {
	const item = app.item ?? app.document;
	if (!item || item.type !== "poder") return;
	const raiz = elemento(html);
	const detalhes = raiz?.querySelector('.tab.details[data-tab="details"]');
	if (!detalhes || detalhes.querySelector(".rel-tecnica")) return;
	const t = dadosTecnica(item);
	const ativo = !!t;
	const nivel = Number(t?.nivel ?? 1);
	const modo = t?.marca ? "marca" : t?.passiva ? "passiva" : "ativa";
	const nivOpts = [0, 1, 2, 3, 4, 5].map((n) => `<option value="${n}" ${n === nivel ? "selected" : ""}>Nível ${n} (a partir do ${ACESSO[n]}º)</option>`).join("");
	const resumo = !ativo ? "" : modo === "ativa" ? `Custa <b>${nivel} ED</b> ao usar.` : modo === "marca" ? "Marca da Bênção: gratuita, não reduz o ED máximo." : `Reserva <b>${nivel} ED</b> do máximo.`;
	const bloco = document.createElement("fieldset");
	bloco.className = "rel-tecnica rel-bloco";
	bloco.innerHTML = `
		<legend>Técnica Divina (Relíquias)</legend>
		<div class="form-group">
			<label>É uma Técnica Divina</label>
			<div class="form-fields"><input type="checkbox" class="rel-t-ativo" ${ativo ? "checked" : ""} ${app.isEditable ? "" : "disabled"}></div>
		</div>
		${ativo ? `
		<div class="form-group">
			<label>Nível</label>
			<div class="form-fields"><select class="rel-t-nivel" ${app.isEditable ? "" : "disabled"}>${nivOpts}</select></div>
		</div>
		<div class="form-group">
			<label>Tipo</label>
			<div class="form-fields"><select class="rel-t-modo" ${app.isEditable ? "" : "disabled"}>
				<option value="ativa" ${modo === "ativa" ? "selected" : ""}>Ativa (custa ED)</option>
				<option value="passiva" ${modo === "passiva" ? "selected" : ""}>Passiva (reserva ED)</option>
				<option value="marca" ${modo === "marca" ? "selected" : ""}>Marca da Bênção (gratuita)</option>
			</select></div>
		</div>
		<p class="notes">${resumo} Sustentar uma técnica custa 1 ED por rodada (desconte no campo ED da ficha).</p>` : `<p class="notes">Marque para usar este poder como Técnica Divina da Bênção.</p>`}`;
	detalhes.prepend(bloco);
	if (!app.isEditable) return;
	const ler = () => {
		if (!bloco.querySelector(".rel-t-ativo").checked) return null;
		const m = bloco.querySelector(".rel-t-modo")?.value ?? "ativa";
		const n = Number(bloco.querySelector(".rel-t-nivel")?.value ?? 1);
		return { nivel: m === "marca" ? 0 : n, passiva: m !== "ativa", marca: m === "marca" };
	};
	bloco.querySelectorAll("input, select").forEach((el) => el.addEventListener("change", (ev) => { ev.stopPropagation(); salvar(item, ler()); }));
}

/** Etiqueta de custo em ED no cartão do chat. */
function etiquetaChat(message, html) {
	const raiz = elemento(html);
	const card = raiz?.querySelector(".chat-card[data-item-id]");
	if (!card || card.querySelector(".rel-custo-ed")) return;
	const actor = game.actors.get(card.dataset.actorId) ?? ChatMessage.getSpeakerActor?.(message.speaker);
	const item = actor?.items.get(card.dataset.itemId);
	const t = dadosTecnica(item);
	if (!t || t.passiva || !Number(t.nivel)) return;
	card.querySelector(".card-header")?.insertAdjacentHTML("beforeend", `<span class="rel-custo-ed" data-tooltip="Técnica Divina nível ${t.nivel}">${t.nivel} ED</span>`);
}

export function iniciarTecnicas() {
	cobrarAoUsar();
	Hooks.on("renderItemSheet", injetarItem);
	if (game.release.generation >= 13) Hooks.on("renderChatMessageHTML", etiquetaChat);
	else Hooks.on("renderChatMessage", etiquetaChat);
}
