---
id: "{{id}}"
person_id: "{{person_id}}"
type: event
# 自由文本含双引号/冒号时，整行改用单引号包或转义，例：title: '她说"我害怕被晾着"'
title: "{{title}}"
event_type: "{{event_type}}"
event_date: "{{date}}"
observed_at: "{{date}}"
recorded_at: "{{created_at}}"
created_at: "{{created_at}}"
updated_at: "{{created_at}}"
status: active
confidence: 0.6
privacy: normal
source: "{{source}}"
disclosure: volunteered          # volunteered（对方主动说）| elicited（你问出来的）—— 禁区话题必须是 volunteered
evidence_strength: medium
i_shared: ""                     # 这一格里你先交出了自己的什么？（协议规则2：你先 commit）
they_reciprocated: unknown       # yes | no | unknown —— 对方主动回敬/反问了吗？（规则5：解锁信号）
love_map_layers: []              # basic_facts / preferences_habits / stress_emotions / dreams_values / relationship
candidate_updates: []
topics:
  - "{{topic}}"
keywords:
  - "{{signal}}"
related_notes: []
tags:
  - person/{{person_id}}
  - status/active
---

# {{title}}

## 原始事件



## 可观察事实

-

## 用户推断

-

## Agent 推断

-

## 双向信号（协议）

- 我先交出了什么（i_shared）：
- 对方有没有主动回敬 / 反问（they_reciprocated）：

## 可能更新的地图层

- [ ] `01_basic-facts`
- [ ] `02_preferences-habits`
- [ ] `03_stress-emotions`
- [ ] `04_dreams-values`
- [ ] `05_relationship`

## 下次可以怎么做

-

## 待确认问题

-
