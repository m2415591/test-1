interface Burger {
    void prepare();
}

class CheeseBurger implements Burger {
    @Override
    public void prepare() {
        System.out.println("Cooking cheeseburger");
    }
}

class HamBurger implements Burger {
    @Override
    public void prepare() {
        System.out.println("Cooking hamburger");
    }
}

abstract class BurgerFactory {
    public abstract Burger createBurger();

    public void makeBurger() {
        Burger burger = createBurger();
        burger.prepare();
    }
}

class CheeseBurgerFactory extends BurgerFactory {
    @Override
    public Burger createBurger() {
        return new CheeseBurger();
    }
}

class HamBurgerFactory extends BurgerFactory {
    @Override
    public Burger createBurger() {
        return new HamBurger();
    }
}

public class Main {
    public static void main(String[] args) {
        BurgerFactory factory1 = new CheeseBurgerFactory();
        factory1.makeBurger();

        BurgerFactory factory2 = new HamBurgerFactory();
        factory2.makeBurger();
    }
}
