class Owners {
	private final Repo repo;
	private final Audit audit;

	Owners(Repo repo, Audit audit) {
		this.repo = repo;
		this.audit = audit;
		repo.warm();
	}
}
