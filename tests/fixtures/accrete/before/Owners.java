class Owners {
	private static final Logger LOG = Logger.get();
	private final Repo repo;
	private final Clock clock;

	Owner create(Owner o) {
		String phone = o.phone();
		String digits = phone.replaceAll("\\D", "");
		o.setPhone(digits);
		return repo.save(o);
	}
}
