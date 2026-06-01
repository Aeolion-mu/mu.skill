# Workflow

> 创建/更新文件由 agent 读 `_schema/templates/` 里的模板、用编辑器直接完成。脚本只负责 `init` / `add-person` / `validate` / `review`，不生成内容。

## 1. 捕捉原始信息

把未经处理的日常信息按 `raw-note-template.md` 放入：

```txt
inbox/YYYY-MM-DD__raw-note__topic.md
```

原始信息可以很粗糙，重点是保留上下文。

## 2. 识别人物

- 能匹配已有 `person_id` → 更新该人的 map。
- 不能匹配 → 先问用户是否创建新 person（`add-person`）。
- 不要擅自合并两个可能不同的人；两个不同的人不要共用一个 id。

## 3. 生成 person event

为每个相关的人，读 `event-template.md` 填好后写到：

```txt
people/{person_id}/events/YYYY/MM/YYYY-MM-DD__type__topic__signal.md
```

事件回答：发生了什么 / 哪些是可观察事实 / 哪些是推断 / 可能更新哪一层 / 下次怎么确认；并填**双向信号**：`i_shared`、`they_reciprocated`、`disclosure`。

## 4. 抽取五层画像

只有长期有用的信息才沉淀为 profile fact（读 `profile-fact-template.md`）。例：

事件「她说最近 deadline 压力很大，希望我先听她说，不要马上给建议」可能沉淀成：

```txt
03_stress-emotions/current-stressors/work-deadline-pressure.md
03_stress-emotions/emotional-needs/needs-reassurance-under-stress.md
03_stress-emotions/support-methods/comfort-before-advice.md
```

事件「她说上一段被冷暴力过，所以很怕被晾着」（**对方主动说**）→ 落到关系层，`disclosure: volunteered`、`privacy: restricted`：

```txt
05_relationship/past-relationship-wounds/hurt-by-stonewalling.md
05_relationship/repair-and-conflict/needs-timely-response-in-conflict.md
```

## 5. 更新而不是堆积

相同主题优先**编辑已有文件**：加 evidence、把 `last_confirmed_at` 顶到今天、调 `confidence`、补待确认问题。不要每次新建，除非确实是新主题。

> `evidence` 有内容时展开成缩进列表；没有保持 `evidence: []`（别让 `[]` 顶格换行）。含双引号的引语整行用单引号包或转义。

## 6. 更新协议层

如果这次互动让某一级**解锁**（你抛出某格 + 对方主动回敬/多讲/反问你），更新 `protocol.md` 对应行，必要时抬高 `current_level`，并同步 `profile.md` 和 `people/index.md`。还没解锁就别往更深的层硬走。

## 7. 处理矛盾和变化

人会变。发现前后不一致时：不删旧信息；新建 `contradictions/` 文件；把旧事实标 `outdated`/`uncertain`/`contradicted`；在新事实里记 evidence。

## 8. 更新 summary

信息重要、重复出现或影响行动建议时，更新 `love-map-summary.md` 或周期 summary（读 `periodic-summary-template.md`）。summary 要短、准、可追溯。

## 9. 定期对齐（人会变）

隔段时间跑：

```bash
python love-map-memory/scripts/love_map.py review love-map-db
```

它按 `last_confirmed_at` 列出超过阈值（默认 90 天）没确认的活跃事实。把它当成下次相处时**温柔地重新确认**的清单——确认后顶新 `last_confirmed_at`、补一条 evidence。这就是“定期坐下来对齐近况”。
