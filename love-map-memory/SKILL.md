---
name: love-map-memory
description: Build and maintain a multi-person Love Map external memory database. Use when turning daily notes into per-person maps (four content layers + a relationship layer + a protocol/handshake layer), creating or updating person maps, checking contradictions, finding facts that are due for re-confirmation, summarizing a person, or answering questions from stored person-map evidence.
---

# Love Map Memory

这是一个**面向多个人的 Love Map 外置记忆系统**。

核心目标不是建模“关系网络”，而是为每个重要的人维护一份**会随时间演化**的个人地图，从而更好地相处、提高亲密的幸福度：

```txt
一个人 = 一个 map
事件 = 证据
四层画像 + 关系层 = 长期理解
协议层 = 你俩到了第几级、是否双向解锁
人会变 = 定期回头重新确认
```

它的底层方法论是仓库根目录的 `认识一个人.md`（L0–L5 渐进协议 + Gottman 四层内心地图 + Aron 36 问）。本系统是那套方法论的**外置记忆**。

## 不做什么

- 不建立复杂 relationship graph，不分析 A 和 B 的关系网络，不做泛化 CRM。
- 不把推断包装成事实。
- 不主动挖掘创伤、前任、疾病、家庭伤痛等敏感字段（pull-only）。
- 不把这套记忆当成单向“查户口”——它要同时记录**你交换了什么**、对方是否回敬。

## 职责边界：脚本 vs agent

脚本 `scripts/love_map.py` **只做确定性的、对整个库的计算与校验**，不生成内容：

| 命令 | 作用 |
|---|---|
| `init` | 铺数据库骨架，并写入一个自我保护的 `.gitignore (*)` |
| `add-person` | 铺一个人的目录树 + profile + summary + protocol |
| `list-people` | 列出 person_id |
| `validate` | 校验结构**并逐文件解析 YAML**（能抓出坏 frontmatter） |
| `review` | 「人会变」引擎：列出**该回头重新确认**的事实 |

**事件 / 画像事实 / 矛盾 / summary 由你（agent）读模板直接创建和更新**——这些需要判断（落哪一层？是事实还是推断？是不是一次变化？），不交给脚本。模板在 `templates/`（init 后也复制到 `love-map-db/_schema/templates/`）。这样创建和更新是同一套机制（你的编辑器），也避免了脚本静默失败、生成坏 YAML 的问题。

## 数据库默认位置与隐私

优先使用当前项目下的 `love-map-db/`。如果不存在：

```bash
python love-map-memory/scripts/love_map.py init love-map-db
```

> ⚠️ **隐私第一**：库里是关于真实的人、往往未经其同意的私人画像。`init` 会在库内写一个 `.gitignore (*)`，默认不进版本库。**不要提交或推送它**，并建议把库放在 repo 之外的私有路径。

## 数据结构

```txt
love-map-db/
├── _schema/                # 字段、命名、标签规范 + templates 副本
├── inbox/                  # 未处理的原始记录
├── people/
│   ├── index.md            # person_id · current_level · status 总览
│   └── {person_id}/
│       ├── profile.md          # 识别信息 + current_level
│       ├── protocol.md         # L0–L5 双向握手状态（能不能往深走）
│       ├── love-map-summary.md # agent 快速读取的压缩画像
│       ├── events/             # 发生过什么（证据），按 YYYY/MM 归档
│       ├── 01_basic-facts/     # 稳定事实；formative-history/ 放 L3 来历与塑造
│       ├── 02_preferences-habits/
│       ├── 03_stress-emotions/
│       ├── 04_dreams-values/
│       ├── 05_relationship/    # L5：feels-loved-by / repair-and-conflict / relationship-wants / past-relationship-wounds
│       ├── summaries/          # weekly / monthly / quarterly
│       └── contradictions/     # 前后变化与冲突
└── attachments/
```

五层含义（对应方法论 L0–L5）：

1. `01_basic-facts`：稳定事实、身份、家庭朋友、工作学习、日常生活；`formative-history/` 放 L3 童年/成长/塑造经历/与父母的关系。
2. `02_preferences-habits`：喜欢、不喜欢、习惯、沟通风格、娱乐与环境偏好（L2 的“为什么”写进正文）。
3. `03_stress-emotions`：近期压力、恐惧、触发点、情绪需求、支持方式。
4. `04_dreams-values`：人生目标、未完成梦想、价值观、身份认同、意义感。
5. `05_relationship`：**离“提高亲密幸福度”最近的一层**——对方怎样感到被爱、吵架后怎么修复、想要什么样的关系、被过去的关系怎么伤过（pull-only）。

`protocol.md` 不是画像，而是**进度**：你和这个人在 L0–L5 里到第几级、每一格你是否**先交出了自己**、对方是否**主动回敬**（解锁信号）。它让你判断“现在能不能往更深走”，避免在 L1 就问 L4 的问题（= 审讯）。

## Agent 更新流程

当用户给出一段日常信息时：

1. **识别人**：判断涉及哪些 `person_id`；不确定先问，不要乱建（也不要把两个不同的人合并到同一个 id）。
2. **保留原始记录**：必要时按模板写入 `inbox/`。
3. **写 person event**：为每个相关的人，读 `_schema/templates/event-template.md`，填好后写到
   `people/{person_id}/events/YYYY/MM/YYYY-MM-DD__type__topic__signal.md`。
   事件里要填**双向信号**：`i_shared`（你先交出了什么）、`they_reciprocated`（对方有没有回敬）、`disclosure`（对方主动说 volunteered / 你问出来的 elicited）。
   写完跑一次 `validate` 兜底：`title` 等自由文本含双引号（如情绪引语 `她说"…"`）时整行改用单引号包或转义，否则 frontmatter 会坏。
4. **抽取候选画像**：只把可长期复用的信息沉淀到五层模型。读 `profile-fact-template.md`，注意：
   - 有证据时把 `evidence: []` 展开成缩进列表；没有就保持 `evidence: []`（**别**让 `[]` 顶格换行，那会坏 YAML）。
   - 关系层事实 `love_map_layer: relationship`。
   - 禁区话题（创伤/前任/疾病/家庭伤痛）只有在 `disclosure: volunteered` 时才记，`privacy: restricted`。
5. **更新而不是堆积**：相同主题优先**编辑已有文件**（加 evidence、把 `last_confirmed_at` 顶到今天、调 `confidence`），不要每次新建。
6. **更新协议**：如果这次互动让某一级解锁（你抛出 + 对方主动回敬），更新 `protocol.md` 对应行和 `current_level`（profile.md / index.md 同步）。
7. **检查矛盾或变化**：发现前后冲突时，新建 `contradictions/` 文件，把旧事实标 `outdated`/`uncertain`/`contradicted`，**不要删除**。
8. **更新 summary**：信息足够重要时更新 `love-map-summary.md` 或周期 summary。

输出时列出：创建/修改的文件、明确事实、推断、待确认问题、是否发现矛盾、协议是否有进展。

## Agent 检索流程

当用户询问某个人时：

1. 先读 `people/index.md` 确认 person 和 `current_level`。
2. 再读该人的 `love-map-summary.md`（压缩画像）与 `profile.md`；需要证据时再回溯具体 fact / event。
3. 根据问题搜索对应 layer。
4. **优先采信** `status: active`、`confidence` 较高、有 `evidence`、`disclosure: volunteered` 的条目；过滤掉 `outdated`/`contradicted`。
5. 回答必须区分：事实 / 推断 / 不确定。
6. 如果用户问“接下来怎么深入”，结合 `protocol.md` 给出**这一级还没解锁/还不知道的、非禁区**的下一步（问题库见 `references/agent-usage.md` 与 `认识一个人.md` 的 Aron 36 问）。

常用搜索（注意都叠加 `status: active` 排除过期信息）：

```bash
rg -n "status: active" love-map-db/people/{person_id}/03_stress-emotions | rg "need/|压力|support"
rg -n "status: active" love-map-db/people/{person_id}/05_relationship           # 被爱方式 / 怎么吵架 / 想要的关系
rg -n "status: active" love-map-db/people/{person_id}/02_preferences-habits | rg "food|喜欢|讨厌|preference"
```

## 定期对齐（“人会变”）

人会变，地图要定期更新。不要只写不回头：

```bash
python love-map-memory/scripts/love_map.py review love-map-db            # 哪些事实超过 90 天没确认
python love-map-memory/scripts/love_map.py review love-map-db --days 30 --person alice
```

把 `review` 的输出当成下次见面/聊天时**温柔地重新确认**的清单——这正是 Gottman 和方法论都点名的“定期坐下来对齐近况”。确认后把那条 fact 的 `last_confirmed_at` 顶到今天、补一条 evidence。

## 常用命令

```bash
python love-map-memory/scripts/love_map.py init love-map-db
python love-map-memory/scripts/love_map.py add-person love-map-db alice --name "Alice" --context "约会对象"
python love-map-memory/scripts/love_map.py list-people love-map-db
python love-map-memory/scripts/love_map.py review love-map-db
python love-map-memory/scripts/love_map.py validate love-map-db
```

（`validate` 的深度 YAML 校验需要 PyYAML：`pip install pyyaml`；没装也能跑结构校验，会提示跳过了 YAML 解析。）

## 隐私和伦理规则

- 这个系统只用于帮助用户更认真地记住和理解别人，并让关系**双向**地变好。
- 库默认不进 git（`init` 写了 `.gitignore`）；敏感信息默认 `privacy: sensitive` 或 `restricted`。
- 创伤、前任、疾病、家庭伤痛等字段 **pull-only**：只记录对方主动分享（`disclosure: volunteered`）的内容；`validate` 会对 `elicited` 的敏感记录报警。
- 不使用该数据库操控、诱导、审讯或攻击别人。
- 协议层是为了**不跳级、你先 commit、对方回敬才解锁**，不是为了把关系“通关”——把它当作尊重对方节奏的提醒。
- Agent 必须明确区分观察事实、用户推断、模型推断和待确认问题。

更多细节见：

- `references/database-structure.md`、`references/workflow.md`、`references/agent-usage.md`
- `_schema/metadata-fields.md`、`_schema/filename-rules.md`、`_schema/tag-taxonomy.md`
