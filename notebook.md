# Project notebook
## Project initiated by Hugo Castaneda - 07/11/2019
### System allowing easy multi layer abstraction representation of a sequence process (content, rules for generating content, etc.)

---
## Goal

The main goal of this project is to propose an architecture in which it is possible to represent information on a multi-dimensional abstraction manner.

Thoses representations from the content of the entity to the logic understanding of its very existance would allow machines to learn more deeper representation and comprehension about the generation of such entities.

One big question leading to this project comes from the threshold beetween physical learning and cognitive learning. Physical learning can be seen as the evolution of a brain neuronal structure through a species. Coginitive learning is the understanding and comprehension of the world and its functionning using only this neural structure to encode new data. The question is:
 * where is this threshold ?
 * what is the most abstract representation we can understand about something ?
 * is there an actual limit ?

---
## Actions

This capacity of level of comprehension can be seen as the "intelligence level" of the system. The more it can abstract the representation, the more intelligent it is.

For this project, one question is: will this representation be manual: you give the knowledge and it learns to generate it or will it be learnt automatically. One good answer would be to create an hybrid system to be able to give knowledge to it and to let it learn by itself. But this answer forces us to consider to learn abstract representation.

---
## Thought examples

 * Sequence : `abcabcabcabcLLLOOOLLLdefdefdefdefLLLOOOLLL`
 * Recurent episodes : `abc` x 4, `def` x 4, `LLL` x 4, `OOO` x 2
 * Generation rules : 4 x `abc`, `ITEM`, 4 x `def`, `ITEM` with `ITEM = LLLOOOLLL`
 * `pattern #0` : generate 3 random items
 * `pattern #1` : generate 3 same items
 * `pattern #2` : `my_pattern` = `[pattern #0]` & `my_pattern` x 4
 * `pattern #3` : `pat1` = `[pattern #1]` & `pat2` = `[pattern #1]` & `pat1 pat2 pat1`
 * `pattern #4` : `[pattern #2]` , `[pattern #3]`
 * `pattern #5` : `[pattern #4]` x 2

At first, the system should re-generate the sequence when only one is given, if a second one is given, it should be able to generalize the rules.

The first step is to try to compress the data

 * Seq 1 : `aaaBBBBaaaBBBB`
   * compression 1 : `a` x 3, `B` x 4, `a` x 3, `B` x 4
   * compression 1 ids : `r1`, `r2`, `r1`, `r2`
   * compression 2 : `r1 -> r2` x 2
   * compression 2 ids : `R1`
 * Seq 2 : `sssFFFFsssFFFF`
   * compression 1 : `s` x 3, `F` x 4, `s` x 3, `F` x 4
   * compression 1 ids : `r1`, `r2`, `r1`, `r2`
   * compression 2 : `r1 -> r2` x 2
   * compression 2 ids : `R1`

Let's compare the rules:
 * `Seq1.r1` = `Seq2.r1` --> `[ FAIL ]`
   * Generalize the rules : `(a or s)` x 3
 * `Seq1.r2` = `Seq2.r2` --> `[ FAIL ]`
   * Generalize the rules : `(B or F)` x 4
 * `Seq1.R1` = `Seq2.R1` --> `[ PASS ]`

The final rules are:
 * `r1` : `(a or s)` x 3
 * `r2` : `(B or F)` x 4
 * `R1` : `r1 -> r2` x 2