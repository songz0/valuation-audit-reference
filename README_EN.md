# Valuation Audit Reference — AI-Powered Workpaper Review Skill

> A Claude Code / Codex skill for reviewing asset-valuation workpapers (DCF / Comparable / Word reports).  
> Turns an AI agent into a disciplined valuation auditor.

**Recommended model**: Claude Opus 4.6 (all real-world examples in this Skill were produced by Opus 4.6). DeepSeek, GLM, MiMo, and other models also work, though results may vary.

**Coverage note**: This version focuses on **Income Approach (DCF)** workpaper review. Market Approach and Word report review are provided as general frameworks. Cost Approach / Asset-based Approach is not yet covered and may be added in future iterations.

---

## 🔴 Compliance Warning

Audit and valuation workpapers contain highly confidential business data — financial projections, profitability models, customer lists, equity structures, and related-party transactions of listed or pre-IPO companies.

**When using this Skill, please ensure:**

1. **Use an enterprise API with Zero Data Retention policy** whenever possible. Claude Enterprise, OpenAI Enterprise, etc. all support this.
2. **If using the web interface, desensitize company names and absolute financial figures** before sending. For example: replace the full company name with "Target Company A", replace "427.2 million" with "approximately 400 million".
3. **Never upload sensitive private data to public cloud services** that use your data for model training.
4. **This Skill includes a knowledge base powered by Google NotebookLM**, covering professional exam textbooks and regulatory databases relevant to asset-valuation auditing. The knowledge base is tied to the author's personal Google account and cannot be directly shared. The script `query_knowledge_base.py` provides the query pipeline — you can use the same script to connect to your own NotebookLM knowledge base (requires your own Google account and uploaded materials). This repository does not contain any knowledge base data.
5. **This Skill uses iFinD (Tonghuashun) enterprise data lookup as an auxiliary verification tool** — for example, verifying company names, registered capital, business scope, and equity structures against workpapers. `templates/ifind_batch_query_template.xlsx` is a batch query template example used by the author (contains no company data). If you don't have an iFinD account, you can skip this file and use public channels such as the National Enterprise Credit Information Publicity System instead.

**Disclaimer**: This Skill is a reference tool. All outputs are draft reviews, not legal opinions or professional conclusions. Users bear full responsibility for any consequences arising from the use of this Skill.

---

## What This Skill Does

Give an AI agent a valuation workpaper (Excel DCF model / comparable analysis / Word valuation report), and it will:

1. **Automatically scan the workpaper** — identify visible/hidden sheets, skip hidden areas to avoid false positives
2. **Run a three-phase audit** — conclusion verification → cell-level formula tracing → assumption evidence assessment
3. **Output a graded report** — 🔴 Fatal → 🟡 Sanity Check → 🔵 Best Practice
4. **Tag every finding with cell coordinates** — `Sheet name + row/column`, so the reviewer can locate it directly

---

## Coverage

### Excel Workpaper Audit (9 Chapters)

| Ch. | Content |
|:--|:--|
| 0 | Agent execution flow & output standards (three-phase audit, visibility filtering, root-cause tracing) |
| 1 | Income Approach (DCF) audit points (formula integrity, 7 common WACC errors, terminal value convergence, management bias testing) |
| 2 | Market Approach audit points (comparable selection, LTM alignment, EV/EBITDA caliber, DLOC/DLOM) |
| 3 | General Excel workpaper audit standards (color coding, data provenance, structure standards) |
| 4 | Three-statement model cross-check (IS/BS/CF linkage, circular reference handling) |
| 5 | EBITDA normalization adjustments (6 adjustment categories, conservative/aggressive basis) |
| 6 | Due diligence audit checklist (Financial / Commercial / Legal / Operational / HR / IT / ESG) |
| 7 | Excel data format standards |
| 8 | Special scenarios & regulatory red lines |

### Word Report Audit (7 Dimensions)

| Dim. | Content |
|:--|:--|
| 1 | Proofreading (typos / placeholders / formatting) |
| 2 | Writing quality + terminology accuracy |
| 3 | Content substance review (scope / basis / special items / valuation techniques / procedure compliance / post-balance-sheet) |
| 4 | Cross-reference error detection (report ↔ workpaper inconsistencies) |
| 5 | Template compliance check (professional standards level) |
| 6 | Excel linkage review (Word ↔ Excel data consistency) |
| 7 | Company data verification (via iFinD or public channels) |

---

## Real Audit Example (Desensitized)

The following is a summary output from an actual income-approach workpaper review performed by this Skill:

> **Target Company A — Income Approach Workpaper Review Report**
>
> | Item | Content |
> |:--|:--|
> | **Valuation Date** | December 31, 2025 |
> | **Model Type** | FCFF → WACC discount → EV → subtract interest-bearing debt → equity value |
> | **Review Conclusion** | 🔴 **3 fatal formula errors** found, causing equity value overstatement of approximately **7.3%** |
> | **Largest Single Error** | Interest-bearing debt deduction omitted long-term borrowings → equity overstatement of **~6.6%** |
> | **Coverage** | 49 of 116 sheets visible; **38 sheets** audited line-by-line (9 primary + 29 secondary) |
> | **Key Risk** | Gross margin assumption cliff (92%→50%) is the most sensitive variable (±1ppt→±9%), terminal value = 72.2% of EV |

**Sample Fatal Error**:

```
🔴 F-1: Double deduction in income tax loss carryforward formula
Location: 14-2 Income Tax Calculation E74
Issue: E74 (current period loss addition) = +8,105,700 (profitable year, should be 0)
       E75 (current period utilization) = +8,105,700 (FIFO utilization, correct)
       Balance formula adds both → carryforward pool over-reduced by 8.1M
Impact: 2027→2028→2029 opening balances carry forward the 8.1M error
Fix: Change E74 formula to =MIN(0, B54), zero for profitable years

🔴 F-2: Long-term borrowings omitted from debt deduction
Location: Conclusion table bridge formula
Issue: EV 491.3M → subtracts interest-bearing debt 64.1M → but omits long-term borrowings
Impact: Equity value overstated by ~28M (6.6%)
```

---

## Installation

```bash
# Clone to Codex skills directory
git clone https://github.com/YOUR_USERNAME/valuation-audit-reference.git ~/.agents/skills/valuation-audit-reference

# Or copy to Claude Code plugin directory
cp -r valuation-audit-reference ~/.claude/plugins/config/
```

### Usage

```bash
# Trigger in Claude Code
/valuation-audit-reference  # Audit the currently open workpaper

# NotebookLM knowledge base query (requires your own Google account + self-built knowledge base)
python ~/.agents/skills/valuation-audit-reference/scripts/query_knowledge_base.py "Standards and regulatory basis for risk-free rate selection in WACC"
```

> ⚠️ **NotebookLM knowledge base must be created by you**: The script `query_knowledge_base.py` provides the query pipeline, but the knowledge base content must be uploaded and maintained by you in Google NotebookLM (CPA textbooks, valuation standards, etc.). The author's knowledge base is tied to a personal Google account and cannot be directly shared.

---

## Repository Structure

```
valuation-audit-reference/
├── LICENSE                              # All rights reserved
├── README.md                            # Chinese version
├── README_EN.md                         # This file (English)
├── SKILL.md                             # Skill main file (trigger logic, output format, workflow)
├── references/
│   ├── valuation_audit_checklist.md     # Excel workpaper audit checklist (9 chapters, 695 lines)
│   └── word_report_audit_checklist.md   # Word report audit checklist (7 dimensions)
├── scripts/
│   └── query_knowledge_base.py          # NotebookLM knowledge base query script
└── templates/
    └── ifind_batch_query_template.xlsx  # iFinD batch query template example (no company data)
```

---

## Output Format

All findings are classified into three severity levels:

| Level | Meaning |
|:--|:--|
| 🔴 **Fatal** | Critical logic error — model breaks, formula errors, material valuation misstatement |
| 🟡 **Sanity Check** | Parameter warning — assumption outliers, high terminal value %, missing adjustments |
| 🔵 **Best Practice** | Standards suggestion — hardcoded values, missing provenance annotations, color code violations |

**Every finding must include**: Sheet name + cell coordinates + issue description + fix suggestion + quantified impact

---

## License

All rights reserved. See [LICENSE](LICENSE).

This repository is provided for private/internal use only. Reproduction, modification, distribution, sublicensing, or publication without explicit written permission from the repository owner is prohibited.