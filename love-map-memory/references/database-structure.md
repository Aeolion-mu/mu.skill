# Database Structure

本数据库是“多个人的 Love Map 集合”，不是关系网络数据库。

## 顶层结构

```txt
love-map-db/
├── .gitignore        # 由 init 写入，内容是 `*`：让整个库默认不进 git（隐私）
├── README.md
├── _schema/          # 字段/命名/标签规范 + templates 副本
├── inbox/
├── people/
│   ├── index.md      # person_id · current_level · status 总览
│   └── {person_id}/
└── attachments/
```

## person map

每个人一个目录：

```txt
people/{person_id}/
├── profile.md            # 识别信息 + current_level
├── protocol.md           # L0–L5 双向握手状态
├── love-map-summary.md
├── events/
├── 01_basic-facts/       # 含 formative-history/ (L3 来历与塑造)
├── 02_preferences-habits/
├── 03_stress-emotions/
├── 04_dreams-values/
├── 05_relationship/      # L5：feels-loved-by / repair-and-conflict / relationship-wants / past-relationship-wounds
├── summaries/
└── contradictions/
```

### `profile.md`

基础识别信息：名字、别名、认识场景、状态、隐私等级、`current_level`。

### `protocol.md`

协议**进度**，不是画像。记录你和这个人在 L0–L5 到第几级、每一格你是否**先 commit**、对方是否**主动回敬**（解锁信号）。agent 判断“能不能往更深走”靠它，避免在低级别问高级别问题（= 审讯）。

### `love-map-summary.md`

agent 快速读取的压缩画像。它不是证据本身，结论需要能追溯到 events 或 profile fact。检索默认先读它，需要证据再回溯。

### `events/`

存“发生过什么”，按年月归档：

```txt
events/YYYY/MM/YYYY-MM-DD__event-type__topic__signal.md
```

事件除了记录发生了什么，还记录**双向信号**：`i_shared`（你交换了什么）、`they_reciprocated`、`disclosure`。一个原始 note 涉及多个人时，拆成多个 person event。

### 五层目录

四层内容画像 + 一层关系画像，存“从事件中沉淀出的长期理解”：

```txt
01_basic-facts/         稳定事实（formative-history/ 放 L3 来历与塑造）
02_preferences-habits/  偏好习惯
03_stress-emotions/     压力情绪需求
04_dreams-values/       梦想价值观意义
05_relationship/        关系层：被爱方式 / 冲突修复 / 想要的关系 / 过去的伤（pull-only）
```

### `summaries/` 与 `contradictions/`

`summaries/` 存 weekly/monthly/quarterly 周期总结（短、准、可追溯）。`contradictions/` 记录前后变化与冲突——人会变，旧信息**不删**，标 `outdated`/`uncertain`/`contradicted` 并记录证据。

## 状态与检索

旧信息永不删除，所以检索时**默认叠加 `status: active`** 过滤，避免过期事实污染结果。`review` 命令按 `last_confirmed_at` 找出该回头确认的事实。

## 为什么事件放在 person 下面

目标是维护“每个人的 map”，不是全局社交事件库。事件作为证据直接归档在对应 person 下，检索某个人时不需要跨关系图。
