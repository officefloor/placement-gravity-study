class Owners {
	Owner create(Owner o) {
		String first = o.firstName().strip();
		String last = o.lastName().strip();
		o.setDisplayName(last + ", " + first);
		return o;
	}
}
