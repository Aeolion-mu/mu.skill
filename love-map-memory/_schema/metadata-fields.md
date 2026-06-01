# Metadata Fields

所有 Markdown 文件尽量使用 YAML frontmatter。

## 通用字段

```yaml
id:
person_id:
type: event | profile_fact | summary | contradiction | raw_note | profile
title:
created_at:
updated_at:
status: active | outdated | uncertain | contradicted
confidence: 0.0
privacy: normal | sensitive | restricted
extraction_status: draft | reviewed | accepted
source: direct_conversation | observation | message | memory | inference | mixed
topics: []
keywords: []
tags: []
related_notes: []
```

## person profile 字段

```yaml
person_id:
display_name:
aliases: []
context:
closeness: unknown | low | medium | high
trust_level: unknown | low | medium | high
status: active | inactive | archived
privacy: normal | sensitive | restricted
```

## event 字段

```yaml
type: event
event_type: conversation | date | observation | message | conflict | plan | memory
event_date:
observed_at:
recorded_at:
love_map_layers: []
candidate_updates: []
evidence_strength: weak | medium | strong
```

## profile_fact 字段

```yaml
type: profile_fact
love_map_layer: basic_facts | preferences_habits | stress_emotions | dreams_values
category:
first_observed_at:
last_confirmed_at:
evidence: []
contradicted_by: []
```

## summary 字段

```yaml
type: summary
summary_period: weekly | monthly | quarterly | overall
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

