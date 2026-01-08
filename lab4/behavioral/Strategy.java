interface SortingStrategy {
    void sort(int[] arr);
}

class BubbleSortStrategy implements SortingStrategy {
    public void sort(int[] arr) {
        System.out.println("Bubble sort");
    }
}

class QuickSortStrategy implements SortingStrategy {
    public void sort(int[] arr) {
        System.out.println("Quick sort");
    }
}

class Sorter {
    private SortingStrategy strategy;

    public void setStrategy(SortingStrategy s) {
        this.strategy = s;
    }

    public void execute(int[] arr) {
        strategy.sort(arr);
    }
}