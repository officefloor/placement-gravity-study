import java.io.BufferedWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.TreeSet;

import org.codetracker.api.CodeTracker;
import org.codetracker.api.History;
import org.codetracker.api.MethodTracker;
import org.codetracker.change.Change;
import org.codetracker.element.Method;
import org.eclipse.jgit.lib.Repository;
import org.refactoringminer.util.GitServiceImpl;

/**
 * CodeTracker's history of each listed method (PLAN.md §4.4): the commits that changed it, back
 * from the start commit, through renames and moves of the method and its class.
 *
 * <pre>
 * java -cp target/classes:target/lib/* Histories REPO LISTING.tsv OUT.jsonl
 * </pre>
 *
 * LISTING.tsv: {@code id<TAB>startCommit<TAB>filePath<TAB>methodName<TAB>declarationLine} per line.
 * Output: one JSON line per method, {"id", "changes": [{"commit", "types": [...]}]} or an "error".
 */
public final class Histories {

	public static void main(String[] args) throws Exception {
		Repository repo = new GitServiceImpl().openRepository(args[0]);
		List<String> rows = Files.readAllLines(Path.of(args[1]), StandardCharsets.UTF_8);
		try (BufferedWriter w = Files.newBufferedWriter(Path.of(args[2]), StandardCharsets.UTF_8)) {
			for (String row : rows) {
				if (row.isBlank()) {
					continue;
				}
				String[] r = row.split("\t");
				StringBuilder b = new StringBuilder("{\"id\":").append(q(r[0]));
				try {
					MethodTracker t = CodeTracker.methodTracker().repository(repo).startCommitId(r[1]).filePath(r[2])
							.methodName(r[3]).methodDeclarationLineNumber(Integer.parseInt(r[4])).build();
					History<Method> h = t.track();
					b.append(",\"changes\":[");
					boolean first = true;
					for (History.HistoryInfo<Method> i : h.getHistoryInfoList()) {
						TreeSet<String> types = new TreeSet<>();
						for (Change c : i.getChangeList()) {
							types.add(c.getType().name());
						}
						b.append(first ? "" : ",").append("{\"commit\":").append(q(i.getCommitId())).append(",\"types\":[");
						boolean f2 = true;
						for (String ty : types) {
							b.append(f2 ? "" : ",").append(q(ty));
							f2 = false;
						}
						b.append("]}");
						first = false;
					}
					b.append(']');
				} catch (Exception | Error e) {
					b.append(",\"error\":").append(q(e.toString()));
				}
				w.write(b.append("}\n").toString());
			}
		}
	}

	static String q(String s) {
		return "\"" + s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", " ") + "\"";
	}
}
