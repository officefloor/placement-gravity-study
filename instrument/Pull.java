import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.github.javaparser.JavaParser;
import com.github.javaparser.JavaToken;
import com.github.javaparser.ParseResult;
import com.github.javaparser.ParserConfiguration;
import com.github.javaparser.ParserConfiguration.LanguageLevel;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.BodyDeclaration;
import com.github.javaparser.ast.body.CallableDeclaration;
import com.github.javaparser.ast.body.CompactConstructorDeclaration;
import com.github.javaparser.ast.body.FieldDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.body.TypeDeclaration;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.ObjectCreationExpr;
import com.github.javaparser.ast.expr.ThisExpr;
import com.github.javaparser.printer.DefaultPrettyPrinter;
import com.github.javaparser.printer.configuration.DefaultConfigurationOption;
import com.github.javaparser.printer.configuration.DefaultPrinterConfiguration;
import com.github.javaparser.printer.configuration.DefaultPrinterConfiguration.ConfigOption;

import net.officefloor.sinewslim.core.Assessment;
import net.officefloor.sinewslim.core.Assessor;
import net.officefloor.sinewslim.facts.MethodIndex;
import net.officefloor.sinewslim.facts.Seam;
import net.officefloor.sinewslim.facts.Var;
import net.officefloor.sinewslim.javaparser.JavaFacts;
import net.officefloor.sinewslim.javaparser.MethodUnit;
import net.officefloor.sinewslim.javaparser.ParsedFile;

/**
 * The pull instrument (PLAN.md §4). For each addition (one checkpoint's change) it reads the before
 * and after version of every changed Java file and writes, per host method, the code added for the
 * new problem and the <b>ties</b> that code has to its location: the data it uses that existed
 * before the change and that it could not have had anywhere else without threading it there.
 *
 * <ul>
 * <li><b>Method ties</b>: the host method's own parameters and locals. A parameter the framework
 * injects (a public method of an OfficeFloor function, see {@code injected}) does not tie: a function
 * placed anywhere can declare it.</li>
 * <li><b>Class ties</b>: the host class's fields and methods.</li>
 * </ul>
 *
 * Only the added code's own references count: for a pure insertion every token of the run, for an
 * edited line only the tokens the edit introduced (a token-level diff against the lines it replaces).
 * Refactoring is set apart with RefactoringMiner's findings, passed as hints: renames are applied to
 * the before version first, moved and restructured code is not an addition, and renamed, moved or
 * re-signatured methods stay matched.
 *
 * <pre>
 * java -cp lib/officefloorslim.jar:instrument/classes Pull MANIFEST.tsv HINTS.tsv OUT.jsonl
 * java -cp lib/officefloorslim.jar:instrument/classes Pull --amount LISTING.tsv OUT.jsonl
 * java -cp lib/officefloorslim.jar:instrument/classes Pull --shape LISTING.tsv OUT.jsonl
 * </pre>
 *
 * MANIFEST.tsv: {@code unit<TAB>path<TAB>before<TAB>after} per changed file ("-" for none).
 * HINTS.tsv ("-" for none), per line {@code unit<TAB>kind<TAB>...}:
 * <ul>
 * <li>{@code method bPath bLine aPath aLine}: the before method containing bLine is the after method
 * containing aLine (original source lines);</li>
 * <li>{@code type bPath bLine aPath aLine}: likewise for a type;</li>
 * <li>{@code rename scope aPath aLine old new}: scope {@code value} (in the after method containing
 * aLine), {@code field} (in aPath) or {@code member} (a method or type, everywhere);</li>
 * <li>{@code moved aPath from to}: after lines holding moved or restructured code;</li>
 * <li>{@code injected Type}: the public methods of this type are wired functions whose parameters
 * are injected.</li>
 * </ul>
 * Positions follow the width harness (long-method-slim-study, width/README.md): the source is
 * pretty-printed without comments and a position is a printed body line holding a token other than
 * a brace, a semicolon or a bare else, try, finally or do, outside nested types.
 */
public final class Pull {

	/** Bump whenever a field's meaning changes. */
	static final int VERSION = 4;

	/** A removed position's text must be at least this long to mark an added one as moved. */
	static final int MOVED_MIN_CHARS = 12;

	static final LanguageLevel[] LEVELS = { LanguageLevel.JAVA_25, LanguageLevel.JAVA_8 };

	public static void main(String[] args) throws Exception {
		if (args[0].equals("--amount")) {
			amount(Path.of(args[1]), Path.of(args[2]));
			return;
		}
		if (args[0].equals("--shape")) {
			shape(Path.of(args[1]), Path.of(args[2]));
			return;
		}
		if (args[0].equals("--methods")) {
			methods(Path.of(args[1]), Path.of(args[2]));
			return;
		}
		Map<String, List<String[]>> units = new LinkedHashMap<>();
		for (String[] r : rows(Path.of(args[0]))) {
			units.computeIfAbsent(r[0], k -> new ArrayList<>()).add(r);
		}
		Map<String, List<String[]>> hints = new HashMap<>();
		if (!args[1].equals("-")) {
			for (String[] r : rows(Path.of(args[1]))) {
				hints.computeIfAbsent(r[0], k -> new ArrayList<>()).add(r);
			}
		}
		try (BufferedWriter w = Files.newBufferedWriter(Path.of(args[2]), StandardCharsets.UTF_8)) {
			for (Map.Entry<String, List<String[]>> u : units.entrySet()) {
				for (String line : new Unit(u.getKey(), u.getValue(), hints.getOrDefault(u.getKey(), List.of()))
						.measure()) {
					w.write(line);
					w.write('\n');
				}
			}
		}
	}

	static List<String[]> rows(Path p) throws IOException {
		List<String[]> out = new ArrayList<>();
		for (String l : Files.readAllLines(p, StandardCharsets.UTF_8)) {
			if (!l.isBlank()) {
				out.add(l.split("\t", -1));
			}
		}
		return out;
	}

	// ----------------------------------------------------------------------------------------
	// what is read from a file
	// ----------------------------------------------------------------------------------------

	record Tok(int line, int col, String text, boolean ident) {
	}

	/** A type: its fields and the names of its methods. */
	record T(String file, String name, int origLine, Set<String> fields, Set<String> utilities, Set<String> methods) {
	}

	/** A method as measured, on the printed source. */
	record M(String file, String type, String name, String signature, MethodUnit unit, Node node, int[] lines,
			String[] texts, List<List<Tok>> toks, int[] origLines, int origDecl, int origEnd, T owner) {

		String key() {
			return type + "#" + signature;
		}

		boolean containsOrig(int line) {
			return origDecl <= line && line <= origEnd;
		}
	}

	record F(List<M> methods, List<T> types) {
	}

	// ----------------------------------------------------------------------------------------
	// one addition
	// ----------------------------------------------------------------------------------------

	static final class Unit {
		final String unit;
		final List<String[]> files, hints;
		final List<String> out = new ArrayList<>();
		final List<M> before = new ArrayList<>(), after = new ArrayList<>();
		final List<T> typesBefore = new ArrayList<>(), typesAfter = new ArrayList<>();
		final Set<String> injected = new HashSet<>();
		final Map<M, M> match = new IdentityHashMap<>();
		final Map<T, T> typeMatch = new IdentityHashMap<>();
		final Map<String, int[][]> moved = new HashMap<>();
		final Map<M, boolean[]> addedOf = new IdentityHashMap<>();
		final Map<M, int[]> pairOf = new IdentityHashMap<>();

		Unit(String unit, List<String[]> files, List<String[]> hints) {
			this.unit = unit;
			this.files = files;
			this.hints = hints;
		}

		List<String> measure() {
			for (String[] r : files) {
				try {
					if (!r[2].equals("-")) {
						F f = file(r[1], Path.of(r[2]), out, unit);
						before.addAll(f.methods);
						typesBefore.addAll(f.types);
					}
					if (!r[3].equals("-")) {
						F f = file(r[1], Path.of(r[3]), out, unit);
						after.addAll(f.methods);
						typesAfter.addAll(f.types);
					}
				} catch (IOException e) {
					out.add(problem(unit, r[1], "unreadable: " + e.getMessage()));
				}
			}
			for (String[] h : hints) {
				switch (h[1]) {
				case "injected" -> injected.add(h[2]);
				case "moved" -> {
					int[][] old = moved.getOrDefault(h[2], new int[0][]);
					int[][] grown = Arrays.copyOf(old, old.length + 1);
					grown[old.length] = new int[] { Integer.parseInt(h[3]), Integer.parseInt(h[4]) };
					moved.put(h[2], grown);
				}
				default -> {
				}
				}
			}
			matchTypes();
			matchMethods();
			diff();
			for (M b : before) {
				if (!match.containsValue(b)) {
					out.add(removedHost(unit, b));
				}
			}
			for (M m : after) {
				String h = host(m);
				if (h != null) {
					out.add(h);
				}
			}
			return out;
		}

		// ---- matching ----

		void matchTypes() {
			for (String[] h : hints) {
				if (h[1].equals("type")) {
					T b = typeAt(typesBefore, h[2], Integer.parseInt(h[3]));
					T a = typeAt(typesAfter, h[4], Integer.parseInt(h[5]));
					if (a != null && b != null && !typeMatch.containsKey(a)) {
						typeMatch.put(a, b);
					}
				}
			}
			for (T a : typesAfter) {
				if (typeMatch.containsKey(a)) {
					continue;
				}
				for (T b : typesBefore) {
					if (b.name.equals(a.name) && !typeMatch.containsValue(b)) {
						typeMatch.put(a, b);
						break;
					}
				}
			}
		}

		/** The type of the file declared nearest the line (RefactoringMiner's start line may include
		 * the javadoc or annotations above the declaration). */
		static T typeAt(List<T> ts, String file, int line) {
			T best = null;
			for (T t : ts) {
				if (t.file.equals(file) && (best == null || Math.abs(t.origLine - line) < Math.abs(best.origLine - line))) {
					best = t;
				}
			}
			return best;
		}

		String beforeTypeName(M m) {
			T b = m.owner == null ? null : typeMatch.get(m.owner);
			return b == null ? m.type : b.name;
		}

		void matchMethods() {
			for (String[] h : hints) {
				if (h[1].equals("method")) {
					M b = methodAt(before, h[2], Integer.parseInt(h[3]));
					M a = methodAt(after, h[4], Integer.parseInt(h[5]));
					if (a != null && b != null && !match.containsKey(a) && !match.containsValue(b)) {
						match.put(a, b);
					}
				}
			}
			Map<String, M> byKey = new HashMap<>();
			Map<String, List<M>> byName = new HashMap<>(), afterByName = new HashMap<>();
			for (M b : before) {
				byKey.put(b.key(), b);
				byName.computeIfAbsent(b.type + "#" + b.name, k -> new ArrayList<>()).add(b);
			}
			for (M m : after) {
				afterByName.computeIfAbsent(beforeTypeName(m) + "#" + m.name, k -> new ArrayList<>()).add(m);
			}
			for (M m : after) {
				if (match.containsKey(m)) {
					continue;
				}
				String type = beforeTypeName(m);
				M b = byKey.get(type + "#" + m.signature);
				if (b == null) {
					List<M> cands = byName.get(type + "#" + m.name);
					if (cands != null && cands.size() == 1 && afterByName.get(type + "#" + m.name).size() == 1) {
						b = cands.get(0);
					}
				}
				if (b != null && !match.containsValue(b)) {
					match.put(m, b);
				}
			}
		}

		static M methodAt(List<M> ms, String file, int line) {
			M best = null;
			for (M m : ms) {
				if (m.file.equals(file) && m.containsOrig(line)
						&& (best == null || m.origEnd - m.origDecl < best.origEnd - best.origDecl)) {
					best = m;
				}
			}
			return best;
		}

		// ---- renames ----

		/** old name -> new name, for the before version of after-method m. */
		Map<String, String> renamesFor(M m) {
			Map<String, String> r = new HashMap<>();
			for (String[] h : hints) {
				if (!h[1].equals("rename")) {
					continue;
				}
				String scope = h[2], path = h[3];
				int line = Integer.parseInt(h[4]);
				boolean applies = switch (scope) {
				case "value" -> path.equals(m.file) && m.containsOrig(line);
				case "field" -> path.equals(m.file);
				default -> true;
				};
				if (applies) {
					r.put(h[5], h[6]);
				}
			}
			return r;
		}

		static String renameText(String text, Map<String, String> renames) {
			for (Map.Entry<String, String> e : renames.entrySet()) {
				text = text.replaceAll("\\b" + Pattern.quote(e.getKey()) + "\\b", Matcher.quoteReplacement(e.getValue()));
			}
			return text;
		}

		// ---- positions: added, moved ----

		void diff() {
			Map<String, Integer> removedTexts = new HashMap<>();
			for (M m : after) {
				M b = match.get(m);
				boolean[] a = new boolean[m.lines.length];
				if (b == null) {
					Arrays.fill(a, true);
				} else {
					Map<String, String> ren = renamesFor(m);
					String[] bt = new String[b.texts.length];
					for (int i = 0; i < bt.length; i++) {
						bt[i] = renameText(b.texts[i], ren);
					}
					boolean[] keptAfter = new boolean[m.lines.length], keptBefore = new boolean[b.lines.length];
					pairOf.put(m, lcs(bt, m.texts, keptBefore, keptAfter));
					for (int i = 0; i < a.length; i++) {
						a[i] = !keptAfter[i];
					}
					for (int i = 0; i < b.lines.length; i++) {
						if (!keptBefore[i]) {
							removedTexts.merge(b.texts[i], 1, Integer::sum);
						}
					}
				}
				addedOf.put(m, a);
			}
			for (M b : before) {
				if (!match.containsValue(b)) {
					for (String t : b.texts) {
						removedTexts.merge(t, 1, Integer::sum);
					}
				}
			}
			this.removedTexts = removedTexts;
		}

		Map<String, Integer> removedTexts;

		/** 0: an addition; 1: moved by RefactoringMiner's finding; 2: moved by identical text. */
		int[] movedKind(M m, boolean[] a) {
			int[] k = new int[a.length];
			int[][] ranges = moved.getOrDefault(m.file, new int[0][]);
			for (int i = 0; i < a.length; i++) {
				if (!a[i]) {
					continue;
				}
				for (int[] r : ranges) {
					if (r[0] <= m.origLines[i] && m.origLines[i] <= r[1]) {
						k[i] = 1;
						break;
					}
				}
				if (k[i] == 0 && m.texts[i].length() >= MOVED_MIN_CHARS
						&& removedTexts.getOrDefault(m.texts[i], 0) > 0) {
					k[i] = 2;
					removedTexts.merge(m.texts[i], -1, Integer::sum);
				}
			}
			return k;
		}

		// ---- one host ----

		String host(M m) {
			M b = match.get(m);
			boolean[] a = addedOf.get(m);
			int[] mk = movedKind(m, a);
			int nAdded = 0, nMovedRm = 0, nMovedText = 0;
			for (int i = 0; i < a.length; i++) {
				if (a[i]) {
					nAdded++;
					nMovedRm += mk[i] == 1 ? 1 : 0;
					nMovedText += mk[i] == 2 ? 1 : 0;
				}
			}
			int removed = b == null ? 0 : b.lines.length - (m.lines.length - nAdded);
			if (b != null && nAdded == 0 && removed == 0) {
				return null; // unchanged host
			}
			boolean isNew = b == null;
			T bt = m.owner == null ? null : typeMatch.get(m.owner);
			Map<String, String> ren = renamesFor(m);
			Set<String> preFields = renamed(bt == null ? Set.of() : bt.fields, ren);
			Set<String> preUtilities = renamed(bt == null ? Set.of() : bt.utilities, ren);
			Set<String> preMethods = renamed(bt == null ? Set.of() : bt.methods, ren);
			preMethods.remove(m.name);
			Set<String> knownNames = new HashSet<>(preFields);
			knownNames.addAll(preUtilities);
			Set<String> knownMethods = new HashSet<>(preMethods);
			knownMethods.add(m.name);
			if (m.owner != null) {
				knownNames.addAll(m.owner.fields);
				knownNames.addAll(m.owner.utilities);
				knownMethods.addAll(m.owner.methods);
			}
			boolean[] organisation = organisation(m, preFields);
			Set<String> values = isNew ? Set.of() : methodValues(m, b, a, ren);
			Set<String> ownVars = new HashSet<>();
			for (Var v : m.unit.facts().vars()) {
				if (v.kind() != Var.Kind.FIELD) {
					ownVars.add(v.name());
				}
			}

			StringBuilder s = new StringBuilder(512);
			s.append("{\"v\":").append(VERSION).append(",\"kind\":\"host\"");
			s.append(",\"unit\":").append(q(unit));
			s.append(",\"path\":").append(q(m.file));
			s.append(",\"type\":").append(q(m.type));
			s.append(",\"name\":").append(q(m.name));
			s.append(",\"signature\":").append(q(m.signature));
			s.append(",\"before_type\":").append(isNew ? "null" : q(b.type));
			s.append(",\"before_name\":").append(isNew ? "null" : q(b.name));
			s.append(",\"before_path\":").append(isNew ? "null" : q(b.file));
			s.append(",\"before_signature\":").append(isNew ? "null" : q(b.signature));
			s.append(",\"host_new\":").append(isNew);
			s.append(",\"class_new\":").append(bt == null);
			s.append(",\"injected\":").append(isInjected(m));
			s.append(",\"pre_positions\":").append(isNew ? 0 : b.lines.length);
			s.append(",\"post_positions\":").append(m.lines.length);
			s.append(",\"added\":").append(nAdded);
			s.append(",\"moved_rm\":").append(nMovedRm);
			s.append(",\"moved_text\":").append(nMovedText);
			s.append(",\"removed\":").append(removed);
			s.append(",\"params\":").append(paramCount(m.signature));

			// runs of added logic: added positions that are neither moved nor organisation
			int nOrganisation = 0;
			for (int i = 0; i < a.length; i++) {
				if (a[i] && mk[i] == 0 && organisation[i]) {
					mk[i] = 3;
					nOrganisation++;
				}
			}
			s.append(",\"organisation\":").append(nOrganisation);
			List<int[]> runs = new ArrayList<>();
			for (int i = 0; i < a.length;) {
				if (a[i] && mk[i] == 0) {
					int j = i;
					while (j + 1 < a.length && a[j + 1] && mk[j + 1] == 0) {
						j++;
					}
					runs.add(new int[] { i, j });
					i = j + 1;
				} else {
					i++;
				}
			}
			MethodIndex index = new MethodIndex(m.unit.facts(), false);
			s.append(",\"runs\":[");
			for (int r = 0; r < runs.size(); r++) {
				int from = runs.get(r)[0], to = runs.get(r)[1];
				int[] rep = isNew ? new int[] { -1, -1 } : replaced(pairOf.get(m), b.lines.length, from, to);
				int replaces = isNew ? 0 : Math.max(0, rep[1] - rep[0] - 1);
				Set<Long> addedTokens = addedTokens(m, b, from, to, rep, replaces, ren);
				Set<Long> lineTokens = new HashSet<>();
				for (int i = from; i <= to; i++) {
					m.toks.get(i).forEach(t -> lineTokens.add(pos(t)));
				}
				// primary: every reference of the run's logic lines (new and edited lines alike)
				Set<String> tm = new TreeSet<>(), tf = new TreeSet<>(), tc = new TreeSet<>(), tu = new TreeSet<>();
				ties(m, from, to, lineTokens, values, ownVars, preFields, preMethods, tm, tf, tc);
				ties(m, from, to, lineTokens, Set.of(), ownVars, preUtilities, Set.of(), new TreeSet<>(), tu,
						new TreeSet<>());
				// secondary: only the references the edit itself introduced
				Set<String> km = new TreeSet<>(), kf = new TreeSet<>(), kc = new TreeSet<>();
				ties(m, from, to, addedTokens, values, ownVars, preFields, preMethods, km, kf, kc);
				// references that resolve to nothing seen: inherited members, static imports
				Set<String> un = unresolved(m, from, to, ownVars, knownNames, knownMethods);
				Seam seam = index.seam(m.lines[from], m.lines[to]);
				if (r > 0) {
					s.append(',');
				}
				s.append("{\"from\":").append(from).append(",\"to\":").append(to);
				s.append(",\"positions\":").append(to - from + 1);
				s.append(",\"replaces\":").append(replaces);
				s.append(",\"added_tokens\":").append(addedTokens.size());
				s.append(",\"inputs\":").append(seam.inputs().size());
				s.append(",\"outputs\":").append(seam.outputs().size());
				s.append(",\"tie_method\":").append(strs(tm));
				Set<String> tp = new TreeSet<>(tm);
				tp.retainAll(params(m));
				s.append(",\"tie_param\":").append(strs(tp));
				s.append(",\"tie_field\":").append(strs(tf));
				s.append(",\"tie_class_method\":").append(strs(tc));
				s.append(",\"utility\":").append(strs(tu));
				s.append(",\"tok_tie_method\":").append(km.size());
				s.append(",\"tok_tie_class\":").append(kf.size() + kc.size());
				s.append(",\"unresolved\":").append(strs(un));
				s.append('}');
			}
			s.append(']');
			if (isNew) {
				s.append(",\"birth_tie\":").append(strs(birthTies(m)));
			}
			s.append('}');
			return s.toString();
		}

		/**
		 * Organisation lines: in a constructor, a statement that only assigns one of its parameters to a
		 * field ({@code this.repo = repo;}), the wiring of an injected dependency.
		 */
		static boolean[] organisation(M m, Set<String> preFields) {
			boolean[] out = new boolean[m.lines.length];
			if (!(m.node instanceof com.github.javaparser.ast.body.ConstructorDeclaration cd)) {
				return out;
			}
			Set<String> params = params(m);
			for (com.github.javaparser.ast.stmt.ExpressionStmt es : cd.findAll(com.github.javaparser.ast.stmt.ExpressionStmt.class)) {
				if (!(es.getExpression() instanceof com.github.javaparser.ast.expr.AssignExpr ae)
						|| ae.getOperator() != com.github.javaparser.ast.expr.AssignExpr.Operator.ASSIGN
						|| !(ae.getValue() instanceof NameExpr v) || !params.contains(v.getNameAsString())) {
					continue;
				}
				boolean toField = ae.getTarget() instanceof FieldAccessExpr fa && fa.getScope() instanceof ThisExpr
						|| ae.getTarget() instanceof NameExpr t && !params.contains(t.getNameAsString());
				int line = es.getBegin().map(p -> p.line).orElse(-1);
				int i = Arrays.binarySearch(m.lines, line);
				if (toField && i >= 0) {
					out[i] = true;
				}
			}
			return out;
		}

		/**
		 * Unqualified calls and lower-case names in the run that resolve to no local, parameter, field or
		 * method of the class before or after: members inherited from a superclass, or static imports.
		 */
		static Set<String> unresolved(M m, int from, int to, Set<String> ownVars, Set<String> names,
				Set<String> methods) {
			Set<String> out = new TreeSet<>();
			int lo = m.lines[from], hi = m.lines[to];
			for (Node n : m.node.findAll(Node.class)) {
				int line = n.getBegin().map(p -> p.line).orElse(-1);
				if (line < lo || line > hi) {
					continue;
				}
				if (n instanceof MethodCallExpr mc && (mc.getScope().isEmpty() || mc.getScope().get() instanceof ThisExpr)
						&& !methods.contains(mc.getNameAsString())) {
					out.add(mc.getNameAsString() + "()");
				} else if (n instanceof NameExpr ne) {
					String x = ne.getNameAsString();
					if (Character.isLowerCase(x.charAt(0)) && !ownVars.contains(x) && !names.contains(x)
							&& !PACKAGE_ROOTS.contains(x)) {
						out.add(x);
					}
				}
			}
			return out;
		}

		/** The first segment of a fully qualified name written in code, which is not a member. */
		static final Set<String> PACKAGE_ROOTS = Set.of("java", "javax", "jakarta", "org", "com", "net", "io");

		static Set<String> renamed(Set<String> names, Map<String, String> ren) {
			Set<String> out = new HashSet<>();
			for (String n : names) {
				out.add(ren.getOrDefault(n, n));
			}
			return out;
		}

		boolean isInjected(M m) {
			String simple = m.type.substring(m.type.lastIndexOf('.') + 1);
			return injected.contains(simple) && m.node instanceof MethodDeclaration md && md.isPublic();
		}

		/**
		 * The host method's values that existed before the change and tie code to it: parameters (not
		 * injected ones) and locals whose declaration is not itself added. Renames are followed.
		 */
		Set<String> methodValues(M m, M b, boolean[] added, Map<String, String> ren) {
			Set<String> declared = params(m), declaredBefore = renamed(params(b), ren);
			Set<String> was = new HashSet<>();
			for (Var v : b.unit.facts().vars()) {
				if (v.kind() != Var.Kind.FIELD) {
					was.add(ren.getOrDefault(v.name(), v.name()));
				}
			}
			boolean injectedHere = isInjected(m);
			Set<String> out = new HashSet<>();
			for (Var v : m.unit.facts().vars()) {
				if (v.kind() == Var.Kind.FIELD || !was.contains(v.name())) {
					continue;
				}
				boolean param = declared.contains(v.name());
				if (param != declaredBefore.contains(v.name())) {
					continue; // became a parameter or stopped being one: not the same value
				}
				if (param && injectedHere) {
					continue; // injected: a function anywhere could declare it
				}
				if (!param && added != null) {
					int p = Arrays.binarySearch(m.lines, v.first());
					if (p >= 0 && added[p]) {
						continue;
					}
				}
				out.add(v.name());
			}
			return out;
		}

		static Set<String> params(M m) {
			Set<String> out = new HashSet<>();
			if (m.node instanceof CallableDeclaration<?> cd) {
				cd.getParameters().forEach(p -> out.add(p.getNameAsString()));
			}
			return out;
		}

		/** The before indices of the kept positions either side of the run: replaced is between. */
		static int[] replaced(int[] pairOf, int beforeLength, int from, int to) {
			int lo = -1, hi = beforeLength;
			for (int k = from - 1; k >= 0; k--) {
				if (pairOf[k] >= 0) {
					lo = pairOf[k];
					break;
				}
			}
			for (int k = to + 1; k < pairOf.length; k++) {
				if (pairOf[k] >= 0) {
					hi = pairOf[k];
					break;
				}
			}
			return new int[] { lo, hi };
		}

		/** The tokens the run adds: all of them for an insertion; for an edit, those not in the replaced lines. */
		static Set<Long> addedTokens(M m, M b, int from, int to, int[] rep, int replaces, Map<String, String> ren) {
			List<Tok> at = new ArrayList<>();
			for (int i = from; i <= to; i++) {
				at.addAll(m.toks.get(i));
			}
			Set<Long> out = new HashSet<>();
			if (replaces == 0) {
				for (Tok t : at) {
					out.add(pos(t));
				}
				return out;
			}
			List<String> bt = new ArrayList<>();
			for (int i = rep[0] + 1; i < rep[1]; i++) {
				for (Tok t : b.toks.get(i)) {
					bt.add(t.ident ? ren.getOrDefault(t.text, t.text) : t.text);
				}
			}
			String[] as = at.stream().map(Tok::text).toArray(String[]::new);
			boolean[] keptA = new boolean[as.length];
			lcs(bt.toArray(String[]::new), as, new boolean[bt.size()], keptA);
			for (int i = 0; i < as.length; i++) {
				if (!keptA[i]) {
					out.add(pos(at.get(i)));
				}
			}
			return out;
		}

		static long pos(Tok t) {
			return ((long) t.line << 20) | t.col;
		}

		static long pos(Node n) {
			return n.getBegin().map(p -> ((long) p.line << 20) | p.column).orElse(-1L);
		}

		/**
		 * The references the run's added code makes to pre-existing method values, fields and methods.
		 * A value is used by added code when its own token is added, or when the expression directly
		 * applied to it is (an added call on it, an added operator beside it).
		 */
		static void ties(M m, int from, int to, Set<Long> addedTokens, Set<String> values, Set<String> ownVars,
				Set<String> fields, Set<String> methods, Set<String> tm, Set<String> tf, Set<String> tc) {
			int lo = m.lines[from], hi = m.lines[to];
			List<Tok> runToks = new ArrayList<>();
			for (int i = from; i <= to; i++) {
				runToks.addAll(m.toks.get(i));
			}
			for (Node n : m.node.findAll(Node.class)) {
				int line = n.getBegin().map(p -> p.line).orElse(-1);
				if (line < lo || line > hi) {
					continue;
				}
				if (n instanceof NameExpr ne) {
					if (!addedTokens.contains(pos(ne.getName())) && !parentAdded(ne, addedTokens, runToks)) {
						continue;
					}
					String name = ne.getNameAsString();
					if (values.contains(name)) {
						tm.add(name);
					} else if (!ownVars.contains(name) && fields.contains(name)) {
						tf.add(name);
					}
				} else if (n instanceof FieldAccessExpr fa && fa.getScope() instanceof ThisExpr
						&& fields.contains(fa.getNameAsString())
						&& (addedTokens.contains(pos(fa.getName())) || parentAdded(fa, addedTokens, runToks))) {
					tf.add(fa.getNameAsString());
				} else if (n instanceof MethodCallExpr mc
						&& (mc.getScope().isEmpty() || mc.getScope().get() instanceof ThisExpr)
						&& addedTokens.contains(pos(mc.getName())) && methods.contains(mc.getNameAsString())) {
					tc.add(mc.getNameAsString());
				}
			}
		}

		/** Whether the parent of n has an added token of its own (not inside one of its children). */
		static boolean parentAdded(Node n, Set<Long> addedTokens, List<Tok> runToks) {
			Node p = n.getParentNode().orElse(null);
			if (p == null || p instanceof com.github.javaparser.ast.stmt.Statement
					|| p instanceof com.github.javaparser.ast.body.VariableDeclarator) {
				return false; // a statement or declaration is not an expression applied to the value
			}
			for (Tok t : runToks) {
				if (!addedTokens.contains(pos(t)) || !within(p, t)) {
					continue;
				}
				boolean inChild = false;
				for (Node c : p.getChildNodes()) {
					if (within(c, t)) {
						inChild = true;
						break;
					}
				}
				if (!inChild) {
					return true;
				}
			}
			return false;
		}

		static boolean within(Node n, Tok t) {
			if (n.getBegin().isEmpty() || n.getEnd().isEmpty()) {
				return false;
			}
			var b = n.getBegin().get();
			var e = n.getEnd().get();
			boolean afterBegin = t.line > b.line || (t.line == b.line && t.col >= b.column);
			boolean beforeEnd = t.line < e.line || (t.line == e.line && t.col <= e.column);
			return afterBegin && beforeEnd;
		}

		/** A new method is tied at birth to its existing callers by the existing values passed to it. */
		Set<String> birthTies(M m) {
			Set<String> bound = new TreeSet<>();
			for (Map.Entry<M, M> e : match.entrySet()) {
				M caller = e.getKey();
				if (!caller.file.equals(m.file)) {
					continue;
				}
				Set<String> callerValues = methodValues(caller, e.getValue(), null, renamesFor(caller));
				for (MethodCallExpr call : caller.node.findAll(MethodCallExpr.class)) {
					if (!call.getNameAsString().equals(m.name) || call.getArguments().size() != paramCount(m.signature)
							|| (call.getScope().isPresent() && !(call.getScope().get() instanceof ThisExpr))) {
						continue;
					}
					for (Expression arg : call.getArguments()) {
						if (arg instanceof NameExpr n && callerValues.contains(n.getNameAsString())) {
							bound.add(caller.name + ":" + n.getNameAsString());
						}
					}
				}
			}
			return bound;
		}
	}

	static String removedHost(String unit, M b) {
		return "{\"v\":" + VERSION + ",\"kind\":\"removed\",\"unit\":" + q(unit) + ",\"path\":" + q(b.file)
				+ ",\"type\":" + q(b.type) + ",\"name\":" + q(b.name) + ",\"signature\":" + q(b.signature)
				+ ",\"pre_positions\":" + b.lines.length + "}";
	}

	/**
	 * Longest common subsequence of two sequences; marks the kept elements of each and returns, for
	 * each element of b, the index in a it is paired with (-1 when not kept).
	 */
	static int[] lcs(String[] a, String[] b, boolean[] keptA, boolean[] keptB) {
		int n = a.length, m = b.length;
		int[][] d = new int[n + 1][m + 1];
		for (int i = n - 1; i >= 0; i--) {
			for (int j = m - 1; j >= 0; j--) {
				d[i][j] = a[i].equals(b[j]) ? d[i + 1][j + 1] + 1 : Math.max(d[i + 1][j], d[i][j + 1]);
			}
		}
		int[] pairOf = new int[m];
		Arrays.fill(pairOf, -1);
		int i = 0, j = 0;
		while (i < n && j < m) {
			if (a[i].equals(b[j])) {
				keptA[i] = true;
				keptB[j] = true;
				pairOf[j] = i;
				i++;
				j++;
			} else if (d[i + 1][j] >= d[i][j + 1]) {
				i++;
			} else {
				j++;
			}
		}
		return pairOf;
	}

	// ----------------------------------------------------------------------------------------
	// the amount
	// ----------------------------------------------------------------------------------------

	/** For each line {@code unit<TAB>dir}: the methods and positions of every .java file under dir. */
	static void amount(Path listing, Path out) throws IOException {
		try (BufferedWriter w = Files.newBufferedWriter(out, StandardCharsets.UTF_8)) {
			for (String[] r : rows(listing)) {
				Path root = Path.of(r[1]);
				List<Path> files;
				try (var s = Files.walk(root)) {
					files = s.filter(p -> p.toString().endsWith(".java")).sorted().toList();
				}
				int methods = 0, positions = 0, problems = 0;
				for (Path p : files) {
					List<String> probs = new ArrayList<>();
					for (M m : file(root.relativize(p).toString(), p, probs, r[0]).methods) {
						methods++;
						positions += m.lines.length;
					}
					problems += probs.size();
				}
				w.write("{\"v\":" + VERSION + ",\"kind\":\"amount\",\"unit\":" + q(r[0]) + ",\"files\":" + files.size()
						+ ",\"methods\":" + methods + ",\"positions\":" + positions + ",\"problems\":" + problems
						+ "}\n");
			}
		}
	}

	/** Every method under dir with its original declaration and name lines (for CodeTracker). */
	static void methods(Path root, Path out) throws IOException {
		try (BufferedWriter w = Files.newBufferedWriter(out, StandardCharsets.UTF_8);
				var s = Files.walk(root)) {
			for (Path p : s.filter(x -> x.toString().endsWith(".java")).sorted().toList()) {
				String rel = root.relativize(p).toString();
				ParsedFile f = JavaFacts.parse(rel, Files.readString(p, StandardCharsets.UTF_8));
				if (f.problem() != null) {
					continue;
				}
				for (MethodUnit u : f.methods()) {
					w.write("{\"path\":" + q(rel) + ",\"type\":" + q(u.type()) + ",\"name\":" + q(u.name())
							+ ",\"signature\":" + q(u.signature()) + ",\"decl_line\":" + u.declLine()
							+ ",\"name_line\":" + u.nameLine() + "}\n");
				}
			}
		}
	}

	// ----------------------------------------------------------------------------------------
	// shape (PLAN.md §4.7): every method of a tree, as the earlier studies read it
	// ----------------------------------------------------------------------------------------

	/**
	 * For each line {@code unit<TAB>dir<TAB>injected} (injected: comma-separated simple names of the
	 * wired types, or "-"), one record per method of every .java file under dir: its positions, SinewSlim's
	 * code lines and conventional assessment ({@link Assessor#DEFAULTS}, as OfficeFloorSlim's conventional
	 * pricing), and the junction counts. {@code in}: the method's parameters, read conventionally (every
	 * parameter, injected or not, as for an ordinary method); {@code in_injection_aware}: the parameters
	 * that are not injected. {@code out}: the arguments the method passes on calls to the application's own
	 * methods (a call whose name and arity match a method declared in the tree, matched lexically). The original line range is given so that
	 * complexity can be read from the source text.
	 */
	static void shape(Path listing, Path out) throws IOException {
		try (BufferedWriter w = Files.newBufferedWriter(out, StandardCharsets.UTF_8)) {
			for (String[] r : rows(listing)) {
				for (String line : shapeOf(r[0], Path.of(r[1]),
						r.length > 2 && !r[2].equals("-") ? Set.of(r[2].split(",")) : Set.of())) {
					w.write(line);
					w.write('\n');
				}
			}
		}
	}

	record Shaped(String rel, F f, List<MethodUnit> om, List<Node> oc) {
	}

	static List<String> shapeOf(String unit, Path root, Set<String> injectedTypes) throws IOException {
		List<String> out = new ArrayList<>();
		List<Path> files;
		try (var s = Files.walk(root)) {
			files = s.filter(p -> p.toString().endsWith(".java")).sorted().toList();
		}
		List<Shaped> parsed = new ArrayList<>();
		Set<String> appMethods = new HashSet<>();
		for (Path p : files) {
			String rel = root.relativize(p).toString();
			List<String> probs = new ArrayList<>();
			F f = file(rel, p, probs, unit);
			out.addAll(probs);
			if (!probs.isEmpty()) {
				continue;
			}
			String source;
			try {
				source = Files.readString(p, StandardCharsets.UTF_8);
			} catch (java.nio.charset.MalformedInputException e) {
				source = Files.readString(p, StandardCharsets.ISO_8859_1);
			}
			ParsedFile o = JavaFacts.parse(rel, source);
			CompilationUnit cu = parse(source);
			List<Node> oc = cu == null ? List.of() : callables(cu);
			if (o.problem() != null || o.methods().size() != f.methods().size() || oc.size() != f.methods().size()) {
				out.add(problem(unit, rel, "shape: original and printed callables differ"));
				continue;
			}
			for (MethodUnit u : o.methods()) {
				appMethods.add(u.name() + "/" + paramCount(u.signature()));
			}
			parsed.add(new Shaped(rel, f, o.methods(), oc));
		}
		int trigger = Assessor.DEFAULTS.params().trigger();
		for (Shaped sh : parsed) {
			for (int i = 0; i < sh.f.methods().size(); i++) {
				M m = sh.f.methods().get(i);
				MethodUnit u = sh.om.get(i);
				Node c = sh.oc.get(i);
				String status, obstacle = null;
				try {
					Assessment a = Assessor.DEFAULTS.assess(u.facts());
					status = a.status().name().toLowerCase();
					obstacle = a.obstacle() == null ? null : a.obstacle().name().toLowerCase();
				} catch (RuntimeException | StackOverflowError e) {
					status = "error";
				}
				String simple = m.type.substring(m.type.lastIndexOf('.') + 1);
				boolean injected = injectedTypes.contains(simple) && c instanceof MethodDeclaration md && md.isPublic();
				int in = paramCount(m.signature), inAware = injected ? 0 : in;
				int passed = 0, calls = 0;
				for (MethodCallExpr mc : c.findAll(MethodCallExpr.class)) {
					if (enclosingCallable(mc) != c || !appMethods.contains(mc.getNameAsString() + "/" + mc.getArguments().size())) {
						continue;
					}
					calls++;
					passed += mc.getArguments().size();
				}
				int length = u.facts().length();
				out.add("{\"v\":" + VERSION + ",\"kind\":\"shape\",\"unit\":" + q(unit) + ",\"path\":" + q(sh.rel)
						+ ",\"type\":" + q(m.type) + ",\"name\":" + q(m.name) + ",\"signature\":" + q(m.signature)
						+ ",\"decl_line\":" + u.declLine() + ",\"end_line\":" + u.endLine()
						+ ",\"positions\":" + m.lines.length + ",\"length\":" + length
						+ ",\"long\":" + (length >= trigger) + ",\"status\":" + q(status)
						+ ",\"obstacle\":" + (obstacle == null ? "null" : q(obstacle))
						+ ",\"injected\":" + injected + ",\"in\":" + in + ",\"in_injection_aware\":" + inAware
						+ ",\"out\":" + passed + ",\"calls\":" + calls
						+ "}");
			}
		}
		return out;
	}

	/** The nearest callable enclosing n: a call in an anonymous class's method belongs to that method. */
	static Node enclosingCallable(Node n) {
		Node p = n.getParentNode().orElse(null);
		while (p != null && !(p instanceof CallableDeclaration || p instanceof CompactConstructorDeclaration)) {
			p = p.getParentNode().orElse(null);
		}
		return p;
	}

	// ----------------------------------------------------------------------------------------
	// one file: methods with their positions, tokens and original lines
	// ----------------------------------------------------------------------------------------

	static F file(String rel, Path disk, List<String> out, String unit) throws IOException {
		F none = new F(List.of(), List.of());
		String source;
		try {
			source = Files.readString(disk, StandardCharsets.UTF_8);
		} catch (java.nio.charset.MalformedInputException e) {
			source = Files.readString(disk, StandardCharsets.ISO_8859_1);
		}
		CompilationUnit cu = parse(source);
		if (cu == null) {
			out.add(problem(unit, rel, "unparsed: " + disk));
			return none;
		}
		String pretty = print(cu);
		CompilationUnit pcu = parse(pretty);
		ParsedFile printed = JavaFacts.parse(rel, pretty);
		ParsedFile original = JavaFacts.parse(rel, source);
		if (pcu == null || printed.problem() != null || original.problem() != null) {
			out.add(problem(unit, rel, "printed source unparsed: " + disk));
			return none;
		}
		List<Node> callables = callables(pcu);
		List<MethodUnit> pm = printed.methods(), om = original.methods();
		if (pm.size() != callables.size() || pm.size() != om.size()) {
			out.add(problem(unit, rel, "callables differ: " + pm.size() + " " + callables.size() + " " + om.size()));
			return none;
		}
		String[] lines = pretty.split("\n", -1);
		int[] lineTokens = new int[lines.length + 2];
		boolean[] substantive = new boolean[lineTokens.length];
		List<List<Tok>> toksByLine = new ArrayList<>();
		for (int i = 0; i < lineTokens.length; i++) {
			toksByLine.add(new ArrayList<>());
		}
		tokens(pcu, lineTokens, substantive, toksByLine);
		int[] origOf = originalLines(cu, pcu, lineTokens.length);

		// types: matched by node order between the printed and original trees
		List<TypeDeclaration> ptypes = pcu.findAll(TypeDeclaration.class), otypes = cu.findAll(TypeDeclaration.class);
		Map<Node, T> typeOf = new IdentityHashMap<>();
		List<T> types = new ArrayList<>();
		for (int i = 0; i < ptypes.size(); i++) {
			TypeDeclaration<?> t = ptypes.get(i);
			Set<String> fields = new HashSet<>(), utilities = new HashSet<>(), methods = new HashSet<>();
			for (FieldDeclaration fd : t.getFields()) {
				// a class utility (a logger) is not a tie: any class can declare its own
				fd.getVariables().forEach(v -> (utility(v) ? utilities : fields).add(v.getNameAsString()));
			}
			for (MethodDeclaration md : t.getMethods()) {
				methods.add(md.getNameAsString());
			}
			int oline = i < otypes.size() ? ((Node) otypes.get(i)).getBegin().map(p -> p.line).orElse(0) : 0;
			T tt = new T(rel, qualifiedName(t), oline, fields, utilities, methods);
			typeOf.put(t, tt);
			types.add(tt);
		}

		List<M> ms = new ArrayList<>();
		for (int i = 0; i < pm.size(); i++) {
			MethodUnit u = pm.get(i);
			Node c = callables.get(i);
			boolean[] nested = new boolean[lineTokens.length];
			nestedLines(c, nested);
			List<Integer> pos = new ArrayList<>();
			for (int l = u.facts().body().start() + 1; l < u.facts().body().end() && l < lineTokens.length; l++) {
				if (substantive[l] && !nested[l]) {
					pos.add(l);
				}
			}
			int[] lineOf = pos.stream().mapToInt(Integer::intValue).toArray();
			String[] texts = new String[lineOf.length];
			int[] orig = new int[lineOf.length];
			List<List<Tok>> toks = new ArrayList<>();
			for (int k = 0; k < lineOf.length; k++) {
				texts[k] = lines[lineOf[k] - 1].strip();
				orig[k] = origOf[lineOf[k]];
				toks.add(toksByLine.get(lineOf[k]));
			}
			T owner = c.findAncestor(TypeDeclaration.class).map(typeOf::get).orElse(null);
			MethodUnit o = om.get(i);
			ms.add(new M(rel, u.type(), u.name(), u.signature(), u, c, lineOf, texts, toks, orig, o.declLine(),
					o.endLine(), owner));
		}
		return new F(ms, types);
	}

	/** The class utilities: so far, loggers (by declared type, or by a logger factory initialiser). */
	static final Set<String> LOGGER_TYPES = Set.of("Logger", "Log", "System.Logger", "XLogger");

	static boolean utility(com.github.javaparser.ast.body.VariableDeclarator v) {
		String type = v.getType().asString();
		type = type.substring(type.lastIndexOf('.') + 1);
		if (LOGGER_TYPES.contains(type) || LOGGER_TYPES.contains(v.getType().asString())) {
			return true;
		}
		return v.getInitializer().map(i -> i.toString().matches("(?s).*\\b(getLogger|getLog|getSystemLogger)\\s*\\(.*"))
				.orElse(false);
	}

	static String qualifiedName(TypeDeclaration<?> t) {
		StringBuilder b = new StringBuilder(t.getNameAsString());
		Node p = t.getParentNode().orElse(null);
		while (p != null) {
			if (p instanceof TypeDeclaration<?> pt) {
				b.insert(0, pt.getNameAsString() + ".");
			}
			p = p.getParentNode().orElse(null);
		}
		return b.toString();
	}

	/**
	 * The original line of each printed line: the begin line, in the original tree, of the first node
	 * beginning on that printed line (the two trees are the same but for comments).
	 */
	static int[] originalLines(CompilationUnit cu, CompilationUnit pcu, int n) {
		List<Node> on = new ArrayList<>(), pn = new ArrayList<>();
		cu.walk(Node.TreeTraversal.PREORDER, x -> {
			if (!(x instanceof Comment)) {
				on.add(x);
			}
		});
		pcu.walk(Node.TreeTraversal.PREORDER, x -> {
			if (!(x instanceof Comment)) {
				pn.add(x);
			}
		});
		int[] map = new int[n];
		if (on.size() != pn.size()) {
			return map; // no mapping: moved ranges and line hints will not apply
		}
		for (int i = pn.size() - 1; i >= 0; i--) {
			int pl = pn.get(i).getBegin().map(p -> p.line).orElse(-1);
			int ol = on.get(i).getBegin().map(p -> p.line).orElse(0);
			if (pl >= 0 && pl < n) {
				map[pl] = ol; // walking backwards leaves the first node of each line
			}
		}
		return map;
	}

	static CompilationUnit parse(String source) {
		for (LanguageLevel level : LEVELS) {
			try {
				ParseResult<CompilationUnit> pr = new JavaParser(new ParserConfiguration().setLanguageLevel(level))
						.parse(source);
				if (pr.isSuccessful() && pr.getResult().isPresent()) {
					return pr.getResult().get();
				}
			} catch (RuntimeException | StackOverflowError e) {
				// next level
			}
		}
		return null;
	}

	static String print(CompilationUnit cu) {
		DefaultPrinterConfiguration conf = new DefaultPrinterConfiguration();
		conf.removeOption(new DefaultConfigurationOption(ConfigOption.PRINT_COMMENTS));
		conf.removeOption(new DefaultConfigurationOption(ConfigOption.PRINT_JAVADOC));
		return new DefaultPrettyPrinter(conf).print(cu);
	}

	static List<Node> callables(CompilationUnit cu) {
		List<Node> out = new ArrayList<>();
		for (Node n : cu.findAll(Node.class,
				x -> x instanceof CallableDeclaration || x instanceof CompactConstructorDeclaration)) {
			if (n instanceof MethodDeclaration md && md.getBody().isEmpty()) {
				continue;
			}
			out.add(n);
		}
		return out;
	}

	static final Set<String> NOT_SUBSTANTIVE = Set.of("{", "}", ";", "else", "try", "finally", "do");

	static void tokens(CompilationUnit cu, int[] perLine, boolean[] substantive, List<List<Tok>> byLine) {
		JavaToken t = cu.getTokenRange().map(tr -> tr.getBegin()).orElse(null);
		while (t != null) {
			if (!t.getCategory().isWhitespaceOrComment() && t.getRange().isPresent()) {
				int line = t.getRange().get().begin.line;
				if (line < perLine.length) {
					perLine[line]++;
					if (!NOT_SUBSTANTIVE.contains(t.getText())) {
						substantive[line] = true;
					}
					byLine.get(line).add(new Tok(line, t.getRange().get().begin.column, t.getText(),
							t.getCategory().isIdentifier()));
				}
			}
			t = t.getNextToken().orElse(null);
		}
	}

	static void nestedLines(Node n, boolean[] nested) {
		for (Node c : n.getChildNodes()) {
			boolean part = c instanceof TypeDeclaration
					|| (n instanceof ObjectCreationExpr && c instanceof BodyDeclaration);
			if (part) {
				int b = c.getBegin().map(p -> p.line).orElse(0), e = c.getEnd().map(p -> p.line).orElse(b);
				for (int l = b; l <= e && l < nested.length; l++) {
					nested[l] = true;
				}
			} else {
				nestedLines(c, nested);
			}
		}
	}

	static int paramCount(String signature) {
		String inside = signature.substring(signature.indexOf('(') + 1, signature.lastIndexOf(')')).trim();
		if (inside.isEmpty()) {
			return 0;
		}
		int depth = 0, count = 1;
		for (char c : inside.toCharArray()) {
			if (c == '<') {
				depth++;
			} else if (c == '>') {
				depth--;
			} else if (c == ',' && depth == 0) {
				count++;
			}
		}
		return count;
	}

	// ----------------------------------------------------------------------------------------
	// JSON
	// ----------------------------------------------------------------------------------------

	static String problem(String unit, String path, String what) {
		return "{\"v\":" + VERSION + ",\"kind\":\"problem\",\"unit\":" + q(unit) + ",\"path\":" + q(path)
				+ ",\"problem\":" + q(what) + "}";
	}

	static String strs(Iterable<String> xs) {
		StringBuilder b = new StringBuilder("[");
		for (String x : xs) {
			if (b.length() > 1) {
				b.append(',');
			}
			b.append(q(x));
		}
		return b.append(']').toString();
	}

	static String q(String s) {
		StringBuilder b = new StringBuilder(s.length() + 2).append('"');
		for (char c : s.toCharArray()) {
			switch (c) {
			case '"' -> b.append("\\\"");
			case '\\' -> b.append("\\\\");
			case '\n' -> b.append("\\n");
			case '\r' -> b.append("\\r");
			case '\t' -> b.append("\\t");
			default -> {
				if (c < 0x20) {
					b.append(String.format("\\u%04x", (int) c));
				} else {
					b.append(c);
				}
			}
			}
		}
		return b.append('"').toString();
	}
}
