"""Scenario stream: APU (Malaysia) degree, then return to India for work.

Separate from QUT files. Builds an APU-sized education loan, then stress-tests
repayment on a mid Rs 10-12 LPA metro India job (same return assumptions as
QUT_return_to_India_scenario.md).

Sources:
  - APU Fee Guide 2026 (Int UG): IT/CS Y1 RM34,900 / Y2 RM36,100 / Y3 RM37,500
    full payment; semester option RM18,200 / 18,900 / 19,600 x2. Fees exclude 6% SST.
  - One-offs: Stage1 RM3,400, Stage2 RM2,000, Registration RM5,000, library deposit RM500,
    personal bond RM1,000; visa renewal ~RM1,100-1,450/yr.
  - Living: APU guide RM1,600-2,000/mo; use RM1,800 mid (twin-share + food + transport).
  - FX: 1 MYR = Rs 22.83 (18 Nov 2026); 1 AUD = Rs 66.82 (held, for side-by-side).

Run: python calc_apu_india_return.py
Writes: APU_return_to_India_scenario.md
"""
RATE = 0.09
TENURE_M = 180
SST = 0.06
MYR_INR = 22.83
AUD_INR = 66.82

# Semester tuition (published semester-payment path) + SST
SEM_TUITION_RM = [
    18_200, 18_200,   # Level 1
    18_900, 18_900,   # Level 2
    19_600, 19_600,   # Level 3
]
SEM_TUITION_RM = [x * (1 + SST) for x in SEM_TUITION_RM]

# One-offs at start (apply SST to fee-like items; deposits as cash outlay)
STAGE1 = 3_400 * (1 + SST)
STAGE2 = 2_000 * (1 + SST)
REG = 5_000 * (1 + SST)
LIB_DEP = 500          # refundable later; still drawn
BOND = 1_000           # refundable if no breach
VISA_RENEW = 1_300     # mid of RM1,100-1,450; years 2 and 3

LIVING_MO_RM = 1_800   # APU guide mid
LIVING_SEM_RM = LIVING_MO_RM * 6

# India side (same as QUT India-return scenario)
SALARIES = [
    ("Low of band", 10.0, 78_000),
    ("Mid (base)", 11.0, 81_000),
    ("High of band", 12.0, 90_000),
]
INDIA_LIVING = [
    ("Shared PG / co-living with meals (or share of flat + food)", 12_000),
    ("Extra food / eating out", 4_000),
    ("Local transport", 3_000),
    ("Phone + internet", 1_000),
    ("Personal, laundry, misc", 3_000),
    ("Health insurance / medical buffer", 1_500),
    ("Family visit / contingency buffer", 2_500),
]
INDIA_LIVING_MO = sum(v for _, v in INDIA_LIVING)


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


def a_from_inr(inr_amt):
    return f"{inr_amt / AUD_INR:,.0f}"


def rm(x):
    return f"{x:,.0f}"


def lakh(x):
    return f"{x / 1e5:.2f}"


def to_inr(rm_amt):
    return rm_amt * MYR_INR


def loan_schedule():
    """Year blocks with time-weighted 9% capitalised annually; amounts in INR."""
    one_offs = STAGE1 + STAGE2 + REG + LIB_DEP + BOND
    # Block draws: (d0_rm, d6_rm) for years 1-3; year 4 grace
    draws_rm = {
        1: [one_offs + SEM_TUITION_RM[0] + LIVING_SEM_RM, SEM_TUITION_RM[1] + LIVING_SEM_RM],
        2: [VISA_RENEW + SEM_TUITION_RM[2] + LIVING_SEM_RM, SEM_TUITION_RM[3] + LIVING_SEM_RM],
        3: [VISA_RENEW + SEM_TUITION_RM[4] + LIVING_SEM_RM, SEM_TUITION_RM[5] + LIVING_SEM_RM],
        4: [0.0, 0.0],
    }
    bal = 0.0
    rows = []
    for b in range(1, 5):
        d0 = to_inr(draws_rm[b][0])
        d6 = to_inr(draws_rm[b][1])
        opening = bal
        interest = (bal + d0) * RATE + d6 * RATE * 0.5
        bal = bal + d0 + d6 + interest
        rows.append((b, opening, d0 + d6, interest, bal, draws_rm[b][0] + draws_rm[b][1]))
    drawn = sum(r[2] for r in rows)
    p48 = bal
    r_m = RATE / 12
    emi = p48 * r_m * (1 + r_m) ** TENURE_M / ((1 + r_m) ** TENURE_M - 1)
    return {
        "rows": rows,
        "drawn": drawn,
        "p48": p48,
        "emi": emi,
        "interest_mor": p48 - drawn,
        "total_paid": emi * TENURE_M,
        "one_offs_rm": one_offs,
        "tuition_rm": sum(SEM_TUITION_RM),
        "living_rm": LIVING_MO_RM * 36,
        "visa_renew_rm": VISA_RENEW * 2,
    }


def takehome_from_ctc(ctc):
    basic = 0.50 * ctc
    epf = 0.12 * basic
    pt = 2_400
    taxable = max(ctc - 75_000, 0)
    if taxable <= 1_200_000:
        tax = 0.0
    else:
        slabs = [(0, 400_000, 0), (400_000, 800_000, 0.05), (800_000, 1_200_000, 0.10),
                 (1_200_000, 1_600_000, 0.15), (1_600_000, 2_000_000, 0.20),
                 (2_000_000, 2_400_000, 0.25), (2_400_000, 1e12, 0.30)]
        tax = 0.0
        for lo, hi, rate in slabs:
            if taxable > lo:
                tax += (min(taxable, hi) - lo) * rate
        tax *= 1.04
    return ctc - epf - pt - tax


def main():
    base = loan_schedule()
    emi = base["emi"]
    need_th = emi + INDIA_LIVING_MO
    be_ctc = None
    for ctc in range(200_000, 4_000_000, 5_000):
        if takehome_from_ctc(ctc) / 12 >= need_th:
            be_ctc = ctc
            break

    L = []
    L.append("# Scenario: APU (Malaysia) study, then return to India for a job\n")
    L.append(
        "Prepared 18 Nov 2026. **Separate risk stream** from the QUT files. "
        "Builds an APU-sized loan (tuition + KL living + visa/registration), then asks the same question as "
        "`QUT_return_to_India_scenario.md`: **can a mid Rs 10-12 LPA India salary cover the EMI plus metro living?** "
        f"FX: **1 MYR = Rs {MYR_INR}** (18 Nov 2026); **1 AUD = Rs {AUD_INR}** (side-by-side only). "
        "Working: `calc_apu_india_return.py`.\n"
    )

    L.append("## 1. What this scenario is testing\n")
    L.append(
        "He does a 3-year IT/CS degree at APU (Bukit Jalil, KL), starting ~Jul 2027, finishes ~mid-2030, "
        "returns to India, finds a metro IT job about 6 months later (~Jan 2031), and the education-loan EMI "
        "starts ~Jul 2031 after a 12-month grace. Unlike the QUT Brisbane plan, **KL living is in the loan** "
        "(no uncle covering board in Malaysia).\n"
    )

    L.append("## 2. APU cost stack (what gets borrowed)\n")
    L.append("| Piece | RM | Rs | A$ |\n|---|---:|---:|---:|")
    tuition = base["tuition_rm"]
    living = base["living_rm"]
    one = base["one_offs_rm"]
    renew = base["visa_renew_rm"]
    pieces = [
        ("Tuition 6 semesters + 6% SST (semester-payment path)", tuition),
        (f"KL living 36 mo @ RM {LIVING_MO_RM}/mo (APU guide mid)", living),
        ("One-offs (Stage1/2, registration, deposits)", one),
        ("Student visa renewals (years 2 and 3)", renew),
    ]
    for label, v in pieces:
        L.append(f"| {label} | {rm(v)} | {inr(to_inr(v))} | {a_from_inr(to_inr(v))} |")
    tot_rm = tuition + living + one + renew
    L.append(f"| **Total drawn (before loan interest)** | **{rm(tot_rm)}** | **{inr(to_inr(tot_rm))}** | **{a_from_inr(to_inr(tot_rm))}** |")
    L.append("")
    L.append(
        "Published full-payment tuition (before SST) is RM34,900 + RM36,100 + RM37,500 = RM108,500. "
        "This model uses the **semester-payment** amounts (slightly higher) + **6% SST**, matching how draws usually land. "
        "DMU dual-degree uplift (GBP 450/level) is **not** included. "
        "Library deposit and personal bond are cash outlays (partly refundable later).\n"
    )

    L.append("### Semester tuition used (incl. SST)\n")
    L.append("| Sem | Level | RM incl. SST | Rs |\n|---|---|---:|---:|")
    labels = ["L1 S1", "L1 S2", "L2 S1", "L2 S2", "L3 S1", "L3 S2"]
    for lab, fee in zip(labels, SEM_TUITION_RM):
        L.append(f"| {lab} | | {rm(fee)} | {inr(to_inr(fee))} |")
    L.append("")

    L.append("## 3. Loan side after interest (same terms as QUT model)\n")
    L.append("| Item | Value |\n|---|---|")
    L.append("| Rate | 9% p.a., capitalised each year (mid-year draws get half a year of interest) |")
    L.append("| Moratorium | 3 years study + 12 months grace; first EMI ~Jul 2031 |")
    L.append("| Tenure | 15 years (180 monthly EMIs) |")
    L.append("")
    L.append("| | Rs | A$ |\n|---|---:|---:|")
    L.append(f"| Total drawn | {inr(base['drawn'])} | {a_from_inr(base['drawn'])} |")
    L.append(f"| Interest added before first EMI | {inr(base['interest_mor'])} | {a_from_inr(base['interest_mor'])} |")
    L.append(f"| Balance when EMIs start | {inr(base['p48'])} | {a_from_inr(base['p48'])} |")
    L.append(f"| **Minimum monthly EMI** | **{inr(emi)}** | **{a_from_inr(emi)}** |")
    L.append(f"| Minimum yearly repayment | {inr(emi*12)} | {a_from_inr(emi*12)} |")
    L.append(f"| Total repaid over 15 years | {inr(base['total_paid'])} | {a_from_inr(base['total_paid'])} |")
    L.append("")
    L.append("### Balance build-up\n")
    L.append("| Year | Phase | Drawn Rs | Interest Rs | Closing Rs |\n|---|---|---:|---:|---:|")
    phases = ["Study yr 1", "Study yr 2", "Study yr 3", "Grace (12 mo)"]
    for (b, op, dr, it, cl, _drm), ph in zip(base["rows"], phases):
        L.append(f"| {b} | {ph} | {inr(dr)} | {inr(it)} | {inr(cl)} |")
    L.append("")

    L.append("## 4. India income and living (same as QUT India-return stream)\n")
    L.append("| Item | Assumption |\n|---|---|")
    L.append("| Location | Metro IT hub, shared housing |")
    L.append("| Starting CTC | Rs 10-12 LPA (base Rs 11 LPA) |")
    L.append("| Tax | New regime; ~zero income tax at 10-12 LPA |")
    L.append(f"| Living | Modest bachelor all-in **Rs {inr(INDIA_LIVING_MO)}/mo** |")
    L.append("")

    L.append("## 5. Affordability: salary vs EMI\n")
    L.append(
        f"EMI is **Rs {inr(emi)}/mo** (~Rs {lakh(emi*12)} lakh/yr). "
        f"That is far below the QUT EMI (Rs 1,41,950), but still a large cut of a fresher salary.\n"
    )
    L.append(
        "| CTC | Take-home /mo | Living /mo | EMI /mo | **Gap /mo** | Gap /yr | Can he self-fund? |\n"
        "|---:|---:|---:|---:|---:|---:|---|"
    )
    for label, ctc, th in SALARIES:
        gap = th - INDIA_LIVING_MO - emi
        flag = "No" if gap < 0 else "Yes (thin)" if gap < 15_000 else "Yes"
        L.append(
            f"| Rs {ctc:.0f} LPA ({label}) | {inr(th)} | {inr(INDIA_LIVING_MO)} | {inr(emi)} | "
            f"**{inr(gap)}** | {inr(gap*12)} | **{flag}** |"
        )
    L.append("")
    L.append(
        f"**Break-even (self-funded):** about **Rs {inr(need_th)}/mo in hand** "
        f"(EMI + living) ~= **Rs {lakh(be_ctc)} LPA CTC** under a simple new-regime + PF model.\n"
    )

    th = 81_000
    gap = th - INDIA_LIVING_MO - emi
    L.append("## 6. Monthly snapshot at Rs 11 LPA (base)\n")
    L.append("| | Rs / month |\n|---|---:|")
    L.append(f"| Take-home | {inr(th)} |")
    L.append(f"| Metro living | {inr(INDIA_LIVING_MO)} |")
    L.append(f"| **EMI (minimum)** | **{inr(emi)}** |")
    L.append(f"| **Left / shortfall** | **{inr(gap)}** |")
    L.append("")
    if gap < 0:
        L.append(
            f"After living he has about **Rs {inr(th - INDIA_LIVING_MO)}** left. "
            f"The EMI is **Rs {inr(emi)}**, so the hole is about **Rs {inr(abs(gap))}/mo** "
            f"(**Rs {inr(abs(gap)*12)}/yr**) unless family/co-applicant covers it or the loan is smaller.\n"
        )
    else:
        L.append(
            f"After living and EMI he has about **Rs {inr(gap)}/mo** left "
            f"(**Rs {inr(gap*12)}/yr**). That is workable only if the job arrives on time and costs stay in band.\n"
        )

    # QUT comparison numbers (hardcoded from prior scenario for side-by-side)
    qut_emi = 141_950
    L.append("## 7. How this compares with QUT -> India\n")
    L.append("| | APU -> India (this file) | QUT -> India |\n|---|---|---|")
    L.append(f"| Study living in loan? | Yes (KL, ~RM1,800/mo) | No (uncle covers Brisbane board) |")
    L.append(f"| Total drawn (approx) | Rs {inr(base['drawn'])} | Rs ~1.10 crore |")
    L.append(f"| Monthly EMI | **Rs {inr(emi)}** | **Rs {inr(qut_emi)}** |")
    L.append(f"| Gap at Rs 11 LPA + living | **Rs {inr(gap)}/mo** | **Rs ~-87,950/mo** |")
    L.append("| Self-fund on Rs 10-12 LPA? | See table above | No |")
    L.append("")
    L.append(
        "APU is a much smaller rupee loan than QUT, so return-to-India is **far less damaging**. "
        "It can still be tight at the low end of the salary band once metro living is paid.\n"
    )

    L.append("## 8. Risks this scenario highlights\n")
    L.append(
        "- **RM/INR moves:** fees and living are in ringgit; a weaker rupee raises the INR loan size at drawdown.\n"
        "- **Semester vs full payment:** semester path + SST costs more than paying each year in full.\n"
        "- **Living overrun:** RM1,800/mo is APU's mid guide; single rooms and eating out push this up.\n"
        "- **Job timing / salary:** below ~break-even CTC, co-applicant carries the gap.\n"
        "- **Degree recognition / market:** India recruiters may weight a Malaysian private degree differently than a QUT BIT; salary outcomes are an assumption, not a placement guarantee.\n"
    )

    L.append("## 9. One-line takeaway\n")
    if gap < 0:
        L.append(
            f"APU + return to India on **Rs 10-12 LPA** still leaves a repayment gap at the mid point "
            f"(~**Rs {inr(abs(gap))}/mo** short at Rs 11 LPA), but the EMI (**Rs {inr(emi)}**) is about "
            f"**{qut_emi/emi:.1f}x smaller** than the QUT path, so family backup needed is much lighter.\n"
        )
    else:
        L.append(
            f"APU + return to India on **Rs 11 LPA** can just about self-fund: EMI **Rs {inr(emi)}/mo**, "
            f"about **Rs {inr(gap)}/mo** left after metro living - workable but not loose. "
            f"The EMI is about **{qut_emi/emi:.1f}x smaller** than the QUT-return path.\n"
        )

    text = "\n".join(L)
    for old, new in (("\u2192", "->"), ("\u2013", "-"), ("\u2014", "-"), ("\u2248", "~")):
        text = text.replace(old, new)
    with open("APU_return_to_India_scenario.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("drawn", round(base["drawn"]), "p48", round(base["p48"]),
          "EMI", round(emi), "gap@11", round(gap), "BE", be_ctc)


if __name__ == "__main__":
    main()
