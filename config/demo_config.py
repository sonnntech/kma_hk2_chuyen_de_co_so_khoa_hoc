"""Central configuration for the source transaction demo."""

CATALOG_NAME: str = "workspace"
SCHEMA_NAME: str = "blockchain_pipeline_demo"
SOURCE_TABLE: str = "source_transactions"
RECORD_COUNT: int = 10_000
RANDOM_SEED: int = 42
SOURCE_SYSTEM: str = "SCHOOL_DEMO"


def qualified_table_name(table_name: str) -> str:
    """Return a fully qualified Unity Catalog table name."""
    if not table_name or not table_name.strip():
        raise ValueError("table_name must not be empty")
    return f"`{CATALOG_NAME}`.`{SCHEMA_NAME}`.`{table_name}`"


def qualified_schema_name() -> str:
    """Return the configured Unity Catalog schema name."""
    return f"`{CATALOG_NAME}`.`{SCHEMA_NAME}`"
