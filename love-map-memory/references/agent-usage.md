# Agent Usage

## 回答问题时

1. 读 `love-map-db/people/index.md`，找到 `person_id` 和 `current_level`。
2. 读 `love-map-summary.md`（压缩画像）与 `profile.md`；需要证据再回溯。
3. 按问题搜索具体 layer。
4. **优先采信** `status: active`、`confidence` 高、有 `evidence`、`disclosure: volunteered` 的条目；过滤 `outdated`/`contradicted`。

## 推荐搜索路径（都叠加 status: active 排除过期信息）

问“她喜欢什么 / 约什么 / 吃什么”：

```bash
rg -n "status: active" love-map-db/people/{person_id}/02_preferences-habits | rg "food|喜欢|讨厌|dislikes|preference"
```

问“她最近压力是什么 / 怎么安慰她”：

```bash
rg -n "status: active" love-map-db/people/{person_id}/03_stress-emotions | rg "current-stressors|emotional-needs|support-methods|need/|安慰|安全感"
```

问“她怎样感到被爱 / 吵架怎么处理 / 想要什么样的关系”（关系层，离亲密幸福度最近）：

```bash
rg -n "status: active" love-map-db/people/{person_id}/05_relationship | rg "feels-loved-by|repair|conflict|relationship-wants|被爱|吵架|修复"
```

问“她真正重视什么 / 来历”：

```bash
rg -n "status: active" love-map-db/people/{person_id}/04_dreams-values
rg -n "status: active" love-map-db/people/{person_id}/01_basic-facts/formative-history
```

## “接下来怎么深入 / 下一步该问什么”

1. 读 `protocol.md` 看 `current_level` 和每一级的握手状态。
2. **只在已解锁或正在解锁的级别**里找“这一级我还不知道的（非禁区）”。
3. 从 `认识一个人.md` 的 Aron 36 问里，按当前级别挑题（Set I↔L0–L2、Set II↔L2–L4、Set III↔L4–L5），标了 *(敏感)* 的留给对方自己提起。
4. 给建议时强调**双向**：你先交出自己同一格的答案，再问对方（协议规则2）。
5. 禁区（创伤/前任/疾病/家庭伤痛）**绝不建议主动问**，只等对方主动 push。

## 定期对齐

```bash
python love-map-memory/scripts/love_map.py review love-map-db --days 30
```

把输出当成“该回头确认”的清单。

## 回答格式建议

```md
## 我查到的稳定事实
## 我查到的近期状态
## 关系层（被爱方式 / 冲突修复 / 想要的关系）
## 我的推断
## 可以怎么做（含：你先交换什么）
## 协议进度 & 下一步可问（非禁区）
## 不确定 / 待确认
```

## 更新数据库时输出

```md
## 已更新 / 新建
- path/to/file.md

## 抽取到的事实
## 抽取到的推断
## 双向信号（我交换了什么 / 对方是否回敬）
## 协议是否有进展
## 待确认问题
## 是否发现矛盾
```
