# Filename Rules

## person_id

`person_id` 用稳定、简短、可读的 kebab-case 或拼音/英文别名：

```txt
alice
bella
chen-yu
li-na
```

不要用容易变化的称呼作为 ID（`current-girlfriend`、`new-girl`、`crush`）。角色写在 `profile.md` 的 metadata 里，不要写死进目录名。

> 两个**不同的人**别共用一个 id。如果两人会 slug 成同一个（如 `Li Na` 与 `li-na`），用可区分的 id：`li-na-hr`、`li-na-2`。`add-person` 检测到撞名且名字不同会报错。

## 事件文件

```txt
people/{person_id}/events/YYYY/MM/YYYY-MM-DD__event-type__topic__signal.md
```

示例：

```txt
2026-06-01__conversation__work-pressure__needs-reassurance.md
2026-06-02__date__japanese-food__liked-quiet-place.md
2026-06-03__conflict__late-reply__felt-neglected.md
2026-06-05__observation__family-topic__became-quiet.md
```

> 同一天对同一个人可能发生多件同类事件。如果 `type/topic/signal` 会撞名，给文件名加个区分后缀（如 `__2` 或时间 `__1930`），**不要**覆盖上一条。

## profile fact 文件

画像文件不一定带日期，重点是语义清楚；放在对应 layer 的 category 目录下：

```txt
01_basic-facts/formative-history/grew-up-in-single-parent-home.md
02_preferences-habits/food/likes-japanese-food.md
03_stress-emotions/emotional-needs/needs-reassurance-under-stress.md
04_dreams-values/values/values-emotional-safety.md
05_relationship/feels-loved-by/feels-loved-through-quality-time.md
05_relationship/repair-and-conflict/wants-cooldown-before-talking.md
05_relationship/past-relationship-wounds/hurt-by-stonewalling.md   # pull-only, privacy: restricted
```

## summary 文件

```txt
YYYY-Www__weekly-summary__topic.md
YYYY-MM__monthly-summary__topic.md
YYYY-Qn__quarterly-summary__topic.md
```

## contradiction 文件

```txt
YYYY-MM-DD__contradiction__old-topic__new-topic.md
```

示例：

```txt
2026-06-10__contradiction__liked-spicy__now-avoids-spicy.md
```
