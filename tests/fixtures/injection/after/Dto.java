class Dto {
	private final String name;

	Dto(String name) {
		this.name = name;
	}

	String dto(String suffix) {
		return name + suffix;
	}
}
