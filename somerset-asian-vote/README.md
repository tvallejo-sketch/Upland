# How Asian American voters in Somerset County, NJ voted (2020, 2024, 2025)

Election returns do not record race, so these are **statistical estimates** made with
ecological inference (EI): each town's vote is compared with its racial makeup.

## Estimates (Asian American voters, Somerset County)

| Election | Democrat | Republican | D margin (90% interval) |
|---|---|---|---|
| 2020 President: Biden vs. Trump | ~70% | ~27% | D+43 (D+8 to D+74) |
| 2024 President: Harris vs. Trump | ~65% | ~28% | D+37 (D+2 to D+69) |
| 2025 Governor: Sherrill vs. Ciattarelli | ~73% | ~27% | D+46 (D+12 to D+75) |

For comparison, the model puts white voters at roughly even in all three elections
(D+8, D+2 and D+1). The county overall was D+21.4 in 2020, D+14.3 in 2024 and D+19.5 in 2025.

**Reading it:** Asian American voters in Somerset backed Democrats clearly in all three elections.
The point estimates show a modest move toward Trump in 2024 (about 6 points on margin) and a
rebound for Sherrill in 2025. The intervals are wide, though: with only 21 towns,
the 2020→2024 shift (−6, 90% interval −19 to +7) and the 2024→2025 shift (+9, −21 to +42)
are **not statistically distinguishable from zero**.

Raw town results tell the same story. In the towns with the largest Asian shares of eligible voters
(Montgomery 32%, Franklin 21%, Green Brook 20%, Bridgewater 19%, Warren 18%, Hillsborough 17%,
Bernards 16%), the 2020→2024 swing to Trump was about 3–9 points, close to the county's 7.
Most of them moved back toward the Democrat in 2025.

## Method

- **Votes:** NJ Division of Elections official municipal results (`data/*.pdf`).
- **Demographics:** Census citizen voting-age population (CVAP) special tabulation, 2019–2023 ACS,
  by municipality (`data/som_mcd.csv`). Asian = Asian alone + Asian & White.
- **Model:** PyEI R×C multinomial-Dirichlet. Groups: Asian, White, Black, Hispanic, Other.
  Outcomes: Dem, Rep, other candidates, did not vote. Shares are computed among voters
  (`scripts/ei.py`, results in `data/ei_results.csv`).
- `scripts/build.py` parses the PDFs and merges them with CVAP into `data/somerset_muni.csv`.

## Limitations

- **Only 21 units.** With so few towns the intervals are wide. The sampler's effective sample size was low for
  some parameters, and some side estimates are implausible (e.g. ~90% Asian turnout in 2020).
  Treat the numbers as rough.
- **Not split by origin.** The model can't separate Indian, Chinese and other Asian American voters.
- **Ecological fallacy.** The model assumes Asian voters behave similarly from town to town after
  accounting for other groups. A simple linear (Goodman) regression on the same data gives
  impossible margins above 100%, a sign of this bias, so only the bounded Bayesian model is reported.
- **Better data would help:** precinct-level returns (~200 districts) would sharpen the estimates a lot.
  Somerset's precinct results are on the county's Clarity site, which blocks automated downloads.
  Block-group CVAP for that follow-up is already in `data/som_bg.csv`.
