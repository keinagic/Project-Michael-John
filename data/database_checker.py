def check_db_integrity(conn):
    # Expected schemas based on the new database.py definitions
    expected_trainees_columns = {
        "unique_trainee_id": "TEXT",
        "first_name": "TEXT",
        "last_name": "TEXT",
        "novice_status": "INTEGER",
    }
    expected_scores_columns = {
        "score_id": "INTEGER",  # Primary key AUTOINCREMENT
        "trainee_id": "TEXT",  # Matches trainees.unique_trainee_id type
        "score": "REAL",
        "role": "TEXT",
        "score_type": "TEXT",  # Renamed from 'type'
    }
    expected_teams_columns = {
        "id": "INTEGER",
        "debate_format": "INTEGER",  # Renamed from 'format'
        "team_name": "TEXT",
    }
    expected_team_members_columns = {
        "team_id": "INTEGER",
        "trainee_id": "TEXT",
    }

    # Check if tables exist before validating their schema
    for table_name, expected_columns in {
        "trainees": expected_trainees_columns,
        "scores": expected_scores_columns,
        "teams": expected_teams_columns,
        "team_members": expected_team_members_columns,
    }.items():
        if table_exists(conn, table_name):
            check_table_schema(conn, table_name, expected_columns)
        else:
            print(f"Table '{table_name}' does not exist.")


def check_table_schema(conn, table_name, expected_columns):
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table_name})")
    actual_columns = {col[1]: col[2] for col in c.fetchall()}

    missing_columns = [col for col in expected_columns if col not in actual_columns]
    extra_columns = [col for col in actual_columns if col not in expected_columns]
    type_mismatches = [
        col
        for col in expected_columns
        if col in actual_columns and expected_columns[col] != actual_columns[col]
    ]

    if missing_columns or extra_columns or type_mismatches:
        print(f"Table '{table_name}' has schema differences:")
        if missing_columns:
            print(f"  Missing columns: {missing_columns}")
        if extra_columns:
            print(f"  Extra columns: {extra_columns}")
        if type_mismatches:
            print(f"  Type mismatches: {type_mismatches}")

        user_consent = input(
            f"Do you want to apply schema changes to '{table_name}'? (yes/no): "
        )
        if user_consent.lower() == "yes":
            apply_schema_changes(conn, table_name, expected_columns, actual_columns)
        else:
            print(f"Schema changes for '{table_name}' not applied.")
    else:
        print(f"Table '{table_name}' schema is correct.")


def apply_schema_changes(conn, table_name, expected_columns, actual_columns):
    c = conn.cursor()
    for col in expected_columns:
        if col not in actual_columns:
            c.execute(
                f"ALTER TABLE {table_name} ADD COLUMN {col} {expected_columns[col]}"
            )
            print(f"Added column '{col}' to '{table_name}'.")
        elif col in actual_columns and expected_columns[col] != actual_columns[col]:
            print(
                f"Type change for column '{col}' is not automatically applied. Manual intervention is needed."
            )
    conn.commit()


def table_exists(conn, table_name):
    c = conn.cursor()
    c.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    )
    return c.fetchone() is not None
