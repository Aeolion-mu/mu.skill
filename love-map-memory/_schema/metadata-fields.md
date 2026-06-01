# Metadata Fields

所有 Markdown 文件尽量使用 YAML frontmatter。**必须是合法 YAML**——`validate` 会逐文件 `yaml.safe_load`，解析失败计为 error。

两个最常踩的坑：

- 空列表写成单行 `evidence: []`，**不要**写成 `evidence:` 换行后 `[]` 顶格（会坏 YAML）。有内容时才换行、每项缩进两格。
- 字符串值里有双引号（如情绪引语 `她说"我害怕被抛弃"`）时，整行用单引号包，或转义内部的 `"`，否则 frontmatter 解析失败。

## 通用字段

```yaml
id:
person_id:
type: event | profile_fact | summary | contradiction | raw_note | profile | protocol | index
title:
created_at:
updated_at:
status: active | outdated | uncertain | contradicted
confidence: 0.0
privacy: normal | sensitive | restricted
disclosure: volunteered | elicited     # 对方主动说 vs 你问出来的；禁区话题必须 volunteered
source: direct_conversation | observation | message | memory | inference | mixed
topics: []
keywords: []
tags: []
related_notes: []
```

> 信任信号用 `status` + `confidence` + 是否有 `evidence` 来表达。**不要**用 `extraction_status`——
> 没有任何模板或命令会写它，按它过滤等于过滤到空。

## person profile 字段

```yaml
person_id:
display_name:
aliases: []
context:
current_level: L0 | L1 | L2 | L3 | L4 | L5   # 协议级别（内容深度），独立于 closeness
closeness: unknown | low | medium | high
trust_level: unknown | low | medium | high
status: active | inactive | archived
privacy: normal | sensitive | restricted
```

## protocol 字段（每人一个 protocol.md）

```yaml
type: protocol
current_level: L0..L5
```

正文是 L0–L5 的握手表：每一级记录 `asked_them` / `i_disclosed`（你先 commit 了没）/ `they_reciprocated`（对方主动回敬了没 → 解锁）/ `unlocked`。

## event 字段

```yaml
type: event
event_type: conversation | date | observation | message | conflict | plan | memory
event_date:
observed_at:
recorded_at:
disclosure: volunteered | elicited
i_shared:                              # 这一格你先交出了自己的什么（协议规则2）
they_reciprocated: yes | no | unknown  # 对方主动回敬/反问了吗（协议规则5：解锁信号）
love_map_layers: []                    # basic_facts / preferences_habits / stress_emotions / dreams_values / relationship
candidate_updates: []
evidence_strength: weak | medium | strong
```

## profile_fact 字段

```yaml
type: profile_fact
love_map_layer: basic_facts | preferences_habits | stress_emotions | dreams_values | relationship
category:
first_observed_at:
last_confirmed_at:                     # `review` 用它判断这条是否该回头重新确认
disclosure: volunteered | elicited
evidence: []                           # 有内容时展开成缩进列表
contradicted_by: []
```

## summary 字段

```yaml
type: summary
summary_period: weekly | monthly | quarterly | overall
current_level:                         # overall summary 可带，方便快速判断进度
period_start:
period_end:
covered_events: []
covered_facts: []
```

## contradiction 字段

```yaml
type: contradiction
old_claim:
new_claim:
resolution_status: unresolved | resolved | likely_changed | needs_confirmation
related_facts: []
related_events: []
```

## raw_note 字段（inbox 原始记录）

```yaml
type: raw_note
note_date:
status: unprocessed | processed     # raw_note 用独立 status 词表（不同于画像的 active/outdated）
people_mentioned: []
```

