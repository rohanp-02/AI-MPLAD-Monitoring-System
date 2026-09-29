import sqlite3
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


def detect_anomalies():

    conn = sqlite3.connect("mplad.db")

    df = pd.read_sql_query("""
        SELECT
            id,
            sanctioned_amount,
            expenditure,
            expected_duration,
            actual_duration,
            physical_progress,
            financial_progress,
            modifications,
            inspections
        FROM projects
    """, conn)

    conn.close()

    # Not enough projects
    if len(df) < 5:
        return {}

    features = [
        "sanctioned_amount",
        "expenditure",
        "expected_duration",
        "actual_duration",
        "physical_progress",
        "financial_progress",
        "modifications",
        "inspections"
    ]

    feature_names = {
        "sanctioned_amount": "Sanctioned amount",
        "expenditure": "Expenditure",
        "expected_duration": "Expected duration",
        "actual_duration": "Actual duration",
        "physical_progress": "Physical progress",
        "financial_progress": "Financial progress",
        "modifications": "Project modifications",
        "inspections": "Inspection records"
    }

    # Handle missing values
    df[features] = df[features].fillna(0)

    # Standardize numerical features
    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])

    # Memory-efficient Isolation Forest
    model = IsolationForest(
        n_estimators=50,
        contamination=0.25,
        random_state=42,
        n_jobs=1
    )

    predictions = model.fit_predict(X)

    # Isolation Forest decision score
    # Higher value = more normal
    decision_scores = model.decision_function(X)

    # Convert into relative anomaly score
    # Higher value = more unusual
    raw_scores = -decision_scores

    min_score = raw_scores.min()
    max_score = raw_scores.max()

    if max_score == min_score:

        anomaly_scores = np.zeros(len(raw_scores))

    else:

        anomaly_scores = (
            (raw_scores - min_score) /
            (max_score - min_score)
        ) * 100

    results = {}

    # Calculate dataset-level unusual features
    means = X.mean(axis=0)
    stds = X.std(axis=0)

    stds = np.where(stds == 0, 1, stds)

    z_scores = (X - means) / stds

    for index, prediction in enumerate(predictions):

        project_id = int(df.iloc[index]["id"])

        # Find unusual features
        feature_scores = []

        for feature_index, feature in enumerate(features):

            z_value = z_scores[index][feature_index]

            if abs(z_value) >= 1.0:

                feature_scores.append(
                    (
                        abs(z_value),
                        feature_names[feature],
                        z_value
                    )
                )

        # Highest unusual features first
        feature_scores.sort(
            key=lambda x: x[0],
            reverse=True
        )

        explanations = []

        for _, name, z_value in feature_scores[:3]:

            if z_value > 0:

                explanations.append(
                    f"{name} is unusually high"
                )

            else:

                explanations.append(
                    f"{name} is unusually low"
                )

        if prediction == -1:

            label = "ANOMALY"

        else:

            label = "NORMAL"

        results[project_id] = {
            "label": label,
            "anomaly_score": round(
                float(anomaly_scores[index]),
                1
            ),
            "decision_score": round(
                float(decision_scores[index]),
                4
            ),
            "explanations": explanations
        }

    return results


if __name__ == "__main__":

    results = detect_anomalies()

    if not results:

        print(
            "Not enough projects for anomaly detection."
        )

    else:

        print("\nAI Anomaly Detection Results")
        print("=" * 45)

        for project_id, result in results.items():

            print(
                f"Project {project_id}: "
                f"{result['label']} | "
                f"Anomaly Score: "
                f"{result['anomaly_score']}/100"
            )

            for explanation in result["explanations"]:

                print(
                    f"  - {explanation}"
                )