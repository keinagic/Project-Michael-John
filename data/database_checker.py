import sqlite3


def check_db_integrity(conn):
    c = conn.cursor()

    # Expected schemas (define these based on your application's requirements)
    expected_trainees_columns = {
        "unique_trainee_id": "TEXT",
        "last_name": "TEXT",
        "first_name": "TEXT",
        "novice_status": "INTEGER",
    }
    expected_scores_columns = {
        "id": "INTEGER",
        "trainee_id": "INTEGER",
        "score": "REAL",
        "role": "TEXT",
        "type": "TEXT",
    }
    expected_teams_columns = {"id": "INTEGER", "format": "TEXT", "team_name": "TEXT"}
    expected_team_members_columns = {
        "id": "INTEGER",
        "team_id": "INTEGER",
        "trainee_id": "TEXT",
    }

    # Check trainees table
    check_table_schema(conn, "trainees", expected_trainees_columns)

    # Check scores table
    check_table_schema(conn, "scores", expected_scores_columns)

    # Check teams table
    check_table_schema(conn, "teams", expected_teams_columns)

    # Check team_members table
    check_table_schema(conn, "team_members", expected_team_members_columns)


def check_table_schema(conn, table_name, expected_columns):
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table_name})")
    actual_columns = {
        col[1]: col[2] for col in c.fetchall()
    }  

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
                f"Type change for column '{col}' is not automatically applied. Manual intervention is needed"
            )  # sqlite does not allow changing column type.
    conn.commit()
