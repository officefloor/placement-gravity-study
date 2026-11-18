import org.springframework.stereotype.Service;

@Service
class Owners {
    static final int LIMIT = 9;
    private final Repo repo;
    private final Clock clock;
    private int created;
    private int audited;

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
        repo.check(name);
        int checked = name.length();
        int extra = 2;
        return total + extra;
    }

    int helper(int count) {
        return count + LIMIT;
    }

    int getCreated() {
        return created;
    }

    void setCreated(int created) {
        this.created = created;
    }

    int getAudited() {
        return audited + created;
    }

    int fresh(int count) {
        return count * 2;
    }
}
