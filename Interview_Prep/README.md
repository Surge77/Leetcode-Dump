# 🔹 Interview Prep Beyond DSA

Everything an SDE interview loop asks besides LeetCode-style coding. Each page is written to be said aloud: short answers, then the follow-ups interviewers ask.

| Round | What it tests | Page |
|---|---|---|
| **Coding (DSA)** | 1–2 problems live, explained as you go | the notes ([INDEX.md](../INDEX.md)) + the [mock interview protocol](Mock_Interview.md) |
| **Machine coding / LLD** | working, extensible code in 60–120 min | [Low_Level_Design.md](Low_Level_Design.md) · OOP and SOLID in [OOP.md](OOP.md) |
| **System design (HLD)** | building blocks, trade-offs, estimates | [System_Design.md](System_Design.md) |
| **CS fundamentals** | DBMS, OS, networks | [DBMS_and_OS.md](DBMS_and_OS.md) · [Computer_Networks.md](Computer_Networks.md) |
| **SQL** | queries on the spot | [SQL.md](SQL.md) (every query verified on SQLite) |
| **Language** | why your code is fast or slow in Python / Java | [Language_Internals.md](Language_Internals.md) |
| **Projects** | the deep dive on what you built | [Projects.md](Projects.md) |
| **Behavioral / HR** | ownership, failure, conflict, judgement | [Behavioral.md](Behavioral.md) |

## 🔹 Infosys SP / DSE Technical Interview

After the online test ([Infosys_SP_DSE](../Infosys_SP_DSE/README.md)), shortlisted candidates face a technical interview and then HR. Public 2025–2026 reports describe the technical round as:

* **2 DSA problems** (Easy–Medium), solved live on a shared screen → the 🔄 notes, out loud, with the [mock interview protocol](Mock_Interview.md).
* **OOP** concepts with code → [OOP.md](OOP.md)
* **DBMS + SQL queries** → [SQL.md](SQL.md) and [DBMS_and_OS.md](DBMS_and_OS.md)
* **OS basics** (occasionally) → [DBMS_and_OS.md](DBMS_and_OS.md#-operating-systems)
* **Your resume and projects**, plus scenario questions → [Projects.md](Projects.md)

> Sourced from unofficial guides and candidate reports; the exact mix varies by interviewer and drive. Infosys's own most-asked LeetCode list (including SQL problems) is in [COMPANIES.md](../COMPANIES.md#infosys).

## 🔹 Live-Coding Habits

* Restate the problem and confirm the input/output format before coding.
* Say the brute force and its complexity first, then optimise.
* Walk through a small example and one edge case (empty input, single element, duplicates) before declaring it done.
* Name variables clearly; interviewers read your code while you type.
