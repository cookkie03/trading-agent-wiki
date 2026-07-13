---
title: "Position Sizing — dimensionamento delle posizioni"
type: build
tags:
  - build
  - strategy
  - execution
created: 2026-06-03
updated: 2026-07-13
status: active
priority: high
area: software
related:
  - "[[system/investment/state-schemas]]"
  - "[[system/execution/execution]]"
  - "[[system/agents/agents]]"
  - "[[system/investment/rating-scoring]]"
confidence: medium
---

# Position Sizing

> Come si decide **quanto** comprare/vendere. È il secondo deliverable concordato con Luca, subito dopo lo [[system/investment/state-schemas]]. Il `position_sizing` è un campo dello state da cui la funzione Trade deterministica estrae l'ordine.

> **Reference design:** il modello risk-based usa `risk_% = base_risk_% × conviction_multiplier`, distanza dallo stop e cap di portfolio heat/titolo. Numeri e dettagli di implementazioni precedenti non sono stato verificato: restano da tarare con backtest. Vedi [[system/_reference/fork-gap-analysis]].

---

## Principio cardine (deciso)

**Sempre relativo al portafoglio, mai valori assoluti** (Luca, call 2026-06-02). Non «compra 1000€ di AAPL» ma «alloca il 4% del portafoglio su AAPL». Questo rende il sizing:
- indipendente dalla dimensione del capitale (scala da [[_meta/glossario#Paper Trading / Testnet|paper trading]] a reale);
- coerente con lo Statuto (riserva 10% cash, % max per asset/settore);
- testabile in backtest senza riscrivere nulla.

---

## Modello proposto (v1): risk-based sizing — si aggancia all'ATR · ✅ impianto approvato da Luca 2026-06-05

> Proposta di Claude 2026-06-05, **impianto approvato da Luca** (*«mi convince»*) — restano da tarare i numeri in backtest. Sfrutta il fatto che la **distanza dallo stop è già nello state** (backbone ATR del [[system/investment/state-schemas]]): `stop_distance = k_stop × ATR`. Questo permette il metodo di sizing più solido e usato dai professionisti — il **fixed-fractional risk** — invece di un peso % a occhio.

**Idea in una frase**: non decidi *quanto comprare*, decidi **quanto sei disposto a perdere** se il trade va male; siccome sai già *a che prezzo metti lo stop* (distanza ATR), la **quantità da comprare si calcola da sola**.

```
1. Budget di rischio del trade (quanto posso perdere):
   risk_%       = base_risk_% × conviction_multiplier
   euro_a_rischio = valore_portafoglio × risk_%

2. Distanza dallo stop (GIÀ nota dallo state — backbone ATR):
   stop_distance = k_stop × ATR        (€ persi per azione se scatta lo stop)

3. Quantità → la size cade fuori da sola:
   quantità          = euro_a_rischio / stop_distance
   valore_posizione  = quantità × entry_price

4. Cap deterministici (Statuto), applicati DOPO:
   - max % per titolo / settore
   - riserva 10% cash sempre intoccabile
   - portfolio heat: somma dei rischi aperti ≤ heat_max_%
   - VaR
```

**Perché è elegante**: fa il **volatility-adjustment gratis**. Un titolo molto volatile ha un ATR grande → stop più largo → `stop_distance` grande → **quantità più piccola** a parità di euro rischiati. Un titolo tranquillo → posizione più grande. Il rischio per trade resta costante anche se i titoli hanno volatilità diverse. (È il punto che in bozza era rimandato a "v2": qui arriva da solo.)

**Conviction scala il *budget di rischio*, non il peso** (così la convinzione e il rischio parlano la stessa lingua):

| `conviction_level` | `conviction_multiplier` | Effetto |
|--------------------|-------------------------|---------|
| Strong Buy / Strong Sell | ~1.5–2.0× | più rischio sul trade + sblocco leva via opzioni |
| Buy / Sell | 1.0× | rischio base |
| Hold | 0 | nessun trade |

**Numeri di partenza (da tarare in backtest, come per l'`entry_price`)**:
- `base_risk_%` = **1%** del portafoglio per trade (classico, prudente).
- `heat_max_%` = **5–6%** di rischio aperto totale su tutte le posizioni (il *portfolio heat*: se sommando i rischi di tutte le posizioni aperte superi questa soglia, non apri altro finché non chiudi qualcosa).
- `max % per titolo` ≈ 10%, cap di settore dallo Statuto.

> **Portfolio heat** = la somma di "quanto perderei se *tutti* gli stop aperti scattassero insieme". Tenerlo sotto una soglia evita che, sommando tanti trade "piccoli e sicuri", il portafoglio sia in realtà esposto a un crollo correlato. È una rete di sicurezza sopra il sizing del singolo trade.

---

## Come si lega alla conviction (nota)

Far dipendere la dimensione dal **`conviction_level`** dello state era l'idea originale di Luca (*«l'idea di farlo dipendere da un [[_meta/glossario#Conviction Level|conviction level]] è molto valida»*). Nel modello sopra la conviction **scala il budget di rischio** (`conviction_multiplier`), non un peso % diretto: stesso spirito, ma ancorato al rischio reale del trade invece che a una percentuale arbitraria. I **cap deterministici** dello Statuto tagliano sempre qualsiasi size che violi [[_meta/glossario#VaR (Value at Risk)|VaR]], % max per area/settore, riserva cash. Vedi guardrail in [[system/agents/agents]].

---

## Kelly Criterion (richiesto da Luca — spiegazione)

> Luca: *«cos'è il [[_meta/glossario#Kelly Criterion|Kelly]] criterion? Aggiungilo alla wiki»*.

Il **Kelly Criterion** è una formula matematica che dice **quale frazione del capitale puntare** su una scommessa per **massimizzare la crescita del capitale nel lungo periodo**, dato che conosci (o stimi) probabilità di vincita e rapporto vincita/perdita.

Formula base (scommessa binaria):
```
f* = p − q/b
```
- `f*` = frazione ottima del capitale da puntare
- `p` = probabilità di vincere
- `q = 1 − p` = probabilità di perdere
- `b` = rapporto vincita/perdita (quanto guadagni per unità rischiata)

**Esempio**: se hai il 60% di probabilità di vincere (`p=0.6`) e guadagni quanto rischi (`b=1`): `f* = 0.6 − 0.4/1 = 0.20` → punta il 20% del capitale.

**Perché ci interessa**: lega la **dimensione della posizione alla qualità del segnale** (probabilità + payoff), esattamente la logica «più convinzione → più size» che vogliamo. Il `conviction_level` e lo storico win-rate degli agenti ([[system/investment/rating-scoring]]) sono i candidati naturali per stimare `p` e `b`.

**Cautele (importanti, da considerare nel design)**:
- Kelly puro è **molto aggressivo**: in pratica si usa **frazionario** (es. *half-Kelly*, metà del valore) perché stimare male `p` porta a sovraesposizione e [[_meta/glossario#Drawdown|drawdown]] pesanti.
- Richiede **stime affidabili** di `p` e `b` — che all'inizio non avremo (no storico). → Kelly è un **obiettivo evolutivo**, non per la prima alpha: si parte con sizing % fisso scalato per conviction, si introduce Kelly frazionario quando c'è storico sufficiente per stimare le probabilità.

---

## Approccio incrementale (coerente con la filosofia di progetto)

Allineato al principio di Luca *«prima un software con un'idea base, poi mano a mano aggiungere pezzi»*:

1. **v0 (prima alpha)**: sizing % fisso (es. peso uguale 1/N), cap da Statuto. Il più semplice possibile, per far partire la pipeline.
2. **v1 (modello proposto sopra)**: **risk-based** — budget di rischio % scalato per conviction, quantità derivata dallo stop ATR. Include **già** il volatility-adjustment (lo stop = `k_stop × ATR` rende la size inversamente proporzionale alla volatilità) + **portfolio heat** come cap aggregato.
3. **v2**: raffinamenti — correlazione tra posizioni (heat "vero" tiene conto di quanto i titoli si muovono insieme), non solo somma lineare dei rischi.
4. **v3**: Kelly frazionario, quando lo storico permette di stimare `p` e `b` per agente/strategia (→ stima dinamica del `base_risk_%` invece che fisso).

---

## Idea da valutare: intervento degli agenti sul sizing (Luca 2026-06-05)

> Luca tiene **sul piatto** l'idea di **permettere agli agenti di intervenire sul position sizing**, *come idea da valutare* — vanno prima **indagati rischi e benefici**, non è una decisione presa.

Il modello v1 è **deterministico** (Python calcola la quantità dal rischio e dallo stop). L'idea è dare all'agente un margine per *aggiustare* la size.

- **Potenziali benefici**: l'agente coglie contesto che la formula non vede (liquidità anomala, event risk imminente, correlazione con posizioni già in portafoglio, sfumature di convinzione oltre l'enum).
- **Potenziali rischi**: rompe il [[_meta/glossario#Principio Deterministico|principio deterministico]] e la pulizia del guardrail di rischio; gli LLM sono **deboli sui numeri**; rischio di **sovraesposizione**; più difficile da backtestare e da rendere riproducibile.
- **Possibile via di mezzo da indagare**: l'agente **non** scavalca i cap dello Statuto né calcola la quantità; propone solo un **fattore di aggiustamento limitato** (es. ±X%) che la funzione deterministica **clampa** dentro i limiti duri. Determinismo sulle barriere di sicurezza, discrezionalità solo nel margine.

→ Da approfondire prima di decidere. Registrata anche come idea in [[artifacts/project-board]] e [[system/foundation/ideas-log]].

---

## Punti aperti

- ~~Reazione di Luca al modello risk-based~~ → **impianto APPROVATO** 2026-06-05; restano i numeri.
- Numeri esatti: `base_risk_%` (1%?), `conviction_multiplier` per livello, `heat_max_%` (5–6%?), cap per titolo/settore → da **tarare in backtest** (stesso meccanismo dell'`entry_price`).
- `heat_max_%` lineare vs corretto per correlazione (v1 vs v2).
- Interazione sizing ↔ leva via opzioni: il sizing di un'opzione è diverso da quello dell'equity spot (vedi [[system/execution/execution]]).
- Aggancio a VaR/CVaR dello Statuto → da chiudere con Salvatore (vedi [[strategy/questions-for-salvatore]]).

---

*Il campo vive in [[system/investment/state-schemas]]; lo consuma la funzione Trade in [[system/execution/execution]]; i cap derivano dallo Statuto in [[system/agents/agents]].*
