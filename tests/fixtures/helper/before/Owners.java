class Owners {
	private final Repo repo;

	Owner create(Owner o) {
		String digits = o.phone().replaceAll("\\D", "");
		o.setPhone(digits);
		return repo.save(o);
	}
}
