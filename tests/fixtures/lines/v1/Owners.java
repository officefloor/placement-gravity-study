class Owners {
    int create(String name, int age) {
        int total = name.length();
        if (age < 0) {
            throw new IllegalArgumentException("age");
        }
        total = total + age;
        return total;
    }
}
