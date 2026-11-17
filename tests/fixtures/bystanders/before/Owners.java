import org.springframework.stereotype.Service;

@Service
class Owners {
    static final int LIMIT = 9;
    private final Repo repo;
    private final Clock clock;
    private int created;

    Owners(Repo repo, Clock clock) {
        this.repo = repo;
        this.clock = clock;
    }

    int create(String name, int age) {
        int total = name.length();
        if (age < 0) {
            String reason = "age";
            throw new IllegalArgumentException(reason);
        }
        int extra = 2;
        return total + extra;
    }
}
