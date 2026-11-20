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
import java.util.TreeMap;
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
 * new problem and the <b>bindings</b> that code has to its location: the data it uses that existed
 * before the change and that it could not have had anywhere else without threading it there.
 *
 * <ul>
 * <li><b>Method bindings</b>: the host method's own parameters and locals. A parameter the framework
 * injects (a public method of an OfficeFloor function, see {@code injected}) does not bind: a function
 * placed anywhere can declare it.</li>
 * <li><b>Class bindings</b>: the host class's fields and methods.</li>
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
 * MANIFEST.tsv: {@code unit<TAB>path<TAB>before<TAB>after[<TAB>beforePath]} per changed file ("-" for
 * none; beforePath is the before version's own path where the file was renamed, else path).
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
	static final int VERSION = 14;

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
		if (args[0].equals("--places")) {
			places(Path.of(args[1]), Path.of(args[2]));
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

	/** A type: its fields, the names of its methods, and which of its fields hold injected dependencies. */
	record T(String file, String name, int origLine, Set<String> fields, Set<String> utilities, Set<String> methods,
			Set<String> injected, Set<String> constants, Map<String, String> fieldTypes, Set<String> supers) {

		/** The fields the class holds: state, injected dependencies and constants (not utilities). */
		int held() {
			return fields.size();
		}
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
						F f = file(r.length > 4 && !r[4].equals("-") ? r[4] : r[1], Path.of(r[2]), out, unit);
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
			// accretion (PLAN.md 4.3a): the fields an addition leaves in a class that already existed
			for (T t : typesAfter) {
				T b = typeMatch.get(t);
				if (b == null) {
					continue;
				}
				// by name: these are the fields the change introduces to the class (PLAN.md 4.3b)
				Set<String> added = new TreeSet<>(t.fields);
				added.removeAll(b.fields);
				out.add("{\"v\":" + VERSION + ",\"kind\":\"class\",\"unit\":" + q(unit) + ",\"path\":" + q(t.file)
						+ ",\"type\":" + q(t.name) + ",\"held_before\":" + b.held() + ",\"held_after\":" + t.held()
						+ ",\"fields_added\":" + added.size() + ",\"fields_added_names\":" + strs(added) + "}");
			}
			for (M b : before) {
				if (!match.containsValue(b)) {
					out.add(removedHost(unit, b));
				}
			}
			for (M m : after) {
				String h = host(m);
				if (h != null) {
					out.add(h);
				} else if (match.get(m) != null && !sameKey(m, match.get(m))) {
					out.add(carried(unit, match.get(m), m));
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
			Set<String> preInjected = renamed(bt == null ? Set.of() : bt.injected, ren);
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
			Set<String> preConstants = renamed(bt == null ? Set.of() : bt.constants, ren);
			Set<String> preAll = isNew ? Set.of() : methodValues(m, b, a, ren, true);
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
			// choice (H5, PLAN.md 4.2a): the declared type of each of the method's parameters and locals,
			// and of each field of its class, so that the places holding the same types can be found
			s.append(",\"var_types\":").append(typeMap(varTypes(m.node)));
			s.append(",\"field_types\":").append(typeMap(m.owner == null ? Map.of() : m.owner.fieldTypes));
			// core and periphery at the class (H2): the class's methods that were there before the change
			// (a call to one is a core value) and those the change added to it
			s.append(",\"class_methods_pre\":").append(strs(new TreeSet<>(preMethods)));
			Set<String> methodsAdded = new TreeSet<>(m.owner == null ? Set.of() : m.owner.methods);
			methodsAdded.removeAll(bt == null ? Set.of() : bt.methods);
			s.append(",\"class_methods_added\":").append(strs(methodsAdded));
			// introduced (PLAN.md 4.3b): the parameters and locals the method has after the change that
			// were not there before it. All of a new method's values are introduced.
			Set<String> introduced = new TreeSet<>(ownVars);
			introduced.removeAll(preAll);
			s.append(",\"introduced_method\":").append(strs(introduced));

			// runs of added logic: added positions that are neither moved nor organisation
			int nOrganisation = 0;
			for (int i = 0; i < a.length; i++) {
				if (a[i] && mk[i] == 0 && organisation[i]) {
					mk[i] = 3;
					nOrganisation++;
				}
			}
			s.append(",\"organisation\":").append(nOrganisation);
			// the line facts for following a problem's own lines (PLAN.md 4.4): per after position, the
			// before position it is kept from (-1: not kept) and its kind (-1 kept, 0 added logic, 1 moved
			// by RefactoringMiner, 2 moved by text, 3 organisation); the text hash of every position
			int[] pair = isNew ? null : pairOf.get(m);
			s.append(",\"pair\":[");
			for (int i = 0; i < a.length; i++) {
				s.append(i > 0 ? "," : "").append(pair == null ? -1 : pair[i]);
			}
			s.append("],\"kinds\":[");
			for (int i = 0; i < a.length; i++) {
				s.append(i > 0 ? "," : "").append(a[i] ? mk[i] : -1);
			}
			s.append("],\"hash\":").append(hashes(m.texts));
			s.append(",\"before_hash\":").append(isNew ? "[]" : hashes(b.texts));
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
				bindings(m, from, to, lineTokens, values, ownVars, preFields, preMethods, tm, tf, tc);
				bindings(m, from, to, lineTokens, Set.of(), ownVars, preUtilities, Set.of(), new TreeSet<>(), tu,
						new TreeSet<>());
				// secondary: only the references the edit itself introduced
				Set<String> km = new TreeSet<>(), kf = new TreeSet<>(), kc = new TreeSet<>();
				bindings(m, from, to, addedTokens, values, ownVars, preFields, preMethods, km, kf, kc);
				// references that resolve to nothing seen: inherited members, static imports
				Set<String> un = unresolved(m, from, to, ownVars, knownNames, knownMethods);
				Seam seam = index.seam(m.lines[from], m.lines[to]);
				// bystanders (PLAN.md 4.3a): the pre-existing values visible where the run starts, and
				// those its lines use. Method values: parameters, injected or not, and locals declared
				// before the run in a scope that encloses it. Fields: state, injected, constants.
				Set<String> visM = visibleValues(m, preAll, m.lines[from]);
				Set<String> needM = new TreeSet<>(), needF = new TreeSet<>();
				for (Node n : m.node.findAll(Node.class)) {
					int line = n.getBegin().map(p -> p.line).orElse(-1);
					if (line < m.lines[from] || line > m.lines[to]) {
						continue;
					}
					if (n instanceof NameExpr ne) {
						String x = ne.getNameAsString();
						if (visM.contains(x)) {
							needM.add(x);
						} else if (!ownVars.contains(x) && preFields.contains(x)) {
							needF.add(x);
						}
					} else if (n instanceof FieldAccessExpr fa && fa.getScope() instanceof ThisExpr
							&& preFields.contains(fa.getNameAsString())) {
						needF.add(fa.getNameAsString());
					}
				}
				int[] vis = new int[3], need = new int[3]; // 0 state, 1 injected, 2 constant
				Set<String> byF = new TreeSet<>();
				for (String f : preFields) {
					int k = preConstants.contains(f) ? 2 : preInjected.contains(f) ? 1 : 0;
					vis[k]++;
					need[k] += needF.contains(f) ? 1 : 0;
					if (!needF.contains(f)) {
						byF.add(f);
					}
				}
				if (r > 0) {
					s.append(',');
				}
				s.append("{\"from\":").append(from).append(",\"to\":").append(to);
				s.append(",\"positions\":").append(to - from + 1);
				s.append(",\"replaces\":").append(replaces);
				s.append(",\"added_tokens\":").append(addedTokens.size());
				s.append(",\"inputs\":").append(seam.inputs().size());
				s.append(",\"outputs\":").append(seam.outputs().size());
				s.append(",\"binding_method\":").append(strs(tm));
				Set<String> tp = new TreeSet<>(tm);
				tp.retainAll(params(m));
				s.append(",\"binding_param\":").append(strs(tp));
				s.append(",\"binding_field\":").append(strs(tf));
				Set<String> ti = new TreeSet<>(tf);
				ti.retainAll(preInjected);
				s.append(",\"binding_field_injected\":").append(strs(ti));
				s.append(",\"binding_class_method\":").append(strs(tc));
				s.append(",\"utility\":").append(strs(tu));
				s.append(",\"tok_binding_method\":").append(km.size());
				s.append(",\"tok_binding_class\":").append(kf.size() + kc.size());
				s.append(",\"unresolved\":").append(strs(un));
				s.append(",\"vis_method\":").append(strs(visM)).append(",\"need_method\":").append(strs(needM));
				s.append(",\"vis_fields\":[").append(vis[0]).append(',').append(vis[1]).append(',').append(vis[2]);
				s.append("],\"need_fields\":[").append(need[0]).append(',').append(need[1]).append(',')
						.append(need[2]).append(']');
				s.append(",\"need_field_names\":").append(strs(needF)).append(",\"by_field_names\":").append(strs(byF));
				s.append('}');
			}
			s.append(']');
			if (isNew) {
				s.append(",\"birth_binding\":").append(strs(birthBindings(m)));
			}
			s.append('}');
			return s.toString();
		}

		/**
		 * Organisation lines: in a constructor, a statement that only assigns one of its parameters to a
		 * field ({@code this.repo = repo;}), the wiring of an injected dependency; and the one statement
		 * of a plain accessor, a method whose whole body returns a field of its class or assigns one of
		 * its parameters to one. A plain accessor exposes the field and holds no logic; one that does
		 * anything more is logic.
		 */
		static boolean[] organisation(M m, Set<String> preFields) {
			boolean[] out = new boolean[m.lines.length];
			if (m.node instanceof MethodDeclaration md && md.getBody().isPresent()
					&& md.getBody().get().getStatements().size() == 1 && m.owner != null) {
				com.github.javaparser.ast.stmt.Statement st = md.getBody().get().getStatement(0);
				Set<String> params = params(m);
				boolean accessor = false;
				if (st instanceof com.github.javaparser.ast.stmt.ReturnStmt rs && rs.getExpression().isPresent()) {
					Expression e = rs.getExpression().get();
					accessor = e instanceof NameExpr n && !params.contains(n.getNameAsString())
							&& m.owner.fields.contains(n.getNameAsString())
							|| e instanceof FieldAccessExpr fa && fa.getScope() instanceof ThisExpr
									&& m.owner.fields.contains(fa.getNameAsString());
				} else if (st instanceof com.github.javaparser.ast.stmt.ExpressionStmt es
						&& es.getExpression() instanceof com.github.javaparser.ast.expr.AssignExpr ae
						&& ae.getOperator() == com.github.javaparser.ast.expr.AssignExpr.Operator.ASSIGN
						&& ae.getValue() instanceof NameExpr v && params.contains(v.getNameAsString())) {
					accessor = ae.getTarget() instanceof FieldAccessExpr fa && fa.getScope() instanceof ThisExpr
							&& m.owner.fields.contains(fa.getNameAsString())
							|| ae.getTarget() instanceof NameExpr t && !params.contains(t.getNameAsString())
									&& m.owner.fields.contains(t.getNameAsString());
				}
				int i = Arrays.binarySearch(m.lines, st.getBegin().map(p -> p.line).orElse(-1));
				if (accessor && i >= 0) {
					out[i] = true;
				}
				return out;
			}
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
		 * The host method's values that existed before the change and bind code to it: parameters (not
		 * injected ones) and locals whose declaration is not itself added. Renames are followed.
		 */
		Set<String> methodValues(M m, M b, boolean[] added, Map<String, String> ren) {
			return methodValues(m, b, added, ren, false);
		}

		/** With keepInjected, injected parameters are kept: what is visible is read alike in both arms. */
		Set<String> methodValues(M m, M b, boolean[] added, Map<String, String> ren, boolean keepInjected) {
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
				if (param && injectedHere && !keepInjected) {
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

		/**
		 * The pre-existing method values visible at a printed line: the parameters, and the locals
		 * declared before it whose scope (the nearest enclosing block, loop, try, switch entry or lambda)
		 * encloses it. A local declared inside an earlier block is not visible after the block.
		 */
		static Set<String> visibleValues(M m, Set<String> pre, int line) {
			Set<String> out = new TreeSet<>(params(m));
			out.retainAll(pre);
			for (com.github.javaparser.ast.body.VariableDeclarator vd : m.node
					.findAll(com.github.javaparser.ast.body.VariableDeclarator.class)) {
				String n = vd.getNameAsString();
				if (!pre.contains(n) || vd.getBegin().map(p -> p.line).orElse(Integer.MAX_VALUE) >= line) {
					continue;
				}
				Node sc = vd.getParentNode().orElse(null);
				while (sc != null && !(sc instanceof com.github.javaparser.ast.stmt.BlockStmt
						|| sc instanceof com.github.javaparser.ast.stmt.ForStmt
						|| sc instanceof com.github.javaparser.ast.stmt.ForEachStmt
						|| sc instanceof com.github.javaparser.ast.stmt.TryStmt
						|| sc instanceof com.github.javaparser.ast.stmt.SwitchEntry
						|| sc instanceof com.github.javaparser.ast.expr.LambdaExpr)) {
					sc = sc.getParentNode().orElse(null);
				}
				if (sc != null && sc.getBegin().isPresent() && sc.getBegin().get().line <= line
						&& line <= sc.getEnd().get().line) {
					out.add(n);
				}
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
		static void bindings(M m, int from, int to, Set<Long> addedTokens, Set<String> values, Set<String> ownVars,
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

		/** A new method is bound at birth to its existing callers by the existing values passed to it. */
		Set<String> birthBindings(M m) {
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
				+ ",\"pre_positions\":" + b.lines.length + ",\"before_hash\":" + hashes(b.texts) + "}";
	}

	static boolean sameKey(M a, M b) {
		return a.file.equals(b.file) && a.type.equals(b.type) && a.signature.equals(b.signature);
	}

	/** An unchanged method whose path, type or signature changed: its lines are carried to the new key. */
	static String carried(String unit, M b, M m) {
		return "{\"v\":" + VERSION + ",\"kind\":\"carried\",\"unit\":" + q(unit) + ",\"path\":" + q(m.file)
				+ ",\"type\":" + q(m.type) + ",\"name\":" + q(m.name) + ",\"signature\":" + q(m.signature)
				+ ",\"before_path\":" + q(b.file) + ",\"before_type\":" + q(b.type) + ",\"before_signature\":"
				+ q(b.signature) + ",\"positions\":" + m.lines.length + "}";
	}

	static String hashes(String[] texts) {
		StringBuilder b = new StringBuilder("[");
		for (int i = 0; i < texts.length; i++) {
			b.append(i > 0 ? "," : "").append(texts[i].hashCode());
		}
		return b.append(']').toString();
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
				int methods = 0, positions = 0, problems = 0, largest = 0;
				for (Path p : files) {
					List<String> probs = new ArrayList<>();
					for (M m : file(root.relativize(p).toString(), p, probs, r[0]).methods) {
						methods++;
						positions += m.lines.length;
						largest = Math.max(largest, m.lines.length);
					}
					problems += probs.size();
				}
				w.write("{\"v\":" + VERSION + ",\"kind\":\"amount\",\"unit\":" + q(r[0]) + ",\"files\":" + files.size()
						+ ",\"methods\":" + methods + ",\"positions\":" + positions + ",\"largest\":" + largest
							+ ",\"problems\":" + problems
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
	// choice (H5, PLAN.md 4.2a): the places of a tree, by the types they hold
	// ----------------------------------------------------------------------------------------

	/** A type as written, without spaces (generic arguments kept: List<Owner> is not List<Pet>). */
	static String typeText(com.github.javaparser.ast.type.Type t) {
		return t.asString().replaceAll("\\s+", "");
	}

	/** The declared type of each parameter and local of a method (a lambda's untyped parameters are left
	 * out; a local declared {@code var} has the type "var"). */
	static Map<String, String> varTypes(Node callable) {
		Map<String, String> out = new TreeMap<>();
		for (com.github.javaparser.ast.body.Parameter p : callable.findAll(com.github.javaparser.ast.body.Parameter.class)) {
			if (!(p.getType() instanceof com.github.javaparser.ast.type.UnknownType)) {
				out.putIfAbsent(p.getNameAsString(), typeText(p.getType()));
			}
		}
		for (com.github.javaparser.ast.body.VariableDeclarator v : callable
				.findAll(com.github.javaparser.ast.body.VariableDeclarator.class)) {
			if (v.getParentNode().filter(n -> n instanceof FieldDeclaration).isEmpty()) {
				out.putIfAbsent(v.getNameAsString(), typeText(v.getType()));
			}
		}
		return out;
	}

	static String typeMap(Map<String, String> m) {
		StringBuilder s = new StringBuilder("{");
		for (Map.Entry<String, String> e : new TreeMap<>(m).entrySet()) {
			s.append(s.length() > 1 ? "," : "").append(q(e.getKey())).append(':').append(q(e.getValue()));
		}
		return s.append('}').toString();
	}

	/** The simple names of the types a type extends or implements. */
	static Set<String> supers(TypeDeclaration<?> t) {
		Set<String> out = new TreeSet<>();
		if (t instanceof com.github.javaparser.ast.body.ClassOrInterfaceDeclaration c) {
			c.getExtendedTypes().forEach(x -> out.add(x.getNameAsString()));
			c.getImplementedTypes().forEach(x -> out.add(x.getNameAsString()));
		} else if (t instanceof com.github.javaparser.ast.body.EnumDeclaration e) {
			e.getImplementedTypes().forEach(x -> out.add(x.getNameAsString()));
		} else if (t instanceof com.github.javaparser.ast.body.RecordDeclaration r) {
			r.getImplementedTypes().forEach(x -> out.add(x.getNameAsString()));
		}
		return out;
	}

	/** A declared type's class: generic arguments and array brackets dropped, the simple name. */
	static String rawSimple(String type) {
		String t = type.replaceAll("<.*>", "").replace("[]", "").replace("...", "");
		return t.substring(t.lastIndexOf('.') + 1);
	}

	/**
	 * The calls a method makes, each as {@code receiver|name|arity}: the receiver is the simple name of
	 * the class the call goes to where the source says it (a local, parameter or field of a declared type;
	 * a class named for a static call), "" for the method's own class ({@code this}, {@code super} or no
	 * receiver), and "?" where it cannot be read without a symbol solver (a chained call, an expression).
	 * A method reference has arity -1 (any).
	 */
	static List<String> calls(M m) {
		Map<String, String> vars = varTypes(m.node);
		Map<String, String> fields = m.owner == null ? Map.of() : m.owner.fieldTypes;
		List<String> out = new ArrayList<>();
		java.util.function.Function<Expression, String> receiver = e -> {
			if (e == null || e instanceof ThisExpr || e instanceof com.github.javaparser.ast.expr.SuperExpr) {
				return "";
			}
			if (e instanceof NameExpr n) {
				String x = n.getNameAsString();
				if (vars.containsKey(x)) {
					return rawSimple(vars.get(x));
				}
				if (fields.containsKey(x)) {
					return rawSimple(fields.get(x));
				}
				return Character.isUpperCase(x.charAt(0)) ? x : "?";
			}
			if (e instanceof FieldAccessExpr fa && fa.getScope() instanceof ThisExpr && fields.containsKey(fa.getNameAsString())) {
				return rawSimple(fields.get(fa.getNameAsString()));
			}
			if (e instanceof com.github.javaparser.ast.expr.TypeExpr te) {
				return rawSimple(te.getType().asString());
			}
			return "?";
		};
		for (MethodCallExpr c : m.node.findAll(MethodCallExpr.class)) {
			out.add(receiver.apply(c.getScope().orElse(null)) + "|" + c.getNameAsString() + "|" + c.getArguments().size());
		}
		for (com.github.javaparser.ast.expr.MethodReferenceExpr r : m.node
				.findAll(com.github.javaparser.ast.expr.MethodReferenceExpr.class)) {
			out.add(receiver.apply(r.getScope()) + "|" + r.getIdentifier() + "|-1");
		}
		return out;
	}

	/**
	 * For each line {@code unit<TAB>dir}, one record per .java file under dir (its path relative to dir):
	 * each class with the types of its injected dependencies and the types it extends or implements, and
	 * each method with the types of its parameters and locals and the calls it makes. H5 counts, for a
	 * bound addition, the other places on its control flow that hold the same types (PLAN.md 4.2a).
	 */
	/** A method's access (H7, PLAN.md 4.2c): public, protected, package or private; an interface's
	 * members without a modifier are public. */
	static String access(Node n) {
		if (!(n instanceof CallableDeclaration<?> cd)) {
			return "package";
		}
		var a = cd.getAccessSpecifier();
		if (a == com.github.javaparser.ast.AccessSpecifier.NONE) {
			boolean inInterface = cd.getParentNode().filter(p -> p instanceof com.github.javaparser.ast.body.ClassOrInterfaceDeclaration c
					&& c.isInterface()).isPresent();
			return inInterface ? "public" : "package";
		}
		return a.asString();
	}

	static void places(Path listing, Path out) throws IOException {
		try (BufferedWriter w = Files.newBufferedWriter(out, StandardCharsets.UTF_8)) {
			for (String[] r : rows(listing)) {
				Path root = Path.of(r[1]);
				if (!Files.isDirectory(root)) {
					continue;
				}
				try (var files = Files.walk(root)) {
					for (Path p : files.filter(x -> x.toString().endsWith(".java")).sorted().toList()) {
						String rel = root.relativize(p).toString();
						List<String> problems = new ArrayList<>();
						F f = file(rel, p, problems, r[0]);
						StringBuilder classes = new StringBuilder(), methods = new StringBuilder();
						for (T t : f == null ? List.<T>of() : f.types()) {
							Set<String> types = new TreeSet<>();
							t.injected().forEach(x -> {
								if (t.fieldTypes().containsKey(x)) {
									types.add(t.fieldTypes().get(x));
								}
							});
							classes.append(classes.length() > 0 ? "," : "").append("{\"name\":").append(q(t.name()))
									.append(",\"injected_types\":").append(strs(types)).append(",\"supers\":")
									.append(strs(t.supers())).append('}');
						}
						for (M m : f == null ? List.<M>of() : f.methods()) {
							methods.append(methods.length() > 0 ? "," : "").append("{\"type\":").append(q(m.type()))
									.append(",\"name\":").append(q(m.name())).append(",\"signature\":")
									.append(q(m.signature())).append(",\"params\":").append(paramCount(m.signature()))
									.append(",\"types\":").append(strs(new TreeSet<>(varTypes(m.node()).values())))
									.append(",\"calls\":").append(strs(calls(m)))
									.append(",\"access\":").append(q(access(m.node()))).append('}');
						}
						w.write("{\"unit\":" + q(r[0]) + ",\"path\":" + q(rel) + ",\"classes\":[" + classes
								+ "],\"methods\":[" + methods + "],\"problems\":" + problems.size() + "}\n");
					}
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
				// the method's own local variables: with its parameters, the values it holds
				int locals = 0;
				for (com.github.javaparser.ast.body.VariableDeclarator v
						: c.findAll(com.github.javaparser.ast.body.VariableDeclarator.class)) {
					if (enclosingCallable(v) == c) {
						locals++;
					}
				}
				out.add("{\"v\":" + VERSION + ",\"kind\":\"shape\",\"unit\":" + q(unit) + ",\"path\":" + q(sh.rel)
						+ ",\"type\":" + q(m.type) + ",\"name\":" + q(m.name) + ",\"signature\":" + q(m.signature)
						+ ",\"decl_line\":" + u.declLine() + ",\"end_line\":" + u.endLine()
						+ ",\"positions\":" + m.lines.length + ",\"length\":" + length
						+ ",\"long\":" + (length >= trigger) + ",\"status\":" + q(status)
						+ ",\"obstacle\":" + (obstacle == null ? "null" : q(obstacle))
						+ ",\"injected\":" + injected + ",\"in\":" + in + ",\"in_injection_aware\":" + inAware
						+ ",\"out\":" + passed + ",\"calls\":" + calls + ",\"locals\":" + locals
						+ ",\"class_held\":" + (m.owner == null ? 0 : m.owner.held())
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
			Set<String> constants = new HashSet<>();
			Map<String, String> fieldTypes = new HashMap<>();
			for (FieldDeclaration fd : t.getFields()) {
				fd.getVariables().forEach(v -> fieldTypes.put(v.getNameAsString(), typeText(v.getType())));
				// a class utility (a logger) is not a binding: any class can declare its own
				fd.getVariables().forEach(v -> (utility(v) ? utilities : fields).add(v.getNameAsString()));
				if (fd.isStatic() && fd.isFinal()) {
					fd.getVariables().forEach(v -> {
						if (!utility(v)) {
							constants.add(v.getNameAsString());
						}
					});
				}
			}
			for (MethodDeclaration md : t.getMethods()) {
				methods.add(md.getNameAsString());
			}
			int oline = i < otypes.size() ? ((Node) otypes.get(i)).getBegin().map(p -> p.line).orElse(0) : 0;
			T tt = new T(rel, qualifiedName(t), oline, fields, utilities, methods, injectedFields(t), constants,
					fieldTypes, supers(t));
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

	/** Annotations that inject a field, a setter's parameter or a configuration value. */
	static final Set<String> INJECT = Set.of("Autowired", "Inject", "Resource", "Value", "Dependency");

	/** Annotations that make a class container-managed, so its constructor parameters are injected. */
	static final Set<String> MANAGED = Set.of("Component", "Service", "Repository", "Controller", "RestController",
			"Configuration", "ControllerAdvice", "RestControllerAdvice");

	static boolean annotated(com.github.javaparser.ast.nodeTypes.NodeWithAnnotations<?> n, Set<String> names) {
		for (com.github.javaparser.ast.expr.AnnotationExpr a : n.getAnnotations()) {
			String s = a.getNameAsString();
			if (names.contains(s.substring(s.lastIndexOf('.') + 1))) {
				return true;
			}
		}
		return false;
	}

	/**
	 * The fields of t that hold injected dependencies: a field annotated for injection; in a
	 * container-managed class, a field assigned from a constructor parameter, or filled by Lombok's
	 * {@code @RequiredArgsConstructor} (final fields) or {@code @AllArgsConstructor}; and a field assigned
	 * from the parameter of a method annotated for injection (setter injection). A constructor parameter of
	 * a class the container does not manage is data, not a dependency.
	 */
	static Set<String> injectedFields(TypeDeclaration<?> t) {
		Set<String> fields = new HashSet<>(), out = new HashSet<>();
		for (FieldDeclaration fd : t.getFields()) {
			fd.getVariables().forEach(v -> fields.add(v.getNameAsString()));
			if (annotated(fd, INJECT)) {
				fd.getVariables().forEach(v -> out.add(v.getNameAsString()));
			}
		}
		if (annotated(t, MANAGED)) {
			for (com.github.javaparser.ast.body.ConstructorDeclaration cd : t.getConstructors()) {
				out.addAll(assignedFromParameters(cd));
			}
			boolean required = annotated(t, Set.of("RequiredArgsConstructor"));
			boolean all = annotated(t, Set.of("AllArgsConstructor"));
			for (FieldDeclaration fd : t.getFields()) {
				if (fd.isStatic() || !(all || (required && (fd.isFinal() || annotated(fd, Set.of("NonNull")))))) {
					continue;
				}
				fd.getVariables().forEach(v -> {
					if (v.getInitializer().isEmpty()) {
						out.add(v.getNameAsString());
					}
				});
			}
		}
		for (MethodDeclaration md : t.getMethods()) {
			if (annotated(md, Set.of("Autowired", "Inject", "Resource"))) {
				out.addAll(assignedFromParameters(md));
			}
		}
		out.retainAll(fields);
		return out;
	}

	/** The fields a callable assigns one of its parameters to ({@code this.f = p;} or {@code f = p;}). */
	static Set<String> assignedFromParameters(CallableDeclaration<?> cd) {
		Set<String> params = new HashSet<>(), out = new HashSet<>();
		cd.getParameters().forEach(p -> params.add(p.getNameAsString()));
		for (com.github.javaparser.ast.expr.AssignExpr ae : cd.findAll(com.github.javaparser.ast.expr.AssignExpr.class)) {
			if (ae.getOperator() != com.github.javaparser.ast.expr.AssignExpr.Operator.ASSIGN
					|| !(ae.getValue() instanceof NameExpr v) || !params.contains(v.getNameAsString())) {
				continue;
			}
			if (ae.getTarget() instanceof FieldAccessExpr fa && fa.getScope() instanceof ThisExpr) {
				out.add(fa.getNameAsString());
			} else if (ae.getTarget() instanceof NameExpr n && !params.contains(n.getNameAsString())) {
				out.add(n.getNameAsString());
			}
		}
		return out;
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
