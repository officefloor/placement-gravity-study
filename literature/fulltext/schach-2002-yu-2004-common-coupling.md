# Schach et al. (2002), Maintainability of the Linux kernel; Yu, Schach, Chen and Offutt (2004), Categorization of common coupling ..., IEEE TSE 30(10)

## Schach et al.

**Read in its technical-report form**, 22 November 2026: George Mason University ISE-TR-01-04,
"Maintainability of the Linux Kernel", 27 July 2001, 16 pp., from the Internet Archive copy (31
July 2024) of cs.gmu.edu/media/techreports/ISE-TR-01-04.pdf (the live copy is behind a cookie
wall). The published version (IEE Proceedings – Software, 2002) was not obtained; the venue and
year in LITERATURE.md remain unconfirmed against the publisher.

- 365 versions of Linux, 17 kernel modules; instances of common (global-variable) coupling between
  each kernel module and all other modules. Abstract: "the number of instances of common coupling
  grows exponentially with version number ... On the other hand, the number of lines of code in
  each kernel modules grows only linearly with version number."
- "We also ignored common coupling of constants" (§3).
- Clandestine coupling: "the number of instances of common coupling between module M and the other
  modules can change drastically, even if module M itself never changes" (e.g. `Panic.c` rising
  to 946 instances over versions 2.1.104–2.1.109 with no change to its code).
- On size and coupling (§2): "If there were no couplings at all in a software product then that
  product would consist of one large module, so some amount of coupling clearly is needed. That is,
  coupling is a necessary consequence of modularization."

Bearing: the size–coupling trade (one large module or coupling) is stated in passing as a
truism, the dispersion side of the study's "concentrate or disperse". The measure is exposure
growth (global data referenced by more modules), counted per version, which is H1's aggregate
analogue, not a per-change forced/chosen split. Constants were excluded, where the plan includes
private constants as forcing.

## Yu et al. 2004

**Not obtained** (IEEE TSE, no open copy found). Index record and abstract only, as before. A
critical reanalysis exists and was not read: Feitelson et al., "Fine-grain analysis of common
coupling and its application to a Linux case study", *JSS* 2007 (the author's copy at
cse.huji.ac.il returned an error page and no archived copy was found).
