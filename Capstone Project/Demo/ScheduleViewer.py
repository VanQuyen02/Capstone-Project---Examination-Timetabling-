from math import inf
from re import S
import tkinter as tk
from PIL import Image, ImageTk
from datetime import date, timedelta
import csv

from entity.Data import Data
from entity.Solution import Solution

DAYS = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
SLOTS = 6  # 0 to 12
TIMES = [
    "7:30-9:00",
    "9:10-10:40",
    "10:50-12:20",
    "12:50-14:20",
    "14:30-16:00",
    "16:10-17:40",
]

data = Data()
data.load_data()
solution = Solution(data)
solution.create_solution()
student_info_dict = {}

for i in range(len(data.list_students)):
    student = data.list_students[i]
    roll_number = student.roll_number
    student_id = student.student_id
    member_code = student.member_code
    full_name = student.full_name
    if roll_number not in student_info_dict.keys():
        student_info_dict[roll_number] = (student_id, member_code, full_name)

invigilator_info_dict = {}

for i in range(len(data.list_invigilators)):
    invigilator = data.list_invigilators[i]
    invigilator_id = invigilator.id
    code = invigilator.code
    if invigilator_id not in student_info_dict.keys():
        invigilator_info_dict[code] = invigilator_id

with open("exam_information.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "Exam Date",
            "Subject Code",
            "Time Start Slot",
            "Time End",
            "Student ID",
            "Student Name",
            "invigilatorID",
            "Room",
        ]
    )
    # Write exam information for each instance
    for exam_info in solution.list_exam_info:
        for student in exam_info.list_student:
            writer.writerow(
                [
                    int(exam_info.time_start / 6) + 1,
                    exam_info.subject.subject_code,
                    exam_info.time_start % 6 + 1,
                    exam_info.time_end % 6 + 1,
                    student.roll_number,
                    student.full_name,
                    exam_info.invigilator.code,
                    data.list_rooms[exam_info.room].name,
                ]
            )
# with open("inivi_schedule.csv", "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(
#         [
#             "Exam Date",
#             "Subject Code",
#             "Time Start Slot",
#             "Time End",
#             "Room",
#             "Number Of Student",
#             "InvigilatorID",
#         ]
#     )
#     # Write exam information for each instance
#     for exam_info in solution.list_exam_info:
#         writer.writerow(
#             [
#                 int(exam_info.time_start / 6) + 1,
#                 exam_info.subject.subject_code,
#                 exam_info.time_start % 6 + 1,
#                 exam_info.time_end % 6 + 1,
#                 data.list_rooms[exam_info.room].name,
#                 len(exam_info.list_student),
#                 exam_info.invigilator.code,
#             ]
#         )
print("perfect write file")


class ScheduleViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Schedule Viewer")
        self.geometry("1400x500")
        self.entries = [[None for _ in DAYS] for _ in range(SLOTS)]
        self.timetable_widgets = []
        self.create_widgets()
        self.load_logo()

    def create_widgets(self):
        # Main title label
        self.main_title_label = tk.Label(
            self, text="Choose the schedule to view", font=("Helvetica", 16)
        )
        self.main_title_label.grid(row=2, column=2, columnspan=8, pady=10)

        # Buttons for choosing schedule
        self.student_button = tk.Button(
            self,
            text="Show schedule of Student",
            command=lambda: self.display_input("student"),
        )
        self.student_button.grid(row=1, column=0, pady=10, padx=100)

        self.invigilator_button = tk.Button(
            self,
            text="Show schedule of Invigilator",
            command=lambda: self.display_input("invigilator"),
        )
        self.invigilator_button.grid(row=1, column=1, pady=10, padx=100)

    def load_logo(self):
        # Load and display logo
        image = Image.open(r"./image/logo_1.png")
        logo_image = ImageTk.PhotoImage(image)

        logo_label = tk.Label(self, image=logo_image)
        logo_label.image = logo_image  # keep a reference!
        logo_label.place(relx=1.0, y=0, anchor="ne")

    def display_input(self, choice):
        # Hide the choice buttons
        self.student_button.grid_remove()
        self.invigilator_button.grid_remove()

        # Display input field
        self.code_label = tk.Label(self, text=f"Enter {choice} code:")
        self.code_label.grid(row=1, column=0)

        self.code_entry = tk.Entry(self)
        self.code_entry.grid(row=1, column=1, padx=5)

        # Create Listbox for suggestions
        self.code_listBox = tk.Listbox(self, width=30)
        self.code_listBox.grid(row=2, column=1, padx=5)

        # Fill the Listbox with student codes or invigilator codes based on choice
        if choice == "student":
            for roll_number in student_info_dict:
                self.code_listBox.insert(tk.END, roll_number)
        else:
            for code in invigilator_info_dict:
                self.code_listBox.insert(tk.END, code)

        # Bind the event to update suggestions when typing in Entry
        self.code_entry.bind(
            "<KeyRelease>",
            lambda event, choice=choice: self.update_suggestions(event, choice),
        )

        # Bind the event to select suggestion when clicking on Listbox
        self.code_listBox.bind("<<ListboxSelect>>", self.on_select_suggestion)

        self.submit_button = tk.Button(
            self,
            text="Submit",
            command=lambda: self.show_schedule(choice, self.code_entry.get()),
        )
        self.submit_button.grid(row=1, column=2)

        # Add a back button to allow user to go back to the previous choices
        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.grid(row=1, column=3, padx=5)

    def on_select_suggestion(self, event):
        # Get the selected item from Listbox
        selected_index = self.code_listBox.curselection()
        if selected_index:
            selected_item = self.code_listBox.get(selected_index)
            # Set the Entry with the selected item
            self.code_entry.delete(0, tk.END)
            self.code_entry.insert(0, selected_item)

    def update_suggestions(self, event, choice):
        search_term = self.code_entry.get().lower()
        self.code_listBox.delete(0, tk.END)
        if choice == "student":
            for roll_number in student_info_dict:
                if search_term in roll_number.lower():
                    self.code_listBox.insert(tk.END, roll_number)
        else:
            for code in invigilator_info_dict:
                if search_term in code.lower():
                    self.code_listBox.insert(tk.END, code)

    def on_select_suggestion(self, event):
        # Get the selected item from Listbox
        selected_index = self.code_listBox.curselection()
        if selected_index:
            selected_item = self.code_listBox.get(selected_index)
            # Set the Entry with the selected item
            self.code_entry.delete(0, tk.END)
            self.code_entry.insert(0, selected_item)

    def go_back(self):
        # Remove the input fields and submit button
        self.code_listBox.destroy()
        self.code_label.destroy()
        self.code_entry.destroy()
        self.submit_button.destroy()
        self.back_button.destroy()
        self.main_title_label.config(text="Choose the schedule to view", fg="black")

        # Show the choice buttons again
        self.student_button.grid()
        self.invigilator_button.grid()

        if len(self.timetable_widgets) > 0:
            for widget in self.timetable_widgets:
                widget.destroy()
            self.timetable_widgets = []  # Clear the list after destroying the widgets

    def get_week_dates(self):
        today = date.today()
        start = today - timedelta(days=today.weekday())  # This is Monday
        return [start + timedelta(days=i) for i in range(len(DAYS))]  # Next 7 days

    def prepare_timetable_grid(self):
        dates = self.get_week_dates()
        width = 15
        height = 2

        tk.Label(self).grid(row=2)

        for i, day in enumerate(DAYS):
            day_label = tk.Label(
                self, text=day, borderwidth=1, relief="solid", width=width
            )
            day_label.grid(row=3, column=i + 2, sticky="ew")
            date_label = tk.Label(
                self,
                text=dates[i % len(dates)].strftime("%d/%m"),
                borderwidth=1,
                relief="solid",
            )
            date_label.grid(row=4, column=i + 2, sticky="ew")
            self.timetable_widgets.append(day_label)
            self.timetable_widgets.append(date_label)

        for slot in range(SLOTS):
            slot_label = tk.Label(
                self,
                text=f"Slot {slot+1} \n {TIMES[slot]}",
                borderwidth=1,
                relief="solid",
                width=width,
                height=height,
            )
            slot_label.grid(row=slot + 5, column=1, sticky="ew")
            self.timetable_widgets.append(slot_label)
            for day in range(len(DAYS)):
                entry = tk.Label(
                    self,
                    text="",
                    borderwidth=1,
                    relief="solid",
                    width=width,
                    height=height,
                )
                entry.grid(row=slot + 5, column=day + 2, sticky="ew")
                # entry = tk.Entry(self, borderwidth=1, relief="solid")
                # entry.grid(row=slot+5, column=day+1, sticky="ew")
                self.timetable_widgets.append(entry)
                self.entries[slot][day] = entry

    def show_schedule(self, choice, code):
        if choice != "":
            self.prepare_timetable_grid()
            if choice == "student":
                student_code = code
                student_info = student_info_dict.get(student_code)

                if student_info:
                    schedule = []
                    self.main_title_label.config(
                        text=f"Examination for {student_info[1]} ({student_info[2]})",
                        fg="blue",
                    )
                    student_id = student_info[0]
                    # Clear previous schedule
                    for row in self.entries:
                        for entry in row:
                            entry.config(text="")
                    for exam in solution.list_exam_info:
                        for student in exam.list_student:
                            if int(student.student_id) == int(student_id):
                                schedule.append(
                                    (
                                        exam.subject.subject_code,
                                        exam.time_start,
                                        exam.time_end,
                                        data.list_rooms[exam.room].name,
                                    )
                                )
                    # Update the schedule
                    for subject, slot_start, slot_end, room in schedule:
                        day = slot_start / 6
                        length = slot_end - slot_start + 1
                        slot_start %= 6
                        for l in range(0, length):
                            self.entries[int(slot_start + l)][int(day)].config(
                                text=f"{subject} \n at {room}"
                            )
                else:
                    if len(self.timetable_widgets) > 0:
                        for widget in self.timetable_widgets:
                            widget.destroy()
                        self.timetable_widgets = (
                            []
                        )  # Clear the list after destroying the widgets
                    self.main_title_label.config(
                        text="Student code not found", fg="blue"
                    )
            else:
                invigilator_code = code
                invigilator_info = invigilator_info_dict.get(invigilator_code)

                if invigilator_info >= 0:
                    schedule = []
                    self.main_title_label.config(
                        text=f"Examination for {invigilator_code}", fg="blue"
                    )
                    invigilator_id = invigilator_info
                    # Clear previous schedule
                    for row in self.entries:
                        for entry in row:
                            entry.config(text="")
                    for exam in solution.list_exam_info:
                        if int(exam.invigilator.id) == int(invigilator_id):
                            schedule.append(
                                (
                                    exam.subject.subject_code,
                                    exam.time_start,
                                    exam.time_end,
                                    data.list_rooms[exam.room].name,
                                )
                            )
                    # Update the schedule
                    for subject, slot_start, slot_end, room in schedule:
                        day = slot_start / 6
                        length = slot_end - slot_start + 1
                        slot_start %= 6
                        for l in range(0, length):
                            self.entries[int(slot_start + l)][int(day)].config(
                                text=f"{subject} \n at {room}"
                            )
                else:
                    if len(self.timetable_widgets) > 0:
                        for widget in self.timetable_widgets:
                            widget.destroy()
                        self.timetable_widgets = (
                            []
                        )  # Clear the list after destroying the widgets
                    self.main_title_label.config(
                        text="Invigilator code not found", fg="blue"
                    )


if __name__ == "__main__":
    app = ScheduleViewer()
    app.mainloop()
