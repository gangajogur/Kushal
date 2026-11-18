# Rs 1.5 crore education loan: 3-year course, staggered drawdown, no payments until grace period ends

This replaces the simplified model in `repayment_table_1.5cr.md` (that one assumed the full amount drawn on day one and only a 15-month moratorium, copied from the website's example). See `calc_repayment_3yr_course.py` for the working.

## Assumptions (confirmed)

| Item | Value |
|---|---|
| Total loan | Rs 1,50,00,000 (Rs 1.5 crore), drawn as Rs 50 lakh at the start of year 1, 2 and 3 |
| Course | 3 years, no payments |
| Grace period | 12 months after course ends, no payments |
| First EMI | Month 49 (end of the first month after the 4-year moratorium) |
| Interest | 9% p.a., **compounded annually** during the moratorium (months 1-48) |
| Repayment | 15 years, 180 monthly EMIs, reducing balance (monthly rate 9%/12, same formula as the website) |
| FX | 1 AUD = Rs 66.82 (fixed, from `report/FRESH_ASSESSMENT_2026-11-01.md`) |

## Step 1: Balance building up during the 4-year moratorium (nothing paid)

Draw is at the start of the year; interest for the year compounds at the year end.

| Moratorium year | Phase | Opening balance (Rs) | Drawn (Rs) | Interest added (Rs) | Closing balance (Rs) | Closing (AUD) |
|---|---|---:|---:|---:|---:|---:|
| 1 | Course yr 1 | 0 | 50,00,000 | 4,50,000 | 54,50,000 | 81,562 |
| 2 | Course yr 2 | 54,50,000 | 50,00,000 | 9,40,500 | 1,13,90,500 | 170,465 |
| 3 | Course yr 3 | 1,13,90,500 | 50,00,000 | 14,75,145 | 1,78,65,645 | 267,370 |
| 4 | Grace (12 months) | 1,78,65,645 | 0 | 16,07,908 | 1,94,73,553 | 291,433 |

**Principal when EMIs start: Rs 1,94,73,553 (AUD 291,433).** That is Rs 1,50,00,000 drawn + Rs 44,73,553 interest (AUD 66,949) that has been added to the loan, i.e. the loan is 1.30x what was borrowed before the first repayment.

## Step 2: EMI

| | Rs | AUD |
|---|---:|---:|
| **Monthly EMI (180 payments)** | **1,97,514** | **2,956** |
| **Yearly repayment (12 x EMI)** | **23,70,165** | **35,471** |
| Total paid in EMIs | 3,55,52,473 | 532,063 |
| Interest paid during repayment | 1,60,78,920 | 240,630 |
| Total interest on the loan (moratorium + repayment) | 2,05,52,473 | 307,580 |
| Total paid vs Rs 1.5 cr borrowed | 2.37x | |

## Step 3: Yearly repayment table (the yearly minimum you must pay)

Repayment year 1 starts in month 49, i.e. loan year 5. Each row sums 12 EMIs. "Minimum" here means the scheduled EMI total: paying less than this puts the loan in arrears.

| Repayment year | Loan year | Total paid in year (Rs) | AUD | Interest (Rs) | Interest (AUD) | Principal (Rs) | Principal (AUD) | Closing balance (Rs) | Closing (AUD) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 23,70,165 | 35,471 | 17,26,498 | 25,838 | 6,43,667 | 9,633 | 1,88,29,886 | 281,800 |
| 2 | 6 | 23,70,165 | 35,471 | 16,66,118 | 24,934 | 7,04,047 | 10,536 | 1,81,25,840 | 271,264 |
| 3 | 7 | 23,70,165 | 35,471 | 16,00,073 | 23,946 | 7,70,091 | 11,525 | 1,73,55,748 | 259,739 |
| 4 | 8 | 23,70,165 | 35,471 | 15,27,834 | 22,865 | 8,42,331 | 12,606 | 1,65,13,417 | 247,133 |
| 5 | 9 | 23,70,165 | 35,471 | 14,48,817 | 21,682 | 9,21,348 | 13,789 | 1,55,92,069 | 233,344 |
| 6 | 10 | 23,70,165 | 35,471 | 13,62,388 | 20,389 | 10,07,777 | 15,082 | 1,45,84,293 | 218,262 |
| 7 | 11 | 23,70,165 | 35,471 | 12,67,852 | 18,974 | 11,02,313 | 16,497 | 1,34,81,980 | 201,766 |
| 8 | 12 | 23,70,165 | 35,471 | 11,64,447 | 17,427 | 12,05,717 | 18,044 | 1,22,76,262 | 183,721 |
| 9 | 13 | 23,70,165 | 35,471 | 10,51,343 | 15,734 | 13,18,822 | 19,737 | 1,09,57,440 | 163,984 |
| 10 | 14 | 23,70,165 | 35,471 | 9,27,628 | 13,882 | 14,42,537 | 21,588 | 95,14,903 | 142,396 |
| 11 | 15 | 23,70,165 | 35,471 | 7,92,308 | 11,857 | 15,77,857 | 23,614 | 79,37,047 | 118,782 |
| 12 | 16 | 23,70,165 | 35,471 | 6,44,294 | 9,642 | 17,25,870 | 25,829 | 62,11,176 | 92,954 |
| 13 | 17 | 23,70,165 | 35,471 | 4,82,396 | 7,219 | 18,87,769 | 28,252 | 43,23,407 | 64,702 |
| 14 | 18 | 23,70,165 | 35,471 | 3,05,310 | 4,569 | 20,64,855 | 30,902 | 22,58,552 | 33,801 |
| 15 | 19 | 23,70,165 | 35,471 | 1,11,613 | 1,670 | 22,58,552 | 33,801 | 0 | 0 |
| **Total** | | **3,55,52,473** | **532,063** | **1,60,78,920** | **240,630** | **1,94,73,553** | **291,433** | 0 | 0 |

In loan years 1-4 (course and grace) the minimum payment is Rs 0. If he wants to stop the balance growing he could pay the interest during the course (see Step 5), which is optional.

## Step 4: How the assumptions change the answer (9%, 15-year EMIs unless noted)

| Scenario | Principal at first EMI (Rs) | Monthly EMI (Rs) | Monthly EMI (AUD) | Total paid (Rs cr) | Total paid (AUD) |
|---|---:|---:|---:|---:|---:|
| **This analysis**: staggered draws, 4-year moratorium, annual compounding | 1,94,73,553 | 1,97,514 | 2,956 | 3.56 | 532,063 |
| Same, but simple interest (public bank style) | 1,90,50,000 | 1,93,218 | 2,892 | 3.48 | 520,491 |
| Earlier file: full Rs 1.5 cr on day 1, 15-month simple moratorium | 1,66,87,500 | 1,69,256 | 2,533 | 3.05 | 455,942 |
| Annual compounding at 8.15% | 1,90,13,367 | 1,83,352 | 2,744 | 3.30 | 493,914 |
| Annual compounding at 10.00% | 2,00,25,500 | 2,15,195 | 3,221 | 3.87 | 579,693 |
| Annual compounding at 11.00% | 2,05,89,007 | 2,34,014 | 3,502 | 4.21 | 630,388 |

## Step 5: Optional, pay the interest during the course

If the family pays the interest each year during the course and grace period (Rs 0 principal change), the balance does not grow. Interest due at the end of each year on the drawn balance at 9%:

| Year | Balance drawn | Interest to pay at year end (Rs) | AUD |
|---|---:|---:|---:|
| 1 | 50,00,000 | 4,50,000 | 6,735 |
| 2 | 1,00,00,000 | 9,00,000 | 13,469 |
| 3 | 1,50,00,000 | 13,50,000 | 20,204 |
| 4 | 1,50,00,000 | 13,50,000 | 20,204 |

Paying that costs Rs 40,50,000 (AUD 60,611) over 4 years, but the loan then starts repayment at Rs 1.5 cr and the EMI is Rs 1,52,140 (AUD 2,277) a month instead of Rs 1,97,514. Total interest is lower because it stops compounding.

## Caveats

- Planning estimate. Lenders differ on: whether interest is simple or compounded in the moratorium, when it is capitalised, whether the rate floats with the repo rate, processing fees, and whether the grace period is 6 or 12 months. Ask each lender for their sanction letter terms.
- Tranche timing: I assumed draws at the start of each year. Drawing later in each year (e.g. by semester) lowers the accrued interest slightly.
- 15-year tenure counted from the first EMI. Some lenders cap the total tenure (including moratorium) at 15 years, which would leave only 11 EMI years and raise the EMI sharply. Worth checking.
- The loan is repaid in INR, so the AUD column moves with the exchange rate.
- A Rs 1.5 crore loan would normally need collateral and a co-applicant (see `background_checks/wemakescholars/`).
- Section 80E: interest (not principal) is deductible for up to 8 years, per the website.
