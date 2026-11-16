@Service
class CtorInjected {
	private static final int MAX = 3;
	private final Repo repo;

	CtorInjected(Repo repo) {
		this.repo = repo;
	}

	void ctorInjected(Owner o) {
		o.touch();
	}
}
