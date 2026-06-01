---
person_id: "{{person_id}}"
type: profile
display_name: "{{display_name}}"
aliases: []
context: "{{context}}"
closeness: unknown
trust_level: unknown
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

## 备注

这里只放用于识别这个人的基础信息，不放复杂关系分析。

## 隐私边界

- 敏感信息使用 `privacy: sensitive` 或 `privacy: restricted`。
- 创伤、前任、疾病、家庭伤痛等内容只记录对方主动分享的信息。

