/**
 * Distribuição de pontos do livro:
 * todos começam com 1 em cada atributo e têm 6 pontos; na criação, no máximo 3; no mínimo -3.
 * Tirar um ponto de um atributo em 1 leva a -1 (não existe 0). Cada passo para cima custa 1 ponto,
 * cada passo para baixo devolve 1 ponto. O resultado vai para o valor base do atributo na ficha
 * (bônus raciais e temporários continuam nos campos próprios do sistema).
 */
import { MOD, cfg } from "./config.mjs";

const ORDEM = ["for", "des", "con", "int", "sab", "car"];
const NOMES = { for: "Força", des: "Destreza", con: "Vigor", int: "Intelecto", sab: "Sabedoria", car: "Presença" };

const subir = (v) => (v === -1 ? 1 : v + 1);
const descer = (v) => (v === 1 ? -1 : v - 1);
/** Pontos gastos para chegar a v partindo de 1. */
const custo = (v) => (v >= 1 ? v - 1 : v);

export async function abrirDistribuicao(actor) {
	if (!actor?.isOwner) return ui.notifications.warn("Você não tem permissão para editar esta ficha.");
	const total = Number(cfg("pontosAtributos", 6));
	const maximo = Number(cfg("maxAtributoInicial", 3));
	const minimo = -3;
	const valores = {};
	for (const k of ORDEM) {
		const b = Number(actor.system.atributos?.[k]?.base ?? 1);
		valores[k] = b === 0 ? 1 : Math.max(minimo, Math.min(maximo, b));
	}
	const restam = () => total - ORDEM.reduce((n, k) => n + custo(valores[k]), 0);

	const linhas = ORDEM.map((k) => `
		<div class="rel-atr-linha" data-atr="${k}">
			<span class="rel-atr-nome">${NOMES[k]}</span>
			<button type="button" class="rel-menos" data-atr="${k}"><i class="fa-solid fa-minus"></i></button>
			<span class="rel-atr-valor"></span>
			<button type="button" class="rel-mais" data-atr="${k}"><i class="fa-solid fa-plus"></i></button>
		</div>`).join("");
	const content = `<div class="rel-distribuicao">
		<p class="rel-nota">Todos começam com <b>1</b>. Você tem <b>${total}</b> pontos; máximo <b>${maximo}</b> e mínimo <b>${minimo}</b>. Tirar um ponto de 1 leva a <b>-1</b> e devolve 1 ponto.</p>
		${linhas}
		<p class="rel-restam">Pontos restantes: <b class="rel-restam-n"></b></p>
		<p class="rel-nota">Bônus de raça e outros bônus continuam nos campos próprios da ficha.</p>
	</div>`;

	const DialogV2 = foundry.applications.api.DialogV2;
	const resultado = await DialogV2.wait({
		window: { title: `Distribuir atributos — ${actor.name}`, icon: "fa-solid fa-dice-d20" },
		classes: ["reliquias", "rel-dialogo"],
		content,
		render: (event, dialog) => {
			const el = dialog instanceof HTMLElement ? dialog : (dialog?.element ?? event?.target?.element);
			const atualizar = () => {
				for (const k of ORDEM) {
					const linha = el.querySelector(`.rel-atr-linha[data-atr="${k}"]`);
					const v = valores[k];
					linha.querySelector(".rel-atr-valor").textContent = v > 0 ? `+${v}` : `${v}`;
					const r = restam();
					linha.querySelector(".rel-mais").disabled = v >= maximo || r < 1;
					linha.querySelector(".rel-menos").disabled = v <= minimo;
				}
				const r = restam();
				const n = el.querySelector(".rel-restam-n");
				n.textContent = r;
				n.classList.toggle("rel-negativo", r < 0);
				const ok = el.querySelector('button[data-action="ok"]');
				if (ok) ok.disabled = r < 0;
			};
			el.querySelectorAll(".rel-mais").forEach((b) => b.addEventListener("click", () => { const k = b.dataset.atr; valores[k] = subir(valores[k]); atualizar(); }));
			el.querySelectorAll(".rel-menos").forEach((b) => b.addEventListener("click", () => { const k = b.dataset.atr; valores[k] = descer(valores[k]); atualizar(); }));
			atualizar();
		},
		buttons: [
			{ action: "ok", label: "Aplicar", icon: "fa-solid fa-check", default: true, callback: () => ({ ...valores }) },
			{ action: "cancelar", label: "Cancelar", icon: "fa-solid fa-xmark", callback: () => null }
		],
		rejectClose: false
	});
	if (!resultado) return;
	if (restam() < 0) return ui.notifications.warn("Você gastou mais pontos do que tem.");
	const upd = {};
	for (const k of ORDEM) upd[`system.atributos.${k}.base`] = resultado[k];
	await actor.update(upd);
	await actor.setFlag(MOD, "distribuicao", { ...resultado, pontos: total });
	ui.notifications.info(`Atributos de ${actor.name} distribuídos.`);
}
