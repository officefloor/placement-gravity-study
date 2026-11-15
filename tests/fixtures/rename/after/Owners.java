class Owners {
	void count(Owner o) {
		int total = o.pets().size();
		o.setPets(total);
		log(total);
	}
}
