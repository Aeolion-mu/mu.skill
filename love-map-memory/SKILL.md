---
name: love-map-memory
description: Build and maintain a multi-person Love Map external memory database. Use when turning daily notes into per-person four-layer maps, creating or updating person maps, checking contradictions, summarizing a person, or answering questions from stored person-map evidence.
---

# Love Map Memory

这是一个**面向多个人的 Love Map 外置记忆系统**。

核心目标不是建模“关系网络”，而是为每个重要的人维护一份长期更新的个人地图：

```txt
一个人 = 一个 map
多个重要的人 = 多个 map
事件 = 证据
四层模型 = 长期画像
```

## 不做什么

- 不建立复杂 relationship graph。
- 不分析 A 和 B 的关系网络。
- 不把系统做成泛化 CRM。
- 不把推断包装成事实。
- 不主动挖掘创伤、前任、疾病、家庭伤痛等敏感字段。

## 数据库默认位置

优先使用当前项目下的：

```txt
love-map-db/
```

如果不存在，可以初始化：

```bash
python love-map-memory/scripts/love_map.py init love-map-db
```

## 数据结构

每个人独立拥有一套四层模型：

```txt
love-map-db/
├── inbox/
├── people/
│   ├── index.md
│   └── {person_id}/
│       ├── profile.md
│       ├── love-map-summary.md
│       ├── events/
│       ├── 01_basic-facts/
│       ├── 02_preferences-habits/
│       ├── 03_stress-emotions/
│       ├── 04_dreams-values/
│       ├── summaries/
│       └── contradictions/
└── attachments/
```

四层含义：

1. `01_basic-facts`：稳定事实、身份、家庭朋友、工作学习、日常生活。
2. `02_preferences-habits`：喜欢、不喜欢、习惯、沟通风格、娱乐和环境偏好。
3. `03_stress-emotions`：近期压力、恐惧、触发点、情绪需求、支持方式。
4. `04_dreams-values`：人生目标、未完成梦想、价值观、身份认同、意义感。

## Agent 更新流程

当用户给出一段日常信息时：

1. **识别人**：判断涉及哪些 `person_id`；不确定时先询问，不要乱建。
2. **保留原始记录**：必要时写入 `inbox/`。
3. **写 person event**：为每个相关的人写入独立事件：
   `people/{person_id}/events/YYYY/MM/YYYY-MM-DD__type__topic__signal.md`
4. **抽取候选画像**：只把可长期复用的信息沉淀到四层模型。
5. **更新或创建 profile fact**：优先更新已有事实；没有再新增。
6. **检查矛盾或变化**：发现前后冲突时写入 `contradictions/`，不要直接删除旧信息。
7. **更新 summary**：信息足够重要时更新 `love-map-summary.md` 或周期 summary。

输出时列出：

- 创建/修改的文件；
- 明确事实；
- 推断；
- 待确认问题；
- 是否发现矛盾。

## Agent 检索流程

当用户询问某个人时：

1. 先读 `people/index.md` 确认 person。
2. 再读该人的 `profile.md` 与 `love-map-summary.md`。
3. 根据问题搜索对应 layer。
4. 优先使用：`status: active`、`extraction_status: accepted`、`confidence` 较高、有 evidence 的条目。
5. 必要时追溯 `events/` 里的证据。
6. 回答必须区分：事实 / 推断 / 不确定。

常用搜索：

```bash
rg -n "need/reassurance|压力|stress|support" love-map-db/people/{person_id}
rg -n "layer/preferences-habits|food|dislikes|喜欢|讨厌" love-map-db/people/{person_id}
rg -n "status: active" love-map-db/people/{person_id}
```

## 常用命令

初始化数据库：

```bash
python love-map-memory/scripts/love_map.py init love-map-db
```

新增一个人：

```bash
python love-map-memory/scripts/love_map.py add-person love-map-db alice --name "Alice" --context "约会对象"
```

创建原始记录：

```bash
python love-map-memory/scripts/love_map.py new-raw love-map-db --title "今天的聊天"
```

创建某个人的事件：

```bash
python love-map-memory/scripts/love_map.py new-event love-map-db alice \
  --event-type conversation \
  --topic work-pressure \
  --signal needs-reassurance \
  --title "工作压力，需要安慰"
```

创建画像事实：

```bash
python love-map-memory/scripts/love_map.py new-fact love-map-db alice \
  --layer stress_emotions \
  --category emotional-needs \
  --title "压力下需要先被安慰"
```

校验数据库：

```bash
python love-map-memory/scripts/love_map.py validate love-map-db
```

## 隐私和伦理规则

- 这个系统只用于帮助用户更认真地记住和理解别人。
- 敏感信息默认 `privacy: sensitive` 或 `privacy: restricted`。
- 创伤、前任、疾病、家庭伤痛等字段默认 pull-only：只记录对方主动分享的内容。
- 不使用该数据库操控、诱导、审讯或攻击别人。
- Agent 必须明确区分观察事实、用户推断、模型推断和待确认问题。

更多细节见：

- `references/database-structure.md`
- `references/workflow.md`
- `references/agent-usage.md`
- `_schema/metadata-fields.md`
- `_schema/filename-rules.md`
- `_schema/tag-taxonomy.md`

