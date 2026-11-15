class Codes {
	private static final int WIDTH = 3;

	String code(String last) {
		String prefix = last.substring(0, WIDTH);
		return prefix;
	}
}
