# 🔹 DBMS and OS Essentials for the Infosys Technical Interview

Short, exam-ready answers. Practice saying each one aloud in under a minute.

## 🔹 DBMS

### Keys
* **Super key:** any set of columns that uniquely identifies a row.
* **Candidate key:** a minimal super key (no column can be removed).
* **Primary key:** the candidate key chosen to identify rows; unique and not `NULL`.
* **Foreign key:** references a key in another table; enforces referential integrity.

### Normalisation
| Form | Rule | Fixes |
|---|---|---|
| **1NF** | Every column holds atomic values; no repeating groups | `phones = "98…, 99…"` in one cell |
| **2NF** | 1NF + no **partial** dependency (non-key columns depend on the *whole* composite key) | `(student, course) → student_name` |
| **3NF** | 2NF + no **transitive** dependency (non-key → non-key) | `emp → dept_id → dept_name` |
| **BCNF** | For every dependency `X → Y`, `X` is a super key | rare edge cases 3NF allows |

*Why normalise:* removes redundancy and update/insert/delete anomalies. *Why denormalise sometimes:* fewer joins for read-heavy reporting.

### Transactions — ACID
* **Atomicity:** all statements of a transaction happen, or none do (rollback).
* **Consistency:** a transaction moves the database from one valid state to another (constraints hold).
* **Isolation:** concurrent transactions do not see each other's partial work.
* **Durability:** once committed, data survives crashes (write-ahead log).

### Isolation levels and the anomalies they allow
| Level | Dirty read | Non-repeatable read | Phantom read |
|---|---|---|---|
| Read Uncommitted | possible | possible | possible |
| Read Committed | — | possible | possible |
| Repeatable Read | — | — | possible (per the SQL standard) |
| Serializable | — | — | — |

### Indexes
* Usually a **B+ tree**: point lookups in `O(log n)`; range scans and ordered reads in `O(log n + k)` for `k` rows returned.
* **Clustered index:** the table rows are stored in index order (one per table, often the primary key). **Non-clustered:** a separate structure pointing to rows (many per table).
* Cost: extra storage and slower `INSERT`/`UPDATE`/`DELETE`. Don't index small tables or columns with very few distinct values.

### Other favourites
* **`DELETE` vs `TRUNCATE` vs `DROP`** — see [SQL.md](SQL.md#-quick-theory-answers).
* **Joins** — `INNER`, `LEFT`, `RIGHT`, `FULL`, `CROSS`, self join (examples in [SQL.md](SQL.md)).
* **Views:** saved queries; **materialised views** store the result and must be refreshed.
* **Stored procedure vs function:** a procedure performs actions and may return several results; a function returns a single value and can be used inside queries.
* **SQL vs NoSQL:** fixed schema + joins + strong consistency vs flexible schema + horizontal scaling (document, key-value, column, graph stores).

## 🔹 Operating Systems

### Process vs thread
* **Process:** a program in execution with its **own** address space; switching between processes is relatively expensive.
* **Thread:** a unit of execution **inside** a process; threads share the process's memory (heap, globals) but each has its own stack and registers — cheaper to create and switch, but shared data needs synchronisation.

### CPU scheduling
| Algorithm | Idea | Watch out for |
|---|---|---|
| FCFS | first come, first served | convoy effect (short jobs wait behind long ones) |
| SJF / SRTF | shortest job (remaining time) first | optimal average waiting time, but starvation of long jobs |
| Round Robin | fixed time quantum, cycle through ready jobs | quantum too small → too many context switches |
| Priority | highest priority first | starvation → fix with **aging** |

### Deadlock
* **Four necessary conditions (Coffman):** mutual exclusion, hold and wait, no preemption, circular wait. All four must hold.
* **Prevention:** break one condition (e.g., acquire locks in a fixed global order → no circular wait).
* **Avoidance:** grant a request only if the system stays in a safe state (**Banker's algorithm**).
* **Detection & recovery:** find cycles in the wait-for graph, then abort or preempt.

### Synchronisation
* **Mutex:** a lock with an owner; only the thread that locked it unlocks it; one thread in the critical section.
* **Semaphore:** a counter; `wait()` decrements (blocks at 0), `signal()` increments. A counting semaphore allows `n` concurrent users; a binary semaphore behaves like a lock without ownership.
* **Race condition:** the result depends on the timing of threads touching shared data.

### Memory
* **Paging:** memory split into fixed-size pages/frames → no external fragmentation, some internal fragmentation.
* **Segmentation:** variable-size logical segments (code, stack, heap) → external fragmentation.
* **Virtual memory:** processes see a large private address space; pages are loaded on demand (page fault when missing).
* **Page replacement:** FIFO (can suffer Bélády's anomaly), LRU (good approximation of optimal), Optimal (evict the page used farthest in the future — theoretical benchmark).
* **Thrashing:** the system spends more time swapping pages than executing, because processes' working sets do not fit in memory.

### Misc
* **Context switch:** saving one task's registers/state and loading another's — pure overhead.
* **Kernel vs user mode:** privileged instructions run only in kernel mode; system calls are the gateway.
* **Starvation vs deadlock:** starvation = a task waits indefinitely while others progress; deadlock = a set of tasks wait on each other and none progress.
