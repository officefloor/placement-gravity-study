class Owners {
	Owner create(Owner o) {
		String name = o.firstName();
		o.setDisplayName(name);
		return o;
	}
}
