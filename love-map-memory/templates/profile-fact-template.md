---
id: "{{id}}"
person_id: "{{person_id}}"
type: profile_fact
# 自由文本含双引号/冒号时，整行改用单引号包或转义，例：title: '她说"我害怕被晾着"'
title: "{{title}}"
# love_map_layer: basic_facts | preferences_habits | stress_emotions | dreams_values | relationship
love_map_layer: "{{layer}}"
category: "{{category}}"
created_at: "{{created_at}}"
updated_at: "{{created_at}}"
first_observed_at: "{{date}}"
last_confirmed_at: "{{date}}"   # `review` 用它判断这条事实是否该回头重新确认
status: active                   # active | outdated | uncertain | contradicted
confidence: 0.6
privacy: normal                  # normal | sensitive | restricted
source: mixed
disclosure: volunteered          # volunteered（对方主动说）| elicited（你问出来的）
evidence: []                     # 有证据时展开成列表：见下方注释
contradicted_by: []
topics: []
keywords: []
tags:
  - person/{{person_id}}
  - layer/{{layer_tag}}
  - status/active
---

<!--
evidence 有内容时改成列表形式（注意每项前两个空格缩进）：
evidence:
  - "event:2026-06-01 她亲口说的"
  - "people/{{person_id}}/events/2026/06/2026-06-01__conversation__food__liked-japanese.md"
关系层(L5)的事实把 love_map_layer 设为 relationship，category 用
feels-loved-by / repair-and-conflict / relationship-wants / past-relationship-wounds。
触及禁区(创伤/前任/疾病/家庭伤痛)时：disclosure 必须是 volunteered，privacy 设 restricted。
-->

# {{title}}

## 一句话结论



## 可确认事实

-

## 我的推断

-

## 证据

-

## 对理解这个人的意义

-

## 下次行动建议

-

## 待确认问题

-
