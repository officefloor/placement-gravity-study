@Service
@RequiredArgsConstructor
class Lombok {
	private final Repo repo;
	private int counter;

	void lombok(Owner o) {
		o.touch();
	}
}
