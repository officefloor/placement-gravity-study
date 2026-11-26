@RestController
public class OwnerController implements OwnersApi {
	private final Repo repo;
	private int served;

	public OwnerController(Repo repo) {
		this.repo = repo;
	}

	@Override
	public Dto getOwner(Integer ownerId) {
		Dto found = repo.find(ownerId);
		return found;
	}

	@GetMapping("/owners")
	public Dto listOwners(String lastName) {
		Dto found = repo.byName(lastName);
		return found;
	}

	public Dto helper(String lastName) {
		Dto found = repo.byName(lastName);
		return found;
	}
}
