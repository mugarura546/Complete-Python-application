CW_WEIGHT = Decimal("0.40")
EXAM_WEIGHT = Decimal("0.60")

def validate_registration(reg, students):
    reg = str(reg).strip().upper()
    if not REG_PATTERN.match(reg):          # VU followed by digits, e.g. VU001
        raise ValueError(f"invalid registration number '{reg}' (expected e.g. VU001)")
    if reg in students:
        raise ValueError(f"duplicate registration number '{reg}'")
    return reg

def validate_mark(text, label):
    text = str(text).strip()
    if text == "":
        raise ValueError(f"{label} mark is missing")
    try:
        value = Decimal(text)
    except Exception:
        raise ValueError(f"{label} mark '{text}' is not a number")
    if not value.is_finite():
        raise ValueError(f"{label} mark '{text}' is not a valid number")
    if value < 0 or value > 100:
        raise ValueError(f"{label} mark {value} is outside the range 0-100")
    return value

def calculate_final(coursework, exam):
    return coursework * CW_WEIGHT + exam * EXAM_WEIGHT

def add_student(students, reg, name, coursework, exam):
    try:
        reg = validate_registration(reg, students)
        name = validate_name(name)
        cw = validate_mark(coursework, "coursework")
        ex = validate_mark(exam, "examination")
    except ValueError as err:
        return False, str(err)
    final = calculate_final(cw, ex)
    record = {"reg": reg, "name": name, "coursework": cw, "exam": ex,
              "final": final, "classification": classify(final)}
    students[reg] = record
    return True, record

def read_count():
    while True:
        text = input("Number of student records: ").strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("Enter a whole number greater than zero.")

def process_results():
    previous, bad = load_results(PREVIOUS_FILE)
    students = {}
    for i in range(1, read_count() + 1):
        ok, result = add_student(students, input("Registration number: "),
                                 input("Student name: "), input("Coursework mark: "),
                                 input("Examination mark: "))
        print("Accepted." if ok else f"Rejected: {result}")
    save_results(students)
    print_results(students)
    print_statistics(students)
