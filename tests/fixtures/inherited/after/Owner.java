class Owner extends Person {
	String display() {
		String first = getFirstName();
		return first + lastName;
	}
}
