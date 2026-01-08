public class Singleton {

    private static Singleton instance;

    private Singleton() {
        System.out.println("Singleton created");
    }

    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }

    public void someMethod() {
        System.out.println("Doing someMethond()");
    }
}
