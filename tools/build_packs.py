# -*- coding: utf-8 -*-
"""Gera os compêndios do módulo (data/*.json + packs LevelDB) a partir de conteudo.py e livro.py.
Uso: python3 tools/build_packs.py   (na raiz do módulo)"""
import json, hashlib, os, re, shutil, sys, struct
sys.path.insert(0, os.path.dirname(__file__))
from conteudo import MOD, ARMAS, ARMADURAS, CUSTO_FORJA, MATERIAIS, REGRA_PENTE
from livro import CAPITULOS
import ldb

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYS = "systems/tormenta20/icons"
IMG = f"modules/{MOD}/images"
STATS = {"coreVersion": "13.351", "systemId": "tormenta20", "systemVersion": "1.5.015", "createdTime": 1792800000000,
         "modifiedTime": 1792800000000, "lastModifiedBy": "reliquias00000000", "compendiumSource": None, "duplicateSource": None, "exportSource": None}
ALFA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def gid(*partes):
    h = hashlib.sha256(("|".join(partes)).encode()).digest()
    return "".join(ALFA[b % 62] for b in h[:16])

# ------------------------------------------------------------ helpers de documento
def pasta(pack, nome, pai=None, cor=None, sort=0):
    return {"_id": gid(pack, "folder", nome, pai or ""), "name": nome, "type": "Item" if pack != "livro" else "JournalEntry",
            "folder": pai, "sorting": "m", "sort": sort, "color": cor, "flags": {}, "description": "", "_stats": STATS}

def item(pack, nome, tipo, img, system, folder=None, effects=(), sort=0, flags=None, ownership=None):
    _id = gid(pack, "item", nome)
    effs = []
    for i, e in enumerate(effects):
        e = dict(e); e["_id"] = gid(pack, nome, "effect", str(i)); e["origin"] = None
        effs.append(e)
    return {"_id": _id, "name": nome, "type": tipo, "img": img, "system": system, "effects": effs, "folder": folder,
            "sort": sort, "flags": flags or {}, "ownership": ownership or {"default": 0}, "_stats": STATS}

def efeito(nome, changes, transfer=True, onuse=False, self_=False, img="icons/svg/aura.svg", desc=""):
    return {"name": nome, "img": img, "type": "base", "system": {}, "tint": "#ffffff", "description": desc,
            "changes": [{"key": k, "mode": m, "value": str(v), "priority": None} for k, v, m in changes],
            "disabled": False, "transfer": transfer, "statuses": [], "sort": 0,
            "duration": {"startTime": None, "combat": None, "seconds": None, "rounds": None, "turns": None, "startRound": None, "startTurn": None},
            "flags": {"tormenta20": {"onuse": onuse, "durationScene": False, "self": self_}}, "_stats": STATS}

FISICO = lambda: {"carregado": True, "espacos": 0, "peso": 0, "qtd": 1, "preco": 0, "pv": {"value": 0, "max": 0}, "rd": 0}
ATIV = lambda **k: {"custo": 0, "condicao": "", "execucao": "passive", "qtd": "", "special": "", **k}
UPG = lambda: {"melhoria1": "", "melhoria2": "", "melhoria3": "", "melhoria4": "", "material": "", "encanto1": "", "encanto2": "", "encanto3": ""}
def base_sys(desc, fonte="As Relíquias do Apocalipse"):
    return {"description": {"value": desc, "unidentified": ""}, "source": fonte, "origin": "", "tags": [], "rolltags": [],
            "automationtags": [], "chatFlavor": "", "chatGif": ""}

# ------------------------------------------------------------ compêndio: equipamentos
def equipamentos():
    P = "equipamentos"
    f_fogo = pasta(P, "Armas de Fogo Arcanas", sort=1)
    f_arm = pasta(P, "Armaduras", sort=2)
    f_esc = pasta(P, "Escudos", sort=3)
    itens = []
    for i, a in enumerate(ARMAS):
        unidade, valor = a["alcance"]
        s = {**base_sys(f"<p>{a['desc']}</p>{REGRA_PENTE}"), **FISICO(),
             "ativacao": ATIV(execucao="action"), "consume": {"amount": 0, "mpMultiplier": False, "target": "", "type": ""},
             "duracao": {"units": "inst", "value": 0, "special": ""}, "range": {"units": "m" if unidade == "m" else "", "value": valor},
             "alcance": unidade, "alvo": "", "area": a["area"], "upgrades": UPG(), "enableAutoUpgrades": True,
             "rolls": [{"name": "Ataque", "key": "ataque0", "type": "ataque", "parts": [["1d20", ""], ["pont", ""], ["", ""]], "adaptavel": "", "versatil": ""},
                       {"name": "Dano", "key": "dano1", "type": "dano", "parts": [[a["dano"], "perfuracao"], ["padrao", ""]], "adaptavel": "", "versatil": ""}],
             "ataques": 0, "equipado": 0, "equipado2": {"slot": 0, "type": "hand"}, "tipoUso": "fog", "proficiencia": "fogo",
             "proposito": "disparo", "empunhadura": a["empunhadura"], "criticoM": 20, "criticoX": 2,
             "propriedades": {"ada": False, "agi": False, "alo": False, "des": False, "dup": False, "ver": False, "hib": False}, "size": "normal"}
        s["preco"] = a["preco"]; s["espacos"] = a["espacos"]
        img = f"{SYS}/itens/equipamentos/{'pistola' if a['empunhadura'] == 'leve' else 'mosquete'}.webp"
        itens.append(item(P, a["nome"], "arma", img, s, f_fogo["_id"], sort=i * 100,
                          flags={MOD: {"pente": a["pente"], "armaFogoArcana": True}}))
    for i, (nome, tipo, d, rd, pen, desl, preco, esp) in enumerate(ARMADURAS):
        escudo = tipo == "escudo"
        desc = f"<p><strong>Bônus de Defesa:</strong> +{d}. <strong>Redução de dano:</strong> {rd if rd else '—'}. <strong>Penalidade:</strong> {pen if pen else '—'}. <strong>Deslocamento:</strong> {desl}.</p>"
        if desl == "-3m": desc += "<p>Reduz o deslocamento em 3m (armadura pesada).</p>"
        s = {**base_sys(desc), **FISICO(), "ativacao": ATIV(), "upgrades": UPG(), "enableAutoUpgrades": True, "rolls": [],
             "equipado": False, "equipado2": {"slot": 0, "type": "hand" if escudo else "body"},
             "armadura": {"maxAtr": 0, "penalidade": pen, "value": d}, "tipo": tipo}
        s["preco"] = preco; s["espacos"] = esp
        effs = [efeito(f"{nome}: redução de dano {rd}", [("system.tracos.resistencias.dano.bonus", rd, 2)], img="icons/svg/shield.svg")] if rd else []
        img = {"Armadura Simples": "armadura-couro", "Armadura Média": "brunea", "Armadura Completa": "armadura-completa",
               "Escudo Leve": "escudo-leve", "Escudo Pesado": "escudo-pesado"}[nome]
        itens.append(item(P, nome, "equipamento", f"{SYS}/itens/equipamentos/{img}.webp", s, (f_esc if escudo else f_arm)["_id"], effs, sort=i * 100))
    return [f_fogo, f_arm, f_esc], itens

# ------------------------------------------------------------ compêndio: forja
MAT_ICON = {"aco-rubi": "aco-rubi", "adamante-meteorico": "adamante", "madeira-de-crystalis": "madeira-magica", "cristal-solar": "po-de-cristal",
            "coracao-de-leviata": "essencia-abissal", "prisma-onirico": "orbe-cristalina", "luz-estelar": "metal-arco-iris", "aco-lunar": "mitral",
            "quitina-de-razza": "ossos-de-monstro", "ferro-vivo": "materia-vermelha", "sangrambaro": "madeira-tollon", "aco-vulcanico": "baga-de-fogo",
            "ferro-etereo": "essencia-mana", "pedra-da-aurora": "gemas-preciosas", "aco-draconico": "dente-de-dragao"}
def consumivel(desc, tipo="material"):
    return {**base_sys(desc), **FISICO(), "ativacao": ATIV(), "consume": {"amount": 0, "mpMultiplier": False, "target": "", "type": ""},
            "upgrades": UPG(), "enableAutoUpgrades": True, "rolls": [], "tipo": tipo, "subtipo": ""}

def forja():
    P = "forja"
    fp = pasta(P, "Pedras da Forja (armas)", sort=1)
    fl = pasta(P, "Ladrilhos da Proteção (armaduras)", sort=2)
    fm = pasta(P, "Materiais Especiais", sort=3)
    itens = []
    for n in range(1, 11):
        c = CUSTO_FORJA[n - 1]
        for nome, pas, alvo, img in ((f"Pedra da Forja +{n}", fp, "uma arma", "pedras"), (f"Ladrilho da Proteção +{n}", fl, "uma armadura ou escudo", "gemas-preciosas")):
            desc = (f"<p>Material de aprimoramento usado para levar {alvo} ao nível <strong>+{n}</strong>. Além dele, o aprimoramento custa <strong>{c:,} Midares</strong>.</p>".replace(",", ".")
                    + "<p>Use o bloco <em>Forja</em> na ficha do item: com este material no inventário do personagem, ele é consumido automaticamente.</p>")
            ic = f"{SYS}/itens/equipamentos/pedras.webp" if img == "pedras" else f"{SYS}/itens/gerais/{img}.webp"
            itens.append(item(P, nome, "consumivel", ic, consumivel(desc), pas["_id"], sort=n * 10, flags={MOD: {"forja": {"nivel": n, "tipo": "arma" if pas is fp else "armadura"}}}))
    for i, (k, nome, lore, a, ar, e) in enumerate(MATERIAIS):
        desc = (f"<p><em>{lore}</em></p><ul><li><strong>Arma:</strong> {a}</li><li><strong>Armadura:</strong> {ar}</li><li><strong>Esotérico:</strong> {e}</li></ul>"
                "<p>Material ancestral: só pode ser aplicado uma única vez, em item de nível 0. Os efeitos escalam com o nível do item (+1/+4/+7/+10). "
                "Aplique pelo bloco <em>Forja</em> na ficha do item.</p>")
        itens.append(item(P, nome, "consumivel", f"{SYS}/itens/gerais/{MAT_ICON[k]}.webp", consumivel(desc), fm["_id"], sort=i * 10, flags={MOD: {"material": k}}))
    return [fp, fl, fm], itens

# ------------------------------------------------------------ compêndio: bênçãos e técnicas
def poder(desc, execucao="passive", custo_ed=0, nivel=0, passiva=False, marca=False, bencao=False):
    s = {**base_sys(desc), "ativacao": ATIV(execucao=execucao),
         "consume": {"amount": custo_ed, "mpMultiplier": False, "target": "ed" if custo_ed else "", "type": "attribute" if custo_ed else ""},
         "duracao": {"units": "inst", "value": 0, "special": ""}, "range": {"units": "", "value": 0}, "alcance": "", "alvo": "", "area": "",
         "rolls": [], "tipo": "distincao", "subtipo": ""}
    fl = {MOD: {"tecnica": {"nivel": nivel, "passiva": passiva, "marca": marca}}} if not bencao else {MOD: {"bencao": True}}
    return s, fl

def bencaos():
    P = "bencaos"
    fb = pasta(P, "Modelos", sort=1)
    itens = []
    s, fl = poder("<p><strong>Bênção de [divindade]</strong>. Fragmento da alma de um deus selado desperto no Arauto. Funciona como uma <strong>Distinção</strong>.</p>"
                  "<p><strong>Atributo-Chave:</strong> Intelecto, Sabedoria ou Presença (escolha no bloco Relíquias da ficha do personagem).</p>"
                  "<p><strong>Domínio:</strong> descreva aqui o domínio do deus. As Técnicas Divinas devem sempre remeter a ele.</p>", bencao=True)
    itens.append(item(P, "Bênção (modelo)", "poder", f"{SYS}/poderes/distincao.webp", s, fb["_id"], sort=0, flags=fl))
    s, fl = poder("<p><strong>Marca da Bênção</strong> (Passiva I). Sinal divino na alma e no corpo do Arauto, recebido no 1º nível. "
                  "Conta como 1 das 3 passivas máximas da Bênção e <strong>não reduz</strong> o ED máximo.</p><p>Descreva o efeito aqui.</p>", nivel=0, passiva=True, marca=True)
    itens.append(item(P, "Marca da Bênção (modelo)", "poder", f"{SYS}/magias/bencao.webp", s, fb["_id"], sort=10, flags=fl))
    acesso = {0: 1, 1: 1, 2: 5, 3: 9, 4: 13, 5: 17}
    for n in range(0, 6):
        s, fl = poder(f"<p><strong>Técnica Divina — Nível {n}</strong> (ativa). Custo: <strong>{n} ED</strong>. Acesso a partir do {acesso[n]}º nível de personagem.</p>"
                      "<p>CD = 10 + ½ do nível + atributo-chave da Bênção.</p><p>Descreva o efeito aqui.</p>", execucao="action", custo_ed=n, nivel=n)
        itens.append(item(P, f"Técnica Divina — Nível {n} (modelo)", "poder", f"{SYS}/magias/intervencao-divina.webp", s, fb["_id"], sort=20 + n, flags=fl))
    for n in range(1, 6):
        s, fl = poder(f"<p><strong>Técnica Divina Passiva — Nível {n}</strong>. Reserva <strong>{n} ED</strong> do seu máximo enquanto estiver na ficha. "
                      f"Acesso a partir do {acesso[n]}º nível. Você pode ter no máximo 3 passivas da Bênção (contando a Marca).</p><p>Descreva o efeito aqui.</p>", nivel=n, passiva=True)
        itens.append(item(P, f"Técnica Divina Passiva — Nível {n} (modelo)", "poder", f"{SYS}/magias/aura-divina.webp", s, fb["_id"], sort=40 + n, flags=fl))
    return [fb], itens

# ------------------------------------------------------------ compêndio: relíquias (do mundo do mestre)
def reliquias():
    P = "reliquias"
    src = os.path.join(RAIZ, "tools", "mundo_reliquias.json")
    if not os.path.exists(src): return [], []
    docs = json.load(open(src, encoding="utf-8"))
    f = pasta(P, "Relíquias e Runas", sort=1)
    trocas = {"ArquivoRPG/Reliquias%20do%20apocalipse/Espada%20do%20Nada.jpg": f"{IMG}/itens/espada-do-nada.webp",
              "ArquivoRPG/Reliquias%20do%20apocalipse/Runa%20Do%20Nada.png": f"{IMG}/itens/runa-do-nada.webp",
              "worlds/reliquias-do-apocalipse/Reliquia%20do%20tempo.png": f"{IMG}/itens/reliquia-do-tempo.webp",
              "worlds/reliquias-do-apocalipse/Runa%20do%20Eco%20Profano.png": f"{IMG}/itens/runa-do-eco-profano.webp"}
    itens = []
    for i, d in enumerate(docs):
        d = json.loads(json.dumps(d))
        novo = item(P, d["name"], d["type"], trocas.get(d["img"], d["img"]), d["system"], f["_id"], sort=i * 10)
        novo["system"]["source"] = novo["system"].get("source") or "As Relíquias do Apocalipse"
        effs = []
        for j, e in enumerate(d.get("effects", [])):
            e = dict(e); e["_id"] = gid(P, d["name"], "effect", str(j)); e["origin"] = None
            if e.get("img") in trocas: e["img"] = trocas[e["img"]]
            effs.append(e)
        novo["effects"] = effs
        itens.append(novo)
    return [f], itens

# ------------------------------------------------------------ compêndio: livro
def livro(indice):
    P = "livro"
    entradas = []
    def link(m):
        nome = m.group(1)
        if nome not in indice: raise SystemExit(f"link para item inexistente: {nome}")
        pack, _id = indice[nome]
        return f"@UUID[Compendium.{MOD}.{pack}.Item.{_id}]{{{nome}}}"
    for ci, (titulo, paginas) in enumerate(CAPITULOS):
        eid = gid(P, "entry", titulo)
        pages = []
        for pi, (nome, html) in enumerate(paginas):
            html = re.sub(r"\{\{item:([^}]+)\}\}", link, html)
            html = re.sub(r"\{\{img:([^}]+)\}\}", lambda m: f"{IMG}/{m.group(1)}", html)
            pages.append({"_id": gid(P, titulo, "page", nome), "name": nome, "type": "text", "title": {"show": True, "level": 1},
                          "image": {}, "text": {"content": html, "format": 1, "markdown": None}, "video": {"controls": True, "volume": 0.5},
                          "src": None, "system": {}, "sort": (pi + 1) * 100000, "ownership": {"default": -1}, "flags": {}, "category": None, "_stats": STATS})
        entradas.append({"_id": eid, "name": f"{ci}. {titulo}" if ci else titulo, "pages": pages, "folder": None, "sort": ci * 100000,
                         "ownership": {"default": 0}, "flags": {MOD: {"livro": True}}, "categories": [], "_stats": STATS})
    return [], entradas

# ------------------------------------------------------------ escrita
def salvar(nome, pastas, docs, colecao):
    os.makedirs(os.path.join(RAIZ, "data"), exist_ok=True)
    json.dump({"folders": pastas, colecao: docs}, open(os.path.join(RAIZ, "data", f"{nome}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dest = os.path.join(RAIZ, "packs", nome)
    shutil.rmtree(dest, ignore_errors=True); os.makedirs(dest)
    kv = []
    for f in pastas: kv.append((f"!folders!{f['_id']}", json.dumps(f, ensure_ascii=False)))
    emb = "effects" if colecao == "items" else "pages"
    for d in docs:
        d = json.loads(json.dumps(d))
        subs = d.get(emb, [])
        d[emb] = [s["_id"] for s in subs]
        kv.append((f"!{colecao}!{d['_id']}", json.dumps(d, ensure_ascii=False)))
        for s in subs: kv.append((f"!{colecao}.{emb}!{d['_id']}.{s['_id']}", json.dumps(s, ensure_ascii=False)))
    kv.sort()
    seq = ldb.write_log(os.path.join(dest, "000003.log"), kv)
    open(os.path.join(dest, "CURRENT"), "w").write("MANIFEST-000002\n")
    # manifesto: comparador bytewise, log 3, próximo arquivo 4, última sequência 0 (o log é reaplicado ao abrir)
    open(os.path.join(dest, "MANIFEST-000002"), "wb").write(bytes.fromhex("918d7451220001011a6c6576656c64622e4279746577697365436f6d70617261746f72020303040400"))
    # confere
    lido = ldb.read_log(os.path.join(dest, "000003.log"))
    assert len(lido) == len(kv), (nome, len(lido), len(kv))
    print(f"{nome}: {len(pastas)} pastas, {len(docs)} documentos, {len(kv)} chaves")

if __name__ == "__main__":
    indice = {}
    resultado = {}
    for nome, fn in (("equipamentos", equipamentos), ("forja", forja), ("bencaos", bencaos), ("reliquias", reliquias)):
        pastas, docs = fn()
        resultado[nome] = (pastas, docs)
        for d in docs: indice[d["name"]] = (nome, d["_id"])
    for nome, (pastas, docs) in resultado.items():
        if docs: salvar(nome, pastas, docs, "items")
    pastas, entradas = livro(indice)
    salvar("livro", pastas, entradas, "journal")
