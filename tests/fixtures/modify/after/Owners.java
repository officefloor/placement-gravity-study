class Owners {
	String code(String last, int seq) {
		String prefix = last.substring(0, 3);
		String code = prefix.toUpperCase() + "-" + seq;
		return code;
	}
}
