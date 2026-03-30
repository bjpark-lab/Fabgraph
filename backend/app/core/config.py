from __future__ import annotations

import os
from pathlib import Path


class Settings:
    app_name: str = os.getenv("FABGRAPH_APP_NAME", "FabGraph API")
    api_prefix: str = os.getenv("FABGRAPH_API_PREFIX", "/api")
    version: str = os.getenv("FABGRAPH_VERSION", "0.1.0")

    postgres_dsn: str = os.getenv(
        "FABGRAPH_POSTGRES_DSN",
        "postgresql://fabgraph:fabgraph@localhost:5432/fabgraph",
    )
    neo4j_uri: str = os.getenv("FABGRAPH_NEO4J_URI", "bolt://localhost:7687")
    neo4j_user: str = os.getenv("FABGRAPH_NEO4J_USER", "neo4j")
    neo4j_password: str = os.getenv("FABGRAPH_NEO4J_PASSWORD", "fabgraph123")

    sample_data_path: Path = Path(
        os.getenv(
            "FABGRAPH_SAMPLE_DATA_PATH",
            Path(__file__).resolve().parents[3] / "samples" / "seed-data" / "latest_wafers.json",
        )
    )

    postgres_connect_timeout_s: float = float(os.getenv("FABGRAPH_POSTGRES_TIMEOUT_S", "1.5"))
    neo4j_connect_timeout_s: float = float(os.getenv("FABGRAPH_NEO4J_TIMEOUT_S", "1.5"))


settings = Settings()
