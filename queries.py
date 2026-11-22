
"""
SQL query functions for the Cyber Incident Investigation Dashboard.
All queries use parameterized statements to prevent SQL injection.
"""

import pandas as pd
from database import create_connection


def execute_query(sql, params=None, fetch=True):
    """Execute a SELECT query and return a DataFrame or empty DataFrame on error."""
    conn = create_connection()
    if not conn:
        return pd.DataFrame()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        if fetch:
            rows = cursor.fetchall()
            return pd.DataFrame(rows)
        return pd.DataFrame()
    except Exception as e:
        print(f"Query error: {e}")
        return pd.DataFrame()
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


def execute_write(sql, params=None):
    """Execute INSERT/UPDATE/DELETE. Returns (success, message)."""
    conn = create_connection()
    if not conn:
        return False, "Could not connect to database."
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params or ())
        conn.commit()
        return True, f"{cursor.rowcount} row(s) affected."
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


def call_procedure(proc_name, args=()):
    """Call a stored procedure."""
    conn = create_connection()
    if not conn:
        return False, "Could not connect to database."
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc(proc_name, args)
        conn.commit()
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        return True, results
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


# ─────────────────────────── KPI Statistics ───────────────────────────

def get_kpi_stats():
    sql = """
        SELECT
            COUNT(*) AS total_incidents,
            SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open_incidents,
            SUM(CASE WHEN status = 'Resolved' THEN 1 ELSE 0 END) AS resolved_incidents,
            SUM(CASE WHEN status = 'Under Investigation' THEN 1 ELSE 0 END) AS under_investigation,
            SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) AS critical_incidents,
            SUM(CASE WHEN severity = 'High' THEN 1 ELSE 0 END) AS high_incidents
        FROM Incidents
    """
    df = execute_query(sql)
    if df.empty:
        return {}
    row = df.iloc[0]
    return {
        "total": int(row.get("total_incidents") or 0),
        "open": int(row.get("open_incidents") or 0),
        "resolved": int(row.get("resolved_incidents") or 0),
        "under_investigation": int(row.get("under_investigation") or 0),
        "critical": int(row.get("critical_incidents") or 0),
        "high": int(row.get("high_incidents") or 0),
    }


def get_total_alerts():
    df = execute_query("SELECT COUNT(*) AS cnt FROM Alerts")
    if df.empty:
        return 0
    return int(df.iloc[0].get("cnt") or 0)


# ─────────────────────────── Charts / Overview ───────────────────────────

def get_incidents_by_severity():
    return execute_query(
        "SELECT severity, COUNT(*) AS count FROM Incidents GROUP BY severity ORDER BY FIELD(severity,'Critical','High','Medium','Low','Unassigned')"
    )


def get_incidents_by_type():
    return execute_query(
        "SELECT incident_type, COUNT(*) AS count FROM Incidents GROUP BY incident_type ORDER BY count DESC"
    )


def get_incidents_by_status():
    return execute_query(
        "SELECT status, COUNT(*) AS count FROM Incidents GROUP BY status"
    )


def get_incident_trend():
    return execute_query(
        "SELECT DATE(reported_at) AS date, COUNT(*) AS count FROM Incidents GROUP BY DATE(reported_at) ORDER BY date"
    )


def get_alerts_by_type():
    return execute_query(
        "SELECT alert_type, COUNT(*) AS count FROM Alerts GROUP BY alert_type ORDER BY count DESC"
    )


def get_alerts_by_severity():
    return execute_query(
        "SELECT severity, COUNT(*) AS count FROM Alerts GROUP BY severity ORDER BY FIELD(severity,'Critical','High','Medium','Low')"
    )


# ─────────────────────────── Incidents ───────────────────────────

def get_all_incidents(severity=None, status=None, incident_type=None, date_from=None, date_to=None):
    sql = """
        SELECT
            i.incident_id,
            i.incident_type,
            i.severity,
            i.status,
            i.description,
            i.reported_at,
            u.name AS affected_user,
            d.device_name,
            d.device_type,
            d.operating_system,
            inv.name AS investigator
        FROM Incidents i
        JOIN Devices d ON i.device_id = d.device_id
        JOIN Users u ON d.user_id = u.user_id
        LEFT JOIN Investigators inv ON i.investigator_id = inv.investigator_id
        WHERE 1=1
    """
    params = []
    if severity and severity != "All":
        sql += " AND i.severity = %s"
        params.append(severity)
    if status and status != "All":
        sql += " AND i.status = %s"
        params.append(status)
    if incident_type and incident_type != "All":
        sql += " AND i.incident_type = %s"
        params.append(incident_type)
    if date_from:
        sql += " AND DATE(i.reported_at) >= %s"
        params.append(str(date_from))
    if date_to:
        sql += " AND DATE(i.reported_at) <= %s"
        params.append(str(date_to))
    sql += " ORDER BY i.reported_at DESC"
    return execute_query(sql, params)


def get_incident_detail(incident_id):
    sql = """
        SELECT
            i.incident_id,
            i.incident_type,
            i.severity,
            i.status,
            i.description,
            i.reported_at,
            u.name AS affected_user,
            u.email AS user_email,
            u.department,
            d.device_name,
            d.device_type,
            d.operating_system,
            inv.name AS investigator,
            inv.email AS investigator_email,
            inv.role AS investigator_role,
            CalculateIncidentAge(i.incident_id) AS incident_age_days
        FROM Incidents i
        JOIN Devices d ON i.device_id = d.device_id
        JOIN Users u ON d.user_id = u.user_id
        LEFT JOIN Investigators inv ON i.investigator_id = inv.investigator_id
        WHERE i.incident_id = %s
    """
    return execute_query(sql, (incident_id,))


def get_incident_alerts(incident_id):
    sql = """
        SELECT a.alert_id, a.alert_type, a.severity, a.detected_at,
               ip.ip_address, ip.ip_type, ip.location
        FROM Alerts a
        LEFT JOIN IP_Addresses ip ON a.ip_id = ip.ip_id
        WHERE a.incident_id = %s
        ORDER BY a.detected_at DESC
    """
    return execute_query(sql, (incident_id,))


def get_incident_status_history(incident_id):
    return execute_query(
        "SELECT history_id, old_status, new_status, changed_at FROM Incident_Status_History WHERE incident_id = %s ORDER BY changed_at",
        (incident_id,)
    )


def get_distinct_incident_types():
    df = execute_query("SELECT DISTINCT incident_type FROM Incidents ORDER BY incident_type")
    if df.empty:
        return []
    return df["incident_type"].tolist()


# ─────────────────────────── Alerts ───────────────────────────

def get_all_alerts(severity=None, alert_type=None):
    sql = """
        SELECT
            a.alert_id,
            a.alert_type,
            a.severity,
            a.detected_at,
            a.incident_id,
            ip.ip_address,
            ip.ip_type,
            ip.location,
            i.incident_type,
            i.status AS incident_status,
            u.name AS affected_user,
            d.device_name
        FROM Alerts a
        LEFT JOIN IP_Addresses ip ON a.ip_id = ip.ip_id
        LEFT JOIN Incidents i ON a.incident_id = i.incident_id
        LEFT JOIN Devices d ON i.device_id = d.device_id
        LEFT JOIN Users u ON d.user_id = u.user_id
        WHERE 1=1
    """
    params = []
    if severity and severity != "All":
        sql += " AND a.severity = %s"
        params.append(severity)
    if alert_type and alert_type != "All":
        sql += " AND a.alert_type = %s"
        params.append(alert_type)
    sql += " ORDER BY a.detected_at DESC"
    return execute_query(sql, params)


def get_alert_logs(alert_id=None):
    sql = """
        SELECT al.alert_log_id, al.alert_id, al.action, al.details, al.logged_at,
               a.alert_type, a.severity
        FROM Alert_Logs al
        JOIN Alerts a ON al.alert_id = a.alert_id
    """
    params = []
    if alert_id:
        sql += " WHERE al.alert_id = %s"
        params.append(alert_id)
    sql += " ORDER BY al.logged_at DESC"
    return execute_query(sql, params)


# ─────────────────────────── Evidence ───────────────────────────

def get_all_evidence(incident_id=None):
    sql = """
        SELECT
            e.evidence_id,
            e.incident_id,
            e.evidence_type,
            e.description,
            e.collected_at,
            e.file_reference,
            i.incident_type,
            i.severity,
            u.name AS affected_user
        FROM Evidence e
        JOIN Incidents i ON e.incident_id = i.incident_id
        JOIN Devices d ON i.device_id = d.device_id
        JOIN Users u ON d.user_id = u.user_id
    """
    params = []
    if incident_id:
        sql += " WHERE e.incident_id = %s"
        params.append(incident_id)
    sql += " ORDER BY e.collected_at DESC"
    return execute_query(sql, params)


def add_evidence(incident_id, evidence_type, description, file_reference=None):
    sql = """
        INSERT INTO Evidence (incident_id, evidence_type, description, collected_at, file_reference)
        VALUES (%s, %s, %s, NOW(), %s)
    """
    return execute_write(sql, (incident_id, evidence_type, description, file_reference or None))


# ─────────────────────────── Investigation Logs ───────────────────────────

def get_investigation_logs(incident_id=None, investigator_id=None):
    sql = """
        SELECT
            il.log_id,
            il.incident_id,
            il.action_performed,
            il.action_timestamp,
            inv.name AS investigator_name,
            inv.role AS investigator_role,
            i.incident_type,
            i.severity,
            i.status
        FROM Investigation_Logs il
        JOIN Investigators inv ON il.investigator_id = inv.investigator_id
        JOIN Incidents i ON il.incident_id = i.incident_id
        WHERE 1=1
    """
    params = []
    if incident_id:
        sql += " AND il.incident_id = %s"
        params.append(incident_id)
    if investigator_id:
        sql += " AND il.investigator_id = %s"
        params.append(investigator_id)
    sql += " ORDER BY il.action_timestamp DESC"
    return execute_query(sql, params)


def add_investigation_log(incident_id, investigator_id, action_performed):
    sql = """
        INSERT INTO Investigation_Logs (incident_id, investigator_id, action_performed, action_timestamp)
        VALUES (%s, %s, %s, NOW())
    """
    return execute_write(sql, (incident_id, investigator_id, action_performed))


# ─────────────────────────── Incident Operations ───────────────────────────

def add_incident(device_id, investigator_id, incident_type, description, severity, status):
    return call_procedure("AddIncident", (device_id, investigator_id, incident_type, description, severity, status))


# ─────────────────────────── Find-or-Create helpers ───────────────────────────

def get_or_create_user(name, email, department):
    """
    Look up a User by email (unique key). If found return existing user_id.
    If not found, insert a new User row and return the new user_id.
    Returns (user_id, created: bool, error_msg or None).
    """
    conn = create_connection()
    if not conn:
        return None, False, "Could not connect to database."
    try:
        cursor = conn.cursor(dictionary=True)

        # Check by email (unique constraint)
        cursor.execute("SELECT user_id FROM Users WHERE email = %s", (email,))
        row = cursor.fetchone()
        if row:
            return row["user_id"], False, None

        # Insert new user
        cursor.execute(
            "INSERT INTO Users (name, email, department) VALUES (%s, %s, %s)",
            (name, email, department),
        )
        conn.commit()
        return cursor.lastrowid, True, None

    except Exception as e:
        conn.rollback()
        return None, False, str(e)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


def get_or_create_device(device_name, device_type, operating_system, user_id):
    """
    Look up a Device by (device_name, user_id). If found return existing device_id.
    If not found, insert and return the new device_id.
    Returns (device_id, created: bool, error_msg or None).
    """
    conn = create_connection()
    if not conn:
        return None, False, "Could not connect to database."
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT device_id FROM Devices WHERE device_name = %s AND user_id = %s",
            (device_name, user_id),
        )
        row = cursor.fetchone()
        if row:
            return row["device_id"], False, None

        cursor.execute(
            "INSERT INTO Devices (user_id, device_name, device_type, operating_system) VALUES (%s, %s, %s, %s)",
            (user_id, device_name, device_type, operating_system),
        )
        conn.commit()
        return cursor.lastrowid, True, None

    except Exception as e:
        conn.rollback()
        return None, False, str(e)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


def get_or_create_ip(ip_address, ip_type, location):
    """
    Look up an IP_Address by ip_address (unique key). Reuse or insert.
    Returns (ip_id, created: bool, error_msg or None).
    """
    conn = create_connection()
    if not conn:
        return None, False, "Could not connect to database."
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT ip_id FROM IP_Addresses WHERE ip_address = %s", (ip_address,))
        row = cursor.fetchone()
        if row:
            return row["ip_id"], False, None

        cursor.execute(
            "INSERT INTO IP_Addresses (ip_address, ip_type, location) VALUES (%s, %s, %s)",
            (ip_address, ip_type, location or None),
        )
        conn.commit()
        return cursor.lastrowid, True, None

    except Exception as e:
        conn.rollback()
        return None, False, str(e)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


def create_incident_full(
    # User
    user_name, user_email, user_department,
    # Device
    device_name, device_type, operating_system,
    # Incident core (reporter-supplied)
    description,
    # Defaults for reporter-submitted incidents
    incident_type="Pending Classification",
    severity="Unassigned",
    status="Pending Assessment",
    # Investigator (None until assigned by investigator)
    investigator_id=None,
    # IP Address (all optional)
    ip_address=None, ip_type=None, ip_location=None,
):
    """
    Transactional workflow for recording a new incident via reporter text entry.

    Steps (single connection — rolled back entirely on any failure):
      1. Find-or-create User       → user_id
      2. Find-or-create Device     → device_id  (linked to user_id)
      3. INSERT Incident with defaults:
            incident_type = 'Pending Classification'
            severity      = 'Unassigned'
            status        = 'Pending Assessment'
      4. If IP provided: find-or-create IP_Address → ip_id
         then INSERT Alert (severity recorded as 'Low' placeholder; updated when assessed)

    Returns (success: bool, message: str, detail_dict: dict).
    """
    conn = create_connection()
    if not conn:
        return False, "Could not connect to database.", {}

    detail = {}
    try:
        cursor = conn.cursor(dictionary=True)

        # ── Step 1: User ──────────────────────────────────────────────
        cursor.execute("SELECT user_id FROM Users WHERE email = %s", (user_email,))
        row = cursor.fetchone()
        if row:
            user_id = row["user_id"]
            detail["user"] = f"Existing user reused (ID {user_id})"
        else:
            cursor.execute(
                "INSERT INTO Users (name, email, department) VALUES (%s, %s, %s)",
                (user_name, user_email, user_department),
            )
            user_id = cursor.lastrowid
            detail["user"] = f"New user created (ID {user_id})"

        # ── Step 2: Device ────────────────────────────────────────────
        cursor.execute(
            "SELECT device_id FROM Devices WHERE device_name = %s AND user_id = %s",
            (device_name, user_id),
        )
        row = cursor.fetchone()
        if row:
            device_id = row["device_id"]
            detail["device"] = f"Existing device reused (ID {device_id})"
        else:
            cursor.execute(
                "INSERT INTO Devices (user_id, device_name, device_type, operating_system) VALUES (%s, %s, %s, %s)",
                (user_id, device_name, device_type, operating_system),
            )
            device_id = cursor.lastrowid
            detail["device"] = f"New device created (ID {device_id})"

        # ── Step 3: Incident ──────────────────────────────────────────
        cursor.execute(
            """
            INSERT INTO Incidents
                (device_id, investigator_id, incident_type, description, severity, status, reported_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """,
            (device_id, investigator_id, incident_type, description, severity, status),
        )
        incident_id = cursor.lastrowid
        detail["incident"] = f"Incident created (ID {incident_id}), status: {status}, severity: {severity}"

        # ── Step 4: IP Address + Alert (optional) ─────────────────────
        if ip_address and ip_address.strip():
            cursor.execute(
                "SELECT ip_id FROM IP_Addresses WHERE ip_address = %s",
                (ip_address.strip(),),
            )
            row = cursor.fetchone()
            if row:
                ip_id = row["ip_id"]
                detail["ip"] = f"Existing IP reused (ID {ip_id})"
            else:
                cursor.execute(
                    "INSERT INTO IP_Addresses (ip_address, ip_type, location) VALUES (%s, %s, %s)",
                    (ip_address.strip(), ip_type or "External", ip_location or None),
                )
                ip_id = cursor.lastrowid
                detail["ip"] = f"New IP created (ID {ip_id})"

            # Alert severity defaults to Low until investigator assesses the incident
            cursor.execute(
                "INSERT INTO Alerts (incident_id, ip_id, alert_type, severity, detected_at) "
                "VALUES (%s, %s, %s, %s, NOW())",
                (incident_id, ip_id, "Suspicious IP Reported", "Low"),
            )
            alert_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO Alert_Logs (alert_id, action, details, logged_at) VALUES (%s, %s, %s, NOW())",
                (alert_id, "Alert Created", "Reporter flagged a suspicious IP address"),
            )
            detail["alert"] = f"Suspicious IP alert created (ID {alert_id})"

        conn.commit()
        return True, f"Incident #{incident_id} submitted for assessment.", detail

    except Exception as e:
        conn.rollback()
        return False, str(e), {}
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


def assess_incident(
    incident_id,
    incident_type,
    severity,
    new_status,
    investigator_id,
    assessment_notes=None,
):
    """
    Investigator assessment: classify incident_type, severity, status, assign investigator.
    Optionally logs assessment notes to Investigation_Logs.
    All writes in a single transaction.
    Returns (success: bool, message: str).
    """
    conn = create_connection()
    if not conn:
        return False, "Could not connect to database."
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE Incidents
               SET incident_type    = %s,
                   severity         = %s,
                   status           = %s,
                   investigator_id  = %s
             WHERE incident_id = %s
            """,
            (incident_type, severity, new_status, investigator_id, incident_id),
        )

        if cursor.rowcount == 0:
            conn.rollback()
            return False, f"Incident #{incident_id} not found."

        # Log the assessment action in Investigation_Logs
        if investigator_id:
            notes = assessment_notes.strip() if assessment_notes and assessment_notes.strip() else \
                f"Incident assessed: type={incident_type}, severity={severity}, status={new_status}"
            cursor.execute(
                """
                INSERT INTO Investigation_Logs
                    (incident_id, investigator_id, action_performed, action_timestamp)
                VALUES (%s, %s, %s, NOW())
                """,
                (incident_id, investigator_id, notes),
            )

        conn.commit()
        return True, f"Incident #{incident_id} assessed successfully."

    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()


def update_incident_status(incident_id, new_status):
    return call_procedure("UpdateIncidentStatus", (incident_id, new_status))


def assign_investigator(incident_id, investigator_id):
    return call_procedure("AssignInvestigator", (incident_id, investigator_id))


# ─────────────────────────── Lookup helpers ───────────────────────────

def get_all_investigators():
    return execute_query("SELECT investigator_id, name, role FROM Investigators ORDER BY name")


def get_all_devices():
    sql = """
        SELECT d.device_id, d.device_name, d.device_type, d.operating_system, u.name AS user_name
        FROM Devices d JOIN Users u ON d.user_id = u.user_id ORDER BY d.device_name
    """
    return execute_query(sql)


def get_all_users():
    return execute_query("SELECT user_id, name, email, department FROM Users ORDER BY name")


def get_all_ip_addresses():
    return execute_query("SELECT ip_id, ip_address, ip_type, location FROM IP_Addresses ORDER BY ip_address")


# ─────────────────────────── Analytical Insights ───────────────────────────

def get_critical_high_incidents():
    return execute_query("""
        SELECT incident_id, incident_type, severity, status, reported_at
        FROM Critical_Incident_Report
        ORDER BY FIELD(severity,'Critical','High'), reported_at DESC
    """)


def get_suspicious_ips():
    return execute_query("""
        SELECT ip.ip_address, ip.ip_type, ip.location,
               COUNT(a.alert_id) AS alert_count
        FROM IP_Addresses ip
        JOIN Alerts a ON ip.ip_id = a.ip_id
        GROUP BY ip.ip_id, ip.ip_address, ip.ip_type, ip.location
        ORDER BY alert_count DESC
    """)


def get_attack_type_analysis():
    return execute_query("""
        SELECT incident_type,
               COUNT(*) AS total,
               SUM(CASE WHEN severity='Critical' THEN 1 ELSE 0 END) AS critical_count,
               SUM(CASE WHEN severity='High' THEN 1 ELSE 0 END) AS high_count,
               SUM(CASE WHEN status='Resolved' THEN 1 ELSE 0 END) AS resolved_count
        FROM Incidents
        GROUP BY incident_type
        ORDER BY total DESC
    """)


def get_resolution_patterns():
    return execute_query("""
        SELECT
            i.incident_id,
            i.incident_type,
            i.severity,
            i.reported_at,
            MIN(h.changed_at) AS resolved_at,
            CalculateResolutionDuration(i.incident_id) AS resolution_hours
        FROM Incidents i
        JOIN Incident_Status_History h ON i.incident_id = h.incident_id
        WHERE h.new_status = 'Resolved'
        GROUP BY i.incident_id, i.incident_type, i.severity, i.reported_at
        ORDER BY i.reported_at DESC
    """)


def get_investigator_workload():
    return execute_query("""
        SELECT investigator_id, investigator_name, role, total_incidents
        FROM Investigator_Workload_Report
        ORDER BY total_incidents DESC
    """)


def get_alert_trends():
    return execute_query("""
        SELECT DATE(detected_at) AS date, COUNT(*) AS count, severity
        FROM Alerts
        GROUP BY DATE(detected_at), severity
        ORDER BY date
    """)


def get_investigation_progress():
    return execute_query("""
        SELECT
            i.status,
            COUNT(DISTINCT i.incident_id) AS incident_count,
            COUNT(DISTINCT il.log_id) AS total_actions
        FROM Incidents i
        LEFT JOIN Investigation_Logs il ON i.incident_id = il.incident_id
        GROUP BY i.status
        ORDER BY incident_count DESC
    """)


# ─────────────────────────── Reports ───────────────────────────

def get_incident_summary_report():
    return execute_query("""
        SELECT
            ir.incident_id,
            ir.affected_user,
            ir.device_name,
            ir.device_type,
            ir.incident_type,
            ir.severity,
            ir.status,
            ir.investigator,
            ir.reported_at,
            CalculateIncidentAge(ir.incident_id) AS age_days
        FROM Incident_Report ir
        ORDER BY ir.reported_at DESC
    """)


def get_resolution_summary():
    return execute_query("""
        SELECT
            i.incident_id,
            i.incident_type,
            i.severity,
            i.reported_at,
            i.status,
            CalculateResolutionDuration(i.incident_id) AS resolution_hours,
            inv.name AS investigator
        FROM Incidents i
        LEFT JOIN Investigators inv ON i.investigator_id = inv.investigator_id
        ORDER BY i.reported_at DESC
    """)
