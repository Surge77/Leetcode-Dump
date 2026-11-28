# 🔹 Project Deep Dives

"Walk me through a project" is in almost every round, and the follow-ups go as deep as you let them. For each project, know the **one decision that matters**, **the numbers**, **what broke**, and **what you'd change**. The facts below come from each project's public README; the blanks are yours to fill.

## 🔹 The 2-Minute Shape

1. **Problem**: who has it and why it matters (one sentence).
2. **What I built**: the main components, and *my* part.
3. **The hard decision**: the alternatives and why I chose mine.
4. **Proof it works**: tests, measurements, users, a demo.
5. **What I'd change next.**

Then expect: *why this database / library?*, *what happens when X fails?*, *how would it handle 10× the load?*, *what was the hardest bug?*

## 🔹 strata: LSM-tree storage engine (C++20)

**Pitch:** an embeddable key-value storage engine built from first principles: write-ahead log with crash recovery, immutable SSTables, Bloom filters, leveled compaction, and durability proven by fault injection. Released as `v1.0.0-rc.1` after 16 phases.

**Numbers to quote:** 96.8% line coverage (100% on the log and the manifest); zero sanitizer findings under GCC and clang; each fuzz target clean for an hour. Every acknowledged write survives `kill -9`; every `sync = true` write survives power loss. Compression: snappy cut the footprint by 34% for 14–18% of throughput, zstd by 43% for 44–52%. Instrumentation costs about 3 ns per call.

**Questions to prepare:**
* Why an LSM tree instead of a B-tree? (Write-heavy workloads: sequential writes and batching vs read amplification. Know write, read and space amplification.)
* How does recovery work after a crash mid-write? What does the WAL guarantee, and when is `fsync` called? ("Every fsync proven load-bearing": how did you prove it?)
* What do Bloom filters save, and how do you size them (bits per key vs false-positive rate)?
* Leveled vs size-tiered compaction: what does each cost?
* The latency defect the open-loop benchmark found (WAL rotation fsyncing while holding the DB mutex): how you found it and the fix.
* Why the benchmark figures are reported as *not* meeting the 5% CV gate. (A strong honesty story: you published what actually ran.)

**My story notes:** *(the hardest bug; what you'd change; time it took)*

## 🔹 CollabBoard: real-time collaborative whiteboard with AI

**Pitch:** an infinite canvas where several people draw together with live cursors, plus AI that generates diagrams from a prompt and summarises the board. Next.js 16 (App Router) · React 19 · TypeScript strict · Tailwind v4 · Auth.js v5 (Google + GitHub OAuth) · Liveblocks for real-time sync · deployed on Vercel.

**The decision that matters:** it ships in two canvas variants, tldraw and Excalidraw. tldraw's Business Source License restricts commercial whiteboard products and its free tier renders a watermark, so the Excalidraw build (MIT) exists alongside it with the same auth, database, real-time layer and AI features.

**Questions to prepare:**
* How does real-time sync work? (Liveblocks rooms, presence vs storage, conflict resolution: what happens when two people move the same shape?)
* Why OAuth via Auth.js, and where are boards persisted?
* How do you test two-client real-time behaviour? (Two-client E2E tests.)
* How does the AI feature turn a prompt into shapes, and what stops it from producing garbage?
* What would change at 1,000 users per board?

**My story notes:** *(a production incident or bug and what you changed so it can't recur; the licence decision as a "trade-off" story)*

## 🔹 Citewise: answers from your PDFs, with the page to prove it (RAG)

**Pitch:** upload PDFs, ask a question, get a short answer where every claim cites its document and page, or a refusal when the documents don't contain the answer.

**Design decisions:** chunking on sentence boundaries that never crosses a page, so citations are exact. Hybrid search: embeddings for paraphrases plus BM25 for exact terms, merged by rank so the score scales never need to agree. A cross-encoder reranker. Refusal decided *before* the LLM call, so off-topic questions cost nothing and can't produce a made-up answer. A whole-library mode when everything fits in one prompt (60,000 characters), for "summarise this PDF" questions that search can't answer.

**Numbers to quote:** retrieval eval on 20 answerable + 6 off-topic questions. hit@1: meaning-only 0.90 → hybrid 0.70 → **hybrid + rerank 1.00**; MRR 0.93 → 0.82 → **1.00**; off-topic refused 1.00. Be ready to say why hybrid alone scored *lower* than meaning-only here, and why 26 questions on one 10-page PDF is a baseline, not a benchmark.

**Questions to prepare:** why rank fusion instead of adding scores; cross-encoder vs bi-encoder cost; how you'd evaluate the generated answers (faithfulness), not just retrieval; how it scales to 10,000 PDFs (an ANN index, metadata filters, async ingestion).

## 🔹 Uptick: distributed uptime monitoring

**Pitch:** probes from multiple regions, decides "down" by quorum, opens incidents instead of spamming alerts, and computes SLA from incident durations.

**Design decisions (each one a ready answer):**
* N consecutive failures before an incident: one blip is usually your network.
* Flapping detection collapses up/down storms into one incident.
* A dependency DAG pages once for the root cause, not for nine downstream services.
* Quorum: at least 2 of 3 regions must agree before declaring an outage.
* SLA from summed incident durations, not `passed / total` (that ratio breaks when the check interval changes).
* 30-day raw retention plus daily rollups; nothing user-facing reads raw checks.
* The status page is served from a *different failure domain* than the app.

**Questions to prepare:** how probes are scheduled and kept from drifting; exactly-once incident creation when two regions report at once; how you stop users pointing probes at internal addresses (SSRF and DNS rebinding); the data model for incidents and rollups.

## 🔹 Atelier: multi-agent DOCX/PPTX generator

**Pitch:** reads your Word and PowerPoint templates, researches the web and a knowledge base, and writes editable documents and decks in your template's own style, then keeps editing them in conversation without losing formatting.

**The decision that matters:** every artifact is a **content plan**; the DOCX/PPTX file is only a rendering of it. The renderer writes through the uploaded template's own styles, so fonts, colours and masters are inherited, never reconstructed. Edits are operations on the plan, document ↔ deck is a pure transform with no model call, and a version is a plan snapshot plus the operations that produced it.

**Questions to prepare:** how the agents divide the work and hand off; how you keep LLM output inside the plan schema; why local Chroma and local embeddings by default (no keys, privacy); how scanned PDFs are handled (a vision model; not available on every provider); what you'd do about cost and latency.

## 🔹 evalgate: pytest for AI quality

**Pitch:** an offline evaluation harness for LLM apps. It runs a golden dataset through your target, grades answers with rule checks and an LLM judge, and fails CI when quality drops below a promoted baseline.

**Numbers to quote:** 60 golden cases in 5 categories; demo accuracy 0.8667; a full offline run takes 1.3 s and costs $0; a sabotaged target drops accuracy to 0.0 and the gate exits 1; **judge–human agreement 92.2%** over 90 labels (±1 tolerance; faithfulness 93.3%, correctness 83.3%, relevance 100%). Four seeded flaws pass every rule check and are caught only by the judge's faithfulness score.

**Questions to prepare:** how you calibrated the judge against human labels and why ±1 tolerance; why rule checks *and* a judge; judge bias and variance (temperature 0, JSON mode, pinned models); how a baseline gets "promoted"; how this plugs into CI.

## 🔹 Template for Another Project

* **Pitch (one sentence):**
* **Stack:**
* **The decision that matters:**
* **Numbers:**
* **What broke and what I changed:**
* **What I'd do next:**
* **Questions I expect:**
