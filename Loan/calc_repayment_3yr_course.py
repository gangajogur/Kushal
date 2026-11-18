"""Education loan model: 3-year course, staggered drawdown, no payments until grace period ends.

Assumptions (confirmed with user 2026-11-08):
  - Total Rs 1.5 crore drawn as Rs 50 lakh at the START of year 1, 2 and 3 (months 0, 12, 24).
  - No payments during the course (36 months) or the grace period (12 months) -> first EMI due after month 48.
  - Interest during the moratorium compounds ANNUALLY (at month 12, 24, 36, 48).
  - Rate 9% p.a.; EMIs: 15 years (180 monthly), standard reducing-balance EMI with monthly rate = 9%/12.
  - 1 AUD = Rs 66.82.

Run: python calc_repayment_3yr_course.py
Writes: repayment_analysis_3yr_course.md, repayment_schedule_3yr_course.csv
"""
import csv

RATE = 0.09
DRAWS = [5_000_000, 5_000_000, 5_000_000]    # at months 0, 12, 24
COURSE_YEARS = 3
GRACE_MONTHS = 12
TENURE_YEARS = 15
AUD_INR = 66.82


def inr(x):
    s = f"{int(round(x))}"
    neg = s.startswith("-")
    s = s.lstrip("-")
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if neg else "") + s


def aud(x):
    return f"{x / AUD_INR:,.0f}"


def moratorium(rate, mode):
    """Return list of yearly rows and the balance at end of moratorium (month 48)."""
    years = COURSE_YEARS + GRACE_MONTHS // 12
    bal = 0.0
    rows = []
    cum_draw = 0.0
    simple_accrued = 0.0
    for y in range(1, years + 1):
        draw = DRAWS[y - 1] if y <= len(DRAWS) else 0.0
        opening = bal
        bal += draw                      # drawn at start of year
        cum_draw += draw
        if mode == "compound":
            interest = bal * rate
            bal += interest
            rows.append((y, opening, draw, interest, bal))
        else:                            # simple: interest on drawn principal only, added at end
            interest = cum_draw * rate
            simple_accrued += interest
            rows.append((y, opening, draw, interest, cum_draw + simple_accrued))
            bal = cum_draw + simple_accrued
    return rows, bal


def emi_of(p, annual, years):
    r = annual / 12
    n = years * 12
    return p * r * (1 + r) ** n / ((1 + r) ** n - 1)


def amortise(p, annual, years):
    r = annual / 12
    n = years * 12
    emi = emi_of(p, annual, years)
    bal = p
    out = []
    for m in range(1, n + 1):
        i = bal * r
        pr = emi - i
        bal -= pr
        out.append((m, emi, i, pr, max(bal, 0.0)))
    return emi, out


def main():
    total_drawn = sum(DRAWS)
    mrows, p48 = moratorium(RATE, "compound")
    emi, sched = amortise(p48, RATE, TENURE_YEARS)
    n = TENURE_YEARS * 12
    total_paid = emi * n
    mor_interest = p48 - total_drawn
    repay_interest = total_paid - p48

    # comparison scenarios
    def scenario(rate, mode, grace_note=""):
        _, p = moratorium(rate, mode)
        e = emi_of(p, rate, TENURE_YEARS)
        return p, e, e * n

    L = []
    L.append("# Rs 1.5 crore education loan: 3-year course, staggered drawdown, no payments until grace period ends\n")
    L.append("This replaces the simplified model in `repayment_table_1.5cr.md` (that one assumed the full amount drawn on day one and only a 15-month moratorium, "
             "copied from the website's example). See `calc_repayment_3yr_course.py` for the working.\n")
    L.append("## Assumptions (confirmed)\n")
    L.append("| Item | Value |\n|---|---|\n"
             "| Total loan | Rs 1,50,00,000 (Rs 1.5 crore), drawn as Rs 50 lakh at the start of year 1, 2 and 3 |\n"
             "| Course | 3 years, no payments |\n"
             "| Grace period | 12 months after course ends, no payments |\n"
             "| First EMI | Month 49 (end of the first month after the 4-year moratorium) |\n"
             f"| Interest | {RATE*100:.0f}% p.a., **compounded annually** during the moratorium (months 1-48) |\n"
             f"| Repayment | {TENURE_YEARS} years, {n} monthly EMIs, reducing balance (monthly rate 9%/12, same formula as the website) |\n"
             f"| FX | 1 AUD = Rs {AUD_INR} (fixed, from `report/FRESH_ASSESSMENT_2026-11-01.md`) |\n")

    L.append("## Step 1: Balance building up during the 4-year moratorium (nothing paid)\n")
    L.append("Draw is at the start of the year; interest for the year compounds at the year end.\n")
    L.append("| Moratorium year | Phase | Opening balance (Rs) | Drawn (Rs) | Interest added (Rs) | Closing balance (Rs) | Closing (AUD) |\n|---|---|---:|---:|---:|---:|---:|")
    phases = ["Course yr 1", "Course yr 2", "Course yr 3", "Grace (12 months)"]
    for (y, op, dr, it, cl), ph in zip(mrows, phases):
        L.append(f"| {y} | {ph} | {inr(op)} | {inr(dr)} | {inr(it)} | {inr(cl)} | {aud(cl)} |")
    L.append("")
    L.append(f"**Principal when EMIs start: Rs {inr(p48)} (AUD {aud(p48)}).** "
             f"That is Rs {inr(total_drawn)} drawn + Rs {inr(mor_interest)} interest (AUD {aud(mor_interest)}) that has been added to the loan, "
             f"i.e. the loan is {p48/total_drawn:.2f}x what was borrowed before the first repayment.\n")

    L.append("## Step 2: EMI\n")
    L.append(f"| | Rs | AUD |\n|---|---:|---:|\n"
             f"| **Monthly EMI ({n} payments)** | **{inr(emi)}** | **{aud(emi)}** |\n"
             f"| **Yearly repayment (12 x EMI)** | **{inr(emi*12)}** | **{aud(emi*12)}** |\n"
             f"| Total paid in EMIs | {inr(total_paid)} | {aud(total_paid)} |\n"
             f"| Interest paid during repayment | {inr(repay_interest)} | {aud(repay_interest)} |\n"
             f"| Total interest on the loan (moratorium + repayment) | {inr(mor_interest + repay_interest)} | {aud(mor_interest + repay_interest)} |\n"
             f"| Total paid vs Rs 1.5 cr borrowed | {total_paid/total_drawn:.2f}x | |\n")

    L.append("## Step 3: Yearly repayment table (the yearly minimum you must pay)\n")
    L.append("Repayment year 1 starts in month 49, i.e. loan year 5. Each row sums 12 EMIs. "
             "\"Minimum\" here means the scheduled EMI total: paying less than this puts the loan in arrears.\n")
    L.append("| Repayment year | Loan year | Total paid in year (Rs) | AUD | Interest (Rs) | Interest (AUD) | Principal (Rs) | Principal (AUD) | Closing balance (Rs) | Closing (AUD) |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    yearly = []
    for y in range(1, TENURE_YEARS + 1):
        chunk = sched[(y - 1) * 12: y * 12]
        paid = sum(c[1] for c in chunk)
        it = sum(c[2] for c in chunk)
        pr = sum(c[3] for c in chunk)
        cl = chunk[-1][4]
        yearly.append((y, paid, it, pr, cl))
        L.append(f"| {y} | {y+4} | {inr(paid)} | {aud(paid)} | {inr(it)} | {aud(it)} | {inr(pr)} | {aud(pr)} | {inr(cl)} | {aud(cl)} |")
    tp = sum(r[1] for r in yearly)
    ti = sum(r[2] for r in yearly)
    tpr = sum(r[3] for r in yearly)
    L.append(f"| **Total** | | **{inr(tp)}** | **{aud(tp)}** | **{inr(ti)}** | **{aud(ti)}** | **{inr(tpr)}** | **{aud(tpr)}** | 0 | 0 |")
    L.append("")
    L.append("In loan years 1-4 (course and grace) the minimum payment is Rs 0. If he wants to stop the balance growing he could pay the interest during the course "
             "(see Step 5), which is optional.\n")

    L.append("## Step 4: How the assumptions change the answer (9%, 15-year EMIs unless noted)\n")
    L.append("| Scenario | Principal at first EMI (Rs) | Monthly EMI (Rs) | Monthly EMI (AUD) | Total paid (Rs cr) | Total paid (AUD) |\n|---|---:|---:|---:|---:|---:|")

    def row(label, p, e, t):
        L.append(f"| {label} | {inr(p)} | {inr(e)} | {aud(e)} | {t/1e7:.2f} | {aud(t)} |")
    p, e, t = scenario(RATE, "compound")
    row("**This analysis**: staggered draws, 4-year moratorium, annual compounding", p, e, t)
    p, e, t = scenario(RATE, "simple")
    row("Same, but simple interest (public bank style)", p, e, t)
    # old model
    p_old = 15_000_000 * (1 + RATE * 15 / 12)
    e_old = emi_of(p_old, RATE, TENURE_YEARS)
    row("Earlier file: full Rs 1.5 cr on day 1, 15-month simple moratorium", p_old, e_old, e_old * n)
    # rate sensitivity
    for rt in (0.0815, 0.10, 0.11):
        p, e, t = scenario(rt, "compound")
        row(f"Annual compounding at {rt*100:.2f}%", p, e, t)
    L.append("")

    L.append("## Step 5: Optional, pay the interest during the course\n")
    L.append("If the family pays the interest each year during the course and grace period (Rs 0 principal change), the balance does not grow. "
             "Interest due at the end of each year on the drawn balance at 9%:\n")
    L.append("| Year | Balance drawn | Interest to pay at year end (Rs) | AUD |\n|---|---:|---:|---:|")
    cum = 0.0
    for y in range(1, 5):
        cum += DRAWS[y - 1] if y <= 3 else 0
        L.append(f"| {y} | {inr(cum)} | {inr(cum*RATE)} | {aud(cum*RATE)} |")
    pay_total = sum((sum(DRAWS[:min(y, 3)]) * RATE) for y in range(1, 5))
    L.append("")
    L.append(f"Paying that costs Rs {inr(pay_total)} (AUD {aud(pay_total)}) over 4 years, but the loan then starts repayment at Rs 1.5 cr and the EMI is "
             f"Rs {inr(emi_of(total_drawn, RATE, TENURE_YEARS))} (AUD {aud(emi_of(total_drawn, RATE, TENURE_YEARS))}) a month instead of Rs {inr(emi)}. "
             f"Total interest is lower because it stops compounding.\n")

    L.append("## Caveats\n")
    L.append("- Planning estimate. Lenders differ on: whether interest is simple or compounded in the moratorium, when it is capitalised, whether the rate floats with the repo rate, processing fees, and whether the grace period is 6 or 12 months. Ask each lender for their sanction letter terms.\n"
             "- Tranche timing: I assumed draws at the start of each year. Drawing later in each year (e.g. by semester) lowers the accrued interest slightly.\n"
             "- 15-year tenure counted from the first EMI. Some lenders cap the total tenure (including moratorium) at 15 years, which would leave only 11 EMI years and raise the EMI sharply. Worth checking.\n"
             "- The loan is repaid in INR, so the AUD column moves with the exchange rate.\n"
             "- A Rs 1.5 crore loan would normally need collateral and a co-applicant (see `background_checks/wemakescholars/`).\n"
             "- Section 80E: interest (not principal) is deductible for up to 8 years, per the website.\n")
    with open("repayment_analysis_3yr_course.md", "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    with open("repayment_schedule_3yr_course.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["emi_month", "loan_month", "emi_inr", "interest_inr", "principal_inr", "outstanding_inr",
                    "emi_aud", "interest_aud", "principal_aud", "outstanding_aud"])
        for m, e, i, pr, b in sched:
            w.writerow([m, m + 48, round(e), round(i), round(pr), round(b),
                        round(e / AUD_INR, 2), round(i / AUD_INR, 2), round(pr / AUD_INR, 2), round(b / AUD_INR, 2)])


if __name__ == "__main__":
    main()
