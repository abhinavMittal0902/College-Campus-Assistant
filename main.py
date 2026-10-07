import json
from datetime import datetime


def load_data(filename):
    with open(filename, "r") as file:
        return json.load(file)


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# =========================
# ATTENDANCE
# =========================

def getAttendance(rollNo):

    attendance = load_data("attendance.json")

    student_attendance = []

    for record in attendance:

        if str(record["rollNo"]).lower() == str(rollNo).lower():
            student_attendance.append(record)

    if len(student_attendance) == 0:
        return "No attendance record found for roll number: " + str(rollNo)

    result = "\nAttendance Report\n"
    result += "-------------------------\n"

    total_classes = 0
    total_attended = 0

    for record in student_attendance:

        percentage = (
            record["attended"] / record["totalClasses"]
        ) * 100

        result += (
            f'{record["subject"]}: '
            f'{percentage:.2f}% '
            f'({record["attended"]}/{record["totalClasses"]})\n'
        )

        total_classes += record["totalClasses"]
        total_attended += record["attended"]

    overall_percentage = (
        total_attended / total_classes
    ) * 100

    result += "-------------------------\n"
    result += f"Overall Attendance: {overall_percentage:.2f}%\n"

    return result


def calculateAttendanceNeeded(rollNo, target):

    attendance = load_data("attendance.json")

    total_classes = 0
    total_attended = 0

    for record in attendance:

        if str(record["rollNo"]).lower() == str(rollNo).lower():

            total_classes += record["totalClasses"]
            total_attended += record["attended"]

    if total_classes == 0:
        return "No attendance record found."

    current_percentage = (
        total_attended / total_classes
    ) * 100

    if current_percentage >= target:

        return (
            f"Your current attendance is "
            f"{current_percentage:.2f}%.\n"
            f"You have already crossed the target "
            f"of {target}%.\n"
            f"Additional classes required: 0"
        )

    required = (
        (target * total_classes) -
        (100 * total_attended)
    ) / (100 - target)

    required = int(required)

    if (
        (total_attended + required)
        / (total_classes + required)
        * 100
    ) < target:

        required += 1

    final_percentage = (
        (total_attended + required)
        / (total_classes + required)
    ) * 100

    return (
        f"Current attendance: {current_percentage:.2f}%\n"
        f"Target attendance: {target}%\n"
        f"Classes you need to attend: {required}\n"
        f"Attendance after attending them: "
        f"{final_percentage:.2f}%"
    )


# =========================
# EXAM
# =========================

def getExamSchedule(course, semester):

    exams = load_data("exams.json")

    result = "\nExam Schedule\n"
    result += "-------------------------\n"

    found = False

    for exam in exams:

        if (
            str(exam["course"]).lower() == str(course).lower()
            and exam["semester"] == semester
        ):

            found = True

            result += (
                f'Subject: {exam["subject"]}\n'
                f'Date: {exam["examDate"]}\n'
                f'Room: {exam["room"]}\n'
                f'-------------------------\n'
            )

    if not found:
        return "No exam schedule found."

    return result


# =========================
# FEES
# =========================

def getFeeStatus(rollNo):

    fees = load_data("fees.json")

    for fee in fees:

        if str(fee["rollNo"]).lower() == str(rollNo).lower():

            due = fee["totalFee"] - fee["paid"]

            result = "\nFee Status\n"
            result += "-------------------------\n"
            result += f'Total Fee: ₹{fee["totalFee"]}\n'
            result += f'Paid: ₹{fee["paid"]}\n'
            result += f'Due: ₹{due}\n'
            result += f'Due Date: {fee["dueDate"]}\n'
            result += f'Status: {fee["status"].upper()}\n'

            return result

    return "No fee record found for " + str(rollNo)


# =========================
# COMPLAINT
# =========================

def raiseComplaint(rollNo, category, text):

    complaints = load_data("complaints.json")

    complaint_number = len(complaints) + 1

    complaint_id = f"C{complaint_number:03d}"

    new_complaint = {
        "complaintId": complaint_id,
        "rollNo": rollNo,
        "category": category,
        "text": text,
        "status": "Open",
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    complaints.append(new_complaint)

    save_data("complaints.json", complaints)

    result = "\nComplaint Registered Successfully!\n"
    result += "-------------------------\n"
    result += f"Complaint ID: {complaint_id}\n"
    result += f"Category: {category}\n"
    result += f"Status: Open\n"

    return result


# =========================
# STUDENT
# =========================

def getStudent(rollNo):

    students = load_data("student.json")

    for student in students:

        if str(student["rollNo"]).lower() == str(rollNo).lower():
            return student

    return None


# =========================
# UNKNOWN QUESTIONS
# =========================

def webSearch(query):

    return (
        "I don't have this information in the college database.\n"
        "I can only answer questions related to college services."
    )


# =========================
# QUESTION PROCESSOR
# =========================

def process_question(question):

    question_lower = question.lower()

    students = load_data("student.json")

    rollNo = None

    # Find roll number from the question
    for student in students:

        student_roll = str(student["rollNo"]).lower()

        if student_roll in question_lower:

            rollNo = str(student["rollNo"])
            break


    # =========================
    # ATTENDANCE
    # =========================

    if (
        "attendance" in question_lower
        or "how many more classes" in question_lower
        or "classes must i attend" in question_lower
        or "reach 75" in question_lower
    ):

        if rollNo is None:

            rollNo = input(
                "Please enter your roll number: "
            )

        # Calculate attendance required
        if (
            "75" in question_lower
            or "target" in question_lower
            or "reach" in question_lower
            or "need" in question_lower
            or "how many more" in question_lower
            or "must i attend" in question_lower
        ):

            return calculateAttendanceNeeded(
                rollNo,
                75
            )

        return getAttendance(rollNo)


    # =========================
    # EXAM + FEES
    # =========================

    if (
        "exam" in question_lower
        or "examination" in question_lower
        or "fee" in question_lower
        or "fees" in question_lower
        or "paid" in question_lower
        or "payment" in question_lower
        or "cleared" in question_lower
    ):

        if rollNo is None:

            rollNo = input(
                "Please enter your roll number: "
            )

        student = getStudent(rollNo)

        if student is None:
            return "Student not found."

        result = ""

        # Exam information
        if (
            "exam" in question_lower
            or "examination" in question_lower
        ):

            result += getExamSchedule(
                student["course"],
                student["semester"]
            )

        # Fee information
        if (
            "fee" in question_lower
            or "fees" in question_lower
            or "paid" in question_lower
            or "payment" in question_lower
            or "cleared" in question_lower
        ):

            result += "\n" + getFeeStatus(rollNo)

        return result


    # =========================
    # COMPLAINT
    # =========================

    if (
        "complaint" in question_lower
        or "broken" in question_lower
        or "not working" in question_lower
        or "problem" in question_lower
    ):

        if rollNo is None:

            rollNo = input(
                "Please enter your roll number: "
            )

        print("\nComplaint detected.")

        category = input(
            "Enter complaint category "
            "(Infrastructure/Academic/Other): "
        )

        return raiseComplaint(
            rollNo,
            category,
            question
        )


    # =========================
    # UNKNOWN QUESTION
    # =========================

    return webSearch(question)


# =========================
# MAIN PROGRAM
# =========================

def main():

    print("\n==========================================")
    print("       COLLEGE CAMPUS ASSISTANT")
    print("==========================================")
    print("Type 'exit' to close the assistant.")
    print("==========================================\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":

            print("\nAssistant: Goodbye!")
            break

        answer = process_question(question)

        print("\nAssistant:", answer)
        print()


if __name__ == "__main__":
    main()