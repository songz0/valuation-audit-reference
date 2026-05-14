# 资产评估审计 AI 审核 Skill

> Claude Code / Codex skill，用于审核评估底稿（DCF / 市场法 / Word 评估报告）。  
> 把 AI Agent 变成一个纪律严明的估值审核员。

**推荐模型**：Claude Opus 4.6（本 Skill 的实战示例均基于 Opus 4.6）。DeepSeek、GLM、MiMo 等国产模型也可使用，效果可能略有差异。

**覆盖说明**：本版本着重审核**收益法（DCF）**底稿，市场法和 Word 报告审核为通用框架。成本法/基础法暂未覆盖，后续可迭代补充。

📄 English version: [README_EN.md](README_EN.md)

---

## 🔴 合规警告

审计与评估底稿包含高度机密的商业数据——上市/拟上市公司的财务预测、盈利模型、客户名单、股权结构、关联交易等内幕信息。

**在使用本 Skill 时，请务必确保：**

1. **优先使用企业版 API（Zero Data Retention 零数据保留政策）**。Claude Enterprise、OpenAI Enterprise 等均支持零数据保留。
2. **如果使用网页版，请务必对企业名称、核心财务绝对值进行脱敏**后再发送。例如：将公司全称替换为"目标公司A"，将"X.XX亿元"替换为"约X亿元"。
3. **绝勿将包含敏感信息的私有数据上传至供模型训练的公有云端**。
4. **本 Skill 搭配了一个基于 Google NotebookLM 的专业知识库**，涵盖资产评估审计相关的考试教材和法规文库，用于查询 checklist 未覆盖的准则条文、行业基准和方法论细节。该知识库绑定了作者的个人 Google 账户，无法直接共享。脚本 `query_knowledge_base.py` 提供了查询管道——你可以用同样的脚本接入自己创建的 NotebookLM 知识库（需自备 Google 账号并上传自己的教材/法规文档）。本仓库不包含知识库数据本身。
5. **本 Skill 使用 iFinD（同花顺）的企业工商信息查询功能作为辅助验证工具**——例如在审核报告中核对企业名称、注册资本、经营范围、股权结构等公开信息是否与底稿一致。`templates/ifind_batch_query_template.xlsx` 是作者实际使用的批量查询模板示例（不含企业数据），展示了如何批量核对目标公司信息。如果你没有 iFinD 账号，可以忽略此文件，改用手动查询国家企业信用信息公示系统等公开渠道。

**免责声明**：本 Skill 为参考工具，所有输出均为审查草稿，不替代专业评估师和审计师的判断。使用本 Skill 产生的任何后果由使用者自行承担。

---

## 这个 Skill 做什么

把一份评估底稿（Excel DCF 模型 / 市场法比较 / Word 评估报告）交给 AI Agent，它会：

1. **自动扫描底稿**——识别可见/隐藏 Sheet，跳过隐藏区域避免误报
2. **三阶段审核**——结论验证 → 逐表公式溯源 → 假设依据审计
3. **分级输出**——🔴 致命错误 → 🟡 参数预警 → 🔵 规范建议
4. **每项发现标注单元格坐标**——`Sheet名 + 行列`，审核人可直接定位

---

## 覆盖范围

### Excel 底稿审查（9 章）

| 章 | 内容 |
|:--|:--|
| 〇 | Agent 执行流与输出规范（三阶段审核、可见性筛选、根因追溯） |
| 一 | 收益法（DCF）审计要点（公式完整性、WACC 七大错误、终值收敛、管理层偏向测试） |
| 二 | 市场法审计要点（可比性验证、LTM 时间对齐、EV 口径排雷、DLOC/DLOM） |
| 三 | 通用 Excel 底稿审计规范（颜色编码、数据溯源、结构规范） |
| 四 | 三表模型交叉校验（IS/BS/CF 勾稽、循环引用处理） |
| 五 | EBITDA 正常化调整（六类调整项、保守/激进口径） |
| 六 | 尽职调查审计清单（财务/商业/法律/运营/HR/IT/ESG） |
| 七 | Excel 数据格式规范 |
| 八 | 特殊场景与监管红线 |

### Word 报告审核（7 维度）

| 维度 | 内容 |
|:--|:--|
| 一 | 低级错误检查（错别字/占位符/格式） |
| 二 | 描述优化 + 术语核对 |
| 三 | 内容实质性审核（范围/依据/特别事项/估值技术/程序合规/权属期后） |
| 四 | 错误引用检查（报告与底稿之间的交叉引用错误） |
| 五 | 模板合规检查（准则条文级） |
| 六 | Excel 勾稽审核（Word ↔ Excel 数据一致性） |
| 七 | 企业信息核对（通过 iFinD 或公开渠道验证） |

---

## 审核实战示例（已脱敏）

以下为本 Skill 实际审核某收益法底稿的输出摘要：

> **目标公司A — 收益法底稿审核报告**
>
> | 项目 | 内容 |
> |:--|:--|
> | **估值基准日** | 2025年12月31日 |
> | **模型类型** | FCFF → WACC折现 → EV → 扣减有息负债 → 股东全部权益价值 |
> | **审核结论** | 🔴 发现 **3项致命公式错误**，合计导致股权价值高估约 **7.3%** |
> | **最大单项错误** | 有息负债扣减遗漏长期借款 → 股权高估 **~6.6%** |
> | **审核覆盖** | 116张Sheet中49张可见；逐表审核 **38张**（9张一级明细 + 29张二级辅助） |
> | **主要风险** | 毛利率假设断崖式下降（92%→50%）为最敏感变量（±1ppt→±9%），终值占比72.2% |

**典型致命错误示例**：

```
🔴 F-1: 所得税亏损弥补公式双重扣减
位置：14-2所得税测算数据 E74
现象：E74（当期增加亏损额）= +8,105,700（盈利年，应为0）
      E75（当期使用可弥补额度）= +8,105,700（FIFO弥补额，正确）
      余额公式将两者都加了 → 弥补池多减了811万
影响：2027→2028→2029年期初余额连续传递偏差
修复：E74 公式改为 =MIN(0, B54)，盈利年为0

🔴 F-2: 有息负债扣减遗漏长期借款
位置：结论表 桥接公式
现象：EV 4.913亿 → 扣减有息负债 0.641亿 → 但遗漏了长期借款
影响：股权价值高估约 2,800万（6.6%）
```

---

## 安装

```bash
# Clone 到 Codex skills 目录
git clone https://github.com/YOUR_USERNAME/valuation-audit-reference.git ~/.agents/skills/valuation-audit-reference

# 或复制到 Claude Code 插件目录
cp -r valuation-audit-reference ~/.claude/plugins/config/
```

### 使用

```bash
# 在 Claude Code 中触发
/valuation-audit-reference  # 对当前打开的底稿执行审核

# NotebookLM 知识库查询（需自备 Google 账号 + 自建知识库）
python ~/.agents/skills/valuation-audit-reference/scripts/query_knowledge_base.py "WACC中无风险利率的选取标准和条文依据"
```

> ⚠️ **NotebookLM 知识库需要你自己创建**：脚本 `query_knowledge_base.py` 提供了查询管道，但知识库内容需要你自己在 Google NotebookLM 中上传和维护（CPA 教材、评估准则等）。作者的知识库绑定了个人 Google 账户，无法直接共享。

---

## 仓库结构

```
valuation-audit-reference/
├── LICENSE                              # All rights reserved
├── README.md                            # 本文件（中文）
├── README_EN.md                         # 英文版说明
├── SKILL.md                             # Skill 主文件（触发逻辑、输出格式、流程说明）
├── references/
│   ├── valuation_audit_checklist.md     # Excel 底稿审查要点（9章，695行）
│   └── word_report_audit_checklist.md   # Word 报告审核要点（7维度）
├── scripts/
│   └── query_knowledge_base.py          # NotebookLM 知识库查询脚本
└── templates/
    └── ifind_batch_query_template.xlsx  # iFinD 批量查询模板示例（不含企业数据）
```

---

## 输出格式

所有发现项按三级分类：

| 等级 | 含义 |
|:--|:--|
| 🔴 **Fatal** | 致命逻辑错误——模型崩溃、公式错误、估值严重偏离 |
| 🟡 **Sanity Check** | 参数预警——假设偏离行业基准、终值占比过高、缺少调整 |
| 🔵 **Best Practice** | 规范建议——硬编码、缺少溯源注释、未遵守颜色编码 |

**每项发现必须包含**：Sheet 名 + 单元格坐标 + 问题描述 + 修复建议 + 影响量化

---

## License

All rights reserved. 详见 [LICENSE](LICENSE)。

本仓库内容仅供私人/内部使用。未经仓库所有者书面授权，禁止使用、复制、修改、分发、再许可或发布。