class Burger {
    private String bun;
    private String meat;
    private String sauce;
    private String topping;

    public void setBun(String bun) {
        this.bun = bun;
    }

    public void setMeat(String meat) {
        this.meat = meat;
    }

    public void setSauce(String sauce) {
        this.sauce = sauce;
    }

    public void setTopping(String topping) {
        this.topping = topping;
    }

    @Override
    public string toString() {
        return "Burger{" +
               "bun'" + bun + '\'' +
               ", meat='" + meat + '\'' +
cat > Builder.java << 'EOF'
class Burger {
    private String bun;
    private String meat;
    private String sauce;
    private String topping;

    public void setBun(String bun) {
        this.bun = bun;
    }

    public void setMeat(String meat) {
        this.meat = meat;
    }

    public void setSauce(String sauce) {
        this.sauce = sauce;
    }

    public void setTopping(String topping) {
        this.topping = topping;
    }

    @Override
    public string toString() {
        return "Burger{" +
               "bun='" + bun + '\'' +
               ", meat='" + meat + '\'' +
               ", sauce='" + sauce + '\'' +
               ", topping='" + topping + '\'' +
               '}';
    }
}

interface BurgerBuilder {
    void buildBun();
    void buildMeat();
    void buildSauce();
    void buildTopping();
    Burger getResult();
}

class CheeseBurgerBuilder implements BurgerBuilder {
    private Burger burger;

    public CheeseBurgerBuilder() {
        this.burger = new Burger();
    }

    @Override
    public void buildBun() {
        burger.setBun("regular bun");
    }

    @Override
    public void buildMeat() {
        burger.setMeat("beef");

cat > Builder.java << 'EOF'
class Burger {
    private String bun;
    private String meat;
    private String sauce;
    private String topping;

    public void setBun(String bun) {
        this.bun = bun;
    }

    public void setMeat(String meat) {
        this.meat = meat;
    }

    public void setSauce(String sauce) {
        this.sauce = sauce;
    }

    public void setTopping(String topping) {
        this.topping = topping;
    }

    @Override
    public string toString() {
        return "Burger{" +
               "bun'" + bun + '\'' +
               ", meat='" + meat + '\'' +
cat > Builder.java << 'EOF'
class Burger {
    private String bun;
    private String meat;
    private String sauce;
    private String topping;

    public void setBun(String bun) {
        this.bun = bun;
    }

    public void setMeat(String meat) {
        this.meat = meat;
    }

    public void setSauce(String sauce) {
        this.sauce = sauce;
    }

    public void setTopping(String topping) {
        this.topping = topping;
    }

    @Override
    public string toString() {
        return "Burger{" +
               "bun='" + bun + '\'' +
               ", meat='" + meat + '\'' +
               ", sauce='" + sauce + '\'' +
               ", topping='" + topping + '\'' +
               '}';
    }
}

interface BurgerBuilder {
    void buildBun();
    void buildMeat();
    void buildSauce();
    void buildTopping();
    Burger getResult();
}

class CheeseBurgerBuilder implements BurgerBuilder {
    private Burger burger;

    public CheeseBurgerBuilder() {
        this.burger = new Burger();
    }

    @Override
    public void buildBun() {
        burger.setBun("regular bun");
    }

    @Override
    public void buildMeat() {
}

interface BurgerBuilder {
    void buildBun();
    void buildMeat();
    void buildSauce();
    void buildTopping();
    Burger getResult();
}

class CheeseBurgerBuilder implements BurgerBuilder {
    private Burger burger;

    public CheeseBurgerBuilder() {
        this.burger = new Burger();
    }

    @Override
    public void buildBun() {
        burger.setBun("regular");
    }

    @Override
    public void buildMeat() {
        burger.setMeat("beef");
    }

    @Override
    public void buildSauce() {
        burger.setSauce("ketchup");
    }

    @Override
    public void buildTopping() {
        burger.setTopping("cheese");
    }

    @Override
    public Burger getResult() {
        return burger;
    }
}

class BurgerDirector {
    private BurgerBuilder builder;

    public BurgerDirector(BurgerBuilder builder) {
        this.builder = builder;
    }

    public void constructBurger() {
        builder.buildBun();
        builder.buildMeat();
        builder.buildSauce();
        builder.buildTopping();
    }
}

public class Main {
    public static void main(String[] args) {
        BurgerBuilder builder = new CheeseBurgerBuilder();
        BurgerDirector director = new BurgerDirector(builder);

        director.constructBurger();
        Burger burger = builder.getResult();

        System.out.println(burger);
    }
}
