class Owners {
	private final Service service;

	void join(String last) {
		String key = last.strip();
		service.all().forEach(existing -> existing.setKey(key));
		service.all().stream().filter(other -> other.matches(key)).forEach(other -> other.mark());
	}
}
