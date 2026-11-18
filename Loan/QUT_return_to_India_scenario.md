# Scenario: QUT study, then return to India for a job

Prepared 18 Nov 2026. **Separate risk stream** from `QUT_loan_fact_check_report.md` (that file assumes he stays and works in Brisbane). Same QUT loan and EMI; only the income and living side change. FX for reference only: 1 A$ = Rs 66.82. Working: `calc_qut_india_return.py`.

## 1. What this scenario is testing

He finishes QUT (~Jun 2030), returns to India, finds a metro IT job about 6 months later (~Jan 2031), and the education-loan EMI still starts on schedule (~Jul 2031). Question: **can a mid Rs 10-12 LPA India salary cover the minimum EMI plus metro living?**

## 2. Loan side (unchanged from Australia base case)

| | Rs | A$ |
|---|---:|---:|
| Total drawn for QUT | 1,09,87,895 | 164,440 |
| Balance when EMIs start (Jul 2031) | 1,39,95,368 | 209,449 |
| **Minimum monthly EMI** | **1,41,950** | **2,124** |
| Minimum yearly repayment | 17,03,404 | 25,492 |

The loan is an **INR** obligation. Earning in India does not shrink the EMI. It removes the AUD salary that was carrying the repayment in the Australia plan.

## 3. India income and living (assumptions)

| Item | Assumption | Tag |
|---|---|---|
| Location | Metro IT hub (Bengaluru / Hyderabad / Pune / Mumbai style), shared housing | [A] |
| Starting CTC | Rs 10-12 LPA mid band (base Rs 11 LPA) | [A] |
| Tax | New regime; ~zero income tax at 10-12 LPA after standard deduction + 87A rebate (FY 2025-26 rules held flat) | [P]/[A] |
| Take-home | After employee PF (~12% of basic) and professional tax; employer PF/gratuity not in hand | [A] |
| Living | Modest bachelor shared PG/flat all-in **Rs 27,000/mo** | [E] |
| Job start | ~Jan 2031; first EMI ~Jul 2031 (same timeline as Australia file) | [A] |

### Living split (monthly)

| Item | Rs/mo |
|---|---:|
| Shared PG / co-living with meals (or share of flat + food) | 12,000 |
| Extra food / eating out | 4,000 |
| Local transport (metro / bus / bike) | 3,000 |
| Phone + internet | 1,000 |
| Personal, laundry, misc | 3,000 |
| Health insurance / medical buffer | 1,500 |
| Family visit / contingency buffer | 2,500 |
| **Total living** | **27,000** |

## 4. Affordability: salary vs EMI (the stress test)

EMI alone is **Rs 1,41,950/mo** (~Rs 17.03 lakh/yr). That is already more than a full Rs 12 LPA CTC before living costs.

| CTC | Take-home /mo | Living /mo | EMI /mo | **Gap /mo** | Gap /yr | Can he self-fund? |
|---:|---:|---:|---:|---:|---:|---|
| Rs 10 LPA (Low of band) | 78,000 | 27,000 | 1,41,950 | **-90,950** | -10,91,404 | **No** |
| Rs 11 LPA (Mid (base)) | 81,000 | 27,000 | 1,41,950 | **-87,950** | -10,55,404 | **No** |
| Rs 12 LPA (High of band) | 90,000 | 27,000 | 1,41,950 | **-78,950** | -9,47,404 | **No** |

**Break-even (self-funded):** he needs about **Rs 1,68,950/mo in hand** (EMI + living). That is roughly **Rs 25.00 LPA CTC** under a simple new-regime + PF model (~Rs 25 LPA). A normal fresher Rs 10-12 LPA offer is nowhere near this.

## 5. Monthly snapshot at Rs 11 LPA (base)

| | Rs / month |
|---|---:|
| Take-home | 81,000 |
| Metro living | 27,000 |
| **EMI (minimum)** | **1,41,950** |
| **Shortfall** | **-87,950** |

After living costs he has about **Rs 54,000** left for everything else. The EMI is **Rs 1,41,950**. The hole is about **Rs 87,950/mo** (**Rs 10,55,404/yr**), which a co-applicant or family would have to cover unless the loan is prepaid or restructured.

## 6. How this compares with the Australia plan

| | Work in Brisbane (main fact-check) | Return to India (this scenario) |
|---|---|---|
| Monthly EMI | Rs 1,41,950 / A$2,124 | Same EMI in Rs |
| Income currency | AUD salary | INR salary |
| Year-1 leftover after tax, living, EMI | ~A$406/yr (tight but near break-even at A$70k) | **Large monthly shortfall at Rs 10-12 LPA** |
| Who realistically pays the EMI? | Mostly him, if the job arrives on time | Mostly co-applicant / family for many years |

Staying in Australia was already tight. Returning to India on a normal graduate salary turns the same loan into a **family cashflow problem**, not a graduate cashflow problem.

## 7. Risks this scenario highlights

- **Scale mismatch:** QUT costs were priced in AUD; a mid India graduate salary cannot service the INR EMI.
- **Co-applicant exposure:** banks will expect the Indian co-applicant to keep paying if he cannot.
- **Career path:** even strong India rises (e.g. to Rs 20-25 LPA in a few years) still leave a multi-year gap versus EMI + living.
- **No AUD earnings hedge:** in Australia, a weaker INR makes the EMI easier in AUD terms; that relief disappears if he earns only INR.
- **Not a reason to skip QUT by itself** - it is a reason to treat **return-to-India without family backup** as a high-risk outcome, and to plan prepaid years / collateral / co-applicant capacity before drawing the loan.

## 8. One-line takeaway

If he studies at QUT and returns to India on a **Rs 10-12 LPA** metro job, the minimum EMI of **Rs 1,41,950/mo** alone exceeds take-home; with shared-rent living the shortfall is about **Rs 87,950/mo**. This path only works if family/co-applicant can carry most of the repayment for years, or if a large part of the loan is never drawn / is prepaid.
