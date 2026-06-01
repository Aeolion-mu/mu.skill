# Agent Usage

## 回答问题时

如果用户问某个人：

1. 读取 `love-map-db/people/index.md`。
2. 找到对应 `person_id`。
3. 读取：

```txt
people/{person_id}/profile.md
people/{person_id}/love-map-summary.md
```

4. 按问题搜索具体 layer。
5. 必要时追溯 evidence 中的事件。

## 推荐搜索路径

问“她喜欢什么 / 约什么 / 吃什么”：

```bash
rg -n "food|restaurant|喜欢|讨厌|dislikes|preference|layer/preferences-habits" love-map-db/people/{person_id}
```

问“她最近压力是什么”：

```bash
rg -n "stress|压力|current-stressors|deadline|焦虑|status: active" love-map-db/people/{person_id}/03_stress-emotions
```

问“怎么安慰她”：

```bash
rg -n "support-methods|emotional-needs|need/|comfort|reassurance|安慰|安全感" love-map-db/people/{person_id}/03_stress-emotions
```

问“她真正重视什么”：

```bash
rg -n "values|life-goals|meaning|底线|在乎|梦想|identity" love-map-db/people/{person_id}/04_dreams-values
```

## 回答格式建议

```md
## 我查到的稳定事实

## 我查到的近期状态

## 我的推断

## 可以怎么做

## 不确定 / 待确认
```

## 更新数据库时

输出：

```md
## 已更新
- path/to/file.md

## 抽取到的事实

## 抽取到的推断

## 待确认问题

## 是否发现矛盾
```

