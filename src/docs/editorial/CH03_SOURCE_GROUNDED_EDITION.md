# Chapter 03 — Internationalism | source-grounded clarity and non-duplication audit

**Status:** editorial pilot; not a reformatting or print-compositor change.

## Sources and authority

1. **Authority:** Andrew Webster, **“Internationalism,”** `20th Century History-03.pdf`, pp. 1–11 of the supplied PDF (the printed chapter runs pp. 39–49; its final argument continues on p. 12 / printed p. 50, followed by notes and reading guide). Source chapter read as a whole, not just extracted headings.
2. **Language reference:** `11- 20TH CENTURY HISTORY.pdf`, chapter 3, PDF pp. 5–6. It suggests direct wording and an approachable order. It does **not** override, supplement or silently revise Webster’s historical argument.
3. **Editing baseline:** `src/chapters/ch03.html` on stacked Chapter 02 review branch `editorial/ch02-source-grounded-nationalism`, PR #18. The compiled `index.html` and content-hashed PWA worker must be rebuilt in exact sync.

## Intellectual identity and the chapter's closing question

Webster sets internationalism against the 'realist' insistence that sovereign power cannot easily be overcome. He distinguishes **(a) voluntary cooperation over shared needs, (b) legally binding duties over security and law, and (c) visions for a more integrated society not defined by national boundaries**. The source's recurring question is not simply 'do nations cooperate?' but **will they surrender independent authority when it most matters?** Pre-1914 public unions, the League, the UN, communist internationalism and non-state humanitarianism are tests of that question. The final bridge metaphor returns explicitly to it, providing conceptual closure without repeating the opening paragraph verbatim.

### Source-coverage reconstruction

| Original PDF | Essential evidence, mechanism or qualification | Placement in edited notes |
| --- | --- | --- |
| p. 1, introduction | Three meanings of internationalism; sovereign states in an anarchic system; contrast with realism | Opener; popups for internationalism, sovereignty, realist view |
| pp. 2–3 | Technical public unions, 1865 telecommunication, 1874 post, commodity management, 250+ conventions in 1864–1914; majority-vote sovereignty problem; British exit from Sugar Commission 1913 | Section 1 and compact union comparison table |
| pp. 2–3 | ICRC 1863 and Geneva rules 1864: non-state aid founded on state consent; Hague 1899/1907: land-war codification without disarmament; non-compulsory arbitration and Belgium 1914 | Section 1; distinct concepts of humanitarian law, codification, arbitration |
| pp. 4–5 | League 1919; 26-article Covenant; Council, Assembly, Secretariat; Articles 10, 12–16; smaller-state role; US never joined; Curzon denied super-state authority | Section 2 and provisions table |
| pp. 5–6 | 1925 Greece–Bulgaria; expanding legal, economic and social functions; 1922 PCIJ; failed 1923/1924 security schemes, 1925 gas ban only on *use*, 1928 Paris Pact lacking enforcement | Section 2; distinguishes functional accomplishments from political enforcement |
| pp. 6–7 | 1930s crisis: Manchuria, economic cooperation, 1932–34 disarmament, Ethiopia 1935, Austria 1938; membership changes; League legacy to UN | Section 2, with balanced verdict rather than 'League simply failed' |
| pp. 7–8 | UN Charter 1945, 111 articles, P5 veto as power recognition, Security Council/Assembly/Secretariat/ICJ, Article 42, prohibition of unilateral force; membership 51 to 191 by author's 2005 vantage point | Section 3 |
| pp. 8–9 | Cold War veto periods (USSR 106 in 1946–65; US 68 in 1971–90), Korean exception, blocs, decolonization, Kuwait 1990, Rwanda/Yugoslavia, Iraq 2003 and legal legitimacy | Section 3, chronology accurately qualified |
| pp. 9–10 | ICJ's inter-state jurisdiction versus Nuremberg/ICTY/1998 Rome Statute/ICC 2002; domestic complementarity; specialized functional agencies | Section 3, ICJ/ICC exam distinction, print revision comparison |
| pp. 10–11 | First, Second and Third Internationals; 1914 socialist collapse; Comintern subjected to Soviet priorities; Mongolia as exception; 1943 dissolution | Section 4; state-versus-class paradox |
| pp. 10–11 | NGOs and transnational associations; ICRC 1949 rules, humanitarian neutrality, new humanitarianism exemplified by MSF; internal wars and civilians | Section 4, contrast rather than false equivalence |
| pp. 11–12 | Boutros-Ghali's 1992 statement, states still foundation stone, 1921 Lange bridge, world networks/global civil society and continuing power of sovereign states | Section 5 and conceptual closure |

## Important factual safeguards

- **Source dates belong to the author's period.** Webster's 191 UN members in 2005 and his discussion of the 2003 Iraq invasion are not presented as contemporary counts or new developments in 2026.
- **Cold War veto counts:** Prior HTML asserted a combined **174 Soviet/US vetoes between 1946 and 1990**, but Webster gives **106 Soviet vetoes in 1946–65** and **68 US vetoes in 1971–90**. These ranges do not correspond to one combined measurement period. The replacement preserves each count and explicitly rejects a misleading combined total.
- **League's coercive provisions:** The simplified guide says it 'lacked enforcement mechanisms'. Webster is more precise: Article 16 provided economic, financial and diplomatic sanctions, but there was no League military force or dependable sovereign willingness to enforce them. A blanket claim of *no* provisions would be wrong.
- **Hague versus League versus UN:** The Hague system made optional arbitration available; the League primarily sought procedures and waiting periods before war; the UN's Charter more directly constrained aggression and provided for Security Council enforcement. They are not interchangeable types of 'global unity'.
- **League successes are real:** Its functional health, labour, economic and legal work mattered even when major-power political support failed. The revision retains both records and the evolution from League institutions into UN successors.
- **Two judicial institutions:** The ICJ resolves legal issues between states, whereas the ICC prosecutes certain international crimes by individuals and is complementary to domestic jurisdictions. They are not the same body, nor did the ICC replace the ICJ.
- **NGOs are not simply independent of governments:** The simple guide presents them as independent of state *influence*. Webster makes clear that ICRC access, humanitarian conventions and jurisdiction depend substantially on state consent and diplomatic choices.
- **Socialism and humanitarianism differ:** The Comintern's class-based effort to end the political salience of nations contrasts with voluntary, professional and humanitarian networks that work through or around state systems.
- **Neutrality is a dilemma, not a moral verdict:** Webster contrasts Red Cross operational neutrality with the politically engaged 'new humanitarianism' associated with Médecins Sans Frontières. The sidebar does not caricature either one as unconcerned for victims or indifferent to relief access.
- **Guide-only generic forecasts:** The simplified guide's broadly worded modern discussion of pandemics, populism and equity is not added as if it were Webster's own argument. The primary chapter already discusses environment, the world economy, Internet coordination and global networks.

## Writing and cognitive scaffolding

The main text now teaches the **full causal chain**, using vocabulary from Webster: *internationalism → sovereignty and realism → functional public unions → collective security → state consent → UN legitimacy and veto → civil society*. Technical terms are dotted-underlined **once** and explained through the reusable popover behavior from PR #17. A reader can understand the argument without opening a popup; popups clarify specialist vocabulary only.

The chapter's original four anchor areas are preserved conceptually: `s1` pre-1914, `s2` League, `s3` UN, `s4` beyond the state. A new `s5` explicitly closes Webster's argument. The final `revision` marker, `src-main`/`src-side` division, six standard note categories and global print engine are retained.

## Popup, sidebar, revision: semantic duplication audit

**Popups:** 16 first-meaningful-use academic terms: *internationalism; sovereignty; realist view; international public unions; international humanitarian law; codification; arbitration; collective security; sanctions; veto; peacekeeping; complementarity; socialist internationalism; non-governmental organizations; humanitarian neutrality; global civil society*. All 16 appear **once** as dotted-underlined buttons, with corresponding 16-row **print-safe revision glossary**.

**Sidebars:** 12 passage-linked cards, all six semantic categories. Exactly one pure definition card, **multilateral convention**, has *no popup*. The other 11 cards perform teaching operations different from their nearby paragraphs:

| Card | Distinct learning operation; why it survives |
| --- | --- |
| Three levels of internationalist ambition | **Classification**: identify how far a particular institution goes beyond voluntary cooperation |
| When is agreement easiest? | **Application**: predict when national security concerns block otherwise useful standards |
| Multilateral convention | Defines an essential related term not covered by any popup |
| Evaluate the League by task | **Exam comparison**: choose examples that expose distinct records of success and failure |
| Did the League outlaw all war? | **Misconception test**: reject a tempting but false interpretation of its Covenant |
| Veto: a design trade-off | **Counterfactual**: consider why a veto might secure major-power membership at the price of constraint |
| Test a veto-count comparison | **Numeracy and source-critical check**: verify that historical counts use comparable time windows |
| ICJ is not ICC | **Institutional discrimination**: avoid confusing two courts with different jurisdiction |
| Two routes beyond national borders | **Paired memory paths**: class internationalism versus practical humanitarian aid |
| Neutrality and advocacy: no false binary | **Interpretive caution**: avoid treating distinct methods as simple goodness versus badness |
| Complete the bridge | **Memory chain**: reconstruct argument from shared needs to binding rules and renewed state limits |
| What counts as international authority? | **Analytical distinction**: separate legal legitimacy, consent and coercive capacity |

**Revision:** The terminology glossary is deliberately kept as the print reference, outside the main notes. The short synthesis, League-versus-UN distinction table and evidence grid are **retrieval tools** and do not duplicate long paragraphs or sidebars. With revision excluded from print, this intentionally repeats the agreed Chapter 01 limitation: popup meanings aren't printed separately, although terms and explanations of causal roles remain in the main narrative.

**Required release checks:** verify 16 unique popups and 16 print glossary rows; preserve stable s1–s4 keys and revision boundary; 12 sidebar learning cards across all six categories; no `data-kind="def"` sidebar title equal to a popup; exact derived HTML replacement; PWA service worker content hash; source↔generated parity; desktop/mobile interaction tests; accessible keyboard/touch; automated print and screenshot gates. This is an editorial update, not a page-fitting exercise; do not alter the compositor or shrink type.
