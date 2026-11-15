class Owners {
	private final Service service;

	void join(String last) {
		String key = last.strip();
		service.all().forEach(existing -> existing.setKey(key));
	}
}
