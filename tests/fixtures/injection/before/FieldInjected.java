@Service
class FieldInjected {
	@Autowired
	private Repo repo;
	@Value("${limit}")
	private int limit;
	private final List<String> cache = new ArrayList<>();

	void fieldInjected(Owner o) {
		o.touch();
	}
}
