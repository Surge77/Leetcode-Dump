# 🔹 System Design (HLD) Basics

For SDE-1/SDE-2 rounds: a repeatable 45-minute structure, the building blocks with their trade-offs, the numbers to estimate with, and three worked sketches. Interviewers grade the *reasoning*, not a "correct" diagram.

## 🔹 The 45-Minute Structure

1. **Requirements (5 min).** Functional: the 3–4 core features, said back. Non-functional: scale (users, QPS), latency, availability vs consistency, durability. Write down what is **out of scope**.
2. **Estimates (5 min).** QPS (average and peak ≈ 2–3×), storage per day/year, bandwidth, read:write ratio. Round hard; the point is to find what dominates.
3. **API (5 min).** 3–5 endpoints with inputs and outputs, e.g. `POST /urls {long} → {short}`, `GET /{code} → 301`.
4. **Data model (5 min).** Entities, keys, access patterns → SQL or NoSQL, and the partition key.
5. **High-level design (10 min).** Client → load balancer → stateless services → cache → database, plus queues and object storage where needed. Walk one request end to end.
6. **Deep dives (10 min).** The 1–2 hardest parts: hot keys, fan-out, consistency, ID generation, failure handling.
7. **Wrap-up (5 min).** Bottlenecks, single points of failure, monitoring, what you'd do at 10× the scale.

## 🔹 Numbers to Estimate With

| | |
|---|---|
| 1 day | ≈ 86,400 s ≈ 10⁵ s, so 1 M requests/day ≈ 12 QPS |
| Memory read / SSD read / same-DC round trip / cross-continent | ~100 ns / ~100 µs / ~0.5 ms / ~150 ms |
| One server | ~10k simple QPS for a cache, ~1k for a web app, a few k writes/s for a relational database |
| Char / int / UUID / tweet-sized row | 1 B / 4–8 B / 16 B / ~300 B |
| Availability | 99.9% ≈ 8.8 h down a year; 99.99% ≈ 53 min |

## 🔹 Building Blocks and Their Trade-offs

* **Load balancer**: spreads traffic across stateless servers; health checks remove dead ones. L4 (fast) vs L7 (routes by path or header).
* **Cache** (Redis, Memcached): cache-aside (app reads the cache, on a miss reads the DB and fills the cache) is the default. Choices: TTL, LRU eviction, write-through vs write-back, invalidation on write. Failure modes: **stampede** (many misses at once → request coalescing, jittered TTLs) and **hot keys** (→ local cache, replicate the key).
* **Database**:
  * *Relational* (PostgreSQL, MySQL): transactions, joins, strong consistency; scale reads with replicas, writes with sharding.
  * *Key-value / wide-column* (DynamoDB, Cassandra): huge write throughput, predictable lookups by key; design tables around queries.
  * *Document* (MongoDB): flexible schema per record. *Search* (Elasticsearch): full-text and faceted search.
* **Replication**: leader–follower (reads scale, followers lag → read-your-writes issues), multi-leader, leaderless with quorums (`R + W > N`).
* **Sharding**: by hash (even spread, no range scans) or by range (range scans, hotspot risk). **Consistent hashing** moves only ~1/N of the keys when a node joins or leaves. Re-sharding and cross-shard queries are the costs.
* **Indexes**: B-tree for range and equality; each index speeds reads and slows writes.
* **Message queue / log** (Kafka, SQS, RabbitMQ): decouple producers from consumers, absorb spikes, retry failures. At-least-once delivery means consumers must be **idempotent**.
* **Object storage + CDN** for blobs (images, video): store metadata in the DB, bytes in S3-like storage, serve through the CDN.
* **Rate limiter**: token bucket (allows bursts) or sliding window, usually in Redis at the gateway.
* **IDs**: UUIDs (no coordination, not sortable), Snowflake-style 64-bit (timestamp + machine + sequence, roughly time-sortable), or a DB sequence (simple, but a bottleneck).

## 🔹 Concepts Interviewers Probe

* **CAP**: during a network partition you choose consistency (refuse some requests) or availability (serve possibly stale data). **PACELC** adds: even without a partition, you trade latency against consistency.
* **Consistency levels**: strong, read-your-writes, monotonic reads, eventual. Pick the weakest the feature tolerates: likes can be eventual, payments can't.
* **Idempotency keys** make retries of `POST /payments` safe: the server stores the key and returns the first result for duplicates.
* **Back-pressure and timeouts**: every remote call needs a timeout, bounded retries with exponential backoff + jitter, and a circuit breaker so a slow dependency doesn't take you down.
* **Fan-out on write vs on read** (feeds): precompute every follower's timeline (fast reads, expensive for celebrities) vs assemble at read time (cheap writes, slow reads). The usual answer is hybrid: push for normal users, pull for accounts with huge follower counts.
* **Observability**: metrics (RED: rate, errors, duration), structured logs, traces, alerts on symptoms users feel.

## 🔹 Worked Sketch 1: URL Shortener

* **Scale**: 100 M new URLs/month (~40 writes/s), 100:1 reads (~4k reads/s, peak 10k). 5 years ≈ 6 B rows × ~500 B ≈ 3 TB.
* **API**: `POST /urls {long_url} → {code}`; `GET /{code}` → `301`/`302` redirect (302 if you want to count clicks).
* **Code**: base62 of a 64-bit ID from a distributed ID generator; 7 chars = 62⁷ ≈ 3.5 × 10¹² codes. Hashing the URL instead needs collision handling.
* **Storage**: key-value table `code → long_url, created, owner`, sharded by `code`.
* **Reads**: cache-aside on `code` (redirects are very hot and immutable, so cache hit rates are high), CDN for the most popular.
* **Deep dives**: custom aliases (uniqueness check), expiry (TTL plus lazy delete), analytics (write a click event to a queue, aggregate asynchronously, never on the redirect path).

## 🔹 Worked Sketch 2: Chat (1:1 and groups)

* **Connections**: clients hold WebSockets to chat servers; a connection registry (Redis: `user → server`) tells you where to deliver.
* **Send path**: client → chat server → assign a per-conversation sequence number → persist (wide-column store keyed by `(conversation_id, seq)`) → look up recipients' servers → push. Offline recipients get a push notification; on reconnect the client fetches messages after its last seen `seq`.
* **Ordering and duplicates**: a per-conversation sequence gives ordering; client-generated message IDs make retries idempotent.
* **Groups**: fan out to members on write for small groups; large channels are read on demand.
* **Presence**: heartbeats with TTL keys; broadcast changes only to contacts who are online.

## 🔹 Worked Sketch 3: Rate Limiter

* **Where**: at the API gateway, keyed by user ID or API key (by IP for anonymous users).
* **Algorithm**: token bucket per key, with `capacity` and a `refill_rate`. Store `(tokens, last_refill)` in Redis and update it atomically with a Lua script or `MULTI`. Sliding-window counters are the alternative when bursts must be smoothed.
* **Response**: `429` with `Retry-After` and `X-RateLimit-Remaining` headers.
* **Failure**: if Redis is down, fail open (availability) or closed (protection), and say which you chose and why.
* **Distributed accuracy**: a local in-memory bucket per node, synced periodically, trades exactness for latency.

## 🔹 How to Practise

* Say each sketch aloud with a 45-minute timer, drawing boxes on paper.
* For every component you add, state the trade-off you're making ("cache-aside, so a write must invalidate the key").
* Your own projects are design stories too; see [Projects.md](Projects.md). Uptick's quorum probing and incident model and Citewise's retrieval pipeline are real design decisions you can defend.
