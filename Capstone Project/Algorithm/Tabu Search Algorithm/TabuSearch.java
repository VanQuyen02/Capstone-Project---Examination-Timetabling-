package tabuSearch;

import utils.Data;

public class TabuSearch {

    private Data data;
    private int maxIteration;
    private int maxTabuSize;
    private int neighborsSize;
    private int numberThread;

    public TabuSearch(Data data, int maxIteration, int maxTabuSize, int neighborsSize, int numberThread) {
        this.data = data;
        this.maxIteration = maxIteration;
        this.maxTabuSize = maxTabuSize;
        this.neighborsSize = neighborsSize;
        this.numberThread = numberThread;
    }

    public Data getData() {
        return data;
    }

    public void setData(Data data) {
        this.data = data;
    }

    public int getMaxIteration() {
        return maxIteration;
    }

    public void setMaxIteration(int maxIteration) {
        this.maxIteration = maxIteration;
    }

    public int getMaxTabuSize() {
        return maxTabuSize;
    }

    public void setMaxTabuSize(int maxTabuSize) {
        this.maxTabuSize = maxTabuSize;
    }

    public int getNeighborsSize() {
        return neighborsSize;
    }

    public void setNeighborsSize(int neighborsSize) {
        this.neighborsSize = neighborsSize;
    }

    public int getNumberThread() {
        return numberThread;
    }

    public void setNumberThread(int numberThread) {
        this.numberThread = numberThread;
    }
}
