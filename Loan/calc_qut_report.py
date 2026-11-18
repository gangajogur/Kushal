"""QUT BIT (Computer Science), July 2027: short fact-check for nephew.

Confirmed 2026-11-13:
  - Loan = QUT costs only (not a round Rs 1.5 cr)
  - Covers tuition + OSHC + student visa + modest personal spend while studying
  - Accommodation + food during study: provided by uncle in Brisbane (not in loan)
  - Tuition +3%/yr after 2027 published fee; no scholarship
  - Semester draws; 9% p.a. capitalised annually (time-weighted within each year)
  - No payments for 3-year course + 12-month grace; first EMI Jul 2031
  - Job ~Jan 2031; starting salary A$70,000 base case
  - Family-pay scenarios: year 3 tuition cash; years 2+3 tuition cash (not drawn)

Run: python calc_qut_report.py
Writes: QUT_loan_fact_check_report.md, qut_base_case_budget.csv
"""
import csv

FX = 66.82
RATE = 0.09
FEE_2027 = 46_700
FEE_GROWTH = 0.03
VISA = 2_500
# Medibank Comprehensive single, ~38 months (visa-length for Jul 2027–~Aug 2030): A$2,829.20 from Nov 2026 rate card
OSHC = 2_830
# Modest personal while living with uncle (food+rent covered): phone, transport, leisure, books, misc
PERSONAL_PER_SEM = 2_100   # A$350/mo x 6 months
TENURE_M = 180
SALARY0 = 70_000
INCREMENTS = [0.07, 0.07, 0.05, 0.05]  # yrs 2-5; then 3.5%
LATER_INC = 0.035
CPI_LIVING = 0.035

# Post-grad shared rental band (user-confirmed)
LIVING_TODAY = [
    ("Shared room + bills (A$265/wk)", 265 * 52),
    ("Groceries / food (A$110/wk)", 110 * 52),
    ("Transport (QLD 50c fares + occasional trips)", 400),
    ("Phone (A$40/mo)", 480),
    ("Eating out / social / leisure (A$200/mo)", 200 * 12),
    ("Clothing, personal care, misc", 1_200),
    ("OVHC / private health (India has no Medicare reciprocal deal)", 1_000),
    ("One trip home to India per year", 1_500),
]
LIVING_TODAY_TOTAL = sum(v for _, v in LIVING_TODAY)
# Inflate today's living band to mid-2031 (~4.5 years at 3.5%/yr) so year-1 repayment is not understated
LIVING_Y1 = LIVING_TODAY_TOTAL * ((1 + CPI_LIVING) ** 4.5)

# Study years: Jul-Jun blocks. Semesters at months 0,6,12,18,24,30 within course.
SEM = [("S2 2027", 2027), ("S1 2028", 2028), ("S2 2028", 2028),
       ("S1 2029", 2029), ("S2 2029", 2029), ("S1 2030", 2030)]
SEM_FEE = [FEE_2027 * (1 + FEE_GROWTH) ** (y - 2027) / 2 for _, y in SEM]


def inr(x):
    s = f"{int(round(abs(x)))}"
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts + [tail])
    return ("-" if x < 0 else "") + s


def rs(aud):
    return inr(aud * FX)


def a(x):
    return f"{x:,.0f}"


def tax_takehome(gross):
    """Stage 3 resident rates from 1 Jul 2024: 16/30/37/45 + Medicare 2% + LITO. Brackets held flat."""
    brackets = [(0, 18_200, 0.0), (18_200, 45_000, 0.16), (45_000, 135_000, 0.30),
                (135_000, 190_000, 0.37), (190_000, 1e12, 0.45)]
    tax = 0.0
    for lo, hi, rate in brackets:
        if gross > lo:
            tax += (min(gross, hi) - lo) * rate
    medicare = gross * 0.02
    if gross <= 37_500:
        lito = 700
    elif gross <= 45_000:
        lito = 700 - (gross - 37_500) * 0.05
    elif gross < 66_667:
        lito = 325 - (gross - 45_000) * 0.015
    else:
        lito = 0.0
    return gross - max(tax - lito, 0) - medicare


def loan_for(paid_semesters):
    """paid_semesters: set of semester indexes 0..5 paid in cash (tuition only). Personal still drawn."""
    # Year blocks 1..3 (course) each have draws at start and mid-year; block 4 = grace.
    # Block 1: visa+OSHC + S0 tuition(+personal) at t0; S1 tuition(+personal) at t6
    # Block 2: S2 at t0-of-block (=month 12); S3 at mid
    # Block 3: S4, S5
    fees = list(SEM_FEE)
    pers = [PERSONAL_PER_SEM] * 6

    def tuition(i):
        return 0.0 if i in paid_semesters else fees[i]

    draws = {
        1: [VISA + OSHC + tuition(0) + pers[0], tuition(1) + pers[1]],
        2: [tuition(2) + pers[2], tuition(3) + pers[3]],
        3: [tuition(4) + pers[4], tuition(5) + pers[5]],
        4: [0.0, 0.0],
    }
    bal = 0.0
    rows = []
    for b in range(1, 5):
        d0, d6 = draws[b]
        opening = bal
        # Time-weighted interest within the year, then capitalised (annual compounding)
        interest = (bal + d0) * RATE + d6 * RATE * 0.5
        bal = bal + d0 + d6 + interest
        rows.append((b, opening, d0 + d6, interest, bal))

    drawn = sum(r[2] for r in rows)
    p48 = bal
    r_m = RATE / 12
    emi = p48 * r_m * (1 + r_m) ** TENURE_M / ((1 + r_m) ** TENURE_M - 1)

    bal2 = p48
    yearly = []
    for y in range(1, 16):
        i_tot = pr_tot = 0.0
        for _ in range(12):
            i = bal2 * r_m
            pr = emi - i
            bal2 -= pr
            i_tot += i
            pr_tot += pr
        yearly.append((y, emi * 12, i_tot, pr_tot, max(bal2, 0.0)))

    cash_tuition = sum(fees[i] for i in paid_semesters)
    return {
        "rows": rows,
        "drawn": drawn,
        "p48": p48,
        "emi": emi,
        "yearly": yearly,
        "cash_tuition": cash_tuition,
        "fees": fees,
        "interest_mor": p48 - drawn,
        "total_paid": emi * TENURE_M,
    }


def salaries():
    s = SALARY0
    out = [s]
    for i in range(14):
        inc = INCREMENTS[i] if i < len(INCREMENTS) else LATER_INC
        s *= 1 + inc
        out.append(s)
    return out


def main():
    base = loan_for(set())
    y3 = loan_for({4, 5})          # study year 3 tuition cash
    y23 = loan_for({2, 3, 4, 5})   # study years 2+3 tuition cash
    sal = salaries()

    # --- report ---
    L = []
    L.append("# QUT loan fact-check (for Kushal)\n")
    L.append(
        "Prepared 13 Nov 2026. Short planning sheet: **Rs (INR)** and **A$ (AUD)** side by side. "
        f"**1 A$ = Rs {FX}** (held flat). "
        "Tags: **[P]** published, **[E]** market estimate, **[A]** assumption. "
        "Working: `calc_qut_report.py`.\n"
    )

    # Bottom line
    L.append("## 1. Bottom line (base case: full loan)\n")
    L.append("| | Rs | A$ |\n|---|---:|---:|")
    L.append(f"| Total drawn (tuition + visa + OSHC + personal) | {rs(base['drawn'])} | {a(base['drawn'])} |")
    L.append(f"| Balance when EMIs start (Jul 2031) | {rs(base['p48'])} | {a(base['p48'])} |")
    L.append(f"| **Minimum monthly EMI (15 years)** | **{rs(base['emi'])}** | **{a(base['emi'])}** |")
    L.append(f"| Minimum yearly repayment | {rs(base['emi']*12)} | {a(base['emi']*12)} |")
    L.append(f"| Total repaid over 15 years | {rs(base['total_paid'])} | {a(base['total_paid'])} |")
    L.append("")
    th1 = tax_takehome(SALARY0)
    left1 = th1 - LIVING_Y1 - base["emi"] * 12
    L.append(
        f"In plain terms: he borrows about **A${a(base['drawn'])}** (Rs {rs(base['drawn'])}) and "
        f"repays about **A${a(base['total_paid'])}** (Rs {rs(base['total_paid'])}), "
        f"roughly **{base['total_paid']/base['drawn']:.1f}x** what was drawn. "
        f"On a starting salary of **A$70,000**, take-home is about **A${a(th1)}**; "
        f"after shared-rent living (**A${a(LIVING_Y1)}**) and the EMI (**A${a(base['emi']*12)}**/yr), "
        f"**about A${a(left1)} a year is left** in repayment year 1 "
        f"(~A${a(left1/12)}/month). That is essentially break-even: one late rent increase or a weaker starting salary tips it negative.\n"
    )

    # High-level backing (keep short; expand only if needed)
    L.append("## 1a. What sits behind those numbers\n")
    L.append("### Timeline\n")
    L.append("| When | What |\n|---|---|")
    L.append("| Jul 2027 | Starts QUT; first semester draw (tuition + personal) + visa + OSHC |")
    L.append("| Every 6 months to Jan 2030 | Next semester tuition + personal drawn |")
    L.append("| ~Jun 2030 | Degree ends. No EMI yet (grace) |")
    L.append("| ~Jan 2031 | Assumed first full-time job (~6 months after finishing) |")
    L.append("| Jul 2031 | Grace ends. **First EMI due.** Then 180 monthly payments to Jun 2046 |")
    L.append("")

    L.append("### Where the A$164,440 loan comes from\n")
    L.append("| Piece | Rs | A$ | Share |\n|---|---:|---:|---:|")
    pieces = [
        ("Tuition (6 semesters, +3%/yr after 2027)", sum(SEM_FEE)),
        ("Personal while studying (A$350/mo x 36)", PERSONAL_PER_SEM * 6),
        ("OSHC (~38 months)", OSHC),
        ("Student visa fee", VISA),
    ]
    drawn_chk = sum(v for _, v in pieces)
    for label, v in pieces:
        L.append(f"| {label} | {rs(v)} | {a(v)} | {100*v/drawn_chk:.0f}% |")
    L.append(f"| **Total drawn** | **{rs(drawn_chk)}** | **{a(drawn_chk)}** | 100% |")
    L.append("")
    L.append(
        f"Rent and food during study are **not** in the loan (covered by uncle). "
        f"Published 2027 fee is A$46,700/yr; later years use +3%/yr because QUT only publishes the current year.\n"
    )

    L.append("### How the EMI is derived (3 steps)\n")
    L.append("| Step | Result |\n|---|---|")
    L.append(
        f"| 1. Draw over 3 years, pay nothing for study + 12-month grace | "
        f"Interest capitalised each July at 9% (mid-year draws get half a year of interest) |"
    )
    L.append(
        f"| 2. Balance at first EMI (Jul 2031) | "
        f"**A${a(base['p48'])}** = A${a(base['drawn'])} drawn + A${a(base['interest_mor'])} interest |"
    )
    L.append(
        f"| 3. Standard reducing-balance EMI over 180 months at 9%/12 | "
        f"**A${a(base['emi'])}/mo** (Rs {rs(base['emi'])}) |"
    )
    L.append("")
    L.append(
        "Same EMI formula as the WeMakeScholars example table; only the principal and draw timing differ. "
        "Lender sanction letters can differ (simple vs compounding interest, floating rate, tenure cap).\n"
    )

    L.append("### Monthly snapshot, repayment year 1 (Jul 2031-Jun 2032)\n")
    L.append("| | Per month A$ | Per year A$ | Per year Rs |\n|---|---:|---:|---:|")
    L.append(f"| Gross salary | {a(SALARY0/12)} | {a(SALARY0)} | {rs(SALARY0)} |")
    L.append(f"| Take-home (after tax + Medicare) | {a(th1/12)} | {a(th1)} | {rs(th1)} |")
    L.append(f"| Shared-rent living | {a(LIVING_Y1/12)} | {a(LIVING_Y1)} | {rs(LIVING_Y1)} |")
    L.append(f"| **EMI (minimum)** | **{a(base['emi'])}** | **{a(base['emi']*12)}** | **{rs(base['emi']*12)}** |")
    L.append(f"| **Left over** | **{a(left1/12)}** | **{a(left1)}** | **{rs(left1)}** |")
    L.append("")
    L.append("Living band used (today's prices, then inflated ~4.5 years at 3.5% to mid-2031):\n")
    L.append("| Item | Today A$/yr |\n|---|---:|")
    for label, v in LIVING_TODAY:
        L.append(f"| {label} | {a(v)} |")
    L.append(f"| **Today total** | **{a(LIVING_TODAY_TOTAL)}** |")
    L.append(f"| **Inflated to Jul 2031** | **{a(LIVING_Y1)}** |")
    L.append("")

    # Facts
    L.append("## 2. Facts used\n")
    L.append("| Item | Value | Tag |\n|---|---|---|")
    L.append("| Course | Bachelor of IT (IN01), Computer Science, Gardens Point; Jul 2027 → ~Jun 2030; 6 semesters | [P] QUT |")
    L.append("| Tuition 2027 | A$46,700/yr (A$23,350/sem). QUT publishes only the current year and says fees rise annually | [P] QUT 2027 International Quick Guide |")
    L.append("| Tuition 2028–2030 | +3%/yr assumed → A$48,101 / A$49,544 / A$51,030 per year | [A] |")
    L.append(f"| Student visa fee | A${a(VISA)} (from 1 Jul 2026) | [P] Study Australia |")
    L.append(f"| OSHC (~38 months, single) | A${a(OSHC)} (Medibank Comprehensive, Nov 2026 rate card) | [P] Medibank |")
    L.append(f"| Personal while studying | A${a(PERSONAL_PER_SEM)}/semester (≈A$350/mo: phone, transport, leisure, books). Rent + food covered by uncle | [A] |")
    L.append("| Scholarship | None | [A] |")
    L.append("| Loan | 9% p.a., interest capitalised each Jul; no payments for 3 yrs study + 12 mo grace; 180 EMIs from Jul 2031 | [A] lender terms vary |")
    L.append("| First job | ~Jan 2031 (6 months after finishing); first EMI Jul 2031 | [A] |")
    L.append("| Starting salary | A$70,000. QILT 2025: international undergrad median A$70,000; Computing & IS international median A$65,000 | [P]/[A] |")
    L.append("| Salary growth | +7%, +7%, +5%, +5%, then +3.5%/yr | [A] |")
    L.append(
        f"| Living after moving out | Today's shared-rent band A${a(LIVING_TODAY_TOTAL)}/yr "
        f"(room+bills A$265/wk, food A$110/wk, extras), inflated ~4.5 yrs at 3.5% to "
        f"**A${a(LIVING_Y1)}/yr** for Jul 2031, then +3.5%/yr | [E]/[A] |"
    )
    L.append("| Tax | Stage 3 resident rates (16%/30%/37%/45%) + Medicare 2% + LITO. Employer super on top, not counted | [P] ATO |")
    L.append("")

    # What is borrowed
    L.append("## 3. What goes into the loan\n")
    L.append("| Draw | When | Item | Rs | A$ |\n|---|---|---|---:|---:|")
    L.append(f"| Start | Jul 2027 | Student visa fee | {rs(VISA)} | {a(VISA)} |")
    L.append(f"| Start | Jul 2027 | OSHC | {rs(OSHC)} | {a(OSHC)} |")
    for i, ((label, _), fee) in enumerate(zip(SEM, SEM_FEE)):
        month = i * 6
        L.append(f"| Sem {i+1} | +{month} mo ({label}) | Tuition | {rs(fee)} | {a(fee)} |")
        L.append(f"| Sem {i+1} | +{month} mo ({label}) | Personal | {rs(PERSONAL_PER_SEM)} | {a(PERSONAL_PER_SEM)} |")
    tot_tuition = sum(SEM_FEE)
    tot_personal = PERSONAL_PER_SEM * 6
    L.append(f"| **Total tuition** | | | **{rs(tot_tuition)}** | **{a(tot_tuition)}** |")
    L.append(f"| **Total personal** | | | **{rs(tot_personal)}** | **{a(tot_personal)}** |")
    L.append(f"| **Total drawn** | | | **{rs(base['drawn'])}** | **{a(base['drawn'])}** |")
    L.append("")
    L.append(
        "Cash needed **outside** the loan: Temporary Graduate (485) visa fee about **A$5,750** (Rs "
        f"{rs(5750)}), plus flights, laptop and setup. Accommodation and food during study are covered by you and are not in these figures.\n"
    )

    # Balance growth
    L.append("## 4. Balance before the first payment\n")
    L.append("Nothing is paid for 4 years. Interest is added each July.\n")
    L.append("| Year | Phase | Opening A$ | Drawn A$ | Interest A$ | Closing A$ | Closing Rs |\n|---|---|---:|---:|---:|---:|---:|")
    phases = ["Study yr 1", "Study yr 2", "Study yr 3", "Grace (12 mo)"]
    for (b, op, dr, it, cl), ph in zip(base["rows"], phases):
        L.append(f"| {b} | {ph} | {a(op)} | {a(dr)} | {a(it)} | {a(cl)} | {rs(cl)} |")
    L.append("")
    L.append(
        f"Interest of **A${a(base['interest_mor'])}** (Rs {rs(base['interest_mor'])}) is added before EMIs start. "
        f"He starts repaying **A${a(base['p48'])}** — about **{base['p48']/base['drawn']:.2f}x** what was drawn.\n"
    )

    # Affordability table
    L.append("## 5. After graduation: salary vs EMI (base case)\n")
    L.append(
        f"**Minimum monthly EMI: Rs {rs(base['emi'])} / A${a(base['emi'])}** (fixed for 15 years). "
        f"Yearly: Rs {rs(base['emi']*12)} / A${a(base['emi']*12)}.\n"
    )
    L.append(
        f"Living costs in repayment year 1: **A${a(LIVING_Y1)}** "
        f"(today's shared-rent band A${a(LIVING_TODAY_TOTAL)}, inflated to mid-2031).\n"
    )
    L.append(
        "| Yr | Period | Gross A$ | Take-home A$ | Living A$ | EMI A$ | **Left A$** | Left Rs lakh | Loan bal A$ |\n"
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|"
    )
    living = LIVING_Y1
    for y, (gross, (_yy, paid, _i, _p, bal)) in enumerate(zip(sal, base["yearly"]), start=1):
        th = tax_takehome(gross)
        emi_y = base["emi"] * 12
        left = th - living - emi_y
        period = f"Jul {2030+y}–Jun {2031+y}"
        L.append(
            f"| {y} | {period} | {a(gross)} | {a(th)} | {a(living)} | {a(emi_y)} | "
            f"**{a(left)}** | {left*FX/1e5:.1f} | {a(bal)} |"
        )
        living *= 1 + CPI_LIVING
        if y >= 10:
            break
    L.append("")
    L.append(
        "Years 11–15 are omitted for length; the EMI stays fixed while salary and living costs keep rising, "
        "so the cushion grows. Full 15-year rows are in `qut_base_case_budget.csv`.\n"
    )
    # Break-even rough
    # Need gross such that takehome - living - emi*12 = 0
    be = None
    for g in range(30_000, 120_000, 100):
        if tax_takehome(g) - LIVING_Y1 - base["emi"] * 12 >= 0:
            be = g
            break
    L.append(
        f"**Break-even:** about **A${a(be)}** gross covers living + EMI with nothing left. "
        f"A$70,000 clears that by about **A${a(SALARY0 - be)}**.\n"
    )

    # Family pay summary
    L.append("## 6. Summary: if family pays later years in cash\n")
    L.append(
        "Tuition for those years is **not drawn**. Visa, OSHC and personal spend stay in the loan. "
        "Cash cost is tuition only at the inflated fee.\n"
    )
    L.append(
        "| | Base (borrow all) | Family pays **year 3** | Family pays **years 2 + 3** |\n"
        "|---|---:|---:|---:|"
    )

    def col(s):
        return s

    scenarios = [("Base", base), ("Year 3 paid", y3), ("Years 2+3 paid", y23)]
    # Build row-wise
    rows_def = [
        ("Cash paid by family (tuition)", lambda s: f"A${a(s['cash_tuition'])} / Rs {rs(s['cash_tuition'])}"),
        ("Total drawn from loan", lambda s: f"A${a(s['drawn'])} / Rs {rs(s['drawn'])}"),
        ("Balance at first EMI", lambda s: f"A${a(s['p48'])} / Rs {rs(s['p48'])}"),
        ("**Monthly EMI**", lambda s: f"**A${a(s['emi'])} / Rs {rs(s['emi'])}**"),
        ("Yearly repayment", lambda s: f"A${a(s['emi']*12)} / Rs {rs(s['emi']*12)}"),
        ("Total repaid (15 yrs)", lambda s: f"A${a(s['total_paid'])} / Rs {rs(s['total_paid'])}"),
    ]
    for label, fn in rows_def:
        L.append(f"| {label} | " + " | ".join(fn(s) for _, s in scenarios) + " |")

    # leftover comparison year 1
    lefts = []
    for _, s in scenarios:
        lefts.append(tax_takehome(SALARY0) - LIVING_Y1 - s["emi"] * 12)
    L.append(
        "| **Left in repayment yr 1** (after tax, living, EMI) | "
        + " | ".join(f"**A${a(x)}**" for x in lefts)
        + " |"
    )
    L.append("")
    L.append(
        f"Paying year 3 in cash costs the family about **A${a(y3['cash_tuition'])}** (Rs {rs(y3['cash_tuition'])}) "
        f"and cuts the monthly EMI by about **A${a(base['emi']-y3['emi'])}**. "
        f"Paying years 2 and 3 costs about **A${a(y23['cash_tuition'])}** (Rs {rs(y23['cash_tuition'])}) "
        f"and cuts the EMI by about **A${a(base['emi']-y23['emi'])}** a month.\n"
    )

    # Risks
    L.append("## 7. What can go wrong\n")
    L.append(
        "- **Job timing:** Only about 42% of international Computing & IS graduates are in full-time work "
        "4–6 months after finishing (QILT 2025). A longer job hunt eats the pre-EMI buffer.\n"
        "- **Salary:** Computing & IS international median is A$65,000, below this A$70,000 base case. "
        f"At A$65,000, year-1 leftover falls to about A${a(tax_takehome(65_000)-LIVING_Y1-base['emi']*12)}.\n"
        "- **Fee rises:** If fees rise faster than 3%/yr, the loan grows. QUT does not publish future fees.\n"
        "- **Loan terms:** Floating rates, simple vs compounding interest, a 15-year cap counted from first drawdown, "
        "collateral and co-applicant rules all change the EMI. Ask the lender for a sanction-letter quote.\n"
        "- **FX:** The loan is repaid in rupees. If the rupee weakens against the AUD while he earns in AUD, "
        "the EMI gets easier in AUD terms; the opposite hurts.\n"
        "- **Not in these numbers:** Your food and rent support during study, 485 visa fee, flights, laptop, "
        "remittance charges.\n"
    )

    L.append("## 8. One-line takeaway\n")
    L.append(
        f"At QUT with you covering board, the loan is about **A${a(base['drawn'])}**, "
        f"the **minimum monthly repayment is about A${a(base['emi'])} (Rs {rs(base['emi'])})**, "
        f"and a **A$70k** graduate job with shared rent leaves only about **A${a(left1)}/yr** "
        f"after tax, living and EMI - essentially break-even. "
        f"Family paying year 3 (or years 2-3) tuition is what makes the cashflow comfortable "
        f"(EMI falls to about A${a(y3['emi'])} or A${a(y23['emi'])}).\n"
    )

    text = "\n".join(L)
    # ASCII-safe punctuation so Windows editors don't mangle arrows/dashes
    for old, new in (
        ("\u2192", "->"), ("\u2013", "-"), ("\u2014", "-"),
        ("\u2248", "~"), ("\u2018", "'"), ("\u2019", "'"),
        ("\u201c", '"'), ("\u201d", '"'),
    ):
        text = text.replace(old, new)
    with open("QUT_loan_fact_check_report.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # CSV full 15 years base case
    with open("qut_base_case_budget.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["repay_year", "gross_aud", "takehome_aud", "living_aud", "emi_aud",
                    "left_aud", "emi_inr", "left_inr", "loan_balance_aud"])
        living = LIVING_Y1
        for y, (gross, (_yy, _paid, _i, _p, bal)) in enumerate(zip(sal, base["yearly"]), start=1):
            th = tax_takehome(gross)
            emi_y = base["emi"] * 12
            left = th - living - emi_y
            w.writerow([y, round(gross), round(th), round(living), round(emi_y),
                        round(left), round(base["emi"] * FX), round(left * FX), round(bal)])
            living *= 1 + CPI_LIVING

    # sanity print
    print("BASE drawn", round(base["drawn"]), "p48", round(base["p48"]),
          "EMI AUD", round(base["emi"]), "EMI INR", round(base["emi"] * FX))
    print("Y3 EMI", round(y3["emi"]), "Y23 EMI", round(y23["emi"]))
    print("Y1 left", round(left1))


if __name__ == "__main__":
    main()
