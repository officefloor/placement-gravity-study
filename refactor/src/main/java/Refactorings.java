import java.io.BufferedWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

import org.eclipse.jgit.lib.Repository;
import org.refactoringminer.api.Refactoring;
import org.refactoringminer.api.RefactoringHandler;
import org.refactoringminer.rm1.GitHistoryRefactoringMinerImpl;
import org.refactoringminer.util.GitServiceImpl;

/**
 * RefactoringMiner at each commit of a listing (PLAN.md §4.1): one JSON line per commit,
 * {"unit": ..., "commit": ..., "refactorings": [RefactoringMiner's own JSON, ...]} or an "error".
 *
 * <pre>
 * java -cp target/classes:target/lib/* Refactorings REPO LISTING.tsv OUT.jsonl
 * </pre>
 *
 * LISTING.tsv: {@code unit<TAB>commit} per line. A commit is compared with its first parent.
 */
public final class Refactorings {

	static final int TIMEOUT_SECONDS = 300;

	public static void main(String[] args) throws Exception {
		Repository repo = new GitServiceImpl().openRepository(args[0]);
		List<String> rows = Files.readAllLines(Path.of(args[1]), StandardCharsets.UTF_8);
		GitHistoryRefactoringMinerImpl miner = new GitHistoryRefactoringMinerImpl();
		try (BufferedWriter w = Files.newBufferedWriter(Path.of(args[2]), StandardCharsets.UTF_8)) {
			for (String row : rows) {
				if (row.isBlank()) {
					continue;
				}
				String[] r = row.split("\t");
				StringBuilder found = new StringBuilder();
				String[] error = { null };
				miner.detectAtCommit(repo, r[1], new RefactoringHandler() {
					@Override
					public void handle(String commitId, List<Refactoring> refactorings) {
						for (Refactoring ref : refactorings) {
							if (found.length() > 0) {
								found.append(',');
							}
							found.append(ref.toJSON().replace('\n', ' '));
						}
					}

					@Override
					public void handleException(String commit, Exception e) {
						error[0] = e.toString();
					}
				}, TIMEOUT_SECONDS);
				w.write("{\"unit\":\"" + r[0] + "\",\"commit\":\"" + r[1] + "\""
						+ (error[0] == null ? "" : ",\"error\":" + quote(error[0])) + ",\"refactorings\":[" + found
						+ "]}\n");
			}
		}
	}

	static String quote(String s) {
		return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", " ") + "\"";
	}
}
