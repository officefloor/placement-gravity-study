class Owners {
	Owner create(Owner o) {
		String name = o.firstName();
		name = name.strip();
		o.setDisplayName(name);
		return o;
	}
}
