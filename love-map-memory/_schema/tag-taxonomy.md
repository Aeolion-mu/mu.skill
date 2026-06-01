# Tag Taxonomy

Tags 用于让 agent 和 `rg` 稳定检索。

## layer tags

```yaml
tags:
  - layer/basic-facts
  - layer/preferences-habits
  - layer/stress-emotions
  - layer/dreams-values
```

## status tags

```yaml
tags:
  - status/active
  - status/uncertain
  - status/outdated
  - status/contradicted
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

