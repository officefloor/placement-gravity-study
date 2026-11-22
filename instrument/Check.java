import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import javax.lang.model.element.Element;
import javax.lang.model.element.ElementKind;
import javax.lang.model.element.ExecutableElement;
import javax.lang.model.element.Modifier;
import javax.lang.model.element.TypeElement;
import javax.tools.JavaCompiler;
import javax.tools.JavaFileObject;
import javax.tools.StandardJavaFileManager;
import javax.tools.ToolProvider;

import com.sun.source.tree.ClassTree;
import com.sun.source.tree.CompilationUnitTree;
import com.sun.source.tree.IdentifierTree;
import com.sun.source.tree.MemberSelectTree;
import com.sun.source.tree.MethodInvocationTree;
import com.sun.source.tree.MethodTree;
import com.sun.source.tree.NewClassTree;
import com.sun.source.tree.Tree;
import com.sun.source.tree.VariableTree;
import com.sun.source.util.JavacTask;
import com.sun.source.util.TreePath;
import com.sun.source.util.TreePathScanner;
import com.sun.source.util.Trees;

/**
 * The compiler's reading of a production tree, to check the instrument against (PLAN.md 4.8).
 *
 * The instrument (Pull.java) resolves names lexically, with no symbol solver. This asks javac, which
 * does resolve them, what each method of a tree refers to: the methods it calls and the fields it
 * reads, each with the class that declares it and whether that class is the application's (declared
 * in the tree), a library's, or not resolved; and, inside the method, the parameters and locals, the
 * fields of its own class (inherited ones too) and the methods of its own class that it uses.
 *
 * <pre>
 * java -cp instrument/classes Check LISTING.tsv OUT.jsonl [CLASSPATH]
 * </pre>
 *
 * LISTING.tsv: label TAB directory of a tree. One JSON line per method with a body, and one per
 * tree ("kind":"tree") with the number of files and of compiler errors. Without the project's
 * libraries on CLASSPATH their types are errors to javac; attribution goes on, and what it cannot
 * resolve is marked "?" and counted, never guessed.
 */
public class Check {

	public static void main(String[] args) throws Exception {
		List<String> listing = Files.readAllLines(Path.of(args[0]));
		String classpath = args.length > 2 ? args[2] : "";
		try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(Path.of(args[1]), StandardCharsets.UTF_8))) {
			for (String line : listing) {
				if (line.isBlank()) {
					continue;
				}
				String[] f = line.split("\t");
				tree(f[0], Path.of(f[1]), classpath, out);
			}
		}
	}

	static void tree(String label, Path root, String classpath, PrintWriter out) throws IOException {
		List<Path> files;
		try (Stream<Path> s = Files.exists(root) ? Files.walk(root) : Stream.<Path>empty()) {
			files = s.filter(p -> p.toString().endsWith(".java")).sorted().collect(Collectors.toList());
		}
		if (files.isEmpty()) {
			out.println("{\"kind\":\"tree\",\"label\":" + q(label) + ",\"files\":0,\"errors\":0,\"failed\":false}");
			return;
		}
		JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
		int[] errors = { 0 };
		boolean failed = false;
		try (StandardJavaFileManager fm = compiler.getStandardFileManager(null, null, StandardCharsets.UTF_8)) {
			List<String> options = new ArrayList<>(List.of("-proc:none", "-nowarn", "-Xlint:none",
					"-XDshould-stop.ifError=FLOW", "-XDshould-stop.ifNoError=FLOW", "-Xmaxerrs", "100000"));
			if (!classpath.isBlank()) {
				options.add("-cp");
				options.add(classpath);
			}
			Iterable<? extends JavaFileObject> units = fm.getJavaFileObjectsFromPaths(files);
			JavacTask task = (JavacTask) compiler.getTask(null, fm, d -> {
				if (d.getKind() == javax.tools.Diagnostic.Kind.ERROR) {
					errors[0]++;
				}
			}, options, null, units);
			List<CompilationUnitTree> cus = new ArrayList<>();
			task.parse().forEach(cus::add);
			try {
				task.analyze();
			} catch (RuntimeException | Error e) {
				failed = true; // what was attributed before the failure is still read
			}
			Trees trees = Trees.instance(task);
			for (CompilationUnitTree cu : cus) {
				String rel = root.relativize(Path.of(cu.getSourceFile().toUri())).toString().replace('\\', '/');
				new Reader(label, rel, trees, out).scan(cu, null);
			}
		}
		out.println("{\"kind\":\"tree\",\"label\":" + q(label) + ",\"files\":" + files.size() + ",\"errors\":"
				+ errors[0] + ",\"failed\":" + failed + "}");
	}

	/** One method being read: what it refers to, as the compiler resolves it. */
	static class M {
		String type, name, signature;
		int params;
		boolean matchable;
		Set<String> calls = new TreeSet<>(), reads = new TreeSet<>();
		Set<String> locals = new TreeSet<>(), ownFields = new TreeSet<>(), ownMethods = new TreeSet<>();
		int unresolved;
	}

	static class Reader extends TreePathScanner<Void, Void> {
		final String label, path;
		final Trees trees;
		final PrintWriter out;
		final Deque<String> types = new ArrayDeque<>();
		final Deque<M> methods = new ArrayDeque<>();
		/** Depth of classes declared inside a method (local and anonymous): their code is the method's. */
		int inside;

		Reader(String label, String path, Trees trees, PrintWriter out) {
			this.label = label;
			this.path = path;
			this.trees = trees;
			this.out = out;
		}

		@Override
		public Void visitClass(ClassTree node, Void p) {
			if (!methods.isEmpty()) {
				// a class declared inside a method: its code is read as the method's, as a lambda's is
				inside++;
				super.visitClass(node, p);
				inside--;
				return null;
			}
			String simple = node.getSimpleName().toString();
			types.push(types.isEmpty() ? simple : types.peek() + "." + simple);
			super.visitClass(node, p);
			types.pop();
			return null;
		}

		@Override
		public Void visitMethod(MethodTree node, Void p) {
			if (inside > 0 || node.getBody() == null || types.isEmpty()) {
				return super.visitMethod(node, p);
			}
			M m = new M();
			m.type = types.peek();
			String simple = m.type.substring(m.type.lastIndexOf('.') + 1);
			m.name = node.getName().contentEquals("<init>") ? simple : node.getName().toString();
			m.params = node.getParameters().size();
			m.signature = m.name + "(" + node.getParameters().stream().map(v -> String.valueOf(v.getType()))
					.collect(Collectors.joining(", ")) + ")";
			m.matchable = true;
			methods.push(m);
			scan(node.getBody(), p); // the body only: the signature is organisation
			methods.pop();
			emit(m);
			return null;
		}

		@Override
		public Void visitMethodInvocation(MethodInvocationTree node, Void p) {
			M m = methods.peek();
			if (m != null) {
				Element e = trees.getElement(new TreePath(getCurrentPath(), node.getMethodSelect()));
				String name = name(node.getMethodSelect());
				int arity = node.getArguments().size();
				if (name.equals("this") || name.equals("super")) {
					// a constructor's call to another constructor: not a call the instrument follows
				} else if (e instanceof ExecutableElement && e.getEnclosingElement() instanceof TypeElement) {
					TypeElement owner = (TypeElement) e.getEnclosingElement();
					m.calls.add(kind(owner) + "|" + simple(owner) + "|" + name + "|" + arity);
					if (unqualified(node.getMethodSelect()) && ownOrInherited(owner)) {
						m.ownMethods.add(name);
					}
				} else {
					m.calls.add("?|?|" + name + "|" + arity);
					m.unresolved++;
				}
			}
			return super.visitMethodInvocation(node, p);
		}

		@Override
		public Void visitNewClass(NewClassTree node, Void p) {
			return super.visitNewClass(node, p);
		}

		@Override
		public Void visitIdentifier(IdentifierTree node, Void p) {
			use(node, node.getName().toString(), true);
			return super.visitIdentifier(node, p);
		}

		@Override
		public Void visitMemberSelect(MemberSelectTree node, Void p) {
			boolean onThis = node.getExpression() instanceof IdentifierTree
					&& ((IdentifierTree) node.getExpression()).getName().contentEquals("this");
			use(node, node.getIdentifier().toString(), onThis);
			return super.visitMemberSelect(node, p);
		}

		@Override
		public Void visitVariable(VariableTree node, Void p) {
			// a declaration is not a use; its initialiser is
			M m = methods.peek();
			if (m == null) {
				return null; // a field's initialiser is not in a method
			}
			scan(node.getInitializer(), p);
			return null;
		}

		/** A name used as a value: a parameter or local, a field of the method's own class, or a field of another. */
		void use(Tree node, String name, boolean own) {
			M m = methods.peek();
			if (m == null) {
				return;
			}
			Element e = trees.getElement(getCurrentPath());
			if (e == null) {
				return;
			}
			ElementKind k = e.getKind();
			if (k == ElementKind.PARAMETER || k == ElementKind.LOCAL_VARIABLE || k == ElementKind.EXCEPTION_PARAMETER
					|| k == ElementKind.RESOURCE_VARIABLE || k.name().equals("BINDING_VARIABLE")) {
				m.locals.add(name);
			} else if (k == ElementKind.FIELD || k == ElementKind.ENUM_CONSTANT) {
				if (!(e.getEnclosingElement() instanceof TypeElement)) {
					return;
				}
				TypeElement owner = (TypeElement) e.getEnclosingElement();
				if (name.equals("length") || name.equals("class") || name.equals("this") || name.equals("super")) {
					return;
				}
				// its own class's field: unqualified, through this, or a static one however it is named
				if (ownOrInherited(owner) && (own || e.getModifiers().contains(Modifier.STATIC))) {
					m.ownFields.add(name);
				} else if (!own) {
					m.reads.add(kind(owner) + "|" + simple(owner) + "|" + name);
				}
			}
		}

		/** Whether the class that declares a member is the method's own, or one it extends or implements. */
		boolean ownOrInherited(TypeElement owner) {
			TreePath path = getCurrentPath();
			while (path != null) {
				if (path.getLeaf() instanceof ClassTree) {
					Element c = trees.getElement(path);
					if (c instanceof TypeElement) {
						TypeElement here = (TypeElement) c;
						if (here.equals(owner) || inherits(here, owner, 0)) {
							return true;
						}
					}
				}
				path = path.getParentPath();
			}
			return false;
		}

		static boolean inherits(TypeElement c, TypeElement owner, int depth) {
			if (depth > 20) {
				return false;
			}
			List<javax.lang.model.type.TypeMirror> ups = new ArrayList<>(c.getInterfaces());
			ups.add(c.getSuperclass());
			for (javax.lang.model.type.TypeMirror t : ups) {
				if (t instanceof javax.lang.model.type.DeclaredType) {
					Element e = ((javax.lang.model.type.DeclaredType) t).asElement();
					if (e instanceof TypeElement && (e.equals(owner) || inherits((TypeElement) e, owner, depth + 1))) {
						return true;
					}
				}
			}
			return false;
		}

		/** app: declared in the tree being read; lib: anything else that resolved. */
		String kind(TypeElement owner) {
			try {
				return trees.getTree(owner) != null ? "app" : "lib";
			} catch (RuntimeException e) {
				return "lib";
			}
		}

		static String simple(TypeElement owner) {
			return owner.getSimpleName().toString();
		}

		static String name(Tree select) {
			if (select instanceof IdentifierTree) {
				return ((IdentifierTree) select).getName().toString();
			}
			if (select instanceof MemberSelectTree) {
				return ((MemberSelectTree) select).getIdentifier().toString();
			}
			return "?";
		}

		static boolean unqualified(Tree select) {
			if (select instanceof IdentifierTree) {
				return true;
			}
			return select instanceof MemberSelectTree
					&& ((MemberSelectTree) select).getExpression() instanceof IdentifierTree
					&& ((IdentifierTree) ((MemberSelectTree) select).getExpression()).getName().contentEquals("this");
		}

		void emit(M m) {
			out.println("{\"kind\":\"method\",\"label\":" + q(label) + ",\"path\":" + q(path) + ",\"type\":" + q(m.type)
					+ ",\"name\":" + q(m.name) + ",\"signature\":" + q(m.signature) + ",\"params\":" + m.params
					+ ",\"calls\":" + list(m.calls) + ",\"reads\":" + list(m.reads) + ",\"locals\":" + list(m.locals)
					+ ",\"own_fields\":" + list(m.ownFields) + ",\"own_methods\":" + list(m.ownMethods)
					+ ",\"unresolved\":" + m.unresolved + "}");
		}
	}

	static String list(Set<String> xs) {
		return xs.stream().map(Check::q).collect(Collectors.joining(",", "[", "]"));
	}

	static String q(String s) {
		StringBuilder b = new StringBuilder("\"");
		for (char c : s.toCharArray()) {
			if (c == '"' || c == '\\') {
				b.append('\\').append(c);
			} else if (c < 0x20) {
				b.append(String.format("\\u%04x", (int) c));
			} else {
				b.append(c);
			}
		}
		return b.append('"').toString();
	}
}
