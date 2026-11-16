class Owners {
    int create(String name, int age) {
        int total = name.length();
        if (age < 0) {
            throw new IllegalArgumentException("age");
        }
        checkName(name);
        total = total + age * 2;
        System.out.println(total);
        return total;
    }

    void checkName(String name) {
        if (name.isEmpty()) {
            throw new IllegalArgumentException("name");
        }
    }
}
