public class CheckX {
	public void service(@Val Dto request, Repo repo) {
		String a = request.a();
		repo.check(a);
	}
}
