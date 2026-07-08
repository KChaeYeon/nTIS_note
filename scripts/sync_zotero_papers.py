#!/usr/bin/env python3
"""Sync the Zotero 'Stimulation' collection tree into docs/02_papers/.

Zotero 라이브러리의 `Stimulation` 컬렉션(+하위 `TibialNerve`, `TIS`)에 들어 있는
논문을 읽어, docs/02_papers/ 에 논문 노트(YYYY_Author_Keyword.md)를 생성/갱신한다.

- 이미 손으로 작성한 노트(같은 `YYYY_Lastname*` 파일 존재)는 **덮어쓰지 않는다**.
- 누락된 논문만 Zotero 메타데이터(제목·저자·저널·DOI·초록)로 스텁 노트를 만든다.
- 재실행 안전(idempotent): 컬렉션에 논문이 추가되면 다시 돌려 반영.

사용:
    python3 scripts/sync_zotero_papers.py            # 기본 Zotero DB 경로
    python3 scripts/sync_zotero_papers.py --db <경로>  # DB 경로 지정
    python3 scripts/sync_zotero_papers.py --dry-run   # 생성 목록만 출력

주의: Zotero 실행 중에는 DB가 잠기므로 임시 복사본을 읽는다(읽기 전용).
"""
from __future__ import annotations
import argparse, os, re, shutil, sqlite3, sys, tempfile
from pathlib import Path

DEFAULT_DB = "/mnt/c/Users/Chaeyeon/Zotero/zotero.sqlite"
PAPERS_DIR = Path(__file__).resolve().parent.parent / "docs" / "02_papers"
# Stimulation 컬렉션 트리 (이름으로 조회 → parent 포함)
ROOT_COLLECTION = "Stimulation"


def field(cur, item_id, name):
    r = cur.execute(
        """SELECT v.value FROM itemData d
           JOIN itemDataValues v ON v.valueID=d.valueID
           JOIN fields f ON f.fieldID=d.fieldID
           WHERE d.itemID=? AND f.fieldName=?""", (item_id, name)).fetchone()
    return r[0] if r else ""


def collection_tree_ids(cur, root_name):
    rows = cur.execute("SELECT collectionID, collectionName, parentCollectionID FROM collections").fetchall()
    by_parent = {}
    root_id = None
    for cid, name, parent in rows:
        by_parent.setdefault(parent, []).append(cid)
        if name == root_name:
            root_id = cid
    if root_id is None:
        return []
    ids, stack = [], [root_id]
    while stack:
        cid = stack.pop()
        ids.append(cid)
        stack.extend(by_parent.get(cid, []))
    return ids


def items_in(cur, coll_ids):
    q = ("SELECT DISTINCT i.itemID, i.key FROM items i "
         "JOIN collectionItems ci ON ci.itemID=i.itemID "
         "WHERE ci.collectionID IN (%s) "
         "AND i.itemID NOT IN (SELECT itemID FROM deletedItems) "
         "AND i.itemTypeID NOT IN (SELECT itemTypeID FROM itemTypes WHERE typeName IN ('attachment','note'))"
         % ",".join("?" * len(coll_ids)))
    return cur.execute(q, coll_ids).fetchall()


def first_author(cur, item_id):
    r = cur.execute(
        """SELECT cr.lastName, cr.firstName FROM itemCreators ic
           JOIN creators cr ON cr.creatorID=ic.creatorID
           WHERE ic.itemID=? ORDER BY ic.orderIndex LIMIT 1""", (item_id,)).fetchone()
    return (r[0] or r[1] or "Unknown") if r else "Unknown"


def slug(text, n=3):
    words = re.findall(r"[A-Za-z0-9]+", text)
    stop = {"the", "a", "an", "of", "for", "in", "on", "and", "to", "using", "via", "with", "based"}
    picked = [w.capitalize() for w in words if w.lower() not in stop][:n]
    return "".join(picked) or "Paper"


def build_note(meta):
    """CLAUDE.md 규칙: 연구 질문 → 방법 → 주요 결과 → 한계점 → 관련 갭."""
    doi = meta["doi"]
    doi_line = f"DOI: [{doi}](https://doi.org/{doi})" if doi else (f"URL: {meta['url']}" if meta['url'] else "")
    cite = f"{meta['author']} et al. ({meta['year']}). *{meta['title']}*."
    if meta["journal"]:
        cite += f" {meta['journal']}."
    abstract = meta["abstract"].strip() or "(초록 없음 — Zotero에 abstract 미등록)"
    return f"""# {meta['author']} {meta['year']} — {meta['title']}

**Citation:** {cite} {doi_line}

> ⚙️ *이 노트는 Zotero `Stimulation` 컬렉션에서 자동 생성된 스텁이다 (`scripts/sync_zotero_papers.py`). 아래 분석 항목은 초록 기반 초안이므로 정독 후 보강할 것.*

---

## 초록 (Abstract)

{abstract}

---

## 연구 질문

(보강 필요)

## 방법

(보강 필요)

## 주요 결과

(보강 필요)

## 한계점

(보강 필요)

## 관련 연구 갭 (nTIS)

(보강 필요 — `docs/03_gaps/gap_analysis.md` 연결)
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.db):
        sys.exit(f"[error] Zotero DB not found: {args.db}")
    tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False).name
    shutil.copy(args.db, tmp)
    con = sqlite3.connect(tmp)
    cur = con.cursor()

    coll_ids = collection_tree_ids(cur, ROOT_COLLECTION)
    if not coll_ids:
        sys.exit(f"[error] '{ROOT_COLLECTION}' 컬렉션을 찾지 못함")

    existing = list(PAPERS_DIR.glob("*.md"))
    existing_stems = {p.stem for p in existing}
    created, skipped = [], []

    for item_id, key in items_in(cur, coll_ids):
        title = field(cur, item_id, "title")
        if not title or title.strip().lower() == "test":
            continue
        date = field(cur, item_id, "date")
        year = (re.search(r"\d{4}", date) or [None])[0] if date else None
        year = re.search(r"\d{4}", date).group(0) if date and re.search(r"\d{4}", date) else "0000"
        author = first_author(cur, item_id)
        author_clean = re.sub(r"[^A-Za-z]", "", author) or "Unknown"
        meta = dict(title=title, year=year, author=author,
                    journal=field(cur, item_id, "publicationTitle"),
                    doi=field(cur, item_id, "DOI"), url=field(cur, item_id, "url"),
                    abstract=field(cur, item_id, "abstractNote"))
        # 이미 같은 (연도, 저자) 노트가 있으면 스킵 (손 작성 노트 보호)
        prefix = f"{year}_{author_clean}"
        if any(s.startswith(prefix) for s in existing_stems):
            skipped.append(f"{prefix} (기존 노트 존재)")
            continue
        fname = f"{year}_{author_clean}_{slug(title)}.md"
        created.append(fname)
        if not args.dry_run:
            (PAPERS_DIR / fname).write_text(build_note(meta), encoding="utf-8")

    con.close()
    os.unlink(tmp)

    print(f"=== Zotero '{ROOT_COLLECTION}' 트리 → 02_papers 동기화 ===")
    print(f"생성 {len(created)}건:")
    for f in created:
        print(f"  + {f}")
    print(f"스킵 {len(skipped)}건 (기존 노트 보호):")
    for s in skipped:
        print(f"  - {s}")


if __name__ == "__main__":
    main()
