# Scenario: APU (Malaysia) study, then return to India for a job

Prepared 18 Nov 2026. **Separate risk stream** from the QUT files. Builds an APU-sized loan (tuition + KL living + visa/registration), then asks the same question as `QUT_return_to_India_scenario.md`: **can a mid Rs 10-12 LPA India salary cover the EMI plus metro living?** FX: **1 MYR = Rs 22.83** (18 Nov 2026); **1 AUD = Rs 66.82** (side-by-side only). Working: `calc_apu_india_return.py`.

## 1. What this scenario is testing

He does a 3-year IT/CS degree at APU (Bukit Jalil, KL), starting ~Jul 2027, finishes ~mid-2030, returns to India, finds a metro IT job about 6 months later (~Jan 2031), and the education-loan EMI starts ~Jul 2031 after a 12-month grace. Unlike the QUT Brisbane plan, **KL living is in the loan** (no uncle covering board in Malaysia).

## 2. APU cost stack (what gets borrowed)

| Piece | RM | Rs | A$ |
|---|---:|---:|---:|
| Tuition 6 semesters + 6% SST (semester-payment path) | 120,204 | 27,44,257 | 41,069 |
| KL living 36 mo @ RM 1800/mo (APU guide mid) | 64,800 | 14,79,384 | 22,140 |
| One-offs (Stage1/2, registration, deposits) | 12,524 | 2,85,923 | 4,279 |
| Student visa renewals (years 2 and 3) | 2,600 | 59,358 | 888 |
| **Total drawn (before loan interest)** | **200,128** | **45,68,922** | **68,377** |

Published full-payment tuition (before SST) is RM34,900 + RM36,100 + RM37,500 = RM108,500. This model uses the **semester-payment** amounts (slightly higher) + **6% SST**, matching how draws usually land. DMU dual-degree uplift (GBP 450/level) is **not** included. Library deposit and personal bond are cash outlays (partly refundable later).

### Semester tuition used (incl. SST)

| Sem | Level | RM incl. SST | Rs |
|---|---|---:|---:|
| L1 S1 | | 19,292 | 4,40,436 |
| L1 S2 | | 19,292 | 4,40,436 |
| L2 S1 | | 20,034 | 4,57,376 |
| L2 S2 | | 20,034 | 4,57,376 |
| L3 S1 | | 20,776 | 4,74,316 |
| L3 S2 | | 20,776 | 4,74,316 |

## 3. Loan side after interest (same terms as QUT model)

| Item | Value |
|---|---|
| Rate | 9% p.a., capitalised each year (mid-year draws get half a year of interest) |
| Moratorium | 3 years study + 12 months grace; first EMI ~Jul 2031 |
| Tenure | 15 years (180 monthly EMIs) |

| | Rs | A$ |
|---|---:|---:|
| Total drawn | 45,68,922 | 68,377 |
| Interest added before first EMI | 12,71,063 | 19,022 |
| Balance when EMIs start | 58,39,985 | 87,399 |
| **Minimum monthly EMI** | **59,233** | **886** |
| Minimum yearly repayment | 7,10,796 | 10,637 |
| Total repaid over 15 years | 1,06,61,943 | 159,562 |

### Balance build-up

| Year | Phase | Drawn Rs | Interest Rs | Closing Rs |
|---|---|---:|---:|---:|
| 1 | Study yr 1 | 16,59,924 | 1,18,478 | 17,78,402 |
| 2 | Study yr 2 | 14,37,559 | 2,57,759 | 34,73,720 |
| 3 | Study yr 3 | 14,71,439 | 4,12,625 | 53,57,784 |
| 4 | Grace (12 mo) | 0 | 4,82,201 | 58,39,985 |

## 4. India income and living (same as QUT India-return stream)

| Item | Assumption |
|---|---|
| Location | Metro IT hub, shared housing |
| Starting CTC | Rs 10-12 LPA (base Rs 11 LPA) |
| Tax | New regime; ~zero income tax at 10-12 LPA |
| Living | Modest bachelor all-in **Rs 27,000/mo** |

## 5. Affordability: salary vs EMI

EMI is **Rs 59,233/mo** (~Rs 7.11 lakh/yr). That is far below the QUT EMI (Rs 1,41,950), but still a large cut of a fresher salary.

| CTC | Take-home /mo | Living /mo | EMI /mo | **Gap /mo** | Gap /yr | Can he self-fund? |
|---:|---:|---:|---:|---:|---:|---|
| Rs 10 LPA (Low of band) | 78,000 | 27,000 | 59,233 | **-8,233** | -98,796 | **No** |
| Rs 11 LPA (Mid (base)) | 81,000 | 27,000 | 59,233 | **-5,233** | -62,796 | **No** |
| Rs 12 LPA (High of band) | 90,000 | 27,000 | 59,233 | **3,767** | 45,204 | **Yes (thin)** |

**Break-even (self-funded):** about **Rs 86,233/mo in hand** (EMI + living) ~= **Rs 11.05 LPA CTC** under a simple new-regime + PF model.

## 6. Monthly snapshot at Rs 11 LPA (base)

| | Rs / month |
|---|---:|
| Take-home | 81,000 |
| Metro living | 27,000 |
| **EMI (minimum)** | **59,233** |
| **Left / shortfall** | **-5,233** |

After living he has about **Rs 54,000** left. The EMI is **Rs 59,233**, so the hole is about **Rs 5,233/mo** (**Rs 62,796/yr**) unless family/co-applicant covers it or the loan is smaller.

## 7. How this compares with QUT -> India

| | APU -> India (this file) | QUT -> India |
|---|---|---|
| Study living in loan? | Yes (KL, ~RM1,800/mo) | No (uncle covers Brisbane board) |
| Total drawn (approx) | Rs 45,68,922 | Rs ~1.10 crore |
| Monthly EMI | **Rs 59,233** | **Rs 1,41,950** |
| Gap at Rs 11 LPA + living | **Rs -5,233/mo** | **Rs ~-87,950/mo** |
| Self-fund on Rs 10-12 LPA? | See table above | No |

APU is a much smaller rupee loan than QUT, so return-to-India is **far less damaging**. It can still be tight at the low end of the salary band once metro living is paid.

## 8. Risks this scenario highlights

- **RM/INR moves:** fees and living are in ringgit; a weaker rupee raises the INR loan size at drawdown.
- **Semester vs full payment:** semester path + SST costs more than paying each year in full.
- **Living overrun:** RM1,800/mo is APU's mid guide; single rooms and eating out push this up.
- **Job timing / salary:** below ~break-even CTC, co-applicant carries the gap.
- **Degree recognition / market:** India recruiters may weight a Malaysian private degree differently than a QUT BIT; salary outcomes are an assumption, not a placement guarantee.

## 9. One-line takeaway

APU + return to India on **Rs 10-12 LPA** still leaves a repayment gap at the mid point (~**Rs 5,233/mo** short at Rs 11 LPA), but the EMI (**Rs 59,233**) is about **2.4x smaller** than the QUT path, so family backup needed is much lighter.
