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

interface Fries {
    void prepare();
}

class CountryFries implements Fries {
    @Override
    public void prepare() {
        System.out.println("Cooking coutnry fries");
    }
}

class FrenchFries implements Fries {
    @Override
    public void prepare() {
        System.out.println("Cooking french fries");
    }
}

interface FastFoodFactory {
    Burger createBurger();
    Fries createFries();
}

class Factory1 implements FastFoodFactory {
    @Override
    public Burger createBurger() {
        return new CheeseBurger();
    }

    @Override
    public Fries createFries() {
        return new FrenchFries();
    }
}

class Factory2 implements FastFoodFactory {
    @Override
    public Burger createBurger() {
        return new HamBurger();
    }

    @Override
    public Fries createFries() {
        return new CountryFries();
    }
}

public class FoodCourt {
    private Burger burger;
    private Fries fries;

    public FoodCourt(FastFoodFactory factory) {
        burger = factory.createBurger();
        fries = factory.createFries();
    }

    public void serveOrder() {
        burger.prepare();
        fries.prepare();
    }
}

public class Main {
    public static void main(String[] args) {
        FoodCourt order1 = new FoodCourt(new Factory1());
        order1.serveOrder();

        FoodCourt order2 = new FoodCourt(new Factory2());
        order2.serveOrder();
    }
}
