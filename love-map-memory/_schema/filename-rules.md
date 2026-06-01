# Filename Rules

## person_id

`person_id` 用稳定、简短、可读的 kebab-case 或拼音/英文别名：

```txt
alice
bella
chen-yu
li-na
```

不要用容易变化的称呼作为 ID，例如：

```txt
current-girlfriend
new-girl
crush
```

角色应该写在 `profile.md` 的 metadata 中，而不是写死进目录名。

## 事件文件

```txt
YYYY-MM-DD__event-type__topic__signal.md
```

示例：

```txt
2026-06-01__conversation__work-pressure__needs-reassurance.md
2026-06-02__date__japanese-food__liked-quiet-place.md
2026-06-03__conflict__late-reply__felt-neglected.md
2026-06-05__observation__family-topic__became-quiet.md
```

路径：

```txt
people/{person_id}/events/YYYY/MM/{filename}.md
```

## profile fact 文件

画像文件不一定带日期，重点是语义清楚：

```txt
likes-japanese-food.md
dislikes-being-interrupted.md
needs-reassurance-under-stress.md
work-deadline-pressure.md
wants-more-freedom-in-career.md
values-emotional-safety.md
```

## summary 文件

```txt
YYYY-Www__weekly-summary__topic.md
YYYY-MM__monthly-summary__topic.md
YYYY-Qn__quarterly-summary__topic.md
```

示例：

```txt
2026-W23__weekly-summary__stress-preferences.md
2026-06__monthly-summary__love-map-updates.md
2026-Q2__quarterly-summary__values-and-patterns.md
```

## contradiction 文件

```txt
YYYY-MM-DD__contradiction__old-topic__new-topic.md
```

示例：

```txt
2026-06-10__contradiction__liked-spicy__now-avoids-spicy.md
```

