import sqlite3

from ml_model import detect_anomalies


def get_peer_benchmark(project):

    conn = sqlite3.connect("mplad.db")
    conn.row_factory = sqlite3.Row

    peers = conn.execute("""
        SELECT
            expenditure,
            physical_progress,
            actual_duration
        FROM projects
        WHERE category = ?
          AND id != ?
    """, (
        project["category"],
        project["id"]
    )).fetchall()

    conn.close()

    if not peers:
        return None

    avg_expenditure = sum(
        p["expenditure"] for p in peers
    ) / len(peers)

    avg_physical = sum(
        p["physical_progress"] for p in peers
    ) / len(peers)

    avg_duration = sum(
        p["actual_duration"] for p in peers
    ) / len(peers)

    return {
        "peer_count": len(peers),
        "avg_expenditure": avg_expenditure,
        "avg_physical": avg_physical,
        "avg_duration": avg_duration
    }


def generate_evidence_explanation(
    project,
    risk_type,
    value=None,
    comparison=None
):

    if risk_type == "delay":

        delay = (
            project["actual_duration"]
            -
            project["expected_duration"]
        )

        return (
            f"The project is {delay} month"
            f"{'s' if delay != 1 else ''} "
            f"behind its expected completion period. "
            f"This can increase project duration and "
            f"requires verification of the current "
            f"physical work status and causes of delay."
        )

    if risk_type == "expenditure":

        ratio = (
            project["expenditure"]
            /
            project["sanctioned_amount"]
        ) * 100

        return (
            f"{ratio:.0f}% of the sanctioned amount has "
            f"already been reported as expenditure. "
            f"Verify bills, supporting financial records "
            f"and whether reported expenditure is "
            f"consistent with the physical work completed."
        )

    if risk_type == "progress_gap":

        gap = (
            project["financial_progress"]
            -
            project["physical_progress"]
        )

        return (
            f"Financial progress is {gap:.0f} percentage "
            f"points ahead of physical progress. "
            f"This difference should be checked against "
            f"measurement records, work completion evidence "
            f"and expenditure documentation."
        )

    if risk_type == "modifications":

        count = project["modifications"]

        return (
            f"The project has {count} recorded modifications. "
            f"Review the modification history, supporting "
            f"justifications and approval records."
        )

    if risk_type == "inspection":

        return (
            "Inspection records are limited. "
            "A field verification or updated inspection "
            "record can help confirm the reported project "
            "status."
        )

    if risk_type == "peer_expenditure":

        return (
            f"Project expenditure is approximately "
            f"{value:.0f}% higher than the average expenditure "
            f"of comparable projects in the same category. "
            f"Review project scope, expenditure records and "
            f"supporting documentation."
        )

    if risk_type == "peer_physical":

        return (
            f"Physical progress is approximately "
            f"{value:.0f} percentage points below comparable "
            f"projects in the same category. "
            f"Verify actual site progress and reported "
            f"completion data."
        )

    if risk_type == "ml_anomaly":

        return (
            "The machine-learning model identified a project "
            "pattern that differs from the other projects "
            "in the dataset. This is an anomaly indicator, "
            "not a finding of wrongdoing. Human verification "
            "is required to determine the reason for the "
            "unusual pattern."
        )

    return (
        "Review the project records and supporting evidence."
    )


def get_recommended_actions(
    project,
    reasons,
    ml_result=None
):

    actions = []

    if project["actual_duration"] > project["expected_duration"]:

        actions.append(
            "Schedule progress verification for the delayed project."
        )

    if project["sanctioned_amount"] > 0:

        expenditure_ratio = (
            project["expenditure"]
            /
            project["sanctioned_amount"]
        ) * 100

        if expenditure_ratio >= 90:

            actions.append(
                "Review expenditure records, bills and supporting documents."
            )

    progress_gap = (
        project["financial_progress"]
        -
        project["physical_progress"]
    )

    if progress_gap >= 25:

        actions.append(
            "Verify physical work completion against reported expenditure."
        )

    if project["modifications"] >= 3:

        actions.append(
            "Review project modification history and approval records."
        )

    elif project["modifications"] == 2:

        actions.append(
            "Review the project's modification records."
        )

    if project["inspections"] <= 1:

        actions.append(
            "Schedule or update field inspection records."
        )

    if ml_result:

        if ml_result.get("label") == "ANOMALY":

            actions.append(
                "Perform human verification of the unusual project pattern."
            )

    if not actions:

        actions.append(
            "Continue routine project monitoring."
        )

    return actions


# ==========================================
# AI EARLY WARNING
# ==========================================

def calculate_early_warning(project, ml_result=None):

    warning_score = 0
    indicators = []

    # --------------------------------------
    # DELAY WARNING
    # --------------------------------------

    if project["actual_duration"] > project["expected_duration"]:

        delay = (
            project["actual_duration"]
            -
            project["expected_duration"]
        )

        if delay >= 3:

            warning_score += 30

            indicators.append(
                f"Project is {delay} months beyond expected duration."
            )

        else:

            warning_score += 15

            indicators.append(
                f"Project is {delay} month beyond expected duration."
            )

    # --------------------------------------
    # FINANCIAL VS PHYSICAL PROGRESS
    # --------------------------------------

    progress_gap = (
        project["financial_progress"]
        -
        project["physical_progress"]
    )

    if progress_gap >= 25:

        warning_score += 30

        indicators.append(
            "Financial progress is significantly ahead of physical progress."
        )

    elif progress_gap >= 15:

        warning_score += 15

        indicators.append(
            "Financial progress is moderately ahead of physical progress."
        )

    # --------------------------------------
    # HIGH EXPENDITURE
    # --------------------------------------

    if project["sanctioned_amount"] > 0:

        expenditure_ratio = (
            project["expenditure"]
            /
            project["sanctioned_amount"]
        ) * 100

        if expenditure_ratio >= 90:

            warning_score += 20

            indicators.append(
                "Expenditure has reached 90% or more of the sanctioned amount."
            )

        elif expenditure_ratio >= 75:

            warning_score += 10

            indicators.append(
                "Expenditure has reached more than 75% of the sanctioned amount."
            )

    # --------------------------------------
    # MODIFICATIONS
    # --------------------------------------

    if project["modifications"] >= 3:

        warning_score += 15

        indicators.append(
            "Multiple project modifications detected."
        )

    elif project["modifications"] == 2:

        warning_score += 8

        indicators.append(
            "Repeated project modifications detected."
        )

    # --------------------------------------
    # INSPECTIONS
    # --------------------------------------

    if project["inspections"] == 0:

        warning_score += 15

        indicators.append(
            "No inspection records are available."
        )

    elif project["inspections"] == 1:

        warning_score += 8

        indicators.append(
            "Inspection records are limited."
        )

    # --------------------------------------
    # ML ANOMALY
    # --------------------------------------

    if ml_result:

        if ml_result.get("label") == "ANOMALY":

            warning_score += 20

            indicators.append(
                "ML detected an unusual project pattern."
            )

    warning_score = min(
        warning_score,
        100
    )

    # --------------------------------------
    # WARNING LEVEL
    # --------------------------------------

    if warning_score >= 60:

        level = "HIGH"

    elif warning_score >= 30:

        level = "MEDIUM"

    else:

        level = "LOW"

    # --------------------------------------
    # EARLY WARNING ACTION
    # --------------------------------------

    if level == "HIGH":

        action = (
            "Prioritize project verification and review "
            "supporting evidence."
        )

    elif level == "MEDIUM":

        action = (
            "Increase monitoring frequency and verify "
            "the identified indicators."
        )

    else:

        action = (
            "Continue routine monitoring."
        )

    return {
        "score": warning_score,
        "level": level,
        "indicators": indicators,
        "action": action
    }


def calculate_risk(
    project,
    ml_result=None
):

    score = 0

    reasons = []

    if (
        project["actual_duration"]
        >
        project["expected_duration"]
    ):

        delay = (
            project["actual_duration"]
            -
            project["expected_duration"]
        )

        if delay >= 3:
            points = 20
        else:
            points = 10

        score += points

        reasons.append({
            "text":
                f"Project delayed by {delay} month"
                f"{'s' if delay != 1 else ''}",
            "points":
                points,
            "explanation":
                generate_evidence_explanation(
                    project,
                    "delay"
                )
        })

    if project["sanctioned_amount"] > 0:

        expenditure_ratio = (
            project["expenditure"]
            /
            project["sanctioned_amount"]
        ) * 100

        if expenditure_ratio >= 90:

            score += 20

            reasons.append({
                "text":
                    f"High expenditure "
                    f"({expenditure_ratio:.0f}% "
                    f"of sanctioned amount)",
                "points":
                    20,
                "explanation":
                    generate_evidence_explanation(
                        project,
                        "expenditure"
                    )
            })

    progress_gap = (
        project["financial_progress"]
        -
        project["physical_progress"]
    )

    if progress_gap >= 25:

        score += 25

        reasons.append({
            "text":
                f"Financial progress is "
                f"{progress_gap:.0f}% higher "
                f"than physical progress",
            "points":
                25,
            "explanation":
                generate_evidence_explanation(
                    project,
                    "progress_gap"
                )
        })

    if project["modifications"] >= 3:

        score += 15

        reasons.append({
            "text":
                f"Multiple project modifications "
                f"({project['modifications']})",
            "points":
                15,
            "explanation":
                generate_evidence_explanation(
                    project,
                    "modifications"
                )
        })

    elif project["modifications"] == 2:

        score += 8

        reasons.append({
            "text":
                "Project has multiple modifications",
            "points":
                8,
            "explanation":
                generate_evidence_explanation(
                    project,
                    "modifications"
                )
        })

    if project["inspections"] == 0:

        score += 10

        reasons.append({
            "text":
                "No inspection records available",
            "points":
                10,
            "explanation":
                generate_evidence_explanation(
                    project,
                    "inspection"
                )
        })

    elif project["inspections"] == 1:

        score += 5

        reasons.append({
            "text":
                "Limited inspection records",
            "points":
                5,
            "explanation":
                generate_evidence_explanation(
                    project,
                    "inspection"
                )
        })

    benchmark = get_peer_benchmark(
        project
    )

    if benchmark:

        if benchmark["avg_expenditure"] > 0:

            expenditure_deviation = (
                (
                    project["expenditure"]
                    -
                    benchmark["avg_expenditure"]
                )
                /
                benchmark["avg_expenditure"]
            ) * 100

            if expenditure_deviation >= 30:

                score += 10

                reasons.append({
                    "text":
                        f"Expenditure is "
                        f"{expenditure_deviation:.0f}% "
                        f"higher than similar projects",
                    "points":
                        10,
                    "explanation":
                        generate_evidence_explanation(
                            project,
                            "peer_expenditure",
                            expenditure_deviation
                        )
                })

        physical_difference = (
            benchmark["avg_physical"]
            -
            project["physical_progress"]
        )

        if physical_difference >= 25:

            score += 10

            reasons.append({
                "text":
                    f"Physical progress is "
                    f"{physical_difference:.0f}% below "
                    f"similar projects",
                "points":
                    10,
                "explanation":
                    generate_evidence_explanation(
                        project,
                        "peer_physical",
                        physical_difference
                    )
            })

    if ml_result is None:

        anomalies = detect_anomalies()

        ml_result = anomalies.get(
            project["id"]
        )

    if ml_result:

        if ml_result["label"] == "ANOMALY":

            score += 15

            reasons.append({
                "text":
                    "ML model detected an unusual "
                    "project pattern",
                "points":
                    15,
                "explanation":
                    generate_evidence_explanation(
                        project,
                        "ml_anomaly"
                    )
            })

    score = min(
        score,
        100
    )

    if score >= 60:

        level = "HIGH"

    elif score >= 30:

        level = "MEDIUM"

    else:

        level = "LOW"

    recommendations = get_recommended_actions(
        project,
        reasons,
        ml_result
    )

    return (
        score,
        level,
        reasons,
        recommendations
    )