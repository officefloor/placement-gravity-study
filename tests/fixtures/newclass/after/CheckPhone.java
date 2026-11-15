public class CheckPhone {
	public void service(Owner o, Repo repo) {
		if (repo.countByPhone(o.phone()) > 0) {
			throw new Conflict();
		}
	}
}
