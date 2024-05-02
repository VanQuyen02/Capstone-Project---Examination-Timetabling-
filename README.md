## Solving The Examination Timetabling Problem: 
## A Nash Equilibrium Approach With Genetic Algorithm And Tabu Search Comparisons
### 1. Introduction
     The Examination Timetabling Problem (ETP) is a critical scheduling issue faced by educational institutions globally.
     Challenges include handling the increasing number of courses and students with limited resources.
     Traditional manual timetabling methods are labor-intensive and error-prone.
     Target of our research is how to scheduling examination such that it balance benefit of all stakeholders.
     Three main group of stakeholders:
        1. The Academic Department wants
        an even distribution of rooms
        between timeslots
        2. Students wish their exams to be
        evenly distributed throughout the
        entire period.
        3. Invigilators wants compress their
        invigilation schedule into as few
        days as possible while keeping the
        number of timeslots as close to the
        required number as they can.
![image](https://github.com/VanQuyen02/Capstone-Project---Examination-Timetabling-/assets/95958989/43b92239-8225-4d52-8d1d-a4d5d943d4ef)

### 2. Methodology
![image](https://github.com/VanQuyen02/Capstone-Project---Examination-Timetabling-/assets/95958989/4af2d5da-e998-487c-856b-e47e18670d1c)

      Modeling Problem using Nash Equilibrium Theory
      Solving Problem using Genetic Algorithm and TabuSearch. We also use Q-Learning but it is time-consuming.
### 3. Experiment and Result
#### 3.1 Dataset
![image](https://github.com/VanQuyen02/Capstone-Project---Examination-Timetabling-/assets/95958989/6e3c9f85-9206-427b-9364-e66a446973df)

![image](https://github.com/VanQuyen02/Capstone-Project---Examination-Timetabling-/assets/95958989/64112b8e-78c5-4722-a738-e77a1599a00b)

#### 3.2 Environment
     CPU: Intel Core i9 gen 11th
     RAM: 64GB
#### 3.3 Result 
##### 3.3.1 Algorithm Comparision
###### Fitness Comparsion
![image](https://github.com/VanQuyen02/Capstone-Project---Examination-Timetabling-/assets/95958989/616fc0bf-d76a-43e7-b314-91b73bd21e14)
###### Hypervolume Indicator
![image](https://github.com/VanQuyen02/Capstone-Project---Examination-Timetabling-/assets/95958989/1f1f6447-b054-4971-be2c-5ceda4678924)
=> Tabu Search outperformance GA

##### 3.3.2 Best Result Analysis
We have reach our target of balancing all stakeholders participating in problem as expectation.
![image](https://github.com/VanQuyen02/Capstone-Project---Examination-Timetabling-/assets/95958989/e4031077-acbd-4a50-93df-e6e127b9b544)
### 4. Conclusion and Future Work
     Addressing the scheduling challenges of exams by integrating game theory – Nash Equilibrium with a Genetic Algorithm and Tabu Search framework.
     Tabu Search has better performance than Genetic Algorithm.
     Future research could explore a hybrid model that combine the strengths of GA and Tabu Search
     Incorporating a wider range of constraints and objectives, such as: invigilator preferences
### 5. Demo
We use Tinker Library to visulize Schedule of each student and each Invigilator for Searching.
We export csv file to save plan aftern scheduling optimization.
