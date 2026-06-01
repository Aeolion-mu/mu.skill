# Love Map Memory

面向多个人的 Love Map 外置记忆系统。

它的目标是：把日常信息转化为每个人自己的长期地图，帮助人和 agent 记住重要的人、重要的细节、重要的**变化**，从而更好地相处、提高亲密的幸福度。它是仓库根目录 `认识一个人.md`（L0–L5 协议 + Gottman 四层 + Aron 36 问）的外置记忆。

> ⚠️ **隐私**：本系统的数据库存放的是关于真实的人、且往往未经其同意的私人画像。`init` 会在库内写一个 `.gitignore (*)` 让它默认不进版本库。**不要提交或推送数据库**，并建议把它放在 repo 之外的私有路径。

## 核心边界

只维护 `people/{person_id}/` 的个人地图；不维护 `relationships/`、`groups/`、social graph。是“多个人的个人地图集合”，不是“关系网络数据库”。

## 脚本 vs agent

脚本只做确定性的、对整个库的**计算与校验**（`init` / `add-person` / `list-people` / `validate` / `review`）。事件、画像事实、矛盾、summary 由 **agent 读 `templates/` 直接创建和更新**——那些需要判断，不交给脚本。

## 快速开始

```bash
python love-map-memory/scripts/love_map.py init love-map-db
python love-map-memory/scripts/love_map.py add-person love-map-db alice --name "Alice" --context "约会对象"
python love-map-memory/scripts/love_map.py validate love-map-db   # 结构 + YAML 校验
python love-map-memory/scripts/love_map.py review love-map-db      # 哪些事实该回头确认了
```

（`validate` 的深度 YAML 校验需要 `pip install pyyaml`；没装也能跑结构校验。）

## 数据库结构

```txt
love-map-db/
├── .gitignore (*)         # init 写入，隐私保护
├── README.md
├── _schema/
├── inbox/
├── people/
│   ├── index.md
│   └── {person_id}/
│       ├── profile.md          # 含 current_level
│       ├── protocol.md         # L0–L5 双向握手
│       ├── love-map-summary.md
│       ├── events/
│       ├── 01_basic-facts/     # 含 formative-history (L3)
│       ├── 02_preferences-habits/
│       ├── 03_stress-emotions/
│       ├── 04_dreams-values/
│       ├── 05_relationship/    # L5
│       ├── summaries/
│       └── contradictions/
└── attachments/
```

## 五层模型 + 协议层

| Layer | 用途 |
|---|---|
| `01_basic-facts` | 稳定事实：身份、家庭朋友、工作学习、日常；`formative-history/` 放 L3 来历与塑造 |
| `02_preferences-habits` | 偏好习惯：喜欢、不喜欢、沟通风格、例行习惯 |
| `03_stress-emotions` | 压力情绪：压力源、恐惧、触发点、情绪需求、支持方式 |
| `04_dreams-values` | 梦想价值观：目标、未完成梦想、价值观、身份认同、意义 |
| `05_relationship` | **关系层（最贴近亲密幸福度）**：被爱方式、冲突修复、想要的关系、过去的伤（pull-only） |
| `protocol.md` | 进度而非画像：到第几级、你是否先 commit、对方是否回敬（解锁） |

## 信息流

```txt
日常原始信息 → inbox/raw note → people/{person_id}/events/ → 五层 profile facts → summary / contradiction
                                          ↑                                   ↓
                                    更新 protocol（解锁）              review 定期回头确认（人会变）
```

## Agent 使用原则

1. 先确认人，再更新 map；两个不同的人不要合并。
2. 事件是证据，画像是沉淀；事件要记**双向信号**（i_shared / they_reciprocated / disclosure）。
3. 不确定用 `status: uncertain`；检索默认叠加 `status: active`。
4. 推断写进“我的推断”，不要写成事实。
5. 人会变，旧信息不删除，改 `outdated`/`contradicted` 并记录矛盾；定期 `review` 回头对齐。
6. 禁区（创伤/前任/疾病/家庭伤痛）pull-only，只记 `disclosure: volunteered`。
