# Love Map Memory

面向多个人的 Love Map 外置记忆系统。

它的目标是：把日常信息转化为每个人自己的长期四层地图，帮助人和 agent 在信息爆炸中记住重要的人、重要的细节、重要的变化。

## 核心边界

这个系统只维护：

```txt
people/{person_id}/ 的个人地图
```

它不维护：

```txt
relationships/
groups/
social graph
```

也就是说，本系统是“多个人的个人地图集合”，不是“关系网络数据库”。

## 快速开始

```bash
python love-map-memory/scripts/love_map.py init love-map-db
python love-map-memory/scripts/love_map.py add-person love-map-db alice --name "Alice" --context "约会对象"
python love-map-memory/scripts/love_map.py validate love-map-db
```

## 数据库结构

```txt
love-map-db/
├── README.md
├── _schema/
├── inbox/
├── people/
│   ├── index.md
│   └── {person_id}/
│       ├── profile.md
│       ├── love-map-summary.md
│       ├── events/
│       ├── 01_basic-facts/
│       ├── 02_preferences-habits/
│       ├── 03_stress-emotions/
│       ├── 04_dreams-values/
│       ├── summaries/
│       └── contradictions/
└── attachments/
```

## 四层模型

| Layer | 用途 |
|---|---|
| `01_basic-facts` | 稳定事实：身份、家庭朋友、工作学习、日常生活 |
| `02_preferences-habits` | 偏好习惯：喜欢、不喜欢、沟通风格、例行习惯 |
| `03_stress-emotions` | 压力情绪：压力源、恐惧、触发点、情绪需求、支持方式 |
| `04_dreams-values` | 梦想价值观：目标、未完成梦想、价值观、身份认同、意义 |

## 信息流

```txt
日常原始信息
  ↓
inbox/raw note
  ↓
people/{person_id}/events/
  ↓
四层 profile facts
  ↓
summary / contradiction
```

## Agent 使用原则

1. 先确认人，再更新 map。
2. 事件是证据，画像是沉淀。
3. 不确定的信息用 `status: uncertain`。
4. 推断写进“我的推断”，不要写成事实。
5. 人会变，旧信息不要删除，改为 `outdated` / `contradicted` 并记录矛盾。

