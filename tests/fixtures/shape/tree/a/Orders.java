package a;

import java.util.ArrayList;
import java.util.List;

public class Orders {

    private final List<String> log = new ArrayList<>();

    /** Junction: receives one value, hands on five on two calls to its own methods. */
    public void place(Order o) {
        check(o, 1);
        price(o, 2, 3);
        log.add(o.toString());
        Runnable r = new Runnable() {
            public void run() {
                check(o, 4);
            }
        };
        r.run();
    }

    void check(Order o, int level) {
        if (level > 0) {
            log.add("checked");
        }
    }

    void price(Order o, int a, int b) {
        log.add("priced " + (a + b));
    }

    /** Long and straight: every piece needs only n. */
    String report(int n) {
        log.add("line 1 " + n);
        log.add("line 2 " + n);
        log.add("line 3 " + n);
        log.add("line 4 " + n);
        log.add("line 5 " + n);
        log.add("line 6 " + n);
        log.add("line 7 " + n);
        log.add("line 8 " + n);
        log.add("line 9 " + n);
        log.add("line 10 " + n);
        log.add("line 11 " + n);
        log.add("line 12 " + n);
        log.add("line 13 " + n);
        log.add("line 14 " + n);
        log.add("line 15 " + n);
        log.add("line 16 " + n);
        log.add("line 17 " + n);
        log.add("line 18 " + n);
        log.add("line 19 " + n);
        log.add("line 20 " + n);
        log.add("line 21 " + n);
        log.add("line 22 " + n);
        log.add("line 23 " + n);
        log.add("line 24 " + n);
        log.add("line 25 " + n);
        log.add("line 26 " + n);
        log.add("line 27 " + n);
        log.add("line 28 " + n);
        return log.toString();
    }

    /** Long, every statement in one loop, with jumps out of the middle. */
    int scan(List<String> xs) {
        int total = 0;
        int seen = 0;
        String last = null;
        for (String x : xs) {
            if (x.startsWith("s1")) {
                total += 1;
                continue;
            }
            if (x.startsWith("s2")) {
                total += 2;
                continue;
            }
            if (x.startsWith("s3")) {
                total += 3;
                continue;
            }
            if (x.startsWith("s4")) {
                total += 4;
                continue;
            }
            if (x.startsWith("s5")) {
                total += 5;
                continue;
            }
            if (x.startsWith("s6")) {
                total += 6;
                continue;
            }
            if (x.startsWith("s7")) {
                total += 7;
                continue;
            }
            if (x.startsWith("s8")) {
                total += 8;
                continue;
            }
            seen++;
            last = x;
            if (seen > total) {
                return seen;
            }
        }
        return total + seen + (last == null ? 0 : 1);
    }
}
