# Curriculum comparison matrix v2 (round 2) - 2026-10-24
Same rubric as 30_curriculum_matrix.md (0-3 per skill; weights DS&A 1, Systems/C++ 1.5, Maths 1, Graphics 1, AI/ML 1.5, Game-specific 1.5, Team/placement 1, Research 1; max 28.5). Evidence: 01b (ISSE), 14/15/16 (Aizu), 23 (TH Koeln), 24 (h_da), 25 (DIT), 41 (DigiPen, Abertay). Scores are my judgement from official module lists; "(a)" = assumed from standard CS curriculum, NOT verified module-by-module.

| Skill (weight) | ISSE | Aizu | Abertay CGT | DigiPen RTIS | h_da A&G Tech | DIT AI | TH Koeln GP |
|---|---|---|---|---|---|---|---|
| DS&A (1) | 3 | 3 (a) | 3 | 3 | 2 (1 module, game-focused) | 3 | 1 |
| Systems / C++ / memory (1.5) | 2 (OS, arch; Python in yr 1; C++ unverified) | 2 (C++ course PL04 confirmed; OS/arch (a)) | 3 (C++, HW arch & OS, engine dev) | 3 (C/C++, low-level, parallel GPU) | 2 (engines, C++/DirectX mentioned) | 1 (OS & networks only) | 2 (arch, OS, engines) |
| Maths (1) | 3 | 3 (MA01-07, signals) | 2 (applied maths 1/2/4) | 3 | 1 | 3 | 1 |
| Graphics / real-time (1) | 2 | 3 (OpenGL, GLSL, physics anim, Unity/VR) | 3 (graphics + shaders) | 3 | 3 | 0 | 3 |
| AI / ML / RL (1.5) | 2 | 2 (AIMA-style AI incl. language modelling; ML course unverified) | 2 (1 module: BT, FSM, RL, NN) | 3 (AI for games + ML + AI/ML specialisation) | 2 (AI & behaviour module, generative AI) | 3 (ML, DL, NLP, CV, robotics) | 1 |
| Game-specific (1.5) | 2 (3 if ICE lab) | 1 (VR/Unity, no game-AI course seen) | 3 | 3 | 3 | 0 | 3 |
| Team / placement (1) | 3 | 2 (group projects, internships encouraged) | 3 | 3 | 3 (30 CP placement + projects) | 3 (30 ECTS internship) | 3 |
| Research / thesis (1) | 3 | 3 (lab + thesis) | 2 | 1 | 2 | 2 | 1 |
| **Weighted /28.5** | **23 (81%)** | **21.5 (75%)** | **25 (88%)** | **26.5 (93%)** | **21.5 (75%)** | **17 (60%)** | **17 (60%)** |

(v1 scores kept: ISSE 23, UWA 17.5, THI 15, Deakin 14, AIE 15.)

## What the curriculum comparison says
1. DigiPen (93%) > Abertay (88%) > ISSE (81%) > Aizu = h_da (75%) > DIT = TH Koeln (60%) on fit to "systems-level gameplay/AI programmer". But DigiPen costs ~Rs 2.8 crore and Abertay ~Rs 1.2-1.4 crore: they are the "ideal curriculum, wrong price" options for a loan-funded student.
2. Among the realistic-price options (<= Rs 90 lakh) ISSE is the best by curriculum score, with Aizu close behind (75%) at ~Rs 50 lakh and h_da (75%) at ~Rs 62-80 lakh. The ISSE-vs-Aizu gap (6 points, ~1.5 skills) is within my scoring error: ISSE's edge is the game-AI lab and Osaka/Kyoto; Aizu's edge is C++/graphics/VR modules and cost. Both must be topped up by self-study of C++ and RL.
3. DIT/THI-style AI degrees give the best generic AI (employability for "applied AI") but nothing on games/graphics/C++.
4. h_da is the only German option with both a mandatory game-AI-ish module and an embedded 30-CP placement, but it is a B.A. with thin maths.
5. All scores for Aizu marked (a) must be verified by reading the 2026 course catalog (cached at agent-tools/839e5c60-...txt and web-ext.u-aizu.ac.jp/official/curriculum/syllabus/2026_1_E_000.html).

## Caveat on method
Counting modules is not measuring teaching quality. Lab/advisor quality (ICE lab at ISSE; Aizu CG/VR labs), peers, and what he builds are bigger drivers than the module list. Scores reflect coverage, not depth.
