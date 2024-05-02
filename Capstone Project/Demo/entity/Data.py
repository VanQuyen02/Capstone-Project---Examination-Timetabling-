from matplotlib.hatch import SouthEastHatch
from entity.Room import Room
from entity.Student import Student
from entity.Subject import Subject
from entity.Invigilator import Invigilator
import pandas as pd
import numpy as np
import os

class Data:
    def __init__(self):
        self.num_students = None
        self.num_invigilators = None
        self.num_rooms = None
        self.num_subjects = None
        self.num_exam_days = None
        self.max_students_per_room = None
        self.num_slots_per_day = None
        self.student_take_subject = None
        self.length_subject = None
        self.invi_can_supervise_subject = None
        self.num_slots_required_invigilators = None
        self.num_slots = None
        self.num_subjects_each_student = None
        self.num_students_each_subject = None
        self.num_rooms_each_subject = None
        self.list_students = None
        self.list_subjects = None
        self.list_invigilators = None
        self.list_rooms = None
        self.student_schedule = {}
        self.invigilator_schedule = {}
        self.subject_take_slot = None
        self.student_take_slot = None
    
    def load_data(self):
        print("start load csv")
        root_path = "./Data"
        students = pd.read_csv(os.path.join(root_path,"Student.csv"))
        invigilators = pd.read_csv(os.path.join(root_path,"Invigilator.csv"))
        subjects = pd.read_csv(os.path.join(root_path,"Subject.csv"))
        rooms = pd.read_csv(os.path.join(root_path,"Room.csv"))
        student_take_subject = pd.read_csv(os.path.join(root_path,"Student_Subject.csv"))
        invigilator_can_supervise_subject = pd.read_csv(os.path.join(root_path,"SubjectInvigilator.csv"))

        self.num_students = students.shape[0]
        self.num_invigilators = invigilators.shape[0]
        self.num_subjects = subjects.shape[0]
        self.num_rooms = 100
        self.num_exam_days = 9
        self.maximum_num_students_each_room = 22
        self.num_slots_per_day = 6

        self.student_take_subject = student_take_subject.values
        self.length_subject = (np.ceil(subjects['ExamDuration'].values / 90)).astype(int)
        self.invi_can_supervise_subject = invigilator_can_supervise_subject.values.T
        self.num_slots_required_for_invigilators = np.ceil(1.5*invigilators['NumberOfClass'].values)
        
        self.num_slots = self.num_slots_per_day * self.num_exam_days
        self.num_subjects_each_student = np.sum(self.student_take_subject, axis=1)
        self.num_students_each_subject = np.sum(self.student_take_subject, axis=0)
        self.num_rooms_each_subject = [None]*self.num_subjects
        for s in range(self.num_subjects):
            self.num_rooms_each_subject[s] = int((self.num_students_each_subject[s]+self.maximum_num_students_each_room-1)/ self.maximum_num_students_each_room)
        self.list_students = [None]*self.num_students
        self.list_invigilators = [None]*self.num_invigilators
        self.list_subjects = [None]*self.num_subjects
        self.list_rooms = [None]*self.num_rooms
        for i in range(0, self.num_students):
            student_id = students['Id'][i]
            roll_num = students['RollNumber'][i]
            member_code = students['MemberCode'][i]
            email = students["Email"][i]
            full_name = students['FullName'][i]
            self.list_students[i] = Student(student_id, roll_num, member_code, email, full_name)
        for i in range(0, self.num_invigilators):
            invigilator_id = invigilators['Id'][i]
            code = invigilators['Code'][i]
            num_class = invigilators["NumberOfClass"][i]
            self.list_invigilators[i] = Invigilator(invigilator_id, code, num_class)
        for i in range(0, self.num_subjects):
            subject_id = subjects['Id'][i]
            subject_code = subjects['SubCode'][i]
            exam_duration = subjects['ExamDuration'][i]
            self.list_subjects[i] = Subject(subject_id, subject_code, exam_duration)
        
        for i in range(self.num_rooms):
            room_id = i
            room_name = rooms['Room'][i]
            self.list_rooms[i] = Room(room_id, room_name)

        