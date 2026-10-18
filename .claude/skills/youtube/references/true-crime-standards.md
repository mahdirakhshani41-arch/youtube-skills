# True-crime standards (Detective Noir)

Defines the IDs, vocabulary, registers and safeguards for true-crime work. Other files
link here and must not redefine these terms. Rules for the installed skills
`source-verification`, `doublecheck` and `humanizer` are in `verification-skill-rules.md`.

## 1. IDs

| Object | Format | Example | Rule |
|---|---|---|---|
| Episode | DN### | DN007 | Never reused |
| Narration segment | N#### + space tag | N0310 · case | Tag `case` (real events) or `frame` (the narrator's world) |
| Claim | C-### | C-012 | One row per checkable statement |
| Source | SRC-### | SRC-004 | One row per document, article, recording or post |
| Source cluster | SCL-## | SCL-02 | All sources that trace back to one origin |
| Person | P-## | P-03 | Every named or identifiable person |
| Script revision | r# | r2 | A new revision for every approved change |

- IDs identify; they do not order. Never renumber or reuse an ID. Number in steps of
  10 so an insert fits between two IDs (N0315).
- Prefix the episode for cross-episode references: `DN007:C-012`.
- The master script cites claims inline as `[^C-012]`. The voice-over script strips
  the markers; nothing else changes.

## 2. Sources

### Tiers
- **T1 primary record**: court record or judgment, inquest finding, official statement,
  official report, legislation.
- **T2 original reporting**: first-hand reporting by a named reporter or outlet that
  names or describes its sourcing.
- **T3 derivative**: aggregators, wikis, summaries, and reporting that repeats others.
- **T4 lead only**: forums, social posts, podcasts, unsourced pages.

### Clusters and independence
- A cluster (SCL) is every source that traces back to one origin: one wire story, one
  anonymous source, one press release, or articles that cite each other.
- Count corroboration in clusters, never in articles. Five outlets repeating one
  anonymous source are one cluster.
- T3 and T4 sources never count as corroboration. Use them to find better sources.
- Record when a later source strengthens a claim beyond its origin (for example, "a
  source said" becoming "police confirmed"). The stronger wording is not supported.

### Official records: what each can establish
"Official" means obtained from the court, coroner or official publisher, with its
provenance recorded. A source can establish only what it explicitly states.

| Source | Tier / class | Can establish | Cannot establish |
|---|---|---|---|
| Court judgment published by the court | T1 | The outcome, orders, and the court's own findings | That allegations or evidence it records are true, beyond its findings |
| Official court-issued summary | T1 | The outcome and any finding it explicitly states | Details it does not contain; exact testimony unless quoted |
| Official inquest finding or summary | T1 | The conclusion, cause and time of death, and other findings it states | Criminal guilt; how the death happened beyond its findings |
| A party's case (prosecution, defence, police theory) | ALLEGATION | That the party asserted it | That it happened |
| Witness evidence recorded in a record | TESTIMONY | That the witness said it | That it is true |
| Reporting about a record | T2 or T3 | That the outlet reported it | The record's content, unless it quotes the record; check the record itself |
| Unofficial summary (wiki, aggregator, blog) | T3 | Nothing on its own | — |

## 3. Claim class: what kind of statement it is

| Class | Meaning | Required wording |
|---|---|---|
| FACT | Established by a T1 record, or by at least two independent T2 clusters | Plain statement |
| ALLEGATION | Asserted by a party (prosecution, police, accuser, defence) and not established | Attributed: "Prosecutors alleged…", "Police said they believed…" |
| TESTIMONY | What a witness said in court or to investigators | Attributed: "X testified that…", "X told police…" |
| STATEMENT | A public or official statement outside court | Attributed: "Police said…" |
| DISPUTED | Credible sources conflict and no T1 record settles the point | Both versions, each with its source |
| UNKNOWN | No reliable source establishes it | "It is not known…", or omit |
| INTERPRETATION | An inference, by us or by a named source | Marked as inference, with its basis |
| FRAME | The narrator's fictional world; says nothing about the real case | See 7.2 |

Rules:
- A court outcome recorded in a T1 record is a FACT about the outcome. It is never
  DISPUTED and never presented as one side of a debate. If people disagree with a
  verdict, state the verdict first as fact, then report the disagreement as an
  attributed STATEMENT or INTERPRETATION.
- A verdict or inquest finding establishes the outcome and the findings it states, not
  every underlying detail. Attribute findings to the court or coroner ("the jury
  convicted…", "the coroner found…"). Underlying facts keep their own class: FACT only
  if independently established, otherwise ALLEGATION, TESTIMONY or UNKNOWN.
- TESTIMONY establishes only that the words were said. Conflicting testimony with no
  T1 resolution is DISPUTED.
- UNKNOWN is stated or omitted, never filled with a likely guess.

## 4. Verification status: how well a claim is supported

| Status | Rule | Publishable |
|---|---|---|
| VERIFIED-PRIMARY | Supported by a T1 record, with a pinpoint | Yes |
| VERIFIED-INDEPENDENT | Supported by at least two independent T2 clusters | Yes |
| SUPPORTED-LIMITED | One T2 cluster, or an unofficial summary of a T1 record | Only with attribution |
| UNRESOLVED | No adequate support found | No |
| CONTRADICTED | Conflicts with a T1 record | No; correct it |
| FABRICATION-RISK | A quote, citation or document that cannot be found | No; remove it |
| INAUTHENTIC | The source itself is fake or altered | No; remove the source |

A material claim about a real, identifiable person must be VERIFIED-PRIMARY or
VERIFIED-INDEPENDENT, or be worded as an attributed ALLEGATION, TESTIMONY or STATEMENT
that is itself verified.

## 5. Legal status

Record one entry per person and offence: P-##, offence, status, the jurisdiction's own
term (verbatim), as-of date, and source (SRC-###).

Person-level values: NOT-SUSPECTED, QUESTIONED, PERSON-OF-INTEREST (only when the
authorities used that term), ARRESTED, RELEASED-WITHOUT-CHARGE, CHARGED, ON-TRIAL,
MISTRIAL, PLEADED-GUILTY, CONVICTED, ACQUITTED, CHARGES-DROPPED, UNDER-APPEAL,
CONVICTION-OVERTURNED, RETRIAL-ORDERED, PARDONED-OR-EXONERATED, DIED-BEFORE-VERDICT.
Case-level values: SOLVED-BY-CONVICTION, UNSOLVED.

| Status | Say | Never say |
|---|---|---|
| ARRESTED | "was arrested on suspicion of…" | "was charged", "the suspect who killed…" |
| RELEASED-WITHOUT-CHARGE | "was released without charge" | anything implying guilt |
| CHARGED | "was charged with…" | "was convicted", "the killer" |
| CONVICTED | "was convicted of [offence]" | a different or broader offence |
| ACQUITTED | "was found not guilty of [offence]" | "got away with it", any implied guilt |
| CONVICTION-OVERTURNED | "the conviction was overturned in [year]" | "the convicted killer" |
| UNSOLVED | "no one has been convicted", with the as-of date | "the killer was never caught" if no one is proven to be a killer |

- The prosecution's case is always ALLEGATION.
- Never describe an acquitted, uncharged or unconvicted person as having done the act.

## 6. Registers (per episode)

- **sources.md**: SRC, title, publisher, author, published date, accessed date, URL,
  tier, cluster (SCL), derived from, notes. Archive links only with the user's approval.
- **claims.md**: C, exact claim, class, status, sources with pinpoint (page, paragraph or
  a short excerpt), independent-cluster count, conflicts, as-of date, segments using it
  (N####), last checked.
- **persons.md**: P, full name and aliases, disambiguators (age or birth year, place,
  role, case), living or deceased, minor at the time (yes/no), legal-status entries.

## 7. Safeguards

### 7.1 People with the same name
- A source counts for a person only if it matches at least two disambiguators from
  persons.md besides the name.
- Web searches include case context (place, year, court or case number), never a name
  alone.
- Discard results about other people with the same name and log them in the claim's
  notes. Never import a fact from them.
- Flag common names, and any second person with the same name connected to the case.

### 7.2 Narrator limits
- `frame` segments may describe the narrator's world (the office, the file, the city)
  and read the public record aloud ("The court record says…").
- In every segment, the narrator never claims to have been present, to have
  interviewed or spoken with anyone ("I sat down with", "told me", "my source"), to
  hold non-public evidence, or to know anything the sources do not establish.
- A `frame` segment makes no factual claim about the real case. Move such a claim to a
  `case` segment and give it a C-### marker.

### 7.3 Legal status freshness
- Every legal-status entry has an as-of date.
- Re-check legal status, including searches for later appeals, retrials, releases,
  deaths and pardons, at script approval and again within 7 days before publication.
- Wording that could go out of date carries its date: "As of October 2026, no one has
  been charged."
- The video description states: "Information correct as of [date]."

## 8. Uncertainty is part of the story
- A case does not need to be solved, fully documented, or free of contradictions.
  Unanswered questions, credible sources that disagree, and unknown or disputed details
  are not grounds to reject a case.
- Recommend rejecting a whole case only when its central narrative rests on unsupported
  allegations or unreliable sources, a risk to an identifiable person cannot be
  mitigated, or a stated editorial or legal constraint applies. Name the reason.
- For an unresolved claim, use the narrowest response that works, in this order:
  verify it; attribute it (if the attribution is supported); present the competing
  accounts with their limits; label it UNKNOWN or DISPUTED; omit only that detail.
- Conflicting accounts: record each account with its source and supporting evidence,
  and where they conflict. Look for stronger or later evidence. If the conflict stays
  unresolved, keep the accounts in the narrative and say what the evidence cannot
  establish. Never prefer an account because more outlets repeat it (count clusters),
  and never present accounts as equally credible when their support differs.
- For each significant uncertainty, record: what is uncertain; which sources support
  each account; how reliable and independent they are; what we can tell the audience;
  and what stays unresolved in the narration.
- State the limits of the evidence once, where they matter, not as a run of disclaimers.
