import sqlite3

conn = sqlite3.connect("mplad.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_code TEXT UNIQUE,
    project_name TEXT,
    location TEXT,
    district TEXT,
    category TEXT,
    implementing_agency TEXT,

    sanctioned_amount REAL,
    released_amount REAL,
    expenditure REAL,

    expected_duration INTEGER,
    actual_duration INTEGER,

    physical_progress REAL,
    financial_progress REAL,

    modifications INTEGER,
    inspections INTEGER,

    status TEXT
)
""")

projects = [
    (
        "MPLAD1024",
        "Community Road Development",
        "Bangalore",
        "Bangalore Urban",
        "Roads",
        "BBMP",
        4000000,
        3900000,
        3800000,
        6,
        11,
        62,
        95,
        4,
        1,
        "Delayed"
    ),
    (
        "MPLAD1025",
        "School Infrastructure Improvement",
        "Mysore",
        "Mysore",
        "Education",
        "Education Department",
        2500000,
        2300000,
        1800000,
        8,
        8,
        100,
        78,
        1,
        3,
        "Completed"
    ),
    (
        "MPLAD1026",
        "Community Hall Construction",
        "Mandya",
        "Mandya",
        "Community Development",
        "Rural Development Department",
        3000000,
        3000000,
        2900000,
        7,
        7,
        100,
        97,
        0,
        4,
        "Completed"
    ),
    (
        "MPLAD1027",
        "Rural Road Improvement",
        "Tumkur",
        "Tumkur",
        "Roads",
        "PWD",
        5000000,
        4900000,
        4850000,
        6,
        10,
        58,
        97,
        3,
        1,
        "Delayed"
    ),
    (
        "MPLAD1028",
        "Drinking Water Facility",
        "Hassan",
        "Hassan",
        "Water Supply",
        "Jal Board",
        2000000,
        1800000,
        1200000,
        5,
        5,
        100,
        67,
        0,
        3,
        "Completed"
    ),
    (
        "MPLAD1029",
        "Primary Health Centre Upgrade",
        "Chikkaballapur",
        "Chikkaballapur",
        "Healthcare",
        "Health Department",
        4500000,
        4000000,
        2100000,
        9,
        7,
        55,
        52,
        1,
        2,
        "Ongoing"
    ),
    (
        "MPLAD1030",
        "Street Lighting Project",
        "Kolar",
        "Kolar",
        "Infrastructure",
        "Municipality",
        1800000,
        1700000,
        1650000,
        4,
        6,
        70,
        97,
        2,
        1,
        "Delayed"
    ),
    (
        "MPLAD1031",
        "Government School Toilet Block",
        "Ramanagara",
        "Ramanagara",
        "Education",
        "Education Department",
        1200000,
        1000000,
        650000,
        5,
        4,
        60,
        65,
        0,
        2,
        "Ongoing"
    )
]

cursor.executemany("""
INSERT OR IGNORE INTO projects (
    project_code,
    project_name,
    location,
    district,
    category,
    implementing_agency,
    sanctioned_amount,
    released_amount,
    expenditure,
    expected_duration,
    actual_duration,
    physical_progress,
    financial_progress,
    modifications,
    inspections,
    status
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", projects)

conn.commit()
conn.close()

print("Realistic MPLAD database created successfully!")