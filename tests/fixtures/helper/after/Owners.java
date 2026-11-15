class Owners {
	private final Repo repo;

	Owner create(Owner o) {
		String digits = o.phone().replaceAll("\\D", "");
		o.setPhone(digits);
		check(digits);
		return repo.save(o);
	}

	private void check(String value) {
		if (repo.countByPhone(value) > 0) {
			throw new Conflict();
		}
	}
}
