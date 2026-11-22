# Pescio, *Notes on Software Design* (2008–2012) and *Physics of Software* papers

Read 22 November 2026 (for the full read dated 21 November 2026). Notes and short quotes only;
the texts are freely available at the sources below and are not copied here.

## Sources fetched

- carlopescio.com, the blog's full-content RSS feed (`/feeds/posts/default?alt=rss`), 57 posts,
  June 2007 to March 2013. Every *Notes on Software Design* chapter that the feed holds was read in
  full: Ch. 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, and "Ask not what an object
  is, but..." (December 2012, which Pescio calls the de facto Ch. 17). Also read in full: "A
  ForceField Diagram" (2009), "Bad Luck, or fighting the forcefield" (2009), "Delaying
  Decisions" (2010), "Life without a controller, case 1" (2012), "Episode 2: the Controller
  Strikes Back" (2012), "Don't do it!" (2012). The rest were searched for *gravit*, *encapsul*,
  *private*, *coupl*, *measure*.
- "The Dependency Structure Matrix" (October 2009) and "A little more on DSM and Gravity"
  (December 2009): no longer served by carlopescio.com (the URLs return the blog's front page);
  read in full from the Internet Archive (snapshots of 23 April 2016).
- physicsofsoftware.weebly.com: "The idea", "The story so far", "Papers" (Pescio's own annotated
  summary of the chapters), "Random notes" (2016–2019 notes, including "Laws and phenomena in the
  physics of software: a better model", 22 July 2016).
- Papers linked from that site, read in full: *Forces in the Physics of Software – the final word*
  (draft v1.2, January 2024, 20 pp., github.com/carlopescio/PhysicsOfSoftware/Forces2024.pdf);
  *Cε-Stationary Design in the Physics of Software* (draft v1.0, March 2024) skimmed for
  growth/coupling/measurement passages; *Compressive Strength and Parameter Passing* (draft v1.5,
  2016) skimmed; the slide scrapbook *A Physics of Software* v0.003 (summary.pdf) skimmed. Not
  read: *Design, Conceptual Integrity, and Algorithmic Information Theory* (2020); the DDD EU 2016
  and nCrafts 2016 talks (video).

## What it says

**Gravity is mass-driven attraction (Ch. 2, 6 December 2008).** "Mass exerts gravitational
attraction ... Gravitational attraction makes large functions or classes to attract more LOCs,
large components to attract more classes and functions ... a table with many fields will attract
more fields". Mass is static size ("a long function has bigger mass than a short one"). "The ugly
side of gravity is that it's a natural, incremental, attractive, self-sustaining force. It starts
with a single line of code. The next line is attracted to the same function, and so on ...
gravity makes sure that the minimum resistance path is followed, and that's always to keep things
together." Fractal: function, class, component, process, database.

**Gravity is neutral and can be exploited (Ch. 4, February 2009).** "if we come up with the right
gravitational centers early on, they will keep attracting the right things. This is the role of
architecture". The wrong partition plus gravity plus inertia "keeps a bad system in a bad state".

**Inertia (Ch. 3, January 2009)** is mass resisting a change of *decision*: "every decomposition
unit affected by that decision will be touched, therefore adding to the mass to be moved".

**Pescio's own later reading of gravity** (Papers page, undated, after 2016): "software tends to
grow in a way that large modules get larger (many have observed this power law distribution). I
postulated a form of gravity, which I thought was some sort of elementary force. Only later on I
understood that it was a combined effect of temporal and spatial entanglement, but that portion
never made it to the blog." Ch. 5 (Multiplicity) he calls "wrong" in the same place.

**Access protection is a separation, i.e. it works against gravity (Ch. 1, November 2008).**
Ways to partition include "In-component access protection, like public/private class members" and
"Data member (inaccessible outside the instance)". "Get/Set functions work against in-component
access protection." Separation "always entails a cost" (Ch. 2: performance, plumbing, human
understanding).

**Visibility decides where code is attracted (DSM posts, October and December 2009).** If
component B uses C but does not reveal it, "Using C from A requires that you discover C existence
... At that point, adding a new service inside B might just be more convenient." If A and B are
only logical components, "Whatever B can access, A can access as well, without any additional
effort. The gravitational field of B is weaker, and some code might be attracted to A". "Attraction
is stronger in the direction of simplicity and lack of effort: if no effort is required to violate
architectural integrity, sooner or later it will be violated." This is the nearest Pescio comes to
"encapsulation forces placement": hiding moves new code to the unit that can reach the hidden
thing. It is stated for components and namespaces, as a design anecdote, not for private fields,
and not measured.

**Distance and coupling (Ch. 8, August 2010).** "coupling must decrease as distance increases ...
small distance requires high coupling ... the code should go where the coupling is stronger ...
That's basically why feature envy is considered a bad smell". "Gravity works to minimize distance,
but in a kind of piecemeal, local minimum way." Private functions in a class may be tightly tied
to their callers: "That's why the class exists in the first place".

**Entanglement (Ch. 12, November 2010; Ch. 13, January 2011).** "Two clusters of information are
entangled when performing a change on one immediately requires a change on the other", refined to
C/R/U/D on one requiring C/R/U/D on the other. Not coupling: "Many systems that would be defined
as 'loosely coupled' are indeed 'heavily entangled'". Connascence named as the closest prior.
"it's easy to classify entanglement as an attractive force. This is an oversimplification". Rejects
grading coupling or connascence by strength: "The safest entanglement is the one with the minimum
likelihood of occurrence."

**Placement redistributes a fixed amount (Ch. 13).** On moving from a switch over a type to
polymorphic classes: "Object-oriented polymorphism 'works' because it changes the gravitational
centers ... Note that we don't really change the mass of code. We just organize it differently,
around different gravitational centers ... The area of the boxes (the amount of code) does not
change." A one-paragraph remark, not developed or measured.

**The Enumeration Law (Ch. 14, February 2011).** "every artifact ... that is enumerating over the
members of set by name is U-U entangled with that set". Example: `Person.Validate` uses its own
class's fields one by one, so adding a field forces a change to `Validate`; "moving portions of
Validate into sub-functions wouldn't make any difference". Code bound to a class's data set grows
with that set.

**Unstable sets in one class (Ch. 16, May 2012).** "if you map an unstable set into a single
software element, that element will be unstable as well"; recommends splitting by inheritance
("what is one must become many"), and calls `Person` with an open set of attributes "an unstable
center".

**Encapsulation as change locality ("Ask not what an object is", December 2012).** Defines an
object-oriented structure as one that, over a set of likely changes, "minimizes the total size of
the artifacts you have to update". "most OO languages have a notion of public and private ... You
can easily see those notions as ways to limit the potential impact of a change. Theoretically, if
a Change requires an Update of a Private part, that change will be local ... If you expose the
private part through a Get/Set, the Update won't be local anymore". Also argues that exposing a
stable abstraction's data (a bounding box) is harmless: "a 'violation of encapsulation' ... is the
kind of primitive and limited reasoning that principles tend to inspire".

**Setters as "sub-gravitational centers"** ("Episode 2", March 2012): "the various setXXX, since
those are the natural sub-gravitational centers in your design, where stuff happens and state is
updated."

**Force redefined (Forces 2024, draft).** A force is no longer a decision or a concern: "a change
in the decision set S induces a force", and "the force induced by a change in setting from S to S'
is the resistance to overcome to transform FR(S) into FR(S')" (p. 6). Pescio retires the words
force and decision for *delta* and *condition* (p. 18–19). Nothing in it on encapsulation,
gravity, size or coupling as quantities.

**Independent of the actor (Forces 2024, pp. 14–15).** "The need to separate an intrinsic property
of the artifact, or an intrinsic force acting on the artifacts, from the actor performing the
change and their efficiency will become more and more central as we move toward artificial actors
creating and maintaining software." "none of the forces that can be actually observed ... will
change at all: only the efficiency of carrying out some work can be impacted by changing the
actor."

**Measurement.** None anywhere. Ch. 8: distance is ordinal, "you can do no math with it". The
2019 note lists "Most of the literature on metrics" among "Failed Attempts" and points to
representational measurement theory. The 2016 compressive-strength draft sketches a measurement
of one property (K) but has no data.

## Bearing

- *Gravity*: Pescio's gravity is attraction **by size** (mass), self-reinforcing, at every scale;
  later reinterpreted by him as an effect of co-change (temporal and spatial entanglement). That
  is the preferential-attachment reading the plan treats as H2's rival, and the "as first
  registered" H1 (bindings rise with host size). It is not H2's core (later code returns to the
  values earlier code was bound to, with host size held fixed). The plan's name is his word with
  a different mechanism; the citation must say which.
- *Encapsulation as a force*: not proposed. In Ch. 1 access protection is a separating mechanism
  (against gravity); in Forces 2024 a force is resistance to a change of setting. Two pieces come
  close: the DSM post (hiding decides which unit new code is "attracted" to, by convenience) and
  "Ask not" (a change to a private part stays local, exposing it via get/set spreads the update).
  Together these anticipate the *concentration/dispersion* consequence of encapsulation in
  argument form, for likely changes, without measurement or a forced/chosen classification.
- *H5 (choice narrows)*: not anticipated; nothing on the number of places that could hold a change.
- *H7 (forced changes couple)*: the "Ask not" passage is the closest: widening (get/set) turns a
  local update into a non-local one. Argument only.
- *H6*: Pescio separates entanglement from structural coupling and says co-change is the real
  phenomenon; that agrees with the plan's reading that co-change spread and the force are
  different things, but he would read co-change (entanglement) as the *cause* of gravity, which
  is the opposite emphasis from H6's "spread does not see it".
- *Conservation*: Ch. 13's "we don't really change the mass of code ... The area of the boxes
  does not change" is an informal precedent for "the problem fixes the amount, placement
  redistributes it". Cite as such.
- *Regardless of author*: Forces 2024 states as a principle that forces are properties of the
  artefacts and the actor (human or AI) changes only efficiency. A prior statement of the framing;
  untested.
