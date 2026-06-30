import json, os, sys
sys.path.insert(0, 'src')
from handbook_rs.llm.client import chat

ont = json.load(open('out/ontology.json')); by_id = {n['id']: n for n in ont['nodes']}
reps = ['area-estimation','sample-based-estimators','ground-survey-estimators','estimator','statistical-survey','area-frame']
concept_block = "\n".join(f"- {r} ({by_id[r]['name']['en']}): {by_id[r]['definition']['en']}" for r in reps if r in by_id)

REFS = """[R1] Olofsson, Foody, Herold, Stehman, Woodcock, Wulder (2014). "Good practices for estimating area and assessing accuracy of land change." Remote Sensing of Environment 148:42-57. doi:10.1016/j.rse.2014.02.015 (FAO-endorsed standard).
[R2] Gallego (2004). "Remote sensing and land cover area estimation." Int. J. Remote Sensing 25(15):3019-3047. doi:10.1080/01431160310001619607.
[R3] Skakun et al. (2025). "The impact of map accuracy on area estimation with remotely sensed data within the stratified estimator." Remote Sensing of Environment. doi:10.1016/j.rse.2025.114805.
[R4] Song et al. (2017). "National-scale soybean mapping and area estimation in the United States." Remote Sensing of Environment 190. doi:10.1016/j.rse.2017.01.008.
[R5] Chhikara (1984). "Effect of mixed (boundary) pixels on crop proportion estimation." Remote Sensing of Environment. doi:10.1016/0034-4257(84)90016-6.
[R6] "Regression coefficient estimation from remote sensing maps" (2024). arXiv:2407.13659."""

EVIDENCE = """VERIFIED RESEARCH FINDINGS (sourced above):
- Pixel-counting mapped area is BIASED (class-dependent classification errors) [R1,R2].
- Remedy: DESIGN-BASED, error-matrix-adjusted area estimator: a probability reference sample builds a confusion matrix; mapped areas are rescaled by reference proportions -> approximately UNBIASED area with standard error and confidence interval [R1].
- SAMPLING: stratified random sampling, strata = map classes; allocation reflects target precision (good-practice triad sampling/response/analysis) [R1].
- Map quality drives EFFICIENCY: better maps cut sample size 20-40% for a target CV; design-based stays unbiased with imperfect maps but precision suffers [R1,R3].
- Mixed/boundary pixels bias crop-proportion estimates; regression/sub-pixel mitigate [R5].
- Modern: regression / prediction-powered estimators combine map predictions with a small probability sample to tighten CIs without bias [R6]."""

sys_p = ("You are a bilingual (EN/ES) scientific editor building a 'documentary brain' for a learning theme "
         "in a course on Remote Sensing for Agricultural Statistics. The UN Handbook is the backbone; deep "
         "research is ADDITIVE and must cite ONLY the provided verified references by their [Rn] tag. Never "
         "invent references. Output strict JSON only.")
user = f"""THEME: Area Estimation from Samples.

HANDBOOK CONCEPTS (backbone):
{concept_block}

{EVIDENCE}

REFERENCES (cite ONLY these as [Rn]):
{REFS}

Produce JSON:
{{"brain_en":"<500-700 word markdown: overview; design-based estimator vs biased pixel-counting; stratified sampling good practice; how it grounds the Handbook concepts; what GAP it fills; cite [Rn]>",
"brain_es":"<same in natural Spanish>",
"enrich":[{{"id":"area-estimation","disambiguation_en":"<1 sentence>","enrich_en":"<=45 words extra scientific layer, cite [Rn]>","enrich_es":"<same Spanish>","refs":["R1","R2"]}}]}}
Include enrich entries for area-estimation, sample-based-estimators, and estimator."""

res = chat(sys_p, user, json_mode=True, max_tokens=6000)
d = res.json()
os.makedirs('out/brains', exist_ok=True)
md = "# Area Estimation from Samples / Estimacion de Areas por Muestras\n\n" + d['brain_en'] + "\n\n---\n\n" + d['brain_es'] + "\n\n## Referencias verificadas\n" + REFS
open('out/brains/area-estimation-from-samples.md', 'w').write(md)
print("=== BRAIN EN (inicio) ===")
print(d['brain_en'][:780])
print("\n=== ENRIQUECIMIENTO ===")
for e in d['enrich']:
    print("\n* " + e['id'])
    print("  desambig: " + e.get('disambiguation_en', ''))
    print("  +EN: " + e['enrich_en'] + "  " + str(e.get('refs')))
    print("  +ES: " + e['enrich_es'][:140])
print("\nguardado: out/brains/area-estimation-from-samples.md (" + str(len(md)) + " chars)")
