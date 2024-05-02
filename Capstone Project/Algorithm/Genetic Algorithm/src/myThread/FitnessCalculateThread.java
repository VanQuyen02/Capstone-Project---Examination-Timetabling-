package myThread;

import dataInput.GeneticData;
import java.util.Arrays;
import entities.Individual;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class FitnessCalculateThread implements Runnable {

    private Individual individual;

    public FitnessCalculateThread(Individual individual) {
        this.individual = individual;
    }

    public Individual getIndividual() {
        return individual;
    }

    public void setIndividual(Individual individual) {
        this.individual = individual;
    }

    public ArrayList<Double> calculateFitess() {
        double w3 = 6/ 20.0;
        double w4 = 13/ 20.0;
        double w5 = 1 / 20.0;
        double fitnessValue;
        double payoffStudent = 0.0;
        double payoffInvigilator = 0.0;
        double payoffP0 = 0.0;
        ArrayList<Double> result = new ArrayList();
        if (individual.passAllConstraints()) {
            payoffStudent = calPayoffStudent(individual.getChromosome());
            payoffInvigilator = calPayoffInvigilator(individual.getChromosome());
            payoffP0 = calPayoffP0(individual.getChromosome());
            fitnessValue = w3 * payoffStudent + w4 * payoffInvigilator + w5 * payoffP0;
        } else {
            fitnessValue = 10000;
        }
        result.add(fitnessValue);
        result.add(payoffStudent);
        result.add(payoffInvigilator);
        result.add(payoffP0);
        return result;
    }

    public double calPayoffStudent(int[][][] chromosome) {
        int[] slotStartOfSubject = individual.getSlotStartOfSubject();
        int[][] slotStartOfStudent = new int[individual.getData().getNumberOfStudents()][individual.getData().getNumberOfSubjects()];

        for (int m = 0; m < individual.getData().getNumberOfStudents(); m++) {
            for (int s = 0; s < individual.getData().getNumberOfSubjects(); s++) {
                slotStartOfStudent[m][s] = individual.getData().getStudentTakeSubject()[m][s] * slotStartOfSubject[s];
            }

        }
        int[][] sortedStartSlotDesc = new int[individual.getData().getNumberOfStudents()][individual.getData().getNumberOfSubjects()];
        for (int m = 0; m < individual.getData().getNumberOfStudents(); m++) {
            sortedStartSlotDesc[m] = Arrays.copyOf(slotStartOfStudent[m], slotStartOfStudent[m].length);
            Arrays.sort(sortedStartSlotDesc[m]);
            reverseArray(sortedStartSlotDesc[m]);
        }

        double payoffValueStudent = 0;
        int cnt = 0;
        for (int m = 0; m < individual.getData().getNumberOfStudents(); m++) {
            double payoffOneStudent = 0.0;
            if (individual.getData().getNumberOfSubjectsOfEachStudent()[m] > 1) {
                cnt++;
                for (int i = 0; i < individual.getData().getNumberOfSubjectsOfEachStudent()[m] - 1; i++) {
                    double diff = sortedStartSlotDesc[m][i] - sortedStartSlotDesc[m][i + 1]
                            - (int) individual.getData().numberOfTotalSlots / individual.getData().getNumberOfSubjectsOfEachStudent()[m];
                    payoffOneStudent += Math.exp(Math.abs(diff));
                }
                payoffOneStudent = Math.log(payoffOneStudent/(individual.getData().getNumberOfSubjectsOfEachStudent()[m] - 1));
            }
            payoffValueStudent += payoffOneStudent;
        }
        return payoffValueStudent / cnt;
    }

    private void reverseArray(int[] arr) {
        int start = 0;
        int end = arr.length - 1;
        while (start < end) {
            int temp = arr[start];
            arr[start] = arr[end];
            arr[end] = temp;
            start++;
            end--;
        }
    }

    public double calPayoffInvigilator(int[][][] chromosome) {
        int[][] numberSlotScheduleInvigilator = new int[individual.getData().getNumberOfInvigilators()][individual.getData().getNumberOfExaminationDays()];
        for (int i = 0; i < chromosome[0][0].length; i++) {
            for (int d = 0; d < individual.getData().getNumberOfExaminationDays(); d++) {
                int count = 0;
                for (int t = individual.getData().getNumberOfSlotsPerDay() * d; t < individual.getData().getNumberOfSlotsPerDay() * (d + 1); t++) {
                    for (int s = 0; s < individual.getData().getNumberOfSubjects(); s++) {
                        count += chromosome[s][t][i];
                    }
                }
                if (count > 0) {
                    numberSlotScheduleInvigilator[i][d] = 1;
                }
            }
        }

        double payoffValueInvigilator;
        double payoff1 = 0;
        double payoff2 = 0;
        double w1 = 1.0 / 2;
        double w2 = 1.0 / 2;

        for (int i = 0; i < chromosome[0][0].length; i++) {
            for (int d = 0; d < individual.getData().getNumberOfExaminationDays(); d++) {
                payoff1 += (double) numberSlotScheduleInvigilator[i][d];
            }
        }

        for (int i = 0; i < individual.getData().getNumberOfInvigilators(); i++) {
            int totalSlotOfInvigilator = 0;
            for (int s = 0; s < individual.getData().getNumberOfSubjects(); s++) {
                for (int t = 0; t < individual.getData().getNumberOfTotalSlots(); t++) {
                    totalSlotOfInvigilator += chromosome[s][t][i];
                }
            }
            payoff2 += Math.abs(totalSlotOfInvigilator - individual.getData().getNumberOfSlotsRequiredForInvigilators()[i]);
        }
        payoffValueInvigilator = (w1 * payoff1 + w2 * payoff2) / individual.getData().getNumberOfInvigilators();
        return payoffValueInvigilator;
    }

    public double calPayoffP0(int[][][] chromosome) {
        double meanRoomEachSlot;
        int totalRooms = 0;
        for (int t = 0; t < chromosome[0].length; t++) {
            for (int s = 0; s < chromosome.length; s++) {
                for (int i = 0; i < chromosome[0][0].length; i++) {
                    totalRooms += chromosome[s][t][i];
                }
            }
        }
        meanRoomEachSlot = (double) totalRooms / individual.getData().getNumberOfTotalSlots();
        double payOffP0 = 0;
        for (int t = 0; t < chromosome[0].length; t++) {
            double totalRoomsEachSlot = 0;
            for (int s = 0; s < chromosome.length; s++) {
                for (int i = 0; i < chromosome[0][0].length; i++) {
                    totalRoomsEachSlot += chromosome[s][t][i];
                }
            }
            payOffP0 += Math.pow(totalRoomsEachSlot - meanRoomEachSlot, 2);
        }
        payOffP0 = Math.sqrt(payOffP0 / (individual.getData().getNumberOfTotalSlots()-1));
        return payOffP0;
    }
    
    

    @Override
    public void run() {
        ArrayList<Double> result = calculateFitess();
        individual.setFitness(result.get(0));
        individual.setPayoffStudent(result.get(1));
        individual.setPayoffInvigilator(result.get(2));
        individual.setPayoffDepartment(result.get(3));
    }

}
