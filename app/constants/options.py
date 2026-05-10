AREA_OPTIONS = [
    "Kuala Lumpur",
    "Petaling Jaya",
    "Subang Jaya",
    "Shah Alam",
    "Puchong",
    "Klang",
    "Cheras",
    "Ampang",
    "Kajang",
    "Selayang",
    "Setapak",
    "Bangi",
    "Cyberjaya",
    "Rawang",
    "Seri Kembangan",
]

UNIVERSITY_OPTIONS = [
    "University of Malaya",
    "Universiti Kebangsaan Malaysia (UKM)",
    "Universiti Putra Malaysia (UPM)",
    "International Islamic University Malaysia (IIUM)",
    "Monash University Malaysia",
    "Taylor's University",
    "Sunway University",
    "UCSI University",
    "INTI International University",
    "Universiti Teknologi MARA (UiTM)",
]


def with_other(options):
    return [(value, value) for value in options] + [("Other", "Other (not listed)")]
