"""Scenario stream: QUT degree, then return to India for work (affordability stress test).

Separate from the Australia fact-check. Same base QUT loan / EMI; only income and living change.
Confirmed 2026-11-18:
  - Return right after graduation (~mid-2030); India job ~6 months later (~Jan 2031)
  - Metro IT hub, shared/rented housing
  - Mid salary band Rs 10-12 LPA
  - Same loan as Australia base case (option 4a)
  - Focus: can India salary cover INR EMI + living?

Run: python calc_qut_india_return.py
Writes: QUT_return_to_India_scenario.md
"""
from calc_qut_report import (
    FX, loan_for, inr, a, rs, SEM_FEE, PERSONAL_PER_SEM, VISA, OSHC,
)

# Same base loan as Australia fact-check
BASE = loan_for(set())
EMI = BASE["emi"] * FX          # INR per month
EMI_Y = EMI * 12
DRAWN_INR = BASE["drawn"] * FX
P48_INR = BASE["p48"] * FX

# Mid band salaries (CTC, LPA) -> monthly take-home estimates under new tax regime FY25-26 style
# Assumptions: ~50% basic, employee PF 12% of basic, prof tax ~200/mo, income tax ~0 up to ~12.75L taxable
SALARIES = [
    # (label, ctc_lpa, takehome_mo)
    ("Low of band", 10.0, 78_000),
    ("Mid (base)", 11.0, 81_000),
    ("High of band", 12.0, 90_000),
]

# Metro shared living (Bengaluru-style bachelor, modest)
LIVING = [
    ("Shared PG / co-living with meals (or share of flat + food)", 12_000),
    ("Extra food / eating out", 4_000),
    ("Local transport (metro / bus / bike)", 3_000),
    ("Phone + internet", 1_000),
    ("Personal, laundry, misc", 3_000),
    ("Health insurance / medical buffer", 1_500),
    ("Family visit / contingency buffer", 2_500),
]
LIVING_MO = sum(v for _, v in LIVING)


def lakh(x):
    return f"{x / 1e5:.2f}"


def main():
    L = []
    L.append("# Scenario: QUT study, then return to India for a job\n")
    L.append(
        "Prepared 18 Nov 2026. **Separate risk stream** from `QUT_loan_fact_check_report.md` "
        "(that file assumes he stays and works in Brisbane). "
        "Same QUT loan and EMI; only the income and living side change. "
        f"FX for reference only: 1 A$ = Rs {FX}. Working: `calc_qut_india_return.py`.\n"
    )

    L.append("## 1. What this scenario is testing\n")
    L.append(
        "He finishes QUT (~Jun 2030), returns to India, finds a metro IT job about 6 months later (~Jan 2031), "
        "and the education-loan EMI still starts on schedule (~Jul 2031). "
        "Question: **can a mid Rs 10-12 LPA India salary cover the minimum EMI plus metro living?**\n"
    )

    L.append("## 2. Loan side (unchanged from Australia base case)\n")
    L.append("| | Rs | A$ |\n|---|---:|---:|")
    L.append(f"| Total drawn for QUT | {inr(DRAWN_INR)} | {a(BASE['drawn'])} |")
    L.append(f"| Balance when EMIs start (Jul 2031) | {inr(P48_INR)} | {a(BASE['p48'])} |")
    L.append(f"| **Minimum monthly EMI** | **{inr(EMI)}** | **{a(BASE['emi'])}** |")
    L.append(f"| Minimum yearly repayment | {inr(EMI_Y)} | {a(BASE['emi']*12)} |")
    L.append("")
    L.append(
        "The loan is an **INR** obligation. Earning in India does not shrink the EMI. "
        "It removes the AUD salary that was carrying the repayment in the Australia plan.\n"
    )

    L.append("## 3. India income and living (assumptions)\n")
    L.append("| Item | Assumption | Tag |\n|---|---|---|")
    L.append("| Location | Metro IT hub (Bengaluru / Hyderabad / Pune / Mumbai style), shared housing | [A] |")
    L.append("| Starting CTC | Rs 10-12 LPA mid band (base Rs 11 LPA) | [A] |")
    L.append("| Tax | New regime; ~zero income tax at 10-12 LPA after standard deduction + 87A rebate (FY 2025-26 rules held flat) | [P]/[A] |")
    L.append("| Take-home | After employee PF (~12% of basic) and professional tax; employer PF/gratuity not in hand | [A] |")
    L.append(f"| Living | Modest bachelor shared PG/flat all-in **Rs {inr(LIVING_MO)}/mo** | [E] |")
    L.append("| Job start | ~Jan 2031; first EMI ~Jul 2031 (same timeline as Australia file) | [A] |")
    L.append("")
    L.append("### Living split (monthly)\n")
    L.append("| Item | Rs/mo |\n|---|---:|")
    for label, v in LIVING:
        L.append(f"| {label} | {inr(v)} |")
    L.append(f"| **Total living** | **{inr(LIVING_MO)}** |")
    L.append("")

    L.append("## 4. Affordability: salary vs EMI (the stress test)\n")
    L.append(
        f"EMI alone is **Rs {inr(EMI)}/mo** (~Rs {lakh(EMI_Y)} lakh/yr). "
        f"That is already more than a full Rs 12 LPA CTC before living costs.\n"
    )
    L.append(
        "| CTC | Take-home /mo | Living /mo | EMI /mo | **Gap /mo** | Gap /yr | Can he self-fund? |\n"
        "|---:|---:|---:|---:|---:|---:|---|"
    )
    for label, ctc, th in SALARIES:
        gap = th - LIVING_MO - EMI
        flag = "No" if gap < 0 else "Yes"
        L.append(
            f"| Rs {ctc:.0f} LPA ({label}) | {inr(th)} | {inr(LIVING_MO)} | {inr(EMI)} | "
            f"**{inr(gap)}** | {inr(gap*12)} | **{flag}** |"
        )
    L.append("")

    # Break-even CTC: need take-home >= EMI + living. Approximate take-home ~ 0.78 of CTC at mid levels,
    # but above ~12.75L tax appears. For break-even message use required in-hand first.
    need_th = EMI + LIVING_MO
    # Rough CTC needed: iterate simple model
    def takehome_from_ctc(ctc):
        basic = 0.50 * ctc
        epf = 0.12 * basic
        pt = 2_400
        # taxable after 75k std ded
        taxable = max(ctc - 75_000, 0)
        # new regime tax + 87A up to 12L taxable -> 0 if taxable <= 12L
        # For taxable > 12L: compute slabs then cess; no full 87A
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
            tax *= 1.04  # cess
        return ctc - epf - pt - tax

    be_ctc = None
    for ctc in range(1_500_000, 6_000_000, 10_000):
        if takehome_from_ctc(ctc) / 12 >= need_th:
            be_ctc = ctc
            break
    L.append(
        f"**Break-even (self-funded):** he needs about **Rs {inr(need_th)}/mo in hand** "
        f"(EMI + living). That is roughly **Rs {lakh(be_ctc)} LPA CTC** under a simple new-regime + PF model "
        f"(~Rs {be_ctc/1e5:.0f} LPA). A normal fresher Rs 10-12 LPA offer is nowhere near this.\n"
    )

    L.append("## 5. Monthly snapshot at Rs 11 LPA (base)\n")
    th = 81_000
    gap = th - LIVING_MO - EMI
    L.append("| | Rs / month |\n|---|---:|")
    L.append(f"| Take-home | {inr(th)} |")
    L.append(f"| Metro living | {inr(LIVING_MO)} |")
    L.append(f"| **EMI (minimum)** | **{inr(EMI)}** |")
    L.append(f"| **Shortfall** | **{inr(gap)}** |")
    L.append("")
    L.append(
        f"After living costs he has about **Rs {inr(th - LIVING_MO)}** left for everything else. "
        f"The EMI is **Rs {inr(EMI)}**. The hole is about **Rs {inr(abs(gap))}/mo** "
        f"(**Rs {inr(abs(gap)*12)}/yr**), which a co-applicant or family would have to cover "
        f"unless the loan is prepaid or restructured.\n"
    )

    L.append("## 6. How this compares with the Australia plan\n")
    L.append("| | Work in Brisbane (main fact-check) | Return to India (this scenario) |\n|---|---|---|")
    L.append(f"| Monthly EMI | Rs {inr(EMI)} / A${a(BASE['emi'])} | Same EMI in Rs |")
    L.append("| Income currency | AUD salary | INR salary |")
    L.append("| Year-1 leftover after tax, living, EMI | ~A$406/yr (tight but near break-even at A$70k) | **Large monthly shortfall at Rs 10-12 LPA** |")
    L.append("| Who realistically pays the EMI? | Mostly him, if the job arrives on time | Mostly co-applicant / family for many years |")
    L.append("")
    L.append(
        "Staying in Australia was already tight. Returning to India on a normal graduate salary "
        "turns the same loan into a **family cashflow problem**, not a graduate cashflow problem.\n"
    )

    L.append("## 7. Risks this scenario highlights\n")
    L.append(
        "- **Scale mismatch:** QUT costs were priced in AUD; a mid India graduate salary cannot service the INR EMI.\n"
        "- **Co-applicant exposure:** banks will expect the Indian co-applicant to keep paying if he cannot.\n"
        "- **Career path:** even strong India rises (e.g. to Rs 20-25 LPA in a few years) still leave a multi-year gap versus EMI + living.\n"
        "- **No AUD earnings hedge:** in Australia, a weaker INR makes the EMI easier in AUD terms; that relief disappears if he earns only INR.\n"
        "- **Not a reason to skip QUT by itself** - it is a reason to treat **return-to-India without family backup** as a high-risk outcome, and to plan prepaid years / collateral / co-applicant capacity before drawing the loan.\n"
    )

    L.append("## 8. One-line takeaway\n")
    L.append(
        f"If he studies at QUT and returns to India on a **Rs 10-12 LPA** metro job, "
        f"the minimum EMI of **Rs {inr(EMI)}/mo** alone exceeds take-home; "
        f"with shared-rent living the shortfall is about **Rs {inr(abs(81_000 - LIVING_MO - EMI))}/mo**. "
        f"This path only works if family/co-applicant can carry most of the repayment for years, "
        f"or if a large part of the loan is never drawn / is prepaid.\n"
    )

    text = "\n".join(L)
    for old, new in (
        ("\u2192", "->"), ("\u2013", "-"), ("\u2014", "-"),
        ("\u2248", "~"), ("\u2018", "'"), ("\u2019", "'"),
    ):
        text = text.replace(old, new)
    with open("QUT_return_to_India_scenario.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("EMI", round(EMI), "living", LIVING_MO, "gap@11L", round(81_000 - LIVING_MO - EMI))
    print("break-even CTC", be_ctc)


if __name__ == "__main__":
    main()
