# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:** Each question is answered by one short reply inside one
thread, so the answer chunk should be findable. I allow one miss because
question 2 (the 4:30 sunset) is a single sentence at the end of a winter thread,
and questions 4 and 5 compete with near-duplicate threads (transfer credits vs
changing major, group project vs late work).

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** I mean answers the model actually generates, not gate
refusals, which have no source to name. It is 5 of 5 rather than 4 because the
grounding instruction already requires a file name and the output has a
"Source:" line. For it to fail, the model would have to ignore that instruction.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:** The gate is the only thing that stops a made-up answer to
an unanswerable question, so I want it strong. I allow one miss because a
question like the ibuprofen one could share vocabulary with student-life advice
threads and land inside the cutoff. I will check this against my real distances
in Milestone 4.

---

## 4. Something about your chunks

In every chunk in the index (listed with `python app.py chunks -n <total>`),
(a) none is shorter than 100 characters, (b) none ends mid-sentence, and
(c) every chunk contains the `THREAD:` title line of the thread it came from.

**Why this target:** The starter's fixed 800-character window cuts long threads
in the middle of a reply and leaves a 2-character fragment on this corpus. A
reply like "16 is the answer" means nothing without its thread title, so a
chunk that lost its title can't answer a question alone. I check every chunk,
not a sample, because the corpus is small and a single bad fragment is enough
to fail the target. 100 characters is roughly one short reply plus its title.

---

## 5. Your choice

For all 5 test questions, the file named on the answer's `Source:` line (not the
"Sources retrieved" list) is the file that contains my `expects` phrase:
thread_laptop_specs.txt (16GB), thread_winter_advice.txt (4:30),
thread_roommate_conflict.txt (mediation), thread_transfer_credits.txt
(staff change), thread_group_project.txt (individual grades).

**Why this target:** Criterion 2 only checks that a source is named, not that
it's the right one. The corpus has near-duplicate threads (transfer credits vs
changing major, group project vs late work), so a wrong citation is plausible,
and a confident wrong pointer is worse than a missed retrieval. I set it at
5 of 5 because each expects phrase appears in exactly one file, so there is no
legitimate ambiguity to excuse a miss.

---
<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
