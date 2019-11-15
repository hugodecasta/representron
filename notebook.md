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
   * compression 2 : `r1 r2` x 2
   * compression 2 ids : `R1`
 * Seq 2 : `sssFFFFsssFFFF`
   * compression 1 : `s` x 3, `F` x 4, `s` x 3, `F` x 4
   * compression 1 ids : `r1`, `r2`, `r1`, `r2`
   * compression 2 : `r1 r2` x 2
   * compression 2 ids : `R1`

Let's compare the rules:
 * `Sys.r1` = `Seq2.r1` --> `[ FAIL ]`
   * Generalize the rules : `(a or s)` x 3
 * `Sys.r2` = `Seq2.r2` --> `[ FAIL ]`
   * Generalize the rules : `(B or F)` x 4
 * `Sys.R1` = `Seq2.R1` --> `[ PASS ]`

The final rules are:
 * `r1` : `(a or s)` x 3
 * `r2` : `(B or F)` x 4
 * `R1` : `r1 r2` x 2

Now a third very different sequence appears:

 * Seq 3 : `aaabbbcccFFFaaabbbccc`
   * compression 1 : `a` x 3, `b` x 3, `c` x 3, `F` x 3
   * compression 1 ids : `r1`, `r2`, `r3`, `r4`
   * sub-seq : `r1 r2 r3 r4 r1 r2 r3`
   * compression 2 : `r1 r2 r3` & `r4` & `r1 r2 r3`
   * compression 2 ids : `R1`, `R2`, `R1`

Something interesting we can pull out from these examples is that we can distinguish 2 types of rules
 * The repetition rule : `a` x 3
 * The successing rule : `a -> b -> c -> ...`

As the begining sequence is only a repetition rule we can alternate the rule understanding by finding first the repetition, until no ne repetition exists, then find the succession, and repeat the process till no ne rule are added.

### repetition detection

 * Seq 1 : `coucou coucou`
   * repetition : `coucou` x 1 , `coucou` x 1
   * succession : `r1 -> r1`
   * repetition : `r1` x 2

Finally, the "succession" step is only a re-symbolisation of the sequence using the defined rules ids. The repetition step is in fact a step where the system find episodes in the segment. It must find rules linking those episods. One episod can be represented as an augmented network (graph).

 * Seq 1 : `coucou coucou`
   * episods : `-> c o u (restart x 2)`
   * re-sequence : `e1 e1`
   * episods : `-> e1 (restart x 2)`
   * re-sequence : `e2`

 * Seq 2 : `abcabcabcabcLLLOOOLLLdefdefdefdefLLLOOOLLL`
   * episods : 
     *  `-> a b c (restart x 4)`
     *  `-> L (restart x 3)`
     *  `-> O (restart x 3)`
     *  `-> L (restart x 3)`
     *  `-> d e f (restart x 4)`
     *  `-> L (restart x 3)`
     *  `-> O (restart x 3)`
     *  `-> L (restart x 3)`
   *  Findings : `e1 ~ e4` -> put in the same episod
      *  `e1 / e4 --> (a|d) (b|e) (c|f) (restart x 4) --> ee14`
   * re-sequence : `ee14 e2 e3 e2 ee14 e2 e3 e2`
   * episods : 
     * `-> ee14 e2 e3 e2 (restart x 2)`
   * re-sequence : `E1`

When trying to find equals episods it is important to look at the content and structure of those epidods. When joining them, we can add the two in a common network.

One first algorithm to do this could be the following:
``` python
  def analyse(sequence):
    history = list()
    while len(sequence) > 1:
      episods = find_episodes(sequence)
      sequence = rewrite(sequence, episods)
      history.append((episods,sequence))
    return history
```

### Finding episods

In order to find episods, the system can generate the augmented network representing the sequence. While generating this network it has to reduce the size of it by using switches by frequence.

Those switches work like stack with rules.

 * sequence : `abcabcabcLLLOLLL`
   * `a` :
     * `-> b`
     * `-> b`
     * `-> b`
   * `c` :
     * `-> a`
     * `-> a`
     * `-> L`

All node with a redondant stack or linear stack is a direct node. Here `a` is direct has every time it is encountered it goes to `b`.

An episod's ending node is a node with a unlinear stack. One first algorithm to detect episods could be the following:
``` python
  def get_epsiods(network):

    episods = list()
    current_episod = null_episod()

    for node in network:
      current_episod.append(node)

      if not node.is_direct:
        episods.append(current_episod)
        current_episod = null_episod()

```

Finaly the intuitive Idea of using the stack trace of a symbol to define wether it is the end of an episod or is contained is an episod is not relevant. Example with the sequence : `abcabcabcLLLOaOLLL`. The face that `a` can be alone does not mean that `abc` is not an episod.

### Another approach

Let's try the fondamental aspect of sequence analysis by ooking at each symbol in the sequence and storing recurrent episods.

 * Seq : `abcabcLLOaOLLabcabc`
   * episods :
     * `ab` x 4
     * `bc` x 4
     * `ca` x 2
     * ...
     * `abc` x 4
     * `bca` x 2
     * ...
     * `abca` x 2
     * `abca` x 2
     * ...
     * `abcabc` x 2

The question here is to find define what is a pertinent episod in order to keep only interesting episods. First, let's build a script creating all those episods.

The goal here is to delete episods having a "representative" in same or higher occurance counter. Example `ab` x 4 has a higher representative `abc` so `ab` is not a usefull episod. On an other hand a bigger episod appearing more and containing only this episod is just another assembly that can be seen in a higher analysis later. Example `abcabc` x 2 is not usefull visavi `abc` x 4 because it is an assembly of it and not a representative. In a later analysis, after the sequence rewriting, `abcabc` will be rewritter as `AA`.

### Finding/comparing episods

One important step is finding episods and comparing them. In order to do that, the system has to find relevant episods (maybe using the old technic) then merge them to find correlation/rules linking them.

A set of possible correlation rule will be given to the system to look for.

 * Seq : `abcLLOaOLLabc`
 * episods : `abc`, `LLO <--> OLL`, `a`
 * rewriting : `0,1,2,1r,0`
 * episods : `0,1 <--> 1r,0`, `2`
 * rewriting : `0,1,0r`

Maybe one of the good thing to do is identify episods separatly and after emit rules to link them in the sequence. Here the problem is that episod `0` of the second rewriting is ambiguous as it contains one `1` and the other is a `1r` wheras the `0`s are the same.

We need a way to fix this problem but still keep the generalisation process. For the moment, we will consider the reversed episods as distinct from the orginial ones.

A lot of episod rules will require to identify a source episod to refer to. For example, the reversed rule need a reference (`0` = `LLO` so the reverse is `0r`). But why would `OLL` be the reverse of `LLO` and not the reverse one ? The reason is that the first episod encountered is `LLO` so it is the source/leader of the rest. This is due to the fact that we estimate a sequence to have been written from the first symbol to the last one. If it is not the case, an ordering system will be needed to analyse symbols from their writting order.

Once an episod has been identified has part of a rule from an other episod, it is deleted an replaced by this rule. Finally a sequence can be rewritten as a set of rules.

 * rules:
   * writting : writte a sequence / episod
   * copy : copy a rule
   * inverse : inverse a rule

* Seq : `abLLOabOLLab`
  * identified rules:
    * `0` : `write(ab)`
    * `1` : `write(LLO)`
    * `2` : `copy(0)`
    * `3` : `inverse(1)`
  * rewritting : `01232`

In this form we can note that copying an element is very important and interesting. Later, if a new sequence appears, we can rewrite the rule `0` using a markov chain but still understand that we have to copy the generated sequence and not only re-use the generator wich might regenerate a different sequence.

But with this rewritting, we kind of lose the higher abstraction representation where `LLO` and `OLL` could be seen has the same episod. It would be good to have a higher representation inclusing this similarity so we could see `01010` instead of `O1232`. One solution could be to process episod on the content of the sequence but keep the ruling sequence as a second sequence and maybe also try to do episod processing on this sequence !