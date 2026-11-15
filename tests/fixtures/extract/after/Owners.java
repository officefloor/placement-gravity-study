class Owners {
	Owner create(Owner o) {
		o.setDisplayName(display(o));
		return o;
	}

	private String display(Owner o) {
		String first = o.firstName().strip();
		String last = o.lastName().strip();
		return last + ", " + first;
	}
}
