from entity.Data import Data
from math import ceil
import numpy as np
from entity.ExamInfomation import ExamInfomation

class Solution:
    def __init__(self, data : Data):
        self.schedule = np.zeros((data.num_subjects, data.num_slots, data.num_invigilators), dtype=int)
        self.list_exam_info = [] 
        self.data = data

    def create_solution(self, file_path = "Data/SolutionTabu.txt"):
        subject_take_slot = np.zeros((self.data.num_subjects, self.data.num_slots), dtype=int)
        invigilator_take_subject = np.zeros((self.data.num_invigilators, self.data.num_subjects), dtype=int)
        room_take_slot = np.zeros((self.data.num_rooms, self.data.num_slots), dtype=int)

        subject_start = {}
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(",")
                subject_index = int(parts[0].split(" ")[1])
                slot_index = int(parts[1].split(" ")[1])
                invigilator_index = int(parts[2].split(":")[0].split(" ")[1])
                status = int(parts[2].split(":")[1])

                self.schedule[subject_index, slot_index, invigilator_index] = status
                
                if status:
                    subject_take_slot[subject_index, slot_index] = 1
                    invigilator_take_subject[invigilator_index, subject_index] = 1

        # create subject start
        for subject in self.data.list_subjects:
            for slot in range(self.data.num_slots):
                if subject_take_slot[subject.id, slot] == 1:
                    subject_start[subject] = slot
                    break

        list_subject_remain = []
        for subject in self.data.list_subjects:
            list_subject_remain.append(subject)

        # create list exam info
        for slot in range (self.data.num_slots):

            list_room = []
            for room in range(self.data.num_rooms):
                if room_take_slot[room, slot] == 0:
                    list_room.append(room)

            for subject in self.data.list_subjects:

                if subject_start[subject] == slot:
                    num_stu_each = ceil(self.data.num_students_each_subject[subject.id] / self.data.num_rooms_each_subject[subject.id])
                    total_stu = self.data.num_students_each_subject[subject.id]
                    list_invi = []

                    for invigilator in self.data.list_invigilators:
                        if invigilator_take_subject[invigilator.id, subject.id] == 1:
                            list_invi.append(invigilator)

                    stu_id = 0
                    for i in range(self.data.num_rooms_each_subject[subject.id]):
                        num_stu_need = min(num_stu_each, total_stu)
                        total_stu -= num_stu_need
                        exam = ExamInfomation()
                        exam.subject = subject
                        exam.time_start = subject_start[subject]
                        exam.time_end = subject_start[subject] + self.data.length_subject[subject.id] - 1
                        exam.invigilator = list_invi[i]
                        while(num_stu_need > 0):
                            if self.data.student_take_subject[stu_id][subject.id] == 1:
                                exam.list_student.append(self.data.list_students[stu_id])
                                num_stu_need -= 1
                            stu_id += 1
                        choosed_room = list_room[0]
                        list_room.pop(0)
                        exam.room = choosed_room
                        for cur_slot in range(slot, slot + self.data.length_subject[subject.id]):
                            room_take_slot[choosed_room][cur_slot] = 1
                        self.list_exam_info.append(exam)
                    

        
                        
