---
person_id: "{{person_id}}"
type: protocol
display_name: "{{display_name}}"
current_level: L0
created_at: "{{date}}"
updated_at: "{{date}}"
tags:
  - person/{{person_id}}
---

# {{display_name}} · 协议状态（L0–L5 双向握手）

> 来自《认识一个人》：**禁止跳级**；每一格要**你先 commit**（i_disclosed），
> 等**对方主动回敬**（they_reciprocated）才算这一级解锁（unlocked）。
> 单向提问 = 查户口。这张表是 agent 判断「现在能不能往更深的层走」的依据。

| level | 主题 | asked_them | i_disclosed | they_reciprocated | unlocked |
|---|---|:--:|:--:|:--:|:--:|
| L0 | 基础档案 / basic facts | ☐ | ☐ | ☐ | ☐ |
| L1 | 当下的生活 / current life | ☐ | ☐ | ☐ | ☐ |
| L2 | 喜好背后的为什么 / the why | ☐ | ☐ | ☐ | ☐ |
| L3 | 来历与塑造 / origins & shaping | ☐ | ☐ | ☐ | ☐ |
| L4 | 内心世界 恐惧/价值观/梦想 | ☐ | ☐ | ☐ | ☐ |
| L5 | 关系层 / 在感情里要什么 | ☐ | ☐ | ☐ | ☐ |

## 当前级别

- current_level: **L0**
- 升级规则：你抛出某一格 + 对方**主动回敬**（也问回你 / 不用问就多讲） → 这一级才解锁，才进下一级。

## 这一级我还不知道的（非禁区，下次自然地问）

-

## 禁区提醒（pull-only，绝不主动挖）

- 创伤 / 前任 / 疾病 / 家庭伤痛：只在对方**主动**说起时记录，标 `disclosure: volunteered`、`privacy: restricted`，落到 `05_relationship/past-relationship-wounds/` 或对应层。
