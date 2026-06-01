# Workflow

## 1. 捕捉原始信息

把未经处理的日常信息放入：

```txt
inbox/YYYY-MM-DD__raw-note__topic.md
```

原始信息可以很粗糙，重点是保留上下文。

## 2. 识别人物

从原始信息中识别涉及的人：

- 如果能匹配已有 `person_id`，直接更新该人的 map。
- 如果不能匹配，先询问用户是否创建新 person。
- 不要擅自合并两个可能不同的人。

## 3. 生成 person event

为每个相关的人创建独立事件：

```txt
people/{person_id}/events/YYYY/MM/YYYY-MM-DD__type__topic__signal.md
```

事件只回答：

- 发生了什么；
- 哪些是可观察事实；
- 哪些是用户推断；
- 这件事可能更新哪一层 map；
- 下次可以如何确认。

## 4. 抽取四层画像

只有长期有用的信息才沉淀为 profile fact。

例如事件：

```txt
她说最近 deadline 压力很大，希望我先听她说，不要马上给建议。
```

可能沉淀成：

```txt
03_stress-emotions/current-stressors/work-deadline-pressure.md
03_stress-emotions/emotional-needs/needs-reassurance-under-stress.md
03_stress-emotions/support-methods/comfort-before-advice.md
```

## 5. 更新而不是堆积

遇到相同主题时，优先更新已有文件：

- 增加 evidence；
- 更新 `last_confirmed_at`；
- 调整 `confidence`；
- 增加待确认问题。

不要每次都创建一个新画像文件，除非它确实是新主题。

## 6. 处理矛盾和变化

人会变。发现前后不一致时：

1. 不删除旧信息；
2. 新建 `contradictions/` 文件；
3. 把旧事实标为 `outdated` / `uncertain` / `contradicted`；
4. 在新事实中记录 evidence。

## 7. 更新 summary

当信息重要、重复出现、或影响行动建议时，更新：

```txt
love-map-summary.md
summaries/weekly/
summaries/monthly/
```

summary 应该短、准、可追溯，不要堆日记。

