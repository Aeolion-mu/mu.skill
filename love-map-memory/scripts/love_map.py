#!/usr/bin/env python3
"""CLI helpers for the Love Map Memory database.

The database is Markdown-first. This script does ONLY deterministic, whole-database
work that an agent is bad at doing reliably by hand:

- ``init``        scaffold the database tree (+ a self-protecting .gitignore)
- ``add-person``  scaffold one person's directory tree, profile, summary, protocol
- ``list-people`` list person IDs
- ``validate``    verify structure AND parse every YAML frontmatter (catches breakage)
- ``review``      the "people change" engine: list facts that are overdue for re-confirming

Content *generation* (events, profile facts, contradictions, summaries) is intentionally
NOT done here. Those require judgment (which layer? fact vs inference? is this a change?),
so the agent authors them directly from the templates in ``_schema/templates/``. Keeping
generation out of the script removes a whole class of silent-failure and broken-YAML bugs
and gives create + update a single mechanism (the agent's editor) instead of two.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

try:  # PyYAML is optional: only `validate` uses it for deep frontmatter parsing.
    import yaml  # type: ignore

    HAVE_YAML = True
except Exception:  # pragma: no cover - environment dependent
    yaml = None  # type: ignore
    HAVE_YAML = False


SKILL_ROOT = Path(__file__).resolve().parents[1]

# layer key -> (directory name, [category folders])
# 01-04 mirror Gottman's four love-map layers; 05 is the relationship/dyad layer (方法论 L5).
# `formative-history` under 01 is where L3 (来历与塑造) lives.
LAYER_DIRS = {
    "basic_facts": (
        "01_basic-facts",
        ["identity", "family-friends", "work-study", "daily-life", "formative-history"],
    ),
    "preferences_habits": (
        "02_preferences-habits",
        ["food", "entertainment", "communication-style", "routines", "dislikes", "activities", "environment"],
    ),
    "stress_emotions": (
        "03_stress-emotions",
        ["current-stressors", "fears", "triggers", "emotional-needs", "support-methods"],
    ),
    "dreams_values": (
        "04_dreams-values",
        ["life-goals", "unfinished-dreams", "values", "identity", "meaning"],
    ),
    "relationship": (
        "05_relationship",
        ["feels-loved-by", "repair-and-conflict", "relationship-wants", "past-relationship-wounds"],
    ),
}

LAYER_TAGS = {
    "basic_facts": "basic-facts",
    "preferences_habits": "preferences-habits",
    "stress_emotions": "stress-emotions",
    "dreams_values": "dreams-values",
    "relationship": "relationship",
}

# Topics that are pull-only (只记录对方主动分享). Used by validate to warn on elicited captures.
# ASCII terms use word boundaries so "ex" doesn't match exam/Alex/next/experience;
# CJK terms can't use \b (CJK chars are word chars) so they match as plain substrings.
SENSITIVE_RE = re.compile(
    r"\b(?:trauma|ex|illness|abuse|family-pain|past-relationship-wounds)\b"
    r"|创伤|前任|疾病|家庭伤痛|冷暴力",
    re.IGNORECASE,
)

STALE_DAYS_DEFAULT = 90


def today() -> str:
    return dt.date.today().isoformat()


def now() -> str:
    return dt.datetime.now().replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[\\/:*?\"<>|]+", "-", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"_+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def yaml_inner(value: str) -> str:
    """Escape a string so it is safe *inside* a double-quoted YAML scalar.

    Templates wrap interpolated fields like ``title: "{{title}}"``; without this,
    a value containing a double quote (very common in emotional quotes, e.g.
    ``她说"我害怕被抛弃"``) produces unparseable frontmatter.
    """
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    value = value.replace("\r", " ").replace("\n", " ")
    return value


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_gitkeep(path: Path) -> None:
    ensure_dir(path)
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.write_text("", encoding="utf-8")


def write_file(path: Path, content: str, force: bool = False) -> bool:
    ensure_dir(path.parent)
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def read_template(name: str) -> str:
    return (SKILL_ROOT / "templates" / name).read_text(encoding="utf-8")


def render(template: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        template = template.replace("{{" + key + "}}", str(value))
    return template


def copy_tree_contents(src: Path, dst: Path, force: bool = False) -> list[Path]:
    copied: list[Path] = []
    if not src.exists():
        return copied
    for item in src.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(src)
        target = dst / rel
        ensure_dir(target.parent)
        if target.exists() and not force:
            continue
        shutil.copy2(item, target)
        copied.append(target)
    return copied


def split_frontmatter(text: str) -> str | None:
    """Return the raw YAML frontmatter block (without the --- fences), or None."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end]


def db_gitignore() -> str:
    # The database holds intimate, often non-consenting profiles of real people.
    # A self-contained `*` ignore keeps it out of git even if the DB is moved or renamed.
    return "# Love Map DB holds sensitive personal data. Never commit it.\n*\n"


def db_readme() -> str:
    return """# Love Map DB

这是一个面向多个人的 Love Map 外置记忆数据库。

> ⚠️ **隐私**：本库存放的是关于真实的人、且往往未经其同意的私人画像。
> 本目录已自带 `.gitignore (*)`，默认不进版本库。**不要**把它提交或推送到任何远端，
> 也建议把它放在 repo 之外的私有路径。

核心原则：

```txt
一个人 = 一个 map
事件 = 证据
四层画像 + 关系层 = 长期理解
协议层 = 你俩到了第几级、是否双向解锁
```

## 结构

```txt
love-map-db/
├── _schema/
├── inbox/
├── people/
│   ├── index.md
│   └── {person_id}/
│       ├── profile.md          # 含 current_level
│       ├── protocol.md         # L0-L5 双向握手状态
│       ├── love-map-summary.md
│       ├── events/
│       ├── 01_basic-facts/     # 含 formative-history (L3)
│       ├── 02_preferences-habits/
│       ├── 03_stress-emotions/
│       ├── 04_dreams-values/
│       ├── 05_relationship/    # L5：被爱方式 / 冲突修复 / 想要的关系
│       ├── summaries/
│       └── contradictions/
└── attachments/
```

## 常用命令

```bash
python love-map-memory/scripts/love_map.py add-person love-map-db alice --name "Alice" --context "约会对象"
python love-map-memory/scripts/love_map.py validate love-map-db   # 结构 + YAML 校验
python love-map-memory/scripts/love_map.py review love-map-db      # 哪些事实该回头确认了
```

事件、画像事实、矛盾、summary 由 agent 读 `_schema/templates/` 里的模板直接创建/更新。
"""


def people_index() -> str:
    # The `>` note goes ABOVE the table so appended data rows stay flush against the
    # separator row (a blank line between separator and data ends a GFM table).
    return f"""---
type: index
title: People Index
updated_at: "{today()}"
---

# People Index

> `person_id` 是稳定 ID；角色和认识场景写在 `context` 或个人 `profile.md` 中，不要写死进目录名。

| person_id | display_name | context | current_level | status | updated_at |
|---|---|---|---|---|---|
"""


def md_cell(value: str) -> str:
    """Make a string safe inside a Markdown table cell."""
    return value.replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def cmd_init(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    if db.exists() and not db.is_dir():
        print(f"Cannot init: {db} exists and is not a directory.", file=sys.stderr)
        return 1
    created: list[Path] = []

    for rel in ["_schema", "_schema/templates", "inbox", "people", "attachments"]:
        ensure_dir(db / rel)

    # Privacy guard FIRST so the directory is self-ignoring before any data lands.
    if write_file(db / ".gitignore", db_gitignore(), args.force):
        created.append(db / ".gitignore")
    if write_file(db / "README.md", db_readme(), args.force):
        created.append(db / "README.md")
    if write_file(db / "people" / "index.md", people_index(), args.force):
        created.append(db / "people" / "index.md")

    created += copy_tree_contents(SKILL_ROOT / "_schema", db / "_schema", args.force)
    created += copy_tree_contents(SKILL_ROOT / "templates", db / "_schema" / "templates", args.force)

    ensure_gitkeep(db / "inbox")
    ensure_gitkeep(db / "attachments")

    print(f"Initialized Love Map DB at {db}")
    print("Privacy: a self-contained .gitignore (*) was written; keep this DB out of git.")
    if created:
        print("Created/copied:")
        for path in created:
            print(f"- {path}")
    return 0


def create_person_dirs(person_dir: Path) -> None:
    ensure_dir(person_dir)
    ensure_gitkeep(person_dir / "events")
    ensure_gitkeep(person_dir / "contradictions")
    for period in ["weekly", "monthly", "quarterly"]:
        ensure_gitkeep(person_dir / "summaries" / period)
    for layer_dir, categories in LAYER_DIRS.values():
        for category in categories:
            ensure_gitkeep(person_dir / layer_dir / category)


def append_people_index(db: Path, person_id: str, display_name: str, context: str) -> None:
    index = db / "people" / "index.md"
    if not index.exists():
        write_file(index, people_index())
    text = index.read_text(encoding="utf-8")
    # Match a whole cell so person ids that are prefixes of each other don't collide.
    if f"| {person_id} |" in text:
        return
    row = f"| {person_id} | {md_cell(display_name)} | {md_cell(context)} | L0 | active | {today()} |\n"
    if not text.endswith("\n"):
        text += "\n"
    index.write_text(text + row, encoding="utf-8")


def _existing_profile_identity(person_dir: Path) -> tuple[str, str] | None:
    """Return (display_name, context) recorded in an existing profile.md, if any."""
    profile = person_dir / "profile.md"
    if not profile.exists():
        return None
    fm = split_frontmatter(profile.read_text(encoding="utf-8")) or ""
    dn = re.search(r'^display_name:\s*"?(.*?)"?\s*$', fm, re.M)
    ctx = re.search(r'^context:\s*"?(.*?)"?\s*$', fm, re.M)
    return (dn.group(1) if dn else "", ctx.group(1) if ctx else "")


def cmd_add_person(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    person_id = slugify(args.person_id)
    display_name = args.name or args.person_id
    context = args.context or ""
    person_dir = db / "people" / person_id

    # Guard against two *different* people slugifying to the same id (e.g. "Li Na" & "li-na").
    existing = _existing_profile_identity(person_dir)
    if existing is not None and not args.force:
        old_name, old_ctx = existing
        # old_name is read back from the (yaml-escaped) profile, so compare same-form.
        same = (old_name == yaml_inner(display_name)) or (not args.name)
        if not same:
            print(
                f"person_id '{person_id}' already exists as '{old_name}' (context: {old_ctx}).\n"
                f"You passed a different name '{display_name}'. If this is a DIFFERENT person, "
                f"use a distinct id (e.g. {person_id}-2, {person_id}-hr). "
                f"To intentionally regenerate scaffolding, pass --force "
                f"(WARNING: --force overwrites profile.md / love-map-summary.md / protocol.md, "
                f"including any hand-written content).",
                file=sys.stderr,
            )
            return 1

    create_person_dirs(person_dir)

    mapping = {
        "person_id": person_id,
        "display_name": yaml_inner(display_name),
        "context": yaml_inner(context),
        "date": today(),
    }
    profile = render(read_template("person-profile-template.md"), mapping)
    summary = render(read_template("love-map-summary-template.md"), mapping)
    protocol = render(read_template("protocol-template.md"), mapping)

    created = []
    skipped = []
    for rel, content in [
        ("profile.md", profile),
        ("love-map-summary.md", summary),
        ("protocol.md", protocol),
    ]:
        if write_file(person_dir / rel, content, args.force):
            created.append(person_dir / rel)
        else:
            skipped.append(person_dir / rel)
    append_people_index(db, person_id, display_name, context)

    print(f"Person map ready: {person_dir}")
    if created:
        print("Created:")
        for path in created:
            print(f"- {path}")
    if skipped:
        print("Already existed (kept as-is; use --force to regenerate):")
        for path in skipped:
            print(f"- {path}")
    return 0


def cmd_list_people(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    people_dir = db / "people"
    if not people_dir.exists():
        print(f"No people directory: {people_dir}", file=sys.stderr)
        return 1
    for path in sorted(people_dir.iterdir()):
        if path.is_dir():
            print(path.name)
    return 0


def _iter_fact_files(db: Path):
    people_dir = db / "people"
    if not people_dir.exists():
        return
    layer_dirs = [d for d, _ in LAYER_DIRS.values()]
    for person_dir in sorted(p for p in people_dir.iterdir() if p.is_dir()):
        for layer_dir in layer_dirs:
            base = person_dir / layer_dir
            if not base.exists():
                continue
            for md in sorted(base.rglob("*.md")):
                yield person_dir.name, md


def _field(fm: str, name: str) -> str | None:
    """Read a top-level scalar from frontmatter, handling quotes and inline `# comments`."""
    m = re.search(rf"^{name}:\s*(.*?)\s*$", fm, re.M)
    if not m:
        return None
    raw = m.group(1)
    if raw[:1] == '"':  # double-quoted: respect \" escapes
        dq = re.match(r'"((?:\\.|[^"\\])*)"', raw)
        return dq.group(1).replace('\\"', '"').replace("\\\\", "\\") if dq else raw[1:]
    if raw[:1] == "'":  # single-quoted
        end = raw.find("'", 1)
        return raw[1:end] if end != -1 else raw[1:]
    return re.split(r"\s+#", raw, maxsplit=1)[0].strip()  # unquoted: drop inline comment


def cmd_review(args: argparse.Namespace) -> int:
    """The "people change" engine: list active facts overdue for re-confirmation."""
    db = Path(args.db_path)
    cutoff = args.days
    today_date = dt.date.today()
    rows: list[tuple[int, str, str, str, str]] = []  # (age, date, person, title, path)

    for person, md in _iter_fact_files(db):
        if args.person and person != slugify(args.person):
            continue
        fm = split_frontmatter(md.read_text(encoding="utf-8"))
        if fm is None:
            continue
        status = (_field(fm, "status") or "active").strip()
        if status in {"outdated", "contradicted"}:
            continue  # already retired; not something to re-confirm
        last = _field(fm, "last_confirmed_at") or _field(fm, "first_observed_at")
        if not last:
            continue
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", last)
        if not m:
            continue
        last_date = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        age = (today_date - last_date).days
        if age < cutoff:
            continue
        title = _field(fm, "title") or md.stem
        rows.append((age, last, person, title, str(md)))

    rows.sort(reverse=True)  # oldest (largest age) first
    if not rows:
        print(f"Nothing overdue (threshold: {cutoff} days). Your maps are fresh. ✅")
        return 0

    print(f"Facts not confirmed in {cutoff}+ days (oldest first) — 该回头对齐一下了：\n")
    for age, last, person, title, path in rows:
        print(f"  [{age:>4}d] {person:<12} {title}")
        print(f"          last_confirmed: {last}  ·  {path}")
    print(f"\n{len(rows)} fact(s) overdue. 把这些当成下次见面/聊天时温柔地重新确认的清单。")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    errors: list[str] = []
    warnings: list[str] = []

    for rel in ["README.md", "_schema", "inbox", "people", "people/index.md", "attachments"]:
        if not (db / rel).exists():
            errors.append(f"Missing {db / rel}")
    if not (db / ".gitignore").exists():
        warnings.append(f"Missing {db / '.gitignore'} — this DB is NOT self-protected from git.")

    people_dir = db / "people"
    if people_dir.exists():
        for person_dir in sorted(p for p in people_dir.iterdir() if p.is_dir()):
            for rel in ["profile.md", "love-map-summary.md", "protocol.md", "events", "summaries", "contradictions"]:
                if not (person_dir / rel).exists():
                    errors.append(f"Missing {person_dir / rel}")
            for layer_dir, _ in LAYER_DIRS.values():
                if not (person_dir / layer_dir).exists():
                    errors.append(f"Missing {person_dir / layer_dir}")
            # current_level should agree across profile.md and protocol.md
            levels: dict[str, str] = {}
            for rel in ["profile.md", "protocol.md"]:
                f = person_dir / rel
                if f.exists():
                    cl = _field(split_frontmatter(f.read_text(encoding="utf-8")) or "", "current_level")
                    if cl:
                        levels[rel] = cl.strip()
            if len(set(levels.values())) > 1:
                warnings.append(f"current_level out of sync for {person_dir.name}: {levels}")

    stale = 0
    today_date = dt.date.today()
    for md in db.rglob("*.md"):
        rel_parts = md.relative_to(db).parts
        if md.name == "README.md" or "_schema" in rel_parts:
            continue  # README + all reference material under _schema/ are not data
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        fm = split_frontmatter(text)
        if fm is None:
            warnings.append(f"No frontmatter: {md}")
            continue
        # Deep YAML parse — this is what catches the broken-frontmatter class of bugs.
        if HAVE_YAML and yaml is not None:
            try:
                yaml.safe_load(fm)
            except Exception as exc:  # noqa: BLE001
                first = str(exc).splitlines()[0] if str(exc) else exc.__class__.__name__
                errors.append(f"Unparseable YAML frontmatter: {md} -> {first}")
        # pull-only guard: an elicited capture on a sensitive topic is an ethics warning.
        in_wounds = "past-relationship-wounds" in rel_parts
        sensitive_hit = in_wounds or bool(SENSITIVE_RE.search(fm + "\n" + text))
        if sensitive_hit and re.search(r"^disclosure:\s*elicited", fm, re.M):
            warnings.append(f"Sensitive topic captured as 'elicited' (should be pull-only/volunteered): {md}")
        # privacy guard: anything in past-relationship-wounds must be privacy: restricted.
        if in_wounds and (_field(fm, "privacy") or "normal").strip() != "restricted":
            warnings.append(f"past-relationship-wounds fact should be `privacy: restricted`: {md}")
        # staleness count
        last = _field(fm, "last_confirmed_at")
        status = (_field(fm, "status") or "active").strip()
        if last and status not in {"outdated", "contradicted"}:
            m = re.match(r"(\d{4})-(\d{2})-(\d{2})", last)
            if m:
                age = (today_date - dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))).days
                if age >= STALE_DAYS_DEFAULT:
                    stale += 1

    if not HAVE_YAML:
        warnings.append("PyYAML not installed — skipped deep YAML parsing (pip install pyyaml to enable).")
    if stale:
        warnings.append(f"{stale} fact(s) not confirmed in {STALE_DAYS_DEFAULT}+ days — run `review` to see them.")

    if errors:
        print("Errors:")
        for err in errors:
            print(f"- {err}")
    if warnings:
        print("Warnings:")
        for warn in warnings:
            print(f"- {warn}")
    if not errors and not warnings:
        print(f"OK: {db}")
    else:
        print(f"Validation finished with {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Love Map Memory CLI (scaffold + verify only)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="initialize a love-map-db")
    p.add_argument("db_path")
    p.add_argument("--force", action="store_true", help="overwrite generated files if they already exist")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add-person", help="create a person map (dirs + profile + summary + protocol)")
    p.add_argument("db_path")
    p.add_argument("person_id")
    p.add_argument("--name", default=None, help="display name")
    p.add_argument("--context", default="", help="how you know this person, not a relationship graph")
    p.add_argument("--force", action="store_true", help="regenerate scaffolding, OVERWRITING hand-edited files")
    p.set_defaults(func=cmd_add_person)

    p = sub.add_parser("list-people", help="list person IDs")
    p.add_argument("db_path")
    p.set_defaults(func=cmd_list_people)

    p = sub.add_parser("review", help="list facts overdue for re-confirmation (the 'people change' engine)")
    p.add_argument("db_path")
    p.add_argument("--days", type=int, default=STALE_DAYS_DEFAULT, help="overdue threshold in days")
    p.add_argument("--person", default=None, help="limit to one person_id")
    p.set_defaults(func=cmd_review)

    p = sub.add_parser("validate", help="validate structure and parse every YAML frontmatter")
    p.add_argument("db_path")
    p.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
