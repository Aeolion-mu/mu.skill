---
person_id: "{{person_id}}"
type: profile
display_name: "{{display_name}}"
aliases: []
context: "{{context}}"
current_level: L0          # L0–L5：你和这个人在协议里到了第几级（见 protocol.md），独立于 closeness
closeness: unknown         # unknown | low | medium | high（由 agent 随相处更新）
trust_level: unknown       # unknown | low | medium | high
status: active
privacy: normal
created_at: "{{date}}"
updated_at: "{{date}}"
tags:
  - person/{{person_id}}
  - status/active
---

# {{display_name}} · Profile

## 基本识别信息

- Person ID: `{{person_id}}`
- 显示名：{{display_name}}
- 认识场景：{{context}}
- 当前协议级别：L0（详见 `protocol.md`）

## 备注

这里只放用于识别这个人的基础信息，不放复杂关系分析。

## 隐私边界

- 敏感信息使用 `privacy: sensitive` 或 `privacy: restricted`。
- 创伤、前任、疾病、家庭伤痛等内容只记录对方**主动**分享的信息（`disclosure: volunteered`）。
