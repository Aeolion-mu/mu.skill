# Tag Taxonomy

Tags 用于让 agent 和 `rg` 稳定检索。模板自动产出的 tag 家族：`person/`、`layer/`、`status/`，summary 模板还产出 `summary/`，contradiction 模板产出 `type/contradiction`；下面其余的（disclosure/topic/need/signal/source/privacy）按需手动补。

## layer tags

```yaml
tags:
  - layer/basic-facts
  - layer/preferences-habits
  - layer/stress-emotions
  - layer/dreams-values
  - layer/relationship
```

## status tags

```yaml
tags:
  - status/active
  - status/uncertain
  - status/outdated
  - status/contradicted
```

## disclosure tags（谁先开口——pull-only 的关键）

```yaml
tags:
  - disclosure/volunteered   # 对方主动说
  - disclosure/elicited      # 你问出来的（禁区话题不该是这个）
```

## source tags

```yaml
tags:
  - source/direct-conversation
  - source/observation
  - source/message
  - source/memory
  - source/inference
```

## topic tags

```yaml
tags:
  - topic/work
  - topic/study
  - topic/family
  - topic/friends
  - topic/food
  - topic/health
  - topic/travel
  - topic/music
  - topic/movie
  - topic/conflict
  - topic/repair          # 吵架后怎么和好
```

## need tags

```yaml
tags:
  - need/reassurance
  - need/listening
  - need/space
  - need/respect
  - need/clarity
  - need/encouragement
```

## signal tags

```yaml
tags:
  - signal/deadline-pressure
  - signal/felt-neglected
  - signal/became-quiet
  - signal/liked-quiet-place
  - signal/reciprocated      # 对方主动回敬 → 协议解锁信号
```

## privacy tags

```yaml
tags:
  - privacy/normal
  - privacy/sensitive
  - privacy/restricted
```

## person tag

每个文件建议带：

```yaml
tags:
  - person/{person_id}
```
