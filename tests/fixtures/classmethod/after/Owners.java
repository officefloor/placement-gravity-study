class Owners {
	Owner create(Owner o) {
		audit(o);
		return o;
	}

	void audit(Owner o) {
	}
}
