class SetterInjected {
	private Repo repo;

	@Autowired
	void setRepo(Repo repo) {
		this.repo = repo;
	}

	void setterInjected(Owner o) {
		o.touch();
		repo.save(o);
	}
}
