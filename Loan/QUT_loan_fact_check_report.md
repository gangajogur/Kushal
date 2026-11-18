# QUT loan fact-check (for Kushal)

Prepared 13 Nov 2026. Short planning sheet: **Rs (INR)** and **A$ (AUD)** side by side. **1 A$ = Rs 66.82** (held flat). Tags: **[P]** published, **[E]** market estimate, **[A]** assumption. Working: `calc_qut_report.py`.

## 1. Bottom line (base case: full loan)

| | Rs | A$ |
|---|---:|---:|
| Total drawn (tuition + visa + OSHC + personal) | 1,09,87,895 | 164,440 |
| Balance when EMIs start (Jul 2031) | 1,39,95,368 | 209,449 |
| **Minimum monthly EMI (15 years)** | **1,41,950** | **2,124** |
| Minimum yearly repayment | 17,03,404 | 25,492 |
| Total repaid over 15 years | 2,55,51,062 | 382,386 |

In plain terms: he borrows about **A$164,440** (Rs 1,09,87,895) and repays about **A$382,386** (Rs 2,55,51,062), roughly **2.3x** what was drawn. On a starting salary of **A$70,000**, take-home is about **A$56,812**; after shared-rent living (**A$30,914**) and the EMI (**A$25,492**/yr), **about A$406 a year is left** in repayment year 1 (~A$34/month). That is essentially break-even: one late rent increase or a weaker starting salary tips it negative.

## 1a. What sits behind those numbers

### Timeline

| When | What |
|---|---|
| Jul 2027 | Starts QUT; first semester draw (tuition + personal) + visa + OSHC |
| Every 6 months to Jan 2030 | Next semester tuition + personal drawn |
| ~Jun 2030 | Degree ends. No EMI yet (grace) |
| ~Jan 2031 | Assumed first full-time job (~6 months after finishing) |
| Jul 2031 | Grace ends. **First EMI due.** Then 180 monthly payments to Jun 2046 |

### Where the A$164,440 loan comes from

| Piece | Rs | A$ | Share |
|---|---:|---:|---:|
| Tuition (6 semesters, +3%/yr after 2027) | 97,89,812 | 146,510 | 89% |
| Personal while studying (A$350/mo x 36) | 8,41,932 | 12,600 | 8% |
| OSHC (~38 months) | 1,89,101 | 2,830 | 2% |
| Student visa fee | 1,67,050 | 2,500 | 2% |
| **Total drawn** | **1,09,87,895** | **164,440** | 100% |

Rent and food during study are **not** in the loan (covered by uncle). Published 2027 fee is A$46,700/yr; later years use +3%/yr because QUT only publishes the current year.

### How the EMI is derived (3 steps)

| Step | Result |
|---|---|
| 1. Draw over 3 years, pay nothing for study + 12-month grace | Interest capitalised each July at 9% (mid-year draws get half a year of interest) |
| 2. Balance at first EMI (Jul 2031) | **A$209,449** = A$164,440 drawn + A$45,009 interest |
| 3. Standard reducing-balance EMI over 180 months at 9%/12 | **A$2,124/mo** (Rs 1,41,950) |

Same EMI formula as the WeMakeScholars example table; only the principal and draw timing differ. Lender sanction letters can differ (simple vs compounding interest, floating rate, tenure cap).

### Monthly snapshot, repayment year 1 (Jul 2031-Jun 2032)

| | Per month A$ | Per year A$ | Per year Rs |
|---|---:|---:|---:|
| Gross salary | 5,833 | 70,000 | 46,77,400 |
| Take-home (after tax + Medicare) | 4,734 | 56,812 | 37,96,178 |
| Shared-rent living | 2,576 | 30,914 | 20,65,647 |
| **EMI (minimum)** | **2,124** | **25,492** | **17,03,404** |
| **Left over** | **34** | **406** | **27,127** |

Living band used (today's prices, then inflated ~4.5 years at 3.5% to mid-2031):

| Item | Today A$/yr |
|---|---:|
| Shared room + bills (A$265/wk) | 13,780 |
| Groceries / food (A$110/wk) | 5,720 |
| Transport (QLD 50c fares + occasional trips) | 400 |
| Phone (A$40/mo) | 480 |
| Eating out / social / leisure (A$200/mo) | 2,400 |
| Clothing, personal care, misc | 1,200 |
| OVHC / private health (India has no Medicare reciprocal deal) | 1,000 |
| One trip home to India per year | 1,500 |
| **Today total** | **26,480** |
| **Inflated to Jul 2031** | **30,914** |

## 2. Facts used

| Item | Value | Tag |
|---|---|---|
| Course | Bachelor of IT (IN01), Computer Science, Gardens Point; Jul 2027 -> ~Jun 2030; 6 semesters | [P] QUT |
| Tuition 2027 | A$46,700/yr (A$23,350/sem). QUT publishes only the current year and says fees rise annually | [P] QUT 2027 International Quick Guide |
| Tuition 2028-2030 | +3%/yr assumed -> A$48,101 / A$49,544 / A$51,030 per year | [A] |
| Student visa fee | A$2,500 (from 1 Jul 2026) | [P] Study Australia |
| OSHC (~38 months, single) | A$2,830 (Medibank Comprehensive, Nov 2026 rate card) | [P] Medibank |
| Personal while studying | A$2,100/semester (~A$350/mo: phone, transport, leisure, books). Rent + food covered by uncle | [A] |
| Scholarship | None | [A] |
| Loan | 9% p.a., interest capitalised each Jul; no payments for 3 yrs study + 12 mo grace; 180 EMIs from Jul 2031 | [A] lender terms vary |
| First job | ~Jan 2031 (6 months after finishing); first EMI Jul 2031 | [A] |
| Starting salary | A$70,000. QILT 2025: international undergrad median A$70,000; Computing & IS international median A$65,000 | [P]/[A] |
| Salary growth | +7%, +7%, +5%, +5%, then +3.5%/yr | [A] |
| Living after moving out | Today's shared-rent band A$26,480/yr (room+bills A$265/wk, food A$110/wk, extras), inflated ~4.5 yrs at 3.5% to **A$30,914/yr** for Jul 2031, then +3.5%/yr | [E]/[A] |
| Tax | Stage 3 resident rates (16%/30%/37%/45%) + Medicare 2% + LITO. Employer super on top, not counted | [P] ATO |

## 3. What goes into the loan

| Draw | When | Item | Rs | A$ |
|---|---|---|---:|---:|
| Start | Jul 2027 | Student visa fee | 1,67,050 | 2,500 |
| Start | Jul 2027 | OSHC | 1,89,101 | 2,830 |
| Sem 1 | +0 mo (S2 2027) | Tuition | 15,60,247 | 23,350 |
| Sem 1 | +0 mo (S2 2027) | Personal | 1,40,322 | 2,100 |
| Sem 2 | +6 mo (S1 2028) | Tuition | 16,07,054 | 24,050 |
| Sem 2 | +6 mo (S1 2028) | Personal | 1,40,322 | 2,100 |
| Sem 3 | +12 mo (S2 2028) | Tuition | 16,07,054 | 24,050 |
| Sem 3 | +12 mo (S2 2028) | Personal | 1,40,322 | 2,100 |
| Sem 4 | +18 mo (S1 2029) | Tuition | 16,55,266 | 24,772 |
| Sem 4 | +18 mo (S1 2029) | Personal | 1,40,322 | 2,100 |
| Sem 5 | +24 mo (S2 2029) | Tuition | 16,55,266 | 24,772 |
| Sem 5 | +24 mo (S2 2029) | Personal | 1,40,322 | 2,100 |
| Sem 6 | +30 mo (S1 2030) | Tuition | 17,04,924 | 25,515 |
| Sem 6 | +30 mo (S1 2030) | Personal | 1,40,322 | 2,100 |
| **Total tuition** | | | **97,89,812** | **146,510** |
| **Total personal** | | | **8,41,932** | **12,600** |
| **Total drawn** | | | **1,09,87,895** | **164,440** |

Cash needed **outside** the loan: Temporary Graduate (485) visa fee about **A$5,750** (Rs 3,84,215), plus flights, laptop and setup. Accommodation and food during study are covered by you and are not in these figures.

## 4. Balance before the first payment

Nothing is paid for 4 years. Interest is added each July.

| Year | Phase | Opening A$ | Drawn A$ | Interest A$ | Closing A$ | Closing Rs |
|---|---|---:|---:|---:|---:|---:|
| 1 | Study yr 1 | 0 | 56,930 | 3,947 | 60,877 | 40,67,833 |
| 2 | Study yr 2 | 60,877 | 53,023 | 9,042 | 122,942 | 82,14,967 |
| 3 | Study yr 3 | 122,942 | 54,487 | 14,726 | 192,155 | 1,28,39,788 |
| 4 | Grace (12 mo) | 192,155 | 0 | 17,294 | 209,449 | 1,39,95,368 |

Interest of **A$45,009** (Rs 30,07,474) is added before EMIs start. He starts repaying **A$209,449** - about **1.27x** what was drawn.

## 5. After graduation: salary vs EMI (base case)

**Minimum monthly EMI: Rs 1,41,950 / A$2,124** (fixed for 15 years). Yearly: Rs 17,03,404 / A$25,492.

Living costs in repayment year 1: **A$30,914** (today's shared-rent band A$26,480, inflated to mid-2031).

| Yr | Period | Gross A$ | Take-home A$ | Living A$ | EMI A$ | **Left A$** | Left Rs lakh | Loan bal A$ |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | Jul 2031-Jun 2032 | 70,000 | 56,812 | 30,914 | 25,492 | **406** | 0.3 | 202,526 |
| 2 | Jul 2032-Jun 2033 | 74,900 | 60,144 | 31,996 | 25,492 | **2,656** | 1.8 | 194,953 |
| 3 | Jul 2033-Jun 2034 | 80,143 | 63,709 | 33,115 | 25,492 | **5,101** | 3.4 | 186,671 |
| 4 | Jul 2034-Jun 2035 | 84,150 | 66,434 | 34,274 | 25,492 | **6,667** | 4.5 | 177,611 |
| 5 | Jul 2035-Jun 2036 | 88,358 | 69,295 | 35,474 | 25,492 | **8,329** | 5.6 | 167,701 |
| 6 | Jul 2036-Jun 2037 | 91,450 | 71,398 | 36,716 | 25,492 | **9,190** | 6.1 | 156,862 |
| 7 | Jul 2037-Jun 2038 | 94,651 | 73,575 | 38,001 | 25,492 | **10,081** | 6.7 | 145,006 |
| 8 | Jul 2038-Jun 2039 | 97,964 | 75,827 | 39,331 | 25,492 | **11,004** | 7.4 | 132,038 |
| 9 | Jul 2039-Jun 2040 | 101,392 | 78,159 | 40,707 | 25,492 | **11,959** | 8.0 | 117,853 |
| 10 | Jul 2040-Jun 2041 | 104,941 | 80,572 | 42,132 | 25,492 | **12,948** | 8.7 | 102,338 |

Years 11-15 are omitted for length; the EMI stays fixed while salary and living costs keep rising, so the cushion grows. Full 15-year rows are in `qut_base_case_budget.csv`.

**Break-even:** about **A$69,500** gross covers living + EMI with nothing left. A$70,000 clears that by about **A$500**.

## 6. Summary: if family pays later years in cash

Tuition for those years is **not drawn**. Visa, OSHC and personal spend stay in the loan. Cash cost is tuition only at the inflated fee.

| | Base (borrow all) | Family pays **year 3** | Family pays **years 2 + 3** |
|---|---:|---:|---:|
| Cash paid by family (tuition) | A$0 / Rs 0 | A$50,287 / Rs 33,60,190 | A$99,110 / Rs 66,22,511 |
| Total drawn from loan | A$164,440 / Rs 1,09,87,895 | A$114,153 / Rs 76,27,704 | A$65,330 / Rs 43,65,384 |
| Balance at first EMI | A$209,449 / Rs 1,39,95,368 | A$150,954 / Rs 1,00,86,753 | A$89,052 / Rs 59,50,452 |
| **Monthly EMI** | **A$2,124 / Rs 1,41,950** | **A$1,531 / Rs 1,02,307** | **A$903 / Rs 60,353** |
| Yearly repayment | A$25,492 / Rs 17,03,404 | A$18,373 / Rs 12,27,679 | A$10,839 / Rs 7,24,241 |
| Total repaid (15 yrs) | A$382,386 / Rs 2,55,51,062 | A$275,594 / Rs 1,84,15,182 | A$162,580 / Rs 1,08,63,619 |
| **Left in repayment yr 1** (after tax, living, EMI) | **A$406** | **A$7,525** | **A$15,060** |

Paying year 3 in cash costs the family about **A$50,287** (Rs 33,60,190) and cuts the monthly EMI by about **A$593**. Paying years 2 and 3 costs about **A$99,110** (Rs 66,22,511) and cuts the EMI by about **A$1,221** a month.

## 7. What can go wrong

- **Job timing:** Only about 42% of international Computing & IS graduates are in full-time work 4-6 months after finishing (QILT 2025). A longer job hunt eats the pre-EMI buffer.
- **Salary:** Computing & IS international median is A$65,000, below this A$70,000 base case. At A$65,000, year-1 leftover falls to about A$-2,969.
- **Fee rises:** If fees rise faster than 3%/yr, the loan grows. QUT does not publish future fees.
- **Loan terms:** Floating rates, simple vs compounding interest, a 15-year cap counted from first drawdown, collateral and co-applicant rules all change the EMI. Ask the lender for a sanction-letter quote.
- **FX:** The loan is repaid in rupees. If the rupee weakens against the AUD while he earns in AUD, the EMI gets easier in AUD terms; the opposite hurts.
- **Not in these numbers:** Your food and rent support during study, 485 visa fee, flights, laptop, remittance charges.

## 8. One-line takeaway

At QUT with you covering board, the loan is about **A$164,440**, the **minimum monthly repayment is about A$2,124 (Rs 1,41,950)**, and a **A$70k** graduate job with shared rent leaves only about **A$406/yr** after tax, living and EMI - essentially break-even. Family paying year 3 (or years 2-3) tuition is what makes the cashflow comfortable (EMI falls to about A$1,531 or A$903).
