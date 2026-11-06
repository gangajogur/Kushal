# Education Loan Repayment Table: Rs 1.5 crore (with AUD equivalent)

Same method and layout as the WeMakeScholars example table (https://www.wemakescholars.com/education-loan#widget-3, Rs 40 lakh at 9% for 15 years). I re-derived their table and matched it to the rupee before scaling up, see `calc_repayment.py`.

## Assumptions

| Item | Value |
|---|---|
| Loan disbursed | Rs 1,50,00,000 (Rs 1.5 crore) = AUD 224,484 |
| Interest rate | 9% p.a., reducing balance (same as website example) |
| Repayment tenure | 15 years (180 monthly EMIs) |
| Moratorium | 15 months, simple interest added to principal (this is what the website example implies: Rs 40 lakh grows to Rs 44.5 lakh) |
| Interest accrued in moratorium | Rs 16,87,500 = AUD 25,254 |
| Principal when EMIs start | Rs 1,66,87,500 = AUD 249,738 |
| FX | 1 AUD = Rs 66.82 (1 Nov 2026 mid-market, from `report/FRESH_ASSESSMENT_2026-11-01.md`; refresh before use) |

## Headline numbers

| | Rs | AUD |
|---|---:|---:|
| **Monthly EMI** | **1,69,256** | **2,533** |
| Total paid over 15 years (EMIs only) | 3,04,66,033 | 455,942 |
| Interest paid during repayment | 1,37,78,533 | 206,204 |
| Total interest incl. moratorium | 1,54,66,033 | 231,458 |

## Repayment table (one EMI shown per year, as on the website)

| Repayment cycle | EMI (Rs) | EMI (AUD) | Interest portion (Rs) | Interest (AUD) | Principal portion (Rs) | Principal (AUD) | Loan outstanding (Rs) | Outstanding (AUD) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Start of loan EMI | 1,69,256 | 2,533 | 1,25,156 | 1,873 | 44,099 | 660 | 1,66,43,401 | 249,078 |
| End of year 1 | 1,69,256 | 2,533 | 1,21,378 | 1,816 | 47,877 | 717 | 1,61,35,922 | 241,483 |
| End of year 2 | 1,69,256 | 2,533 | 1,16,887 | 1,749 | 52,368 | 784 | 1,55,32,602 | 232,454 |
| End of year 3 | 1,69,256 | 2,533 | 1,11,975 | 1,676 | 57,281 | 857 | 1,48,72,686 | 222,578 |
| End of year 4 | 1,69,256 | 2,533 | 1,06,601 | 1,595 | 62,654 | 938 | 1,41,50,866 | 211,776 |
| End of year 5 | 1,69,256 | 2,533 | 1,00,724 | 1,507 | 68,532 | 1,026 | 1,33,61,334 | 199,960 |
| End of year 6 | 1,69,256 | 2,533 | 94,295 | 1,411 | 74,960 | 1,122 | 1,24,97,739 | 187,036 |
| End of year 7 | 1,69,256 | 2,533 | 87,263 | 1,306 | 81,992 | 1,227 | 1,15,53,132 | 172,899 |
| End of year 8 | 1,69,256 | 2,533 | 79,572 | 1,191 | 89,684 | 1,342 | 1,05,19,915 | 157,437 |
| End of year 9 | 1,69,256 | 2,533 | 71,159 | 1,065 | 98,097 | 1,468 | 93,89,775 | 140,523 |
| End of year 10 | 1,69,256 | 2,533 | 61,957 | 927 | 1,07,299 | 1,606 | 81,53,620 | 122,024 |
| End of year 11 | 1,69,256 | 2,533 | 51,892 | 777 | 1,17,364 | 1,756 | 68,01,505 | 101,788 |
| End of year 12 | 1,69,256 | 2,533 | 40,882 | 612 | 1,28,374 | 1,921 | 53,22,552 | 79,655 |
| End of year 13 | 1,69,256 | 2,533 | 28,840 | 432 | 1,40,416 | 2,101 | 37,04,864 | 55,445 |
| End of year 14 | 1,69,256 | 2,533 | 15,668 | 234 | 1,53,588 | 2,299 | 19,35,425 | 28,965 |
| End of year 15 | 1,69,256 | 2,533 | 1,260 | 19 | 1,67,996 | 2,514 | 0 | 0 |

Note: as on the website, each row is the split of that single month's EMI (month 1, 12, 24 ... 180), and the outstanding balance is after that payment. Final row outstanding is 0.

## Sensitivity: monthly EMI for Rs 1.5 crore at other rates / tenures

Same 15-month moratorium. Cells show EMI in Rs / AUD. Website quotes secured rates from ~8.15% and says banks offer up to 15 years.

| Rate \ Tenure | 7 yrs | 10 yrs | 12 yrs | 15 yrs |
|---|---:|---:|---:|---:|
| 8.15% | 2,58,848 / AUD 3,874 | 2,01,844 / AUD 3,021 | 1,80,271 / AUD 2,698 | 1,59,386 / AUD 2,385 |
| 9.00% | 2,68,486 / AUD 4,018 | 2,11,390 / AUD 3,164 | 1,89,909 / AUD 2,842 | 1,69,256 / AUD 2,533 |
| 10.00% | 2,80,145 / AUD 4,193 | 2,23,004 / AUD 3,337 | 2,01,669 / AUD 3,018 | 1,81,340 / AUD 2,714 |
| 11.00% | 2,92,152 / AUD 4,372 | 2,35,036 / AUD 3,517 | 2,13,888 / AUD 3,201 | 1,93,932 / AUD 2,902 |
| 12.00% | 3,04,510 / AUD 4,557 | 2,47,487 / AUD 3,704 | 2,26,565 / AUD 3,391 | 2,07,029 / AUD 3,098 |

Total repaid (EMIs x months), Rs crore / AUD:

| Rate \ Tenure | 7 yrs | 10 yrs | 12 yrs | 15 yrs |
|---|---:|---:|---:|---:|
| 8.15% | 2.17 cr / AUD 325,400 | 2.42 cr / AUD 362,486 | 2.60 cr / AUD 388,492 | 2.87 cr / AUD 429,355 |
| 9.00% | 2.26 cr / AUD 337,517 | 2.54 cr / AUD 379,629 | 2.73 cr / AUD 409,262 | 3.05 cr / AUD 455,942 |
| 10.00% | 2.35 cr / AUD 352,173 | 2.68 cr / AUD 400,487 | 2.90 cr / AUD 434,606 | 3.26 cr / AUD 488,493 |
| 11.00% | 2.45 cr / AUD 367,266 | 2.82 cr / AUD 422,094 | 3.08 cr / AUD 460,938 | 3.49 cr / AUD 522,414 |
| 12.00% | 2.56 cr / AUD 382,802 | 2.97 cr / AUD 444,455 | 3.26 cr / AUD 488,257 | 3.73 cr / AUD 557,696 |

## Caveats

- Planning estimate only. Real EMI depends on lender, rate type (floating rates change with repo rate), processing fees, and whether you pay interest during the moratorium (paying it keeps the principal at Rs 1.5 cr and lowers the EMI).
- The AUD column is a straight conversion at today's rate. The loan is repaid in INR, so the AUD value moves with the exchange rate. If he later earns in AUD, the INR cost in AUD terms is what matters. The AUD has been about Rs 66-67 recently.
- Rs 1.5 crore would normally need collateral and a co-applicant. The website says unsecured loans are mostly capped around Rs 50-85 lakh (see `background_checks/wemakescholars/`).
- Section 80E allows deduction of interest (not principal) for up to 8 years, per the website.
