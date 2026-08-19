# pepkio-nih-modular-budget-builder

A Python client for programmatically calculating, rounding, and validating NIH modular grant proposal budgets, personnel effort allocations, and institutional F&A indirect cost rates.

# What It Does

`pepkio-nih-modular-budget-builder` automates financial planning and compliance validation for National Institutes of Health (NIH) modular research grant applications (such as R01, R21, R03, and R15 awards). It enforces Institutional Base Salary (IBS) caps under Executive Level II federal limits, converts effort percentages into calendar or academic person-months, applies fringe rates and multi-year salary escalation, rounds direct costs into standard $25,000 NIH modules up to $250,000 per year, and computes Facilities & Administrative (F&A) indirect costs on Modified Total Direct Cost (MTDC) bases.

# Features

- **Executive Level II Salary Cap Enforcement**: Automatically caps base salaries exceeding federal limits before calculating direct salary requests.
- **Effort & Person-Month Conversion**: Converts percentage effort into calendar (12-month), academic (9-month), and summer person-months.
- **Modular Direct Cost Rounding**: Groups raw personnel, supplies, equipment, and consortium costs into standard $25,000 NIH direct cost modules.
- **F&A & MTDC Indirect Engine**: Calculates indirect costs while properly excluding capital equipment ($\ge \$5,000$) and subaward direct costs exceeding $25,000.
- **Consortium & Subaward Allocation**: Separates consortium direct costs and subaward F&A costs according to PHS 398 policy guidelines.
- **Multi-Year Project Escalation**: Projects multi-year grant budgets (up to 5 years) with configurable annual salary escalation rates.
- **Effort Compliance Ledger**: Audits total investigator effort across active and pending awards to prevent over-commitment (>12 person-months).

# Installation

```bash
pip install pepkio-nih-modular-budget-builder
```

# Quick Example

```python
import os
from pepkio_nih_modular_budget_builder import (
    BudgetInput,
    CostsConfig,
    ModularBudgetInput,
    PepkioClient,
    PersonnelMember,
)

api_key = os.getenv("PEPKIO_API_KEY", "your_api_key_here")

with PepkioClient(api_key=api_key) as client:
    budget_input = ModularBudgetInput(
        action="calculate",
        budget=BudgetInput(
            fiscalYear=2026,
            costs=CostsConfig(
                projectYears=5,
                faRatePercent=54.5,
                escalationRatePercent=3.0,
                equipment=12000.0,
                consortiumDirect=15000.0,
                consortiumFa=8250.0,
            ),
            personnel=[
                PersonnelMember(
                    name="Dr. Maria Rodriguez",
                    role="Principal Investigator",
                    appointmentType="calendar",
                    ibs=235000.0,  # Above NIH cap; automatically capped
                    effortPercent=25.0,  # 3.0 person-months
                    fringeRatePercent=28.5,
                ),
                PersonnelMember(
                    name="Dr. Chen Wei",
                    role="Co-Investigator",
                    appointmentType="academic",
                    ibs=110000.0,
                    effortPercent=22.22,  # 2.0 academic person-months
                    fringeRatePercent=26.0,
                ),
            ],
        ),
    )

    result = client.run(budget_input)
    print(f"Status: {result.status}")
    print(f"Run ID: {result.run_id}")
    if result.result:
        budget = result.result.get("budget", {})
        print(f"Cumulative Project Total: ${budget.get('cumulativeSummary', {}).get('totalProjectFunding', 0):,.2f}")
```

# Typical Use Cases

- **5-Year NIH R01 Research Grant**: Modeling multi-year personnel effort, annual salary escalation (e.g. 3%), fringe benefits, and $25,000 modular direct cost allocations.
- **2-Year NIH R21 Exploratory Grant**: Structuring uneven annual modular requests ($175,000 in Year 1, $100,000 in Year 2) while verifying module thresholds.
- **Multi-Center Subaward Allocation**: Computing consortium direct and F&A allocations with MTDC exclusion rules ($25,000 subaward threshold).
- **Investigator Effort Ledger Audit**: Verifying cross-grant effort commitments across calendar and academic appointments to prevent over-commitment (>100% or >12 person-months).

# Scientific Background

Grant financial planning for NIH awards follows federal accounting standards defined in the NIH Grants Policy Statement and 2 CFR 200 (Uniform Guidance):

- **Person-Months**: Dedicated project time based on formal appointment: $\text{Person-Months} = \text{Appointment Months} \times (\text{Effort \%} / 100)$.
- **Executive Level II Salary Cap**: Direct salary requested is capped at federal mandates: $\text{Direct Salary} = \min(\text{IBS}, \, \text{Cap}) \times (\text{Effort \%} / 100)$.
- **Modular Direct Costs**: Direct costs requested in $25,000 increments up to the $250,000/year limit: $\text{Modules} = \lceil \text{Direct Costs} / 25000 \rceil$.
- **MTDC & F&A Indirect Costs**: Facilities & Administrative rates apply to Modified Total Direct Costs, excluding capital equipment ($\ge \$5,000$) and subaward direct costs beyond $25,000.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/nih-modular-budget-builder

The web application provides visual cost breakdowns, interactive scenario modeling, PHS 398 budget worksheets, and shareable calculation links.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-nih-modular-budget-builder

Web Application: https://www.pepkio.com/tools/nih-modular-budget-builder

Source code and issue tracking are maintained on [GitHub](https://github.com/pepkio/pepkio-nih-modular-budget-builder).

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

NIH modular budget, grant budget calculator, salary cap calculator, effort conversion, person-months calculator, modular direct costs, F&A rate calculator, modified total direct costs, MTDC calculator, consortium direct costs, subaward indirect costs, institutional base salary, executive level II cap, grant personnel costs, fringe benefit calculator, academic effort, calendar months effort, R01 budget, R21 budget, PHS 398 budget, grant budget Python, multi-year grant budget, subaward budget, NIH grant tools, grant financial planner, NIH modular budget calculator Python, convert effort percentage to person months, NIH Executive Level II salary cap limits, round grant direct costs to 25k modules, calculate indirect costs F&A for NIH grants, subaward MTDC exclusions for consortium grants, 5 year R01 grant budget template, NIH modular vs detailed budget, NIH grant effort allocation calculator, institutional base salary cap calculation, academic vs calendar effort calculation, automated NIH modular budget Python SDK, grant administration tool for NIH applications, subaward direct vs indirect cost calculation, estimate fringe benefit costs for NIH grants, NIH salary escalation calculation, auditing investigator effort across NIH grants, generating NIH modular budget justification
