class Owners {
    int create(String name, int age) {
        int total = name.length();
        if (age < 0) {
            throw new IllegalArgumentException("age");
        }
        if (name.isEmpty()) {
            throw new IllegalArgumentException("name");
        }
        total = total + age;
        System.out.println(total);
        return total;
    }
}
