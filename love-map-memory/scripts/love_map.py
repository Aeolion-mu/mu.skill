#!/usr/bin/env python3
"""CLI helpers for the Love Map Memory database.

The database is Markdown-first. This script only creates structure and templates;
the Markdown files remain the source of truth for humans and agents.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]

LAYER_DIRS = {
    "basic_facts": ("01_basic-facts", ["identity", "family-friends", "work-study", "daily-life"]),
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
}

LAYER_TAGS = {
    "basic_facts": "basic-facts",
    "preferences_habits": "preferences-habits",
    "stress_emotions": "stress-emotions",
    "dreams_values": "dreams-values",
}


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


def db_readme() -> str:
    return """# Love Map DB

这是一个面向多个人的 Love Map 外置记忆数据库。

核心原则：

```txt
一个人 = 一个 map
事件 = 证据
四层模型 = 长期画像
```

## 结构

```txt
love-map-db/
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

## 使用方式

新增一个人：

```bash
python love-map-memory/scripts/love_map.py add-person love-map-db alice --name "Alice" --context "约会对象"
```

校验：

```bash
python love-map-memory/scripts/love_map.py validate love-map-db
```
"""


def people_index() -> str:
    return f"""---
type: index
title: People Index
updated_at: "{today()}"
---

# People Index

| person_id | display_name | context | status | updated_at |
|---|---|---|---|---|

> `person_id` 是稳定 ID；角色和认识场景写在 `context` 或个人 `profile.md` 中，不要写死进目录名。
"""


def cmd_init(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    created: list[Path] = []

    for rel in ["_schema", "_schema/templates", "inbox", "people", "attachments"]:
        ensure_dir(db / rel)

    if write_file(db / "README.md", db_readme(), args.force):
        created.append(db / "README.md")
    if write_file(db / "people" / "index.md", people_index(), args.force):
        created.append(db / "people" / "index.md")

    created += copy_tree_contents(SKILL_ROOT / "_schema", db / "_schema", args.force)
    created += copy_tree_contents(SKILL_ROOT / "templates", db / "_schema" / "templates", args.force)

    ensure_gitkeep(db / "inbox")
    ensure_gitkeep(db / "attachments")

    print(f"Initialized Love Map DB at {db}")
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
    row_prefix = f"| {person_id} |"
    if row_prefix in text:
        return
    row = f"| {person_id} | {display_name} | {context} | active | {today()} |\n"
    lines = text.splitlines(keepends=True)
    insert_at = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("> `person_id`"):
            insert_at = i
            break
    lines.insert(insert_at, row)
    index.write_text("".join(lines), encoding="utf-8")


def cmd_add_person(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    person_id = slugify(args.person_id)
    display_name = args.name or args.person_id
    context = args.context or ""
    person_dir = db / "people" / person_id

    create_person_dirs(person_dir)

    mapping = {
        "person_id": person_id,
        "display_name": display_name,
        "context": context,
        "date": today(),
    }
    profile = render(read_template("person-profile-template.md"), mapping)
    summary = render(read_template("love-map-summary-template.md"), mapping)

    created = []
    if write_file(person_dir / "profile.md", profile, args.force):
        created.append(person_dir / "profile.md")
    if write_file(person_dir / "love-map-summary.md", summary, args.force):
        created.append(person_dir / "love-map-summary.md")
    append_people_index(db, person_id, display_name, context)

    print(f"Person map ready: {person_dir}")
    if created:
        print("Created:")
        for path in created:
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


def cmd_new_raw(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    date = args.date or today()
    title = args.title or "raw note"
    slug = slugify(title)
    filename = f"{date}__raw-note__{slug}.md"
    path = db / "inbox" / filename
    mapping = {
        "id": f"raw-{date.replace('-', '')}-{dt.datetime.now().strftime('%H%M%S')}",
        "title": title,
        "date": date,
        "created_at": now(),
        "source": args.source,
        "body": args.body or "",
    }
    content = render(read_template("raw-note-template.md"), mapping)
    write_file(path, content, args.force)
    print(path)
    return 0


def cmd_new_event(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    person_id = slugify(args.person_id)
    person_dir = db / "people" / person_id
    if not person_dir.exists():
        print(f"Unknown person: {person_id}. Run add-person first.", file=sys.stderr)
        return 1
    date = args.date or today()
    event_type = slugify(args.event_type)
    topic = slugify(args.topic)
    signal = slugify(args.signal)
    title = args.title or f"{event_type} · {topic} · {signal}"
    yyyy, mm = date.split("-")[:2]
    path = person_dir / "events" / yyyy / mm / f"{date}__{event_type}__{topic}__{signal}.md"
    mapping = {
        "id": f"event-{date.replace('-', '')}-{dt.datetime.now().strftime('%H%M%S')}",
        "person_id": person_id,
        "title": title,
        "event_type": event_type,
        "topic": topic,
        "signal": signal,
        "date": date,
        "created_at": now(),
        "confidence": str(args.confidence),
        "source": args.source,
    }
    content = render(read_template("event-template.md"), mapping)
    write_file(path, content, args.force)
    print(path)
    return 0


def cmd_new_fact(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    person_id = slugify(args.person_id)
    person_dir = db / "people" / person_id
    if not person_dir.exists():
        print(f"Unknown person: {person_id}. Run add-person first.", file=sys.stderr)
        return 1
    if args.layer not in LAYER_DIRS:
        print(f"Unknown layer: {args.layer}. Choices: {', '.join(LAYER_DIRS)}", file=sys.stderr)
        return 1

    layer_dir = LAYER_DIRS[args.layer][0]
    category = slugify(args.category)
    title = args.title
    slug = slugify(args.slug or title)
    date = args.date or today()
    path = person_dir / layer_dir / category / f"{slug}.md"
    evidence = "[]"
    if args.evidence:
        evidence = "\n" + "\n".join(f"  - {item}" for item in args.evidence)
    mapping = {
        "id": f"fact-{date.replace('-', '')}-{dt.datetime.now().strftime('%H%M%S')}",
        "person_id": person_id,
        "title": title,
        "layer": args.layer,
        "layer_tag": LAYER_TAGS[args.layer],
        "category": category,
        "date": date,
        "created_at": now(),
        "confidence": str(args.confidence),
        "evidence": evidence,
    }
    content = render(read_template("profile-fact-template.md"), mapping)
    write_file(path, content, args.force)
    print(path)
    return 0


def has_frontmatter(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return True
    return text.startswith("---\n") and "\n---" in text[4:]


def cmd_validate(args: argparse.Namespace) -> int:
    db = Path(args.db_path)
    errors: list[str] = []
    warnings: list[str] = []

    for rel in ["README.md", "_schema", "inbox", "people", "people/index.md", "attachments"]:
        if not (db / rel).exists():
            errors.append(f"Missing {db / rel}")

    people_dir = db / "people"
    if people_dir.exists():
        for person_dir in sorted(p for p in people_dir.iterdir() if p.is_dir()):
            for rel in ["profile.md", "love-map-summary.md", "events", "summaries", "contradictions"]:
                if not (person_dir / rel).exists():
                    errors.append(f"Missing {person_dir / rel}")
            for layer_dir, _categories in LAYER_DIRS.values():
                if not (person_dir / layer_dir).exists():
                    errors.append(f"Missing {person_dir / layer_dir}")

    for md in db.rglob("*.md"):
        if md.name == "README.md" or md.match("_schema/*.md"):
            continue
        if not has_frontmatter(md):
            warnings.append(f"No frontmatter: {md}")

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
    parser = argparse.ArgumentParser(description="Love Map Memory CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="initialize a love-map-db")
    p.add_argument("db_path")
    p.add_argument("--force", action="store_true", help="overwrite generated files if they already exist")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add-person", help="create a person map")
    p.add_argument("db_path")
    p.add_argument("person_id")
    p.add_argument("--name", default=None, help="display name")
    p.add_argument("--context", default="", help="how you know this person, not a relationship graph")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_add_person)

    p = sub.add_parser("list-people", help="list person IDs")
    p.add_argument("db_path")
    p.set_defaults(func=cmd_list_people)

    p = sub.add_parser("new-raw", help="create an inbox raw note")
    p.add_argument("db_path")
    p.add_argument("--date", default=None)
    p.add_argument("--title", default="raw note")
    p.add_argument("--source", default="memory")
    p.add_argument("--body", default="")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new_raw)

    p = sub.add_parser("new-event", help="create a person-specific event")
    p.add_argument("db_path")
    p.add_argument("person_id")
    p.add_argument("--date", default=None)
    p.add_argument("--event-type", default="conversation")
    p.add_argument("--topic", required=True)
    p.add_argument("--signal", required=True)
    p.add_argument("--title", default=None)
    p.add_argument("--source", default="memory")
    p.add_argument("--confidence", type=float, default=0.6)
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new_event)

    p = sub.add_parser("new-fact", help="create a profile fact in one of the four layers")
    p.add_argument("db_path")
    p.add_argument("person_id")
    p.add_argument("--layer", required=True, choices=sorted(LAYER_DIRS.keys()))
    p.add_argument("--category", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--slug", default=None)
    p.add_argument("--date", default=None)
    p.add_argument("--confidence", type=float, default=0.6)
    p.add_argument("--evidence", action="append", default=[])
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new_fact)

    p = sub.add_parser("validate", help="validate database structure")
    p.add_argument("db_path")
    p.set_defaults(func=cmd_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

