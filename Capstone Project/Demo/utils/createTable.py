import tkinter as tk

from entity.Solution import Solution

padding = 5

def create_student_table(frame, student_id: int, schedule: Solution):

    frame.title("Student Schedule")

    student = None
    for stu in schedule.data.list_students:
        if stu.roll_number == student_id:
            student = stu
            break
    
    signed_date = {}

    for exam in schedule.list_exam_info:
        if student in exam.list_student:
            for slot in range(exam.time_start, exam.time_end + 1):
                signed_date[slot] = exam

    if student:
        student_info_label = tk.Label(frame, text=f"Schedule table for student {student.roll_number}")
        student_info_label.grid(row=3, column=0, padx=0, pady=0)

        for i in range(padding):
            label = tk.Label(frame, text="", width=18, height=7, borderwidth=1)
            label.grid(row=i, column= 20)
        
        for i in range(schedule.data.num_exam_days):
            content = f"Day : {i + 1} "
            label = tk.Label(frame, text=content, width=18, height=7, borderwidth=1, relief="solid")
            label.grid(row=padding - 1, column= i + padding)
        for i in range(schedule.data.num_slots_per_day):
            content = f"Slot : {i + 1} "
            label = tk.Label(frame, text=content, width=18, height=7, borderwidth=1, relief="solid")
            label.grid(row=i + padding, column= padding - 1)
        for i in range(schedule.data.num_slots_per_day):
            for j in range(schedule.data.num_exam_days):
                value = i + (schedule.data.num_slots_per_day) * j
                if value not in signed_date.keys():
                    label = tk.Label(frame, text="", width=18, height=7, borderwidth=1, relief="solid", anchor="center")
                    label.grid(row=i + padding, column=j + padding)
                else:
                    exam = signed_date[value]
                    content = f"Subject: {exam.subject.subject_code}\nRoom: {exam.room}\nInvigilator: {exam.invigilator.code}"
                    label = tk.Label(frame, text=content, width=18, height=7, borderwidth=1, relief="solid")
                    label.grid(row=i + padding, column=j + padding)

    else:
        error_label = tk.Label(frame, text="Student not found!")
        error_label.grid(row=3, column=0, padx=10, pady=10)


def create_gv_table(frame, gv_id: int, schedule: Solution):
    frame.title("Invigilator Schedule")

    invigilator = None
    for invi in schedule.data.list_invigilators:
        if invi.code == gv_id:
            invigilator = invi
            break

    signed_date = {}

    for exam in schedule.list_exam_info:
        if invigilator == exam.invigilator:
            for slot in range(exam.time_start, exam.time_end + 1):
                signed_date[slot] = exam

    if invigilator:
        invigilator_info_label = tk.Label(frame, text=f"Schedule table for invigilator {invigilator.code}")
        invigilator_info_label.grid(row=3, column=0, padx=5, pady=5)

        for i in range(padding):
            label = tk.Label(frame, text="", width=18, height=7, borderwidth=1)
            label.grid(row=i, column=20)
        
        for i in range(schedule.data.num_exam_days):
            content = f"Day : {i + 1} "
            label = tk.Label(frame, text=content, width=18, height=7, borderwidth=1, relief="solid")
            label.grid(row=padding - 1, column=i + padding)
        
        for i in range(schedule.data.num_slots_per_day):
            content = f"Slot : {i + 1} "
            label = tk.Label(frame, text=content, width=18, height=7, borderwidth=1, relief="solid")
            label.grid(row=i + padding, column=padding - 1)
        
        for i in range(schedule.data.num_slots_per_day):
            for j in range(schedule.data.num_exam_days):
                value = i + (schedule.data.num_slots_per_day) * j
                if value not in signed_date.keys():
                    label = tk.Label(frame, text="", width=18, height=7, borderwidth=1, relief="solid", anchor="center")
                    label.grid(row=i + padding, column=j + padding)
                else:
                    exam = signed_date[value]
                    content = f"Subject: {exam.subject.subject_code}\nRoom: {exam.room}"
                    label = tk.Label(frame, text=content, width=18, height=7, borderwidth=1, relief="solid")
                    label.grid(row=i + padding, column=j + padding)
    else:
        error_label = tk.Label(frame, text="Invigilator not found!")
        error_label.grid(row=0, column=0, padx=10, pady=10)
