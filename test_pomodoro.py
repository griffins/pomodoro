"""Tests for the Pomodoro Timer application.

Note: The source modules use Python 2 syntax (raw_input, print statements)
and cannot be imported directly in Python 3. These tests validate the
underlying business logic and database operations by replicating the
core algorithms.
"""

import pytest
import sqlite3
import datetime
import time as time_mod


# ---------------------------------------------------------------------------
# Helper: replicate core functions from the source modules
# ---------------------------------------------------------------------------

def time_in_sec(time_str):
    """Replicates countdown_timer.time_in_sec logic."""
    total_time = time_str.split(':')
    for i in [0, 1, 2]:
        total_time[i] = int(total_time[i])
    return total_time[2] + (total_time[1] * 60) + (total_time[0] * 60 * 60)


def cycle(tasks_length, tasks_time):
    """Replicates new_task.cycle logic."""
    if time_in_sec(tasks_length) < time_in_sec(tasks_time):
        return 1
    else:
        return time_in_sec(tasks_length) // time_in_sec(tasks_time)


def validate_time_format(time_str):
    """Replicates the time validation logic used in config functions."""
    parts = time_str.split(':')
    for i in [0, 1, 2]:
        parts[i] = int(parts[i])
    return True


def validate_sound(value):
    """Replicates sound_settings validation logic from config.py."""
    if value == '':
        return True
    elif value == '0':
        return False
    elif value == '1':
        return True
    else:
        raise ValueError("Invalid sound setting")


# ---------------------------------------------------------------------------
# Database fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def db(tmp_path):
    """Create a temporary database matching the Pomodoro schema."""
    db_path = str(tmp_path / "test_pomodoro.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Pomodoro (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        taskname TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        totaltime TEXT,
        cycles INT,
        shortb TEXT,
        longb TEXT,
        sound INT)
    ''')
    conn.commit()
    yield conn
    conn.close()


def insert_task(conn, task_name, time_stamp, cycle_time, cycles, shortb, longb, sound):
    """Replicates sql_file.input_data logic."""
    c = conn.cursor()
    c.execute(
        "INSERT INTO Pomodoro (taskname, timestamp, totaltime, cycles, shortb, longb, sound) "
        "VALUES (?,?,?,?,?,?,?)",
        (task_name, time_stamp, cycle_time, cycles, shortb, longb, sound),
    )
    conn.commit()


# ===========================================================================
# Tests: time_in_sec (countdown_timer.py)
# ===========================================================================

class TestTimeInSec:

    def test_one_hour(self):
        assert time_in_sec("01:00:00") == 3600

    def test_one_minute(self):
        assert time_in_sec("00:01:00") == 60

    def test_one_second(self):
        assert time_in_sec("00:00:01") == 1

    def test_zero(self):
        assert time_in_sec("00:00:00") == 0

    def test_default_cycle_time(self):
        assert time_in_sec("00:25:00") == 1500

    def test_default_short_break(self):
        assert time_in_sec("00:05:00") == 300

    def test_default_long_break(self):
        assert time_in_sec("00:15:00") == 900

    def test_complex_time(self):
        # 1*3600 + 30*60 + 45 = 5445
        assert time_in_sec("01:30:45") == 5445

    def test_large_hours(self):
        assert time_in_sec("10:00:00") == 36000

    def test_invalid_format_raises(self):
        with pytest.raises((ValueError, IndexError)):
            time_in_sec("invalid")

    def test_missing_field_raises(self):
        with pytest.raises((ValueError, IndexError)):
            time_in_sec("00:00")

    def test_empty_string_raises(self):
        with pytest.raises((ValueError, IndexError)):
            time_in_sec("")


# ===========================================================================
# Tests: cycle calculation (new_task.py)
# ===========================================================================

class TestCycle:

    def test_task_shorter_than_cycle(self):
        # task length < cycle time → 1 cycle
        assert cycle("00:10:00", "00:25:00") == 1

    def test_exact_division(self):
        # 50 min / 25 min = 2
        assert cycle("00:50:00", "00:25:00") == 2

    def test_with_remainder(self):
        # 60 min / 25 min = 2 (integer division)
        assert cycle("01:00:00", "00:25:00") == 2

    def test_multiple_cycles(self):
        # 120 min / 25 min = 4
        assert cycle("02:00:00", "00:25:00") == 4

    def test_equal_times(self):
        assert cycle("00:25:00", "00:25:00") == 1

    def test_default_settings(self):
        # Default: task_length=01:00:00, cycle_time=00:25:00
        assert cycle("01:00:00", "00:25:00") == 2

    def test_debug_defaults(self):
        # Debug defaults from new_task.py: 00:01:00 / 00:00:15 = 4
        assert cycle("00:01:00", "00:00:15") == 4

    def test_single_second_cycles(self):
        # 10 seconds / 2 seconds = 5
        assert cycle("00:00:10", "00:00:02") == 5


# ===========================================================================
# Tests: database operations (sql_file.py)
# ===========================================================================

class TestDatabaseSchema:

    def test_table_exists(self, db):
        c = db.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Pomodoro'")
        assert c.fetchone() is not None

    def test_table_columns(self, db):
        c = db.cursor()
        c.execute("PRAGMA table_info(Pomodoro)")
        columns = {row[1]: row[2] for row in c.fetchall()}
        expected = {
            "id": "INTEGER",
            "taskname": "TEXT",
            "timestamp": "TEXT",
            "totaltime": "TEXT",
            "cycles": "INT",
            "shortb": "TEXT",
            "longb": "TEXT",
            "sound": "INT",
        }
        for col, dtype in expected.items():
            assert col in columns
            assert columns[col] == dtype

    def test_id_autoincrement(self, db):
        insert_task(db, "A", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        insert_task(db, "B", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("SELECT id FROM Pomodoro ORDER BY id")
        ids = [row[0] for row in c.fetchall()]
        assert ids == [1, 2]


class TestInsertData:

    def test_insert_single_task(self, db):
        insert_task(db, "Study", "2026:02:26", "01:00:00", 3, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("SELECT * FROM Pomodoro")
        rows = c.fetchall()
        assert len(rows) == 1
        assert rows[0][1] == "Study"
        assert rows[0][2] == "2026:02:26"
        assert rows[0][3] == "01:00:00"
        assert rows[0][4] == 3
        assert rows[0][5] == "00:05:00"
        assert rows[0][6] == "00:15:00"
        assert rows[0][7] == 1

    def test_insert_multiple_tasks(self, db):
        insert_task(db, "Task1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        insert_task(db, "Task2", "2026:02:26", "00:30:00", 1, "00:05:00", "00:15:00", 0)
        insert_task(db, "Task3", "2026:02:27", "02:00:00", 4, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("SELECT COUNT(*) FROM Pomodoro")
        assert c.fetchone()[0] == 3

    def test_insert_with_sound_boolean(self, db):
        insert_task(db, "T1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", True)
        insert_task(db, "T2", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", False)
        c = db.cursor()
        c.execute("SELECT sound FROM Pomodoro ORDER BY id")
        rows = c.fetchall()
        assert rows[0][0] == 1
        assert rows[1][0] == 0


class TestDeleteAllTasks:

    def test_delete_all(self, db):
        insert_task(db, "Task1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        insert_task(db, "Task2", "2026:02:27", "00:30:00", 1, "00:05:00", "00:15:00", 0)
        c = db.cursor()
        c.execute("DELETE FROM Pomodoro")
        db.commit()
        c.execute("SELECT COUNT(*) FROM Pomodoro")
        assert c.fetchone()[0] == 0

    def test_delete_all_empty_table(self, db):
        c = db.cursor()
        c.execute("DELETE FROM Pomodoro")
        db.commit()
        c.execute("SELECT COUNT(*) FROM Pomodoro")
        assert c.fetchone()[0] == 0


class TestListByDate:

    def test_filter_by_date(self, db):
        insert_task(db, "Task1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        insert_task(db, "Task2", "2026:02:27", "00:30:00", 1, "00:05:00", "00:15:00", 0)
        insert_task(db, "Task3", "2026:02:26", "02:00:00", 4, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("SELECT * FROM Pomodoro WHERE timestamp = ?", ("2026:02:26",))
        rows = c.fetchall()
        assert len(rows) == 2
        assert rows[0][1] == "Task1"
        assert rows[1][1] == "Task3"

    def test_no_results_for_date(self, db):
        insert_task(db, "Task1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("SELECT * FROM Pomodoro WHERE timestamp = ?", ("2099:01:01",))
        assert len(c.fetchall()) == 0

    def test_all_tasks_same_date(self, db):
        for i in range(5):
            insert_task(db, f"Task{i}", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("SELECT * FROM Pomodoro WHERE timestamp = ?", ("2026:02:26",))
        assert len(c.fetchall()) == 5


class TestListAll:

    def test_list_all_tasks(self, db):
        insert_task(db, "Task1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        insert_task(db, "Task2", "2026:02:27", "00:30:00", 1, "00:05:00", "00:15:00", 0)
        c = db.cursor()
        c.execute("SELECT * FROM Pomodoro")
        assert len(c.fetchall()) == 2

    def test_list_all_empty(self, db):
        c = db.cursor()
        c.execute("SELECT * FROM Pomodoro")
        assert len(c.fetchall()) == 0


class TestUpdateOperations:

    def test_update_short_break(self, db):
        insert_task(db, "Task1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("UPDATE Pomodoro SET shortb = ? WHERE id = ?", ("00:10:00", 1))
        db.commit()
        c.execute("SELECT shortb FROM Pomodoro WHERE id = 1")
        assert c.fetchone()[0] == "00:10:00"

    def test_update_long_break(self, db):
        insert_task(db, "Task1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("UPDATE Pomodoro SET longb = ? WHERE id = ?", ("00:20:00", 1))
        db.commit()
        c.execute("SELECT longb FROM Pomodoro WHERE id = 1")
        assert c.fetchone()[0] == "00:20:00"

    def test_update_sound(self, db):
        insert_task(db, "Task1", "2026:02:26", "01:00:00", 2, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("UPDATE Pomodoro SET sound = ? WHERE id = ?", (0, 1))
        db.commit()
        c.execute("SELECT sound FROM Pomodoro WHERE id = 1")
        assert c.fetchone()[0] == 0

    def test_update_nonexistent_task(self, db):
        c = db.cursor()
        c.execute("UPDATE Pomodoro SET shortb = ? WHERE id = ?", ("00:10:00", 999))
        db.commit()
        c.execute("SELECT COUNT(*) FROM Pomodoro")
        assert c.fetchone()[0] == 0


# ===========================================================================
# Tests: config validation (config.py)
# ===========================================================================

class TestConfigTimeValidation:

    def test_valid_cycle_time(self):
        assert validate_time_format("00:25:00") is True

    def test_valid_short_break(self):
        assert validate_time_format("00:05:00") is True

    def test_valid_long_break(self):
        assert validate_time_format("00:15:00") is True

    def test_valid_task_length(self):
        assert validate_time_format("01:00:00") is True

    def test_valid_all_zeros(self):
        assert validate_time_format("00:00:00") is True

    def test_invalid_missing_seconds(self):
        with pytest.raises((ValueError, IndexError)):
            validate_time_format("00:25")

    def test_invalid_non_numeric(self):
        with pytest.raises(ValueError):
            validate_time_format("ab:cd:ef")

    def test_invalid_empty(self):
        with pytest.raises((ValueError, IndexError)):
            validate_time_format("")

    def test_extra_colons_still_parses(self):
        # The source validation only checks indices 0-2, so extra fields are ignored
        assert validate_time_format("00:25:00:00") is True


class TestSoundValidation:

    def test_default_returns_true(self):
        assert validate_sound('') is True

    def test_off_returns_false(self):
        assert validate_sound('0') is False

    def test_on_returns_true(self):
        assert validate_sound('1') is True

    def test_invalid_number(self):
        with pytest.raises(ValueError):
            validate_sound('2')

    def test_invalid_text(self):
        with pytest.raises(ValueError):
            validate_sound('yes')

    def test_invalid_negative(self):
        with pytest.raises(ValueError):
            validate_sound('-1')


# ===========================================================================
# Tests: timestamp format (new_task.py)
# ===========================================================================

class TestTimestamp:

    def test_format_matches_expected_pattern(self):
        t = time_mod.time()
        ts = datetime.datetime.fromtimestamp(t).strftime('%Y:%m:%d')
        parts = ts.split(':')
        assert len(parts) == 3
        assert len(parts[0]) == 4  # year
        assert len(parts[1]) == 2  # month
        assert len(parts[2]) == 2  # day

    def test_valid_year(self):
        t = time_mod.time()
        ts = datetime.datetime.fromtimestamp(t).strftime('%Y:%m:%d')
        year = int(ts.split(':')[0])
        assert year >= 2020

    def test_valid_month(self):
        t = time_mod.time()
        ts = datetime.datetime.fromtimestamp(t).strftime('%Y:%m:%d')
        month = int(ts.split(':')[1])
        assert 1 <= month <= 12

    def test_valid_day(self):
        t = time_mod.time()
        ts = datetime.datetime.fromtimestamp(t).strftime('%Y:%m:%d')
        day = int(ts.split(':')[2])
        assert 1 <= day <= 31

    def test_timestamp_usable_as_db_key(self, db):
        """Verify the timestamp format works for database queries."""
        t = time_mod.time()
        ts = datetime.datetime.fromtimestamp(t).strftime('%Y:%m:%d')
        insert_task(db, "Test", ts, "01:00:00", 2, "00:05:00", "00:15:00", 1)
        c = db.cursor()
        c.execute("SELECT * FROM Pomodoro WHERE timestamp = ?", (ts,))
        assert len(c.fetchall()) == 1
