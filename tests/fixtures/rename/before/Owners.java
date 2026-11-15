class Owners {
	void count(Owner o) {
		int count = o.pets().size();
		o.setPets(count);
	}
}
