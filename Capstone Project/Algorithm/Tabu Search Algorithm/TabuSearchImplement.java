package tabuSearch;

import thread.NeighborsThread;
import utils.Data;
import utils.Solution;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class TabuSearchImplement {
    TabuSearch tabuSearch;
    Solution bestSolution;

    public TabuSearchImplement(TabuSearch tabuSearch) {
        this.tabuSearch = tabuSearch;
    }

    public void implement(String fileName) throws IOException {
        Data data = tabuSearch.getData();

        String fitnessFilename = "Fitness"+fileName;

        File myObj = new File(fitnessFilename);

        if (myObj.createNewFile()) {
            System.out.println("File created: " + myObj.getName());
            bestSolution = Solution.createSolution(data);
        } else {
            System.out.println("File " + myObj.getName() + " already exists.");
            bestSolution = Solution.readSolution(data, fileName);
        }

        FileWriter fileWriter = new FileWriter(fitnessFilename, true);
        BufferedWriter writer = new BufferedWriter(fileWriter);

        double bestFitness = bestSolution.fitness;
        Solution curSolution = bestSolution.clone();
        ArrayList<Solution> tabuList = new ArrayList<>();
        Solution bestNeighbor = null;
        double bestNeighborFitness;


        for (int i = 0; i < tabuSearch.getMaxIteration(); i++) {
            bestNeighbor = getBestNeighbor(curSolution, tabuList);

            if (bestNeighbor == null) {
                System.out.println("No non-tabu neighbors found");
                break;
            }

            bestNeighborFitness = bestNeighbor.fitness;
            curSolution = bestNeighbor.clone();
            tabuList.add(bestNeighbor);

            if (tabuList.size() > tabuSearch.getMaxTabuSize()) {
                tabuList.removeFirst();
            }

            if (bestNeighborFitness < bestFitness) {
                if (!(new Solution(data, bestNeighbor.D).passAllConstraint())){
                    System.out.println("Error in finding best neighbor!");
                    break;
                }
                bestSolution.writeSolution(fileName);
                bestSolution = bestNeighbor.clone();
                bestFitness = bestNeighborFitness;

            }
            System.out.println("Iter: " + i + " - Cur Fitness: " + bestNeighborFitness + " - Best Fitness: " + bestFitness);
            writer.write(bestFitness + "\n");
        }
        writer.close();
    }

    public Solution getBestNeighbor(Solution curSolution, ArrayList<Solution> tabuList) throws IOException {
        Data data = tabuSearch.getData();
        ExecutorService executorService = Executors.newFixedThreadPool(tabuSearch.getNumberThread());

        ArrayList<ArrayList<Integer>> subjectInvigilator = Solution.getSubjectInvigilator(data, curSolution.H, curSolution.D);
        ArrayList<Solution> neighbors = new ArrayList<>();

        for (int i = 0; i < tabuSearch.getNeighborsSize(); i++) {
            Runnable thread = new NeighborsThread(data, curSolution, neighbors, tabuList, subjectInvigilator);
            executorService.execute(thread);
        }

        executorService.shutdown();

        while (!executorService.isTerminated()){

        }

        Solution bestNeighbor = neighbors.getFirst();
        double bestNeighborFitness = bestNeighbor.fitness;

        for (int i = 1; i < neighbors.size(); i++) {
            if (neighbors.get(i).fitness < bestNeighborFitness) {
                bestNeighbor = neighbors.get(i);
                bestNeighborFitness = bestNeighbor.fitness;
            }
            neighbors.get(i).writePayoff("PayoffSolutionTabu.txt");
        }
        neighbors.clear();
        return bestNeighbor;
    }

}
