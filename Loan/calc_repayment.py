"""Education loan repayment table, same method as WeMakeScholars' example table.

Verified: with P=40 lakh, 9%, 15 yrs, 15-month moratorium, this reproduces their
published table exactly (EMI 45,135; month-1 interest 33,375; outstanding 4,438,240).

Method:
  1. Moratorium: simple interest on the principal for MORATORIUM_MONTHS, added to principal.
  2. EMI = P' * r * (1+r)^n / ((1+r)^n - 1), r = annual/12, n = tenure months.
  3. Table rows = the EMI split (interest / principal) of payment #1, #12, #24 ... #n,
     plus outstanding after that payment.

Run: python calc_repayment.py   (writes repayment_table_1.5cr.md and repayment_schedule_full.csv)
"""
import csv

LOAN_INR = 15_000_000          # 1.5 crore
RATE = 0.09                    # 9% p.a. (same as the website example)
TENURE_YEARS = 15
MORATORIUM_MONTHS = 15         # 24-month course style assumption in the site's example (implied 15 months)
AUD_INR = 66.82                # 1 AUD = Rs 66.82 (mid-market 1 Nov 2026, from report/FRESH_ASSESSMENT_2026-11-01.md)


def emi_of(p, annual, years):
    r = annual / 12
    n = years * 12
    return p * r * (1 + r) ** n / ((1 + r) ** n - 1)


def schedule(loan, annual, years, moratorium_months):
    p0 = loan * (1 + annual * moratorium_months / 12)
    r = annual / 12
    n = years * 12
    emi = emi_of(p0, annual, years)
    bal = p0
    rows = []
    for m in range(1, n + 1):
        i = bal * r
        pr = emi - i
        bal -= pr
        rows.append((m, emi, i, pr, max(bal, 0.0)))
    return p0, emi, rows


def inr(x):
    """Indian digit grouping, e.g. 1,66,87,500."""
    s = f"{int(round(x))}"
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


def aud(x):
    return f"{x / AUD_INR:,.0f}"


def main():
    p0, emi, rows = schedule(LOAN_INR, RATE, TENURE_YEARS, MORATORIUM_MONTHS)
    n = TENURE_YEARS * 12
    total_paid = emi * n
    total_interest_repay = total_paid - p0
    moratorium_interest = p0 - LOAN_INR

    out = []
    out.append("# Education Loan Repayment Table: Rs 1.5 crore (with AUD equivalent)\n")
    out.append("Same method and layout as the WeMakeScholars example table "
               "(https://www.wemakescholars.com/education-loan#widget-3, Rs 40 lakh at 9% for 15 years). "
               "I re-derived their table and matched it to the rupee before scaling up, see `calc_repayment.py`.\n")
    out.append("## Assumptions\n")
    out.append(f"| Item | Value |\n|---|---|\n"
               f"| Loan disbursed | Rs {inr(LOAN_INR)} (Rs 1.5 crore) = AUD {aud(LOAN_INR)} |\n"
               f"| Interest rate | {RATE*100:.0f}% p.a., reducing balance (same as website example) |\n"
               f"| Repayment tenure | {TENURE_YEARS} years ({n} monthly EMIs) |\n"
               f"| Moratorium | {MORATORIUM_MONTHS} months, simple interest added to principal (this is what the website example implies: Rs 40 lakh grows to Rs 44.5 lakh) |\n"
               f"| Interest accrued in moratorium | Rs {inr(moratorium_interest)} = AUD {aud(moratorium_interest)} |\n"
               f"| Principal when EMIs start | Rs {inr(p0)} = AUD {aud(p0)} |\n"
               f"| FX | 1 AUD = Rs {AUD_INR} (1 Nov 2026 mid-market, from `report/FRESH_ASSESSMENT_2026-11-01.md`; refresh before use) |\n")
    out.append("## Headline numbers\n")
    out.append(f"| | Rs | AUD |\n|---|---:|---:|\n"
               f"| **Monthly EMI** | **{inr(emi)}** | **{aud(emi)}** |\n"
               f"| Total paid over {TENURE_YEARS} years (EMIs only) | {inr(total_paid)} | {aud(total_paid)} |\n"
               f"| Interest paid during repayment | {inr(total_interest_repay)} | {aud(total_interest_repay)} |\n"
               f"| Total interest incl. moratorium | {inr(total_interest_repay + moratorium_interest)} | {aud(total_interest_repay + moratorium_interest)} |\n"
               f"")
    out.append("## Repayment table (one EMI shown per year, as on the website)\n")
    out.append("| Repayment cycle | EMI (Rs) | EMI (AUD) | Interest portion (Rs) | Interest (AUD) | Principal portion (Rs) | Principal (AUD) | Loan outstanding (Rs) | Outstanding (AUD) |\n"
               "|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    picks = [(1, "Start of loan EMI")] + [(12 * y, f"End of year {y}") for y in range(1, TENURE_YEARS + 1)]
    for m, label in picks:
        _, e, i, pr, b = rows[m - 1]
        out.append(f"| {label} | {inr(e)} | {aud(e)} | {inr(i)} | {aud(i)} | {inr(pr)} | {aud(pr)} | {inr(b)} | {aud(b)} |")
    out.append("")
    out.append("Note: as on the website, each row is the split of that single month's EMI (month 1, 12, 24 ... 180), "
               "and the outstanding balance is after that payment. Final row outstanding is 0.\n")

    # sensitivity
    out.append("## Sensitivity: monthly EMI for Rs 1.5 crore at other rates / tenures\n")
    out.append("Same 15-month moratorium. Cells show EMI in Rs / AUD. Website quotes secured rates from ~8.15% and says banks offer up to 15 years.\n")
    rates = [0.0815, 0.09, 0.10, 0.11, 0.12]
    tenures = [7, 10, 12, 15]
    out.append("| Rate \\ Tenure | " + " | ".join(f"{t} yrs" for t in tenures) + " |")
    out.append("|---|" + "---:|" * len(tenures))
    for rt in rates:
        cells = []
        for t in tenures:
            _, e, _rows = schedule(LOAN_INR, rt, t, MORATORIUM_MONTHS)
            cells.append(f"{inr(e)} / AUD {aud(e)}")
        out.append(f"| {rt*100:.2f}% | " + " | ".join(cells) + " |")
    out.append("")
    out.append("Total repaid (EMIs x months), Rs crore / AUD:\n")
    out.append("| Rate \\ Tenure | " + " | ".join(f"{t} yrs" for t in tenures) + " |")
    out.append("|---|" + "---:|" * len(tenures))
    for rt in rates:
        cells = []
        for t in tenures:
            _, e, _rows = schedule(LOAN_INR, rt, t, MORATORIUM_MONTHS)
            tot = e * t * 12
            cells.append(f"{tot/1e7:.2f} cr / AUD {aud(tot)}")
        out.append(f"| {rt*100:.2f}% | " + " | ".join(cells) + " |")
    out.append("")
    out.append("## Caveats\n")
    out.append("- Planning estimate only. Real EMI depends on lender, rate type (floating rates change with repo rate), processing fees, and whether you pay interest during the moratorium (paying it keeps the principal at Rs 1.5 cr and lowers the EMI).\n"
               "- The AUD column is a straight conversion at today's rate. The loan is repaid in INR, so the AUD value moves with the exchange rate. "
               "If he later earns in AUD, the INR cost in AUD terms is what matters. The AUD has been about Rs 66-67 recently.\n"
               "- Rs 1.5 crore would normally need collateral and a co-applicant. The website says unsecured loans are mostly capped around Rs 50-85 lakh (see `background_checks/wemakescholars/`).\n"
               "- Section 80E allows deduction of interest (not principal) for up to 8 years, per the website.\n")
    with open("repayment_table_1.5cr.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    with open("repayment_schedule_full.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["month", "emi_inr", "interest_inr", "principal_inr", "outstanding_inr",
                    "emi_aud", "interest_aud", "principal_aud", "outstanding_aud"])
        for m, e, i, pr, b in rows:
            w.writerow([m, round(e), round(i), round(pr), round(b),
                        round(e / AUD_INR, 2), round(i / AUD_INR, 2), round(pr / AUD_INR, 2), round(b / AUD_INR, 2)])


if __name__ == "__main__":
    main()
