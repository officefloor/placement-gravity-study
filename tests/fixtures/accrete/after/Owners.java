class Owners {
	private static final Logger LOG = Logger.get();
	private final Repo repo;
	private final Clock clock;
	private final Audit audit;

	Owner create(Owner o) {
		String phone = o.phone();
		String digits = phone.replaceAll("\\D", "");
		o.setPhone(digits);
		int n = repo.countByPhone(digits);
		if (n > 0) {
			throw new Conflict();
		}
		audit.log("created");
		LOG.info(digits);
		return repo.save(o);
	}
}
