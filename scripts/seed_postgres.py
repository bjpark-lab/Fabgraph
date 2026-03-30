from __future__ import annotations

from pathlib import Path

from app.db.postgres import get_conn


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    sql_paths = [
        root / "infra" / "postgres" / "init" / "001-schema.sql",
        root / "infra" / "postgres" / "init" / "002-seed.sql",
    ]

    with get_conn() as conn:
        with conn.cursor() as cur:
            for sql_path in sql_paths:
                cur.execute(sql_path.read_text(encoding="utf-8"))
        conn.commit()

    print("PostgreSQL seed complete.")


if __name__ == "__main__":
    main()
