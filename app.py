from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import sqlite3
from datetime import datetime

from risk_engine import (
    calculate_risk,
    get_peer_benchmark,
    calculate_early_warning
)
from ml_model import detect_anomalies


app = Flask(__name__)
app.secret_key = "mplad-ai-secret-key"

DATABASE = "mplad.db"


# ============================================================
# ROLE-BASED ACCESS CONTROL
# ============================================================

USERS = {
    "verification": {
        "password": "verify123",
        "role": "Verification Officer"
    },
    "project": {
        "password": "project123",
        "role": "Project Officer"
    },
    "supervisor": {
        "password": "super123",
        "role": "Supervisor"
    },
    "admin": {
        "password": "admin123",
        "role": "Admin"
    }
}


ROLE_PERMISSIONS = {
    "Verification Officer": {
        "dashboard",
        "projects",
        "project_detail",
        "review_queue",
        "verify",
        "districts"
    },

    "Project Officer": {
        "dashboard",
        "projects",
        "project_detail"
    },

    "Supervisor": {
        "dashboard",
        "projects",
        "project_detail",
        "review_queue",
        "verify",
        "districts",
        "audit"
    },

    "Admin": {
        "dashboard",
        "projects",
        "project_detail",
        "review_queue",
        "verify",
        "districts",
        "audit"
    }
}


def login_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "username" not in session:
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    return wrapped_view


def role_required(permission):

    def decorator(view):

        @wraps(view)
        def wrapped_view(*args, **kwargs):

            if "username" not in session:
                return redirect(url_for("login"))

            role = session.get("role")

            allowed = ROLE_PERMISSIONS.get(
                role,
                set()
            )

            if permission not in allowed:

                return (
                    "<h2>403 - Access Denied</h2>"
                    f"<p>Your role ({role}) does not have "
                    f"permission to access this page.</p>"
                    "<p>"
                    "<a href='/dashboard'>"
                    "Return to Dashboard"
                    "</a>"
                    "</p>"
                ), 403

            return view(*args, **kwargs)

        return wrapped_view

    return decorator


@app.context_processor
def inject_user():

    return {
        "current_username":
            session.get("username"),

        "current_role":
            session.get("role"),

        "logged_in":
            "username" in session
    }


# ============================================================
# DATABASE
# ============================================================

def get_db():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


def init_database():

    conn = get_db()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)

    for username, data in USERS.items():

        cursor.execute("""
            INSERT OR IGNORE INTO users
            (username, password, role)
            VALUES (?, ?, ?)
        """, (
            username,
            data["password"],
            data["role"]
        ))

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_code TEXT,
            action TEXT,
            user_role TEXT,
            remark TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()

    conn.close()


# ============================================================
# LOGIN
# ============================================================

@app.route("/")
def home():

    if "username" in session:
        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        user = USERS.get(username)

        if user and user["password"] == password:

            session.clear()

            session["username"] = username

            session["role"] = user["role"]

            flash(
                f"Welcome, {user['role']}.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "error"
        )

    return render_template(
        "login.html"
    )


@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ============================================================
# PROJECT HELPERS
# ============================================================

def get_project_name(project):

    for key in (
        "name",
        "project_name",
        "title",
        "project_title",
        "work_name"
    ):

        try:

            value = project[key]

            if value not in (
                None,
                ""
            ):

                return str(value)

        except Exception:

            pass

    try:

        return str(
            project["project_code"]
        )

    except Exception:

        return "Unknown Project"


def get_project_category(project):

    for key in (
        "category",
        "project_category",
        "sector",
        "type",
        "project_type"
    ):

        try:

            value = project[key]

            if value not in (
                None,
                ""
            ):

                return str(value)

        except Exception:

            pass

    return "Infrastructure"


def prepare_project(project):

    project = dict(project)

    project["name"] = get_project_name(
        project
    )

    project["category"] = \
        get_project_category(
            project
        )

    return project


def get_all_projects():

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM projects"
    ).fetchall()

    conn.close()

    return [
        prepare_project(row)
        for row in rows
    ]


def get_project(project_id):

    conn = get_db()

    row = conn.execute(
        """
        SELECT *
        FROM projects
        WHERE id = ?
        """,
        (project_id,)
    ).fetchone()

    conn.close()

    if row is None:
        return None

    return prepare_project(row)


def get_risk_data(project):

    try:

        return calculate_risk(
            project
        )

    except Exception:

        return (
            0,
            "LOW",
            [],
            []
        )


def normalize_reasons(reasons):

    normalized = []

    if not reasons:
        return normalized

    for reason in reasons:

        if isinstance(
            reason,
            dict
        ):

            normalized.append(
                reason
            )

        else:

            normalized.append({
                "text": str(reason),
                "points": 0,
                "explanation": ""
            })

    return normalized


# ============================================================
# ML
# ============================================================

def get_ml_results():

    try:

        result = detect_anomalies()

        if isinstance(
            result,
            dict
        ):

            return result

    except Exception:

        pass

    return {}


# ============================================================
# EARLY WARNING
# ============================================================

def get_early_warning(
    project,
    ml_result=None
):

    try:

        result = calculate_early_warning(
            project,
            ml_result
        )

        if isinstance(
            result,
            dict
        ):

            return {
                "score":
                    result.get(
                        "score",
                        0
                    ),

                "level":
                    result.get(
                        "level",
                        "LOW"
                    ),

                "indicators":
                    result.get(
                        "indicators",
                        []
                    ),

                "action":
                    result.get(
                        "action",
                        "Continue routine monitoring."
                    )
            }

    except Exception:

        pass

    return {
        "score": 0,
        "level": "LOW",
        "indicators": [],
        "action":
            "Continue routine monitoring."
    }


# ============================================================
# REVIEW STATUS
# ============================================================

def get_review_status(project_code):

    conn = get_db()

    row = conn.execute(
        """
        SELECT action
        FROM audit
        WHERE project_code = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (project_code,)
    ).fetchone()

    conn.close()

    if row is None:
        return "PENDING REVIEW"

    action = row["action"]

    if action == "Verified":
        return "VERIFIED"

    if action == "Flagged for Review":
        return "FLAGGED"

    if action == "Escalated":
        return "ESCALATED"

    if action == "Under Verification":
        return "UNDER VERIFICATION"

    return "PENDING REVIEW"


# ============================================================
# DISTRICT DATA
# ============================================================

DISTRICT_MAP = {

    "MPLAD1024":
        "Bengaluru Urban",

    "MPLAD1025":
        "Mysuru",

    "MPLAD1026":
        "Tumakuru",

    "MPLAD1027":
        "Bengaluru Rural",

    "MPLAD1028":
        "Mandya",

    "MPLAD1029":
        "Hassan",

    "MPLAD1030":
        "Chikkaballapur",

    "MPLAD1031":
        "Kolar"
}


DISTRICT_COORDINATES = {

    "Bengaluru Urban":
        (12.9716, 77.5946),

    "Mysuru":
        (12.2958, 76.6394),

    "Tumakuru":
        (13.3392, 77.1010),

    "Bengaluru Rural":
        (13.2847, 77.6070),

    "Mandya":
        (12.5218, 76.8951),

    "Hassan":
        (13.0068, 76.1004),

    "Chikkaballapur":
        (13.4355, 77.7315),

    "Kolar":
        (13.1357, 78.1320)
}


def get_district(project):

    try:

        district = project.get(
            "district"
        )

        if district:
            return district

    except Exception:

        pass

    try:

        return DISTRICT_MAP.get(
            project["project_code"],
            "Unknown District"
        )

    except Exception:

        return "Unknown District"


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@role_required("dashboard")
def dashboard():

    projects = get_all_projects()

    ml_results = get_ml_results()

    total_projects = len(projects)

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    delayed_projects = 0
    ml_anomalies = 0

    rule_based_attention = 0
    ml_only_cases = 0

    total_expenditure = 0
    total_physical_progress = 0

    review_queue_count = 0

    risk_projects = []
    early_warning_projects = []

    for project in projects:

        project_code = project.get(
            "project_code",
            ""
        )

        score, level, reasons, recommendations = \
            get_risk_data(project)

        reasons = normalize_reasons(
            reasons
        )

        try:
            score = float(score)
        except Exception:
            score = 0

        level = str(level).upper()

        if level == "HIGH":
            high_risk += 1

        elif level == "MEDIUM":
            medium_risk += 1

        else:
            low_risk += 1

        total_expenditure += float(
            project.get(
                "expenditure",
                0
            ) or 0
        )

        total_physical_progress += float(
            project.get(
                "physical_progress",
                0
            ) or 0
        )

        if (
            project.get(
                "actual_duration",
                0
            )
            >
            project.get(
                "expected_duration",
                0
            )
        ):
            delayed_projects += 1

        ml_result = ml_results.get(
            project.get("id"),
            {
                "label": "NORMAL",
                "anomaly_score": 0,
                "decision_score": 0,
                "explanations": []
            }
        )

        if ml_result.get(
            "label"
        ) == "ANOMALY":
            ml_anomalies += 1

        early_warning = get_early_warning(
            project,
            ml_result
        )

        if early_warning.get(
            "level"
        ) in (
            "HIGH",
            "MEDIUM"
        ):
            rule_based_attention += 1

        if (
            ml_result.get("label")
            == "ANOMALY"
            and level == "LOW"
        ):
            ml_only_cases += 1

        requires_review = (
            level in (
                "HIGH",
                "MEDIUM"
            )
            or
            ml_result.get(
                "label"
            ) == "ANOMALY"
            or
            early_warning.get(
                "level"
            ) in (
                "HIGH",
                "MEDIUM"
            )
        )

        if requires_review:
            review_queue_count += 1

        risk_projects.append({
            "project": project,
            "score": score,
            "risk_score": score,
            "level": level,
            "risk_level": level,
            "reasons": reasons,
            "recommendations": recommendations,
            "ml_result": ml_result,
            "early_warning": early_warning,
            "review_status":
                get_review_status(
                    project_code
                )
        })

        early_warning_projects.append({
            "project": project,
            "score": score,
            "level": level,
            "early_warning": early_warning
        })

    if total_projects > 0:

        avg_expenditure = (
            total_expenditure
            /
            total_projects
        )

        avg_physical_progress = (
            total_physical_progress
            /
            total_projects
        )

    else:

        avg_expenditure = 0
        avg_physical_progress = 0

    district_data = {}

    for project in projects:

        score, level, reasons, recommendations = \
            get_risk_data(project)

        ml_result = ml_results.get(
            project.get("id"),
            {
                "label": "NORMAL"
            }
        )

        district = get_district(
            project
        )

        if district not in district_data:

            latitude, longitude = \
                DISTRICT_COORDINATES.get(
                    district,
                    (15.3173, 75.7139)
                )

            district_data[district] = {
                "district": district,
                "projects": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "anomalies": 0,
                "risk_total": 0,
                "latitude": latitude,
                "longitude": longitude
            }

        data = district_data[district]

        data["projects"] += 1
        data["risk_total"] += float(score)

        if str(level).upper() == "HIGH":
            data["high"] += 1

        elif str(level).upper() == "MEDIUM":
            data["medium"] += 1

        else:
            data["low"] += 1

        if ml_result.get(
            "label"
        ) == "ANOMALY":
            data["anomalies"] += 1

    district_list = []

    for district, data in district_data.items():

        risk_score = round(
            data["risk_total"]
            /
            data["projects"],
            1
        )

        if risk_score >= 60:
            risk_level = "HIGH"

        elif risk_score >= 30:
            risk_level = "MEDIUM"

        else:
            risk_level = "LOW"

        district_list.append({
            **data,
            "risk_score": risk_score,
            "risk_level": risk_level
        })

    district_list.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return render_template(
        "dashboard.html",

        total_projects=total_projects,

        high_risk=high_risk,
        medium_risk=medium_risk,
        low_risk=low_risk,

        delayed_projects=delayed_projects,

        ml_anomalies=ml_anomalies,

        rule_based_attention=
            rule_based_attention,

        ml_only_cases=
            ml_only_cases,

        avg_expenditure=
            avg_expenditure,

        avg_physical_progress=
            avg_physical_progress,

        review_queue_count=
            review_queue_count,

        risk_projects=
            risk_projects,

        early_warning_projects=
            early_warning_projects,

        district_list=
            district_list,

        district_names=[
            x["district"]
            for x in district_list
        ],

        district_projects=[
            x["projects"]
            for x in district_list
        ],

        district_high=[
            x["high"]
            for x in district_list
        ],

        district_medium=[
            x["medium"]
            for x in district_list
        ],

        district_low=[
            x["low"]
            for x in district_list
        ],

        district_anomalies=[
            x["anomalies"]
            for x in district_list
        ],

        district_risk_scores=[
            x["risk_score"]
            for x in district_list
        ]
    )


# ============================================================
# PROJECTS
# ============================================================

@app.route("/projects")
@role_required("projects")
def projects():

    projects = get_all_projects()

    ml_results = get_ml_results()

    project_data = []

    for project in projects:

        score, level, reasons, recommendations = \
            get_risk_data(project)

        reasons = normalize_reasons(
            reasons
        )

        ml_result = ml_results.get(
            project.get("id"),
            {
                "label": "NORMAL",
                "anomaly_score": 0,
                "decision_score": 0,
                "explanations": []
            }
        )

        early_warning = get_early_warning(
            project,
            ml_result
        )

        project_data.append({
            "project": project,
            "score": score,
            "risk_score": score,
            "level": level,
            "risk_level": level,
            "reasons": reasons,
            "recommendations": recommendations,
            "ml_result": ml_result,
            "early_warning": early_warning,
            "review_status":
                get_review_status(
                    project.get(
                        "project_code",
                        ""
                    )
                )
        })

    return render_template(
        "projects.html",
        projects=project_data,
        project_data=project_data
    )


# ============================================================
# PROJECT DETAILS
# ============================================================

@app.route(
    "/project/<int:project_id>"
)
@role_required("project_detail")
def project_detail(project_id):

    project = get_project(
        project_id
    )

    if project is None:
        return "Project not found", 404

    score, level, reasons, recommendations = \
        get_risk_data(project)

    reasons = normalize_reasons(
        reasons
    )

    ml_results = get_ml_results()

    ml_result = ml_results.get(
        project.get("id"),
        {
            "label": "NORMAL",
            "anomaly_score": 0,
            "decision_score": 0,
            "explanations": []
        }
    )

    early_warning = get_early_warning(
        project,
        ml_result
    )

    try:

        peer_benchmark = get_peer_benchmark(
            project
        )

    except Exception:

        peer_benchmark = {}

    review_status = get_review_status(
        project.get(
            "project_code",
            ""
        )
    )

    return render_template(
        "project.html",

        project=project,

        score=score,
        risk_score=score,

        level=str(level).upper(),
        risk_level=str(level).upper(),

        reasons=reasons,

        recommendations=
            recommendations,

        ml_result=
            ml_result,

        peer_benchmark=
            peer_benchmark,

        early_warning=
            early_warning,

        review_status=
            review_status
    )


# ============================================================
# HUMAN VERIFICATION
# ============================================================

@app.route(
    "/verify/<int:project_id>",
    methods=["POST"]
)
@role_required("verify")
def verify_project(project_id):

    project = get_project(
        project_id
    )

    if project is None:
        return "Project not found", 404

    action = request.form.get(
        "action",
        "Flagged for Review"
    )

    remark = request.form.get(
        "remark",
        ""
    )

    role = session.get(
        "role"
    )

    allowed_actions = {

        "Verification Officer": {
            "Under Verification",
            "Verified",
            "Flagged for Review"
        },

        "Supervisor": {
            "Verified",
            "Flagged for Review",
            "Escalated"
        },

        "Admin": {
            "Under Verification",
            "Verified",
            "Flagged for Review",
            "Escalated"
        }
    }

    if action not in allowed_actions.get(
        role,
        set()
    ):

        return (
            "<h2>403 - Action Not Allowed</h2>"
            f"<p>{role} cannot perform "
            f"the action '{action}'.</p>"
            "<p>"
            "<a href='/dashboard'>"
            "Return to Dashboard"
            "</a>"
            "</p>"
        ), 403

    project_code = project.get(
        "project_code",
        ""
    )

    conn = get_db()

    conn.execute(
        """
        INSERT INTO audit
        (
            project_code,
            action,
            user_role,
            remark,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            project_code,
            action,
            role,
            remark,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    conn.commit()

    conn.close()

    flash(
        "Project verification action recorded successfully.",
        "success"
    )

    return redirect(
        url_for(
            "project_detail",
            project_id=project_id
        )
    )


# ============================================================
# REVIEW QUEUE
# ============================================================

@app.route("/review-queue")
@role_required("review_queue")
def review_queue():

    projects = get_all_projects()

    ml_results = get_ml_results()

    review_items = []

    for project in projects:

        score, level, reasons, recommendations = \
            get_risk_data(project)

        reasons = normalize_reasons(
            reasons
        )

        ml_result = ml_results.get(
            project.get("id"),
            {
                "label": "NORMAL",
                "anomaly_score": 0,
                "decision_score": 0,
                "explanations": []
            }
        )

        early_warning = get_early_warning(
            project,
            ml_result
        )

        requires_review = (
            str(level).upper()
            in ("HIGH", "MEDIUM")
            or
            ml_result.get(
                "label"
            ) == "ANOMALY"
            or
            early_warning.get(
                "level"
            )
            in ("HIGH", "MEDIUM")
        )

        if not requires_review:
            continue

        review_items.append({

            "project": project,

            "score": score,

            "risk_score": score,

            "level":
                str(level).upper(),

            "risk_level":
                str(level).upper(),

            "reasons":
                reasons,

            "recommendations":
                recommendations,

            "ml_result":
                ml_result,

            "early_warning":
                early_warning,

            "review_status":
                get_review_status(
                    project.get(
                        "project_code",
                        ""
                    )
                )
        })

    review_items.sort(
        key=lambda x: x.get(
            "score",
            0
        ),
        reverse=True
    )

    return render_template(
        "review_queue.html",

        review_items=
            review_items,

        reviews=
            review_items,

        review_queue=
            review_items
    )


# ============================================================
# AUDIT TRAIL
# ============================================================

@app.route("/audit")
@role_required("audit")
def audit():

    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM audit
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    audit_records = [
        dict(row)
        for row in rows
    ]

    return render_template(
        "audit.html",

        audit_records=
            audit_records,

        audits=
            audit_records
    )


# ============================================================
# DISTRICTS
# ============================================================

@app.route("/districts")
@role_required("districts")
def districts():

    projects = get_all_projects()

    ml_results = get_ml_results()

    district_data = {}

    for project in projects:

        score, level, reasons, recommendations = \
            get_risk_data(project)

        ml_result = ml_results.get(
            project.get("id"),
            {
                "label": "NORMAL"
            }
        )

        district = get_district(
            project
        )

        if district not in district_data:

            latitude, longitude = \
                DISTRICT_COORDINATES.get(
                    district,
                    (15.3173, 75.7139)
                )

            district_data[district] = {

                "district":
                    district,

                "projects":
                    0,

                "high":
                    0,

                "medium":
                    0,

                "low":
                    0,

                "anomalies":
                    0,

                "risk_total":
                    0,

                "latitude":
                    latitude,

                "longitude":
                    longitude
            }

        data = district_data[
            district
        ]

        data["projects"] += 1

        data["risk_total"] += float(
            score
        )

        level = str(
            level
        ).upper()

        if level == "HIGH":
            data["high"] += 1

        elif level == "MEDIUM":
            data["medium"] += 1

        else:
            data["low"] += 1

        if ml_result.get(
            "label"
        ) == "ANOMALY":

            data["anomalies"] += 1

    district_list = []

    for district, data in district_data.items():

        risk_score = round(
            data["risk_total"]
            /
            data["projects"],
            1
        )

        if risk_score >= 60:
            risk_level = "HIGH"

        elif risk_score >= 30:
            risk_level = "MEDIUM"

        else:
            risk_level = "LOW"

        district_list.append({

            "district":
                data["district"],

            "projects":
                data["projects"],

            "high":
                data["high"],

            "medium":
                data["medium"],

            "low":
                data["low"],

            "anomalies":
                data["anomalies"],

            "risk_total":
                data["risk_total"],

            "latitude":
                data["latitude"],

            "longitude":
                data["longitude"],

            "risk_score":
                risk_score,

            "risk_level":
                risk_level
        })

    district_list.sort(
        key=lambda x:
            x["risk_score"],
        reverse=True
    )

    return render_template(
        "districts.html",
        districts=district_list
    )


# ============================================================
# INR FILTER
# ============================================================

@app.template_filter("inr")
def inr_filter(value):

    try:

        value = float(value)

    except Exception:

        return "₹0"

    return "₹{:,.0f}".format(
        value
    )


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return (
        "<h2>404 - Page Not Found</h2>"
        "<p>"
        "<a href='/dashboard'>"
        "Return to Dashboard"
        "</a>"
        "</p>"
    ), 404


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    init_database()

    app.run(
        debug=True
    )