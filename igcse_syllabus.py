# -*- coding: utf-8 -*-
"""
IGCSE Physics 0625 syllabus (2023-2025) topic taxonomy.

Each topic has a number (1-6) and a list of subsections (e.g. 1.1).
Categorization for the organizer happens at the subsection level.
"""

TOPIC_COLORS = {
    "1": "#8fa3ad",  # Motion, forces and energy
    "2": "#c2a878",  # Thermal physics
    "3": "#7fa39a",  # Waves
    "4": "#8497a8",  # Electricity and magnetism
    "5": "#ba8c95",  # Nuclear physics
    "6": "#a3a578",  # Space physics
}

# topic -> (title, [(sub_code, sub_title), ...])
SYLLABUS = [
    ("1", "MOTION, FORCES AND ENERGY", [
        ("1.1", "Physical quantities and measurement techniques"),
        ("1.2", "Motion"),
        ("1.3", "Mass and weight"),
        ("1.4", "Density"),
        ("1.5", "Forces"),
        ("1.6", "Momentum"),
        ("1.7", "Energy, work and power"),
        ("1.8", "Pressure"),
    ]),
    ("2", "THERMAL PHYSICS", [
        ("2.1", "Kinetic particle model of matter"),
        ("2.2", "Thermal properties and temperature"),
        ("2.3", "Transfer of thermal energy"),
    ]),
    ("3", "WAVES", [
        ("3.1", "General properties of waves"),
        ("3.2", "Light"),
        ("3.3", "Electromagnetic spectrum"),
        ("3.4", "Sound"),
    ]),
    ("4", "ELECTRICITY AND MAGNETISM", [
        ("4.1", "Simple phenomena of magnetism"),
        ("4.2", "Electrical quantities"),
        ("4.3", "Electric circuits"),
        ("4.4", "Electrical safety"),
        ("4.5", "Electromagnetic effects"),
    ]),
    ("5", "NUCLEAR PHYSICS", [
        ("5.1", "The nuclear model of the atom"),
        ("5.2", "Radioactivity"),
    ]),
    ("6", "SPACE PHYSICS", [
        ("6.1", "The Earth and the Solar System"),
        ("6.2", "Stars and the Universe"),
    ]),
]

# Short topic-name label for a subsection code (used in slice filenames / JSON).
SUB_LABELS = {}
TOPIC_TITLES = {}
for _t, _title, _subs in SYLLABUS:
    TOPIC_TITLES[_t] = _title
    for _code, _subtitle in _subs:
        SUB_LABELS[_code] = _subtitle


def topic_of(code):
    """Return the topic number ('1'..'6') for a subsection code like '3.2'."""
    return code.split(".")[0]


def js_syllabus():
    """Emit the IGCSE syllabus as a JS array in the same shape the 9702 app
    consumes (topic -> subs -> subsubs). Each subsection gets a single subsub
    whose code equals the subsection code, so question data can be keyed by it."""
    import json
    out = []
    for t, title, subs in SYLLABUS:
        subs_js = []
        for code, sub_title in subs:
            subs_js.append({
                "code": code,
                "title": sub_title,
                "subsubs": [{"code": code, "desc": sub_title}],
            })
        out.append({"topic": t, "title": title, "subs": subs_js})
    return json.dumps(out, indent=2, ensure_ascii=False)
