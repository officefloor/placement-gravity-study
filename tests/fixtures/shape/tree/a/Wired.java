package a;

public class Wired {

    public void service(Order order, Orders orders) {
        orders.place(order);
    }

    private int helper(int x) {
        return x + 1;
    }
}
