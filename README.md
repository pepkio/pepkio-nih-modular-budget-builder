# NIH Modular Budget Builder

Programmatic calculation, personnel effort tracking, and financial validation engine for National Institutes of Health (NIH) modular research grant applications (R01, R21, R03, R15).

# Overview

Preparing a National Institutes of Health (NIH) grant proposal requires precise financial planning that satisfies strict Public Health Service (PHS) guidelines. Principal investigators (PIs), biostatisticians, bioinformaticians, and research administrators frequently spend significant time translating personnel effort into calendar or academic person-months, capping salaries according to federal mandates, applying institutional fringe rates, calculating Facilities & Administrative (F&A) indirect costs, and rounding direct costs into $25,000 modules.

The **NIH Modular Budget Builder** (`pepkio-nih-modular-budget-builder`) automates the construction and validation of NIH modular grant budgets. It provides a standardized calculation engine that handles institutional base salary (IBS) caps (Executive Level II salary cap), effort conversions, subaward/consortium indirect cost allocations, multi-year escalation rates, and effort ledger checks across overlapping grant mechanisms.

Researchers and research administration offices utilize this tool via Python programmatic scripts, command-line interface (CLI) commands, or interactive scenario modeling via the [NIH Modular Budget Builder web application](https://www.pepkio.com/tools/nih-modular-budget-builder).

Alternative search terms and related industry concepts:
* NIH grant budget calculator
* Modular grant budget template
* NIH salary cap calculation tool
* R01 modular budget generator
* Person-months effort calculator
* Direct vs indirect cost allocation
* F&A rate calculation engine
* Modified Total Direct Cost (MTDC) calculator
* Consortium direct costs budget tool
* Multi-year project budget planner

# Features

* **Automated Modular Direct Cost Rounding**: Automatically converts raw personnel, supplies, equipment, and subaward direct costs into standard $25,000 NIH direct cost modules up to the $250,000 per year limit.
* **Executive Level II Salary Cap Enforcement**: Automatically caps Institutional Base Salary (IBS) according to federal executive limits before calculating requested direct salaries.
* **Effort & Person-Month Conversion**: Calculates person-months from percentage effort for calendar (12-month), academic (9-month), and summer appointments.
* **Fringe Benefit Calculation**: Applies role-specific or institutional fringe rates to capped salary baselines.
* **F&A (Indirect Cost) Engine**: Computes Facilities & Administrative indirect costs based on Modified Total Direct Costs (MTDC), properly excluding equipment, tuition, and subaward direct costs exceeding $25,000.
* **Multi-Year Budget Escalation**: Models multi-year project periods (up to 5 years) with configurable annual salary escalation rates (e.g., 3% per year).
* **Consortium & Subaward Allocation**: Separates consortium direct costs and consortium F&A costs to ensure compliance with PHS 398 modular budget limits.
* **Effort Compliance Ledger**: Verifies total effort allocation across active grants to prevent over-commitment (>12 person-months or >100% total effort).
* **CSV Export & Data Exchange**: Generates structured JSON summaries and CSV budget tables formatted for administrative copy-pasting into Grants.gov or ERA Commons PHS 398 budget pages.

# Common Use Cases

### 5-Year NIH R01 Research Project Grant
A principal investigator in a molecular biology lab is preparing a 5-year R01 application involving a PI (25% effort), a co-investigator bioinformatician (15% effort), a full-time postdoctoral researcher (100% effort), and a graduate student researcher (50% effort). The tool calculates individual capped salaries, applies institutional fringe rates, factors in a 3% annual escalation across years 1–5, and calculates the exact number of $25,000 modules needed for each project year while computing the total F&A indirect cost based on the university's 55% MTDC rate.

### 2-Year NIH R21 Exploratory/Developmental Grant
A genomics laboratory is submitting an exploratory R21 proposal with a budget limit of $275,000 direct costs over two years (e.g., $175,000 in Year 1 for sequencing reagents and $100,000 in Year 2 for computational analysis). The tool verifies that each project year requests valid $25,000 modules (7 modules in Year 1, 4 modules in Year 2) without exceeding allowable subaward MTDC caps.

### Multi-Center Consortium Subaward Budgeting
A multi-institutional grant proposal involves a primary university and two subaward consortium sites. The lead investigator uses the tool to aggregate personnel costs, exclude individual subaward direct costs above $25,000 from the primary institution's MTDC base, and add consortium F&A costs as a direct cost module requirement per NIH policy.

### Investigator Effort Ledger Audit
A research management team needs to audit a co-investigator's committed effort across three active NIH R01 grants and a pending NSF award. The tool evaluates the investigator's effort ledger across all calendar months to ensure total effort does not exceed 100% (12.0 person-months).

# Why This Tool Exists

Grant budgeting in academic and biomedical research environments is historically conducted using ad-hoc Excel spreadsheets. Manual spreadsheet calculations introduce significant operational risks into grant submissions:

1. **Formula Corruption & Copy-Paste Errors**: Linking multi-year sheets and updating IBS or fringe rates manually frequently breaks cell references or formulas.
2. **Salary Cap Miscalculations**: Uncapped salary figures in preliminary budgets lead to unallowable cost requests, requiring post-award budget reductions or administrative rejections.
3. **Incorrect Modular Rounding**: Failing to round direct costs up to the nearest $25,000 module or exceeding the $250,000 direct cost cap without requesting prior approval from NIH program officers.
4. **Subaward F&A Accounting Mistakes**: NIH regulations require consortium F&A costs to be included in total direct cost modules requested by the primary institution, but excluded from the primary institution's F&A base calculation. Manual budget spreadsheets frequently apply indirect rates incorrectly to consortium figures.
5. **Over-Commitment of Investigator Effort**: Miscalculating person-months across academic vs. calendar appointments can cause effort over-commitment audit findings.

`pepkio-nih-modular-budget-builder` solves these issues by providing a deterministic, validated programmatic engine that enforces federal guidelines by design. Researchers can run calculations locally via Python or CLI, or evaluate scenarios using the web interface at https://www.pepkio.com/tools/nih-modular-budget-builder.

# Installation

Install the official package from [PyPI](https://pypi.org/project/pepkio-nih-modular-budget-builder/):

```bash
pip install pepkio-nih-modular-budget-builder
```

Requirements:
* Python >= 3.11
* `httpx` >= 0.27.0
* `pydantic` >= 2.0.0
* `click` >= 8.1.0

Source code and development instructions are available on the [GitHub repository](https://github.com/pepkio/pepkio-nih-modular-budget-builder).

# Quick Start

### Python Programmatic Interface

```python
import json
from pepkio_nih_modular_budget_builder import (
    BudgetInput,
    CostsConfig,
    ModularBudgetInput,
    PepkioClient,
    PersonnelMember,
)

# Initialize client (reads PEPKIO_API_KEY from environment or pass api_key="...")
with PepkioClient(api_key="your_api_key_here") as client:
    # Construct budget input object
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
                    id="pi-1",
                    name="Dr. Maria Rodriguez",
                    role="Principal Investigator",
                    appointmentType="calendar",
                    ibs=235000.0,  # IBS above NIH Cap ($221,900); automatically capped
                    effortPercent=25.0,  # 3.0 person-months
                    fringeRatePercent=28.5,
                ),
                PersonnelMember(
                    id="bioinfo-1",
                    name="Dr. Chen Wei",
                    role="Co-Investigator (Bioinformatics)",
                    appointmentType="academic",
                    ibs=110000.0,
                    effortPercent=22.22,  # 2.0 academic person-months
                    fringeRatePercent=26.0,
                ),
                PersonnelMember(
                    id="postdoc-1",
                    name="Dr. Sarah Jenkins",
                    role="Postdoctoral Scholar",
                    appointmentType="calendar",
                    ibs=68000.0,
                    effortPercent=100.0,  # 12.0 person-months
                    fringeRatePercent=24.0,
                ),
            ],
        ),
    )

    # Execute calculation
    run_result = client.run(budget_input)

    # Print run details
    print(f"Run ID: {run_result.run_id}")
    print(f"Status: {run_result.status}")

    # Inspect resulting budget summary
    if run_result.result:
        print(json.dumps(run_result.result, indent=2))
```

### Command Line Interface (CLI)

```bash
# Set your API key
export PEPKIO_API_KEY="your_api_key_here"

# Display available examples from the live manifest
pepkio-nih-modular-budget-builder manifest --examples

# Run a default R01 calculation example
pepkio-nih-modular-budget-builder run --example calculate_r01

# Execute calculation using a custom JSON payload
pepkio-nih-modular-budget-builder run --input-json '{
  "action": "calculate",
  "budget": {
    "fiscalYear": 2026,
    "costs": {
      "projectYears": 5,
      "faRatePercent": 55.0,
      "escalationRatePercent": 3.0
    },
    "personnel": [
      {
        "name": "Dr. Alex Taylor",
        "role": "Principal Investigator",
        "appointmentType": "calendar",
        "ibs": 195000,
        "effortPercent": 25.0,
        "fringeRatePercent": 28.0
      }
    ]
  }
}'
```

# Example Output

Running a modular budget calculation yields structured output detailing individual personnel calculations, direct cost totals, modular rounding allocations, MTDC exclusions, and indirect F&A costs across each project year:

```json
{
  "run_id": "run_budget_8f92a1c4",
  "status": "completed",
  "result": {
    "budget": {
      "fiscalYear": 2026,
      "projectYears": 5,
      "salaryCap": 221900.0,
      "personnelSummary": [
        {
          "name": "Dr. Maria Rodriguez",
          "role": "Principal Investigator",
          "appointmentType": "calendar",
          "personMonths": 3.0,
          "uncappedIbs": 235000.0,
          "cappedIbs": 221900.0,
          "baseSalaryRequested": 55475.0,
          "fringeBenefits": 15810.38,
          "totalPersonnelCost": 71285.38
        },
        {
          "name": "Dr. Chen Wei",
          "role": "Co-Investigator (Bioinformatics)",
          "appointmentType": "academic",
          "personMonths": 2.0,
          "uncappedIbs": 110000.0,
          "cappedIbs": 110000.0,
          "baseSalaryRequested": 24442.0,
          "fringeBenefits": 6354.92,
          "totalPersonnelCost": 30796.92
        },
        {
          "name": "Dr. Sarah Jenkins",
          "role": "Postdoctoral Scholar",
          "appointmentType": "calendar",
          "personMonths": 12.0,
          "uncappedIbs": 68000.0,
          "cappedIbs": 68000.0,
          "baseSalaryRequested": 68000.0,
          "fringeBenefits": 16320.0,
          "totalPersonnelCost": 84320.0
        }
      ],
      "yearlyBreakdown": [
        {
          "year": 1,
          "rawDirectPersonnel": 186402.30,
          "equipment": 12000.0,
          "consortiumDirect": 15000.0,
          "consortiumFa": 8250.0,
          "otherDirectCosts": 15000.0,
          "totalRawDirectCosts": 236652.30,
          "modulesRequested": 10,
          "modularDirectCost": 250000.0,
          "mtdcBase": 223000.0,
          "faRatePercent": 54.5,
          "indirectCostsFa": 121535.0,
          "totalYearCost": 371535.0
        }
      ],
      "cumulativeSummary": {
        "totalModularDirectCosts": 1250000.0,
        "totalIndirectCosts": 607675.0,
        "totalProjectFunding": 1857675.0
      }
    }
  }
}
```

# Scientific Background

Grant management in biomedical research requires navigating federal accounting standards defined by the NIH Grants Policy Statement (GPS) and Code of Federal Regulations (2 CFR 200 - Uniform Guidance).

### 1. Person-Months and Effort Allocation
NIH requests effort commitments to be expressed in **Person-Months** rather than hours or percentage effort alone. Person-months quantify the time dedicated to a project based on the individual's formal appointment period.

For a 12-month **Calendar Appointment**:
$$\text{Person-Months} = 12 \times \left( \frac{\text{Effort \%}}{100} \right)$$

For a 9-month **Academic Appointment**:
$$\text{Academic Person-Months} = 9 \times \left( \frac{\text{Effort \%}}{100} \right)$$

For a 3-month **Summer Appointment**:
$$\text{Summer Person-Months} = 3 \times \left( \frac{\text{Summer Effort \%}}{100} \right)$$

### 2. NIH Executive Level II Salary Cap
Under federal law, direct salary charges for individuals supported by NIH grants are restricted to the Executive Level II salary cap established by Congress. If an investigator's Institutional Base Salary (IBS) exceeds the cap limit ($\text{Cap}$), direct salary requested is calculated against the capped rate:

$$\text{Capped IBS} = \min(\text{IBS}, \, \text{Cap})$$

$$\text{Direct Salary Requested} = \text{Capped IBS} \times \left( \frac{\text{Effort \%}}{100} \right)$$

Fringe benefits are subsequently calculated on the capped salary amount:

$$\text{Fringe Benefits Cost} = \text{Direct Salary Requested} \times \left( \frac{\text{Fringe Rate \%}}{100} \right)$$

### 3. Modular Direct Cost Structure ($25,000 Modules)
NIH modular grant applications (R01, R21, R03, R15, R34) request direct costs in modules of $25,000 up to a maximum of $250,000 per year. Detailed categorical budgets (Form PHS 398) are replaced by modular estimates unless direct costs exceed $250,000 annually.

$$\text{Modules Count} = \left\lceil \frac{\text{Total Estimated Direct Costs}}{25000} \right\rceil$$

$$\text{Modular Direct Cost Request} = \min\left( \text{Modules Count} \times 25000, \, 250000 \right)$$

### 4. Modified Total Direct Costs (MTDC) & F&A Rates
Facilities & Administrative (F&A) indirect costs reimburse recipient institutions for facility maintenance, utilities, administrative staff, and core infrastructure. Indirect costs are computed on the **Modified Total Direct Cost (MTDC)** base, defined under 2 CFR 200.68.

MTDC excludes specific direct cost categories:
* Equipment (capital items $\ge \$5,000$)
* Patient care costs
* Tuition remission and student fees
* Rental costs of off-site facilities
* Subaward / Consortium direct costs in excess of $25,000 per subaward

$$\text{MTDC} = \text{Total Direct Costs} - \text{Equipment} - \text{Tuition} - \text{Exceeded Subaward Directs (> \$25k)}$$

$$\text{Indirect Costs (F\&A)} = \text{MTDC} \times \left( \frac{\text{F\&A Rate \%}}{100} \right)$$

### 5. Multi-Year Escalation Formula
Personnel salaries typically increase annually due to cost-of-living adjustments or institutional merit increases. For a project year $t \in \{1, 2, 3, 4, 5\}$ with annual escalation rate $r$:

$$\text{Escalated IBS}_t = \text{IBS}_1 \times (1 + r)^{t-1}$$

# Frequently Asked Questions

### What is an NIH modular budget?
An NIH modular budget is a simplified grant application budget format used for research project grant applications requesting up to $250,000 per year in direct costs. Instead of itemizing every pencil, test tube, or travel expense, direct costs are requested in modules of $25,000.

### Which grant mechanisms use the modular budget format?
Modular budget guidelines apply primarily to NIH R01 (Research Project Grants), R21 (Exploratory/Developmental Grants), R03 (Small Grants), R15 (Academic Research Enhancement Awards), and R34 (Clinical Trial Planning Grants) submitted by domestic U.S. institutions.

### How do I convert percentage effort into person-months?
Multiply the percentage effort by the total months of the academic or calendar appointment. For example, 25% effort on a 12-month calendar appointment equals $12 \times 0.25 = 3.0$ calendar person-months. On a 9-month academic appointment, 25% effort equals $9 \times 0.25 = 2.25$ academic person-months.

### What is the current NIH Executive Level II salary cap?
The NIH Executive Level II salary cap is set annually by federal legislation. For calendar year 2024/2025, the cap is set at $221,900 (subject to yearly updates by HHS). The `pepkio-nih-modular-budget-builder` package automatically updates and applies the applicable cap limit during calculations.

### How are institutional base salary (IBS) and salary cap limits enforced?
If an investigator's IBS is higher than the federal salary cap, the tool substitutes the cap limit as the max baseline salary before multiplying by effort percentage. The institution may pay the remaining salary from non-federal sources, but only the capped salary amount can be charged to the grant.

### What is the difference between direct costs and indirect (F&A) costs?
Direct costs directly support project execution (personnel salaries, laboratory reagents, specialized equipment, subawards). Indirect costs (Facilities & Administrative, F&A) support institutional infrastructure (lab utilities, library access, compliance oversight, building maintenance).

### How are indirect costs calculated on modular budgets?
Indirect costs are calculated by multiplying the institution's federally negotiated F&A rate by the Modified Total Direct Cost (MTDC) base. MTDC is calculated from actual estimated direct costs (or modular direct cost allocations) after subtracting excluded items like capital equipment and subaward amounts exceeding $25,000.

### Are consortium / subaward indirect costs included in the $250,000 modular limit?
No. NIH policy dictates that consortium indirect (F&A) costs are included in the total direct costs requested on the primary institution's cover sheet, but they do NOT count against the $250,000 direct cost module limit for determining modular budget eligibility.

### How does subaward F&A exclusion work for MTDC calculations?
When calculating the primary institution's MTDC base, only the first $25,000 of each subaward's total direct costs is included over the entire project period. Subaward direct costs beyond $25,000, as well as all subaward F&A costs, are excluded from the primary institution's F&A base.

### What items are excluded from the MTDC indirect cost base?
Under federal guidelines (2 CFR 200.68), MTDC excludes capital equipment (unit cost $\ge \$5,000$), tuition remission, patient care expenses, rental costs of off-site space, and the portion of individual subawards exceeding $25,000.

### What happens if direct costs exceed $250,000 in a single year?
If requested direct costs (excluding subaward F&A) exceed $250,000 in any project year, the application can no longer use the modular budget format and must submit a detailed categorical budget (SF424 R&R Budget Form), unless prior approval is granted by the NIH funding institute.

### How does annual salary escalation affect multi-year budgets?
Multi-year budgets apply an annual escalation rate (typically 3% to 5%) to personnel salaries and fringe benefits for years 2 through 5. The tool automatically projects escalated salaries for future project years when performing multi-year modular allocations.

### How are calendar months and academic/summer months differentiated in NIH budgets?
NIH requires effort to be explicitly designated as Calendar Months (12-month appointments), Academic Months (9-month appointments), or Summer Months (typically 1 to 3 months). The tool tracks these appointment types separately in personnel objects to ensure accurate person-month conversions.

### How can I export budget calculations for Grants.gov or ERA Commons?
The Python SDK and CLI export calculation results in structured JSON or CSV format. These tables match the layout required by PHS 398 Modular Budget forms, allowing easy copy-pasting into administrative submission systems.

### Does this tool verify investigator effort limits across multiple grants?
Yes. The `effort_check` action enables researchers and grant officers to construct an effort ledger for an investigator across multiple active and pending grants, flagging potential over-commitments (>12 calendar person-months).

# Web Application

The hosted [NIH Modular Budget Builder](https://www.pepkio.com/tools/nih-modular-budget-builder) provides an intuitive web interface for building NIH grant budgets. The web version provides an interactive interface, shareable links, protocol generation, printable worksheets, and visualization tools.

Researchers and research administrators can use the web interface to model personnel scenarios, adjust institutional F&A rates dynamically, generate printable budget justification summaries, and share read-only calculation links with institutional signing officials (AORs).

# Related Resources

* **GitHub Repository**: https://github.com/pepkio/pepkio-nih-modular-budget-builder
* **PyPI Package**: https://pypi.org/project/pepkio-nih-modular-budget-builder/
* **Web Application**: https://www.pepkio.com/tools/nih-modular-budget-builder

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

Pepkio provides analytical capabilities and technical support across computational biology domains, including:
* RNA-seq analysis
* Single-cell RNA-seq analysis
* Spatial transcriptomics analysis
* Functional enrichment analysis
* Custom bioinformatics workflows

Website: https://www.pepkio.com/

# Citation

If you use `pepkio-nih-modular-budget-builder` or the Pepkio web application in grant planning or research publications, please cite:

```bibtex
@software{pepkio_nih_modular_budget_builder,
  author       = {Pepkio Team},
  title        = {pepkio-nih-modular-budget-builder: NIH Modular Grant Budget Calculation and Validation Engine},
  year         = {2026},
  publisher    = {Pepkio},
  url          = {https://github.com/pepkio/pepkio-nih-modular-budget-builder}
}
```

# License

This project is licensed under the MIT License - see the `LICENSE` file for details.

# Keywords

NIH modular budget builder, NIH grant budget calculator, modular budget template, R01 budget builder, R21 grant calculator, NIH salary cap calculator, person months calculator, grant effort ledger, NIH F&A rate calculator, modified total direct costs, MTDC calculator, consortium direct costs, subaward indirect costs, Institutional Base Salary, Executive Level II salary cap, modular direct costs, grant personnel cost calculator, fringe rate calculation, academic effort allocation, calendar month conversion, summer effort calculator, NIH R03 budget, NIH R15 budget, SF424 grant budget, NIH funding calculator, grant budget Python package, NIH budget escalation rate, research project grant budget, NIH subaward budget builder, grant proposal budget tool, research budget automation, bioinformatic grant planning, PHS 398 modular budget, direct cost rounding, NIH grant financial planner, how to calculate NIH modular budget, how to convert percent effort to person months, NIH Executive Level II salary cap limits, how to round grant direct costs to 25k modules, calculating F&A indirect costs for NIH grants, subaward MTDC exclusions for consortium grants, 5 year R01 budget planning template Python, modular grant budget vs detailed budget NIH, NIH grant effort allocation calculator, Institutional Base Salary cap calculation formula, academic year vs calendar year effort calculation, Python client for NIH grant budget calculations, automated NIH modular budget generation CSV, grant administration tool for NIH R01 applications, subaward direct vs indirect cost calculation NIH, how to estimate fringe benefit costs for NIH grants, NIH budget escalation rate formula 3 percent, checking investigator effort across NIH grants, generating NIH modular budget justification table, NIH modular budget limit 250k per module year
