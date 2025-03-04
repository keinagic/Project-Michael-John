from pathlib import Path
from database_modules.tournament_database import TournamentDatabaseTables as tdbtables
import sqlite3
from cfg import TOURNAMENT_DATABASE

# Constants for debate formats (you might want to define these elsewhere as well)
AP_FORMAT = 1
BP_FORMAT = 0


class CommonModules:
    @staticmethod
    def set_tournament_name(tournament_name: str) -> str:
        """Return the tournament name (could be processed or validated here)."""
        return tournament_name

    @staticmethod
    def make_inrounds(inround_quanti: int):
        """
        Create in-round tables.
        For each round (from 1 to inround_quanti), a table will be created
        using a function from the db module (not implemented here).
        """
        for round_number in range(1, inround_quanti + 1):
            tdbtables.create_round()
            print(f"Creating table for in-round {round_number}")  # Placeholder

    @staticmethod
    def make_outrounds(outround_teams: int, debate_format: int) -> str:
        """
        Determine the round name for the outrounds based on the number of teams
        and debate format, then create the table for that round (table creation not shown).
        """
        mapping = {
            AP_FORMAT: {
                2: "Grand Finals",
                3: "Pre-Grand Finals",
                4: "Semi Finals",
                8: "Quarter Finals",
                12: "Pre-Quarter Finals",
                16: "Octofinals",
            },
            BP_FORMAT: {
                4: "Grand Finals",
                6: "Pre-Grand Finals",
                8: "Semi Finals",
                12: "Quarter Finals",
                16: "Pre-Quarter Finals",
                24: "Octofinals",
            },
        }
        outround_name = mapping.get(debate_format, {}).get(
            outround_teams, "Does not compute; please eliminate more teams."
        )
        # Here you would call a function to create the round's table, e.g., db.create_round(outround_name)
        print(f"Creating table for outround: {outround_name}")  # Placeholder
        return outround_name

    @staticmethod
    def break_calculator(
        team_id,
        team_score: int,
        debate_format: int,
        speaker_totals: dict,
        reply_total: int,
    ):
        conn = sqlite3.connect(TOURNAMENT_DATABASE)
        c = conn.cursor()

        sp1 = speaker_totals.get("sp1", 0)
        sp2 = speaker_totals.get("sp2", 0)
        sp3 = speaker_totals.get("sp3", 0)
        rep = reply_total

        if debate_format == AP_FORMAT:
            # Adjust the calculation as needed. For example, summing all speaker scores:
            summed_speaks = sp1 + sp2 + sp3 + rep
            c.execute(
                """
                INSERT INTO break_data(
                    team_id,
                    summed_speaks,
                    team_score
                )
                """(
                    team_id, summed_speaks, team_score
                )
            )
        elif debate_format == BP_FORMAT:
            summed_speaks = sp1 + sp2
            c.execute(
                """
            INSERT INTO break_data(
                team_id,
                summed_speaks,
                team_score
            )
            """(
                    team_id, summed_speaks, team_score
                )
            )
        else:
            summed_speaks = 0

    @staticmethod
    def record_inround_speaks(
        unique_trainee_id: str, round_id: str, speaker_score: int
    ) -> int:
        """
        Record an individual speaker score for a given round.
        In a full implementation, this would insert data into the appropriate round table.
        """
        print(
            f"Recording in-round speaker score for {unique_trainee_id} in round {round_id}: {speaker_score}"
        )
        return speaker_score

    @staticmethod
    def record_judge_scores(
        unique_trainee_id: str, round_id: str, judge_score: int
    ) -> int:
        """
        Record an individual judge score for a given round.
        In a full implementation, this would insert data into the appropriate round table.
        """
        print(
            f"Recording judge score for {unique_trainee_id} in round {round_id}: {judge_score}"
        )
        return judge_score

    @staticmethod
    def adj_average_calculator(total_judge_score: int, round_number: int) -> float:
        """
        Calculate the adjudicator's average score.
        Returns total_judge_score if round_number is 1 to avoid division by zero.
        """
        if round_number <= 1:
            return float(total_judge_score)
        else:
            adj_average_score = total_judge_score / (round_number - 1)
            print(f"Calculated adjudicator average: {adj_average_score}")
            return adj_average_score

    @staticmethod
    def adj_allocator():
        """
        Allocate adjudicators based on calculated averages and available judging capacity.
        Implementation details to be added.
        """
        print("Allocating adjudicators... (not implemented)")
        pass

    @staticmethod
    def anomaly_notifier(speaker_score: int, judge_score: int) -> str:
        """
        Notify if there is an anomaly in scores.
        For example, speaker scores should be within 72-78 and judge scores within a valid range.
        """
        anomaly_alert = "Anomaly Detected"
        if speaker_score < 72 or speaker_score > 78:
            return anomaly_alert
        if judge_score < 1 or judge_score > 10:
            return anomaly_alert
        return "All is well"
