# Database Structure

本数据库是“多个人的 Love Map 集合”，不是关系网络数据库。

## 顶层结构

```txt
love-map-db/
├── README.md
├── _schema/
├── inbox/
├── people/
│   ├── index.md
│   └── {person_id}/
└── attachments/
```

## person map

每个人一个目录：

```txt
people/{person_id}/
├── profile.md
├── love-map-summary.md
├── events/
├── 01_basic-facts/
├── 02_preferences-habits/
├── 03_stress-emotions/
├── 04_dreams-values/
├── summaries/
└── contradictions/
```

### `profile.md`

存这个人的基础索引信息：名字、别名、认识场景、状态、隐私等级等。

### `love-map-summary.md`

存 agent 快速读取的阶段性压缩画像。它不是证据本身，结论需要能追溯到事件或 profile fact。

### `events/`

存“发生过什么”。事件按年月归档：

```txt
events/YYYY/MM/YYYY-MM-DD__event-type__topic__signal.md
```

一个原始 note 如果涉及多个人，可以被拆成多个 person event，分别进入不同人的 `events/`。

### 四层目录

四层目录存“从事件中沉淀出的长期画像”。

```txt
01_basic-facts/       稳定事实
02_preferences-habits/偏好习惯
03_stress-emotions/   压力情绪需求
04_dreams-values/     梦想价值观意义
```

### `summaries/`

周期性总结：

```txt
summaries/weekly/
summaries/monthly/
summaries/quarterly/
```

### `contradictions/`

记录前后变化、冲突、过期信息。例如：以前喜欢辣，现在因为身体原因避免辣。

## 为什么事件放在 person 下面

本系统的目标是维护“每个人的 map”，不是维护全局社交事件库。事件作为证据，直接归档在对应 person 下，agent 检索某个人时不需要跨关系图。

如果一条日常记录涉及多个人，做法是：保留一条 `inbox/` 原始记录，再拆成多个 person-specific event。

