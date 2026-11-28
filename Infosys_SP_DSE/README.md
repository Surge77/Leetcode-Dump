# 🔹 Infosys SP / DSE — Exam-Structured Practice

This folder organises the repo around the **Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)** online test: full mock tests in the exam's format, a judge that scores your own code, a Python contest template, and a map from each exam slot to the problems in this repo.

> The pattern below comes from public 2025–2026 candidate reports and prep guides, **not** an official Infosys document. Patterns change between hiring cycles — confirm against the notice for your drive.

---

## 🔹 Exam Structure

* **3 coding questions in 3 hours** — one Easy, one Medium, one Hard.
* **Languages:** C, C++, Java, Python (depends on the test portal).
* **Partial scoring by test cases** — a correct brute force that passes the small tests can earn roughly half the marks of a question.
* **Sectional cut-off for each question.**
* **One test, two outcomes:** roughly 2+ questions fully solved → SP interview; 1–1.5 → DSE.
* **After the test:** a technical interview (2 Easy–Medium DSA problems solved live, OOP, DBMS/SQL, your projects), then HR.

| Slot | Difficulty | What usually appears | Time to budget | Practise with |
|---|---|---|---|---|
| **Q1** | Easy | arrays, strings, hashing, counting, basic math | 20–30 min | Hashing, Prefix Sum, Sliding Window, Two Pointers, number-theory basics, Mock Q1s |
| **Q2** | Medium | DP (1D / knapsack / grid), greedy, BFS/DFS, binary search on answer | 50–60 min | DP folders, Greedy, Graph traversals, Modified Binary Search, Mock Q2s |
| **Q3** | Hard | 2D / bitmask / digit / tree DP, segment tree & Fenwick, advanced graphs, number theory with mod | rest (~90 min) | DP_Bitmask, DP_Digit, DP_On_Trees, Segment_Tree, Fenwick_Tree, Graph_* folders, Mock Q3s |

---

## 🔹 Mock Tests (original problems, exam format)

Every problem reads **stdin** and prints to **stdout** and has constraints that force the intended complexity. The problem files contain **only the statement**. Each one's brute force (partial score) and optimized solution, checked against each other on random inputs, are in that mock's `solutions/` folder.

| Mock | Q1 — Easy | Q2 — Medium | Q3 — Hard |
|---|---|---|---|
| **1** | [Festival Pairs](Mock_Test_1/Q1_Easy_Festival_Pairs.md) | [Lucky Subsets](Mock_Test_1/Q2_Medium_Lucky_Subsets.md) | [Stock Ticker Queries](Mock_Test_1/Q3_Hard_Stock_Ticker_Queries.md) |
| **2** | [Server Rack Shuffle](Mock_Test_2/Q1_Easy_Server_Rack_Shuffle.md) | [Toll Pass](Mock_Test_2/Q2_Medium_Toll_Pass.md) | [Treasure Route](Mock_Test_2/Q3_Hard_Treasure_Route.md) |
| **3** | [Special Numbers](Mock_Test_3/Q1_Easy_Special_Numbers.md) | [Factory Output](Mock_Test_3/Q2_Medium_Factory_Output.md) | [Smooth Numbers](Mock_Test_3/Q3_Hard_Smooth_Numbers.md) |
| **4** | [Balanced Segments](Mock_Test_4/Q1_Easy_Balanced_Segments.md) | [Rival Teams](Mock_Test_4/Q2_Medium_Rival_Teams.md) | [Gold Roads](Mock_Test_4/Q3_Hard_Gold_Roads.md) |
| **5** | [Coin Piles](Mock_Test_5/Q1_Easy_Coin_Piles.md) | [Price Spread](Mock_Test_5/Q2_Medium_Price_Spread.md) | [Critical Routers](Mock_Test_5/Q3_Hard_Critical_Routers.md) |
| **6** | [Festival Lamps](Mock_Test_6/Q1_Easy_Festival_Lamps.md) | [Stair Climber](Mock_Test_6/Q2_Medium_Stair_Climber.md) | [Rising Streaks](Mock_Test_6/Q3_Hard_Rising_Streaks.md) |
| **7** | [Signal Boost](Mock_Test_7/Q1_Easy_Signal_Boost.md) | [Price Volatility](Mock_Test_7/Q2_Medium_Price_Volatility.md) | [Lantern Paths](Mock_Test_7/Q3_Hard_Lantern_Paths.md) |
| **8** 🔒 | [Ferry Seats](Mock_Test_8/Q1_Easy_Ferry_Seats.md) | [Island Hopping](Mock_Test_8/Q2_Medium_Island_Hopping.md) | [Office Network](Mock_Test_8/Q3_Hard_Office_Network.md) |
| **9** 🔒 | [Even Streak](Mock_Test_9/Q1_Easy_Even_Streak.md) | [Exam Hall](Mock_Test_9/Q2_Medium_Exam_Hall.md) | [Gem Splitter](Mock_Test_9/Q3_Hard_Gem_Splitter.md) |
| **10** 🔒 | [Tray Stack](Mock_Test_10/Q1_Easy_Tray_Stack.md) | [Club Merge](Mock_Test_10/Q2_Medium_Club_Merge.md) | [Freight Limits](Mock_Test_10/Q3_Hard_Freight_Limits.md) |

🔒 **Mocks 8–10 are held out.** Random papers never use them. Leave them unopened, including their separate spoiler block below, until the week before the exam. Then sit `python tools/judge/paper.py --final` once, under a 3-hour timer. It is the only paper that tells you how you would do on problems you have never seen.

<details>
<summary>Topic of each question (spoilers: spotting the pattern is part of the test)</summary>

| Mock | Q1 | Q2 | Q3 |
|---|---|---|---|
| 1 | hashing on remainders | DP over remainders, mod | segment tree, custom merge |
| 2 | circular sliding window | Dijkstra on states | BFS + bitmask DP |
| 3 | sieve, divisors | binary search on answer | digit DP, mod |
| 4 | prefix sum + hashing | bipartite + subset-sum DP | SCC condensation + DAG DP |
| 5 | Sprague–Grundy | sparse table | articulation points |
| 6 | inclusion–exclusion | matrix exponentiation | DP + Fenwick tree |
| 7 | difference array | monotonic stack, contribution technique | nCr mod p + DP over obstacles |

</details>

<details>
<summary>🔒 Topics of the held-out mocks 8-10 (open only after sitting <code>paper.py --final</code>)</summary>

| Mock | Q1 | Q2 | Q3 |
|---|---|---|---|
| 8 | greedy two pointers | 0-1 BFS | rerooting DP on a weighted tree |
| 9 | sliding window | binary search on answer | meet-in-the-middle knapsack |
| 10 | stack with running max | union-find with sizes | binary lifting, path maximum |

</details>

### Judge your own code

```bash
python tools/judge/judge.py M1Q2 my_q2.py   # samples + 50 random tests + max-size tests, scored /100
python tools/judge/judge.py --list          # every problem key
python tools/judge/paper.py                 # random paper: one Easy, Medium, Hard from three different mocks 1-7
python tools/judge/paper.py --final         # the held-out mocks 8-10: sit it once, in the last week
```

The judge compares your program with the reference solution. Small tests (the samples plus random ones) are worth 50 points and the max-constraint tests 50, so a correct brute force scores about half, as in the real exam. The time limit on large tests is 3× the reference's own time on your machine (at least 2 s), so it adjusts to how fast your computer is. A failing small test prints its input, the expected output and your output. Every run prints its seed; rerun with `--seed N` to reproduce a failure.

**How to sit a mock:**
1. Run `python tools/judge/paper.py`, or pick a mock. Set a timer for **3 hours** and use no notes.
2. Order: solve Q1 fully, then submit a **brute force for Q3** to bank its partial score, then solve Q2, then come back and optimise Q3.
3. Judge every answer, then read the `solutions/` file. Flip **Status** to ✅ only when you can re-code the optimized version unaided and it scores 100.

Keep [Python_Contest_Template.md](Python_Contest_Template.md) memorised — fast input, sieve, nCr mod p, DSU, Dijkstra, Fenwick, segment tree, binary search on answer.

---

## 🔹 Topic Map → Problems in This Repo

The table below picks the most exam-relevant problems per slot. For the full set (463 notes, five complete sheets), work through [SHEETS.md](../SHEETS.md) topic by topic. Drill the 🔄 ones daily with `python tools/review.py`.

| Topic | Slot | Problems |
|---|---|---|
| Hashing & prefix sums | Q1 | [1](../Arrays_and_Hashing/1.Two_Sum.md) · [560](../Prefix_Sum/560.Subarray_Sum_Equals_K.md) · [304](../Prefix_Sum/304.Range_Sum_Query_2D_Immutable.md) · [Festival Pairs](Mock_Test_1/Q1_Easy_Festival_Pairs.md) · [Balanced Segments](Mock_Test_4/Q1_Easy_Balanced_Segments.md) |
| Sliding window & two pointers | Q1–Q2 | [76](../Sliding_Window/76.Minimum_Window_Substring.md) · [239](../Sliding_Window/239.Sliding_Window_Maximum.md) · [42](../Stack/42.Trapping_Rain_Water.md) · [Server Rack Shuffle](Mock_Test_2/Q1_Easy_Server_Rack_Shuffle.md) |
| Number theory & modular arithmetic | Q1–Q3 | [204](../Math/204.Count_Primes.md) · [372](../Math/372.Super_Pow.md) · [1922](../Math/1922.Count_Good_Numbers.md) · [2521](../Math/2521.Distinct_Prime_Factors_of_Product_of_Array.md) · [1359](../Math/1359.Count_All_Valid_Pickup_and_Delivery_Options.md) · [Special Numbers](Mock_Test_3/Q1_Easy_Special_Numbers.md) · [96](../Math/96.Unique_Binary_Search_Trees.md) · [Festival Lamps](Mock_Test_6/Q1_Easy_Festival_Lamps.md) · [2400](../Math/2400.Number_of_Ways_to_Reach_a_Position_After_Exactly_k_Steps.md) (nCr mod p) · [1569](../Math/1569.Number_of_Ways_to_Reorder_Array_to_Get_Same_BST.md) |
| Difference array & sweep line | Q1–Q3 | [1094](../Prefix_Sum/1094.Car_Pooling.md) · [2381](../Prefix_Sum/2381.Shifting_Letters_II.md) · [2251](../Intervals/2251.Number_of_Flowers_in_Full_Bloom.md) |
| Meet in the middle | Q3 | [1755](../Divide_and_Conquer/1755.Closest_Subsequence_Sum.md) · [2035](../Divide_and_Conquer/2035.Partition_Array_Into_Two_Arrays_to_Minimize_Sum_Difference.md) |
| Binary search on the answer | Q2 | [875](../Binary_Search/875.Koko_Eating_Bananas.md) · [1011](../Binary_Search/1011.Capacity_To_Ship_Packages_Within_D_Days.md) · [410](../Binary_Search/410.Split_Array_Largest_Sum.md) · [1201](../Binary_Search/1201.Ugly_Number_III.md) · [Factory Output](Mock_Test_3/Q2_Medium_Factory_Output.md) · [878](../Binary_Search/878.Nth_Magical_Number.md) |
| Greedy & heaps | Q2 | [55](../Greedy/55.Jump_Game.md) · [45](../Greedy/45.Jump_Game_II.md) · [134](../Greedy/134.Gas_Station.md) · [621](../Greedy/621.Task_Scheduler.md) · [452](../Intervals/452.Minimum_Number_of_Arrows_to_Burst_Balloons.md) · [502](../Greedy/502.IPO.md) · [630](../Greedy/630.Course_Schedule_III.md) |
| DP — 1D, knapsack, counting | Q2 | [198](../DP/198.House_Robber.md) · [139](../DP/139.Word_Break.md) · [309](../DP/309.Best_Time_to_Buy_and_Sell_Stock_with_Cooldown.md) · [322](../DP_Knapsack/322.Coin_Change.md) · [518](../DP_Knapsack/518.Coin_Change_II.md) · [416](../DP_Knapsack/416.Partition_Equal_Subset_Sum.md) · [494](../DP_Knapsack/494.Target_Sum.md) · [1155](../DP_Knapsack/1155.Number_of_Dice_Rolls_With_Target_Sum.md) · [Lucky Subsets](Mock_Test_1/Q2_Medium_Lucky_Subsets.md) |
| DP — 2D, strings, LIS | Q2–Q3 | [62](../DP_Grid_and_Strings/62.Unique_Paths.md) · [64](../DP_Grid_and_Strings/64.Minimum_Path_Sum.md) · [1143](../DP_Grid_and_Strings/1143.Longest_Common_Subsequence.md) · [72](../DP_Grid_and_Strings/72.Edit_Distance.md) · [115](../DP_Grid_and_Strings/115.Distinct_Subsequences.md) · [329](../DP_Grid_and_Strings/329.Longest_Increasing_Path_in_a_Matrix.md) · [300](../DP/300.Longest_Increasing_Subsequence.md) · [354](../DP/354.Russian_Doll_Envelopes.md) · [1235](../DP/1235.Maximum_Profit_in_Job_Scheduling.md) |
| DP — interval, bitmask, digit, trees | Q3 | [312](../DP_Advanced/312.Burst_Balloons.md) · [516](../DP_Advanced/516.Longest_Palindromic_Subsequence.md) · [698](../DP_Advanced/698.Partition_to_K_Equal_Sum_Subsets.md) · [847](../DP_Advanced/847.Shortest_Path_Visiting_All_Nodes.md) · [1986](../DP_Advanced/1986.Minimum_Number_of_Work_Sessions_to_Finish_the_Tasks.md) · [233](../DP_Advanced/233.Number_of_Digit_One.md) · [902](../DP_Advanced/902.Numbers_At_Most_N_Given_Digit_Set.md) · [337](../DP_Advanced/337.House_Robber_III.md) · [968](../DP_Advanced/968.Binary_Tree_Cameras.md) · [834](../DP_Advanced/834.Sum_of_Distances_in_Tree.md) (rerooting) · [2581](../DP_Advanced/2581.Count_Number_of_Possible_Root_Nodes.md) · [124](../Trees/124.Binary_Tree_Maximum_Path_Sum.md) · [Treasure Route](Mock_Test_2/Q3_Hard_Treasure_Route.md) · [Smooth Numbers](Mock_Test_3/Q3_Hard_Smooth_Numbers.md) |
| DP — matrix exponentiation | Q2–Q3 | [935](../DP_Advanced/935.Knight_Dialer.md) · [1220](../DP_Advanced/1220.Count_Vowels_Permutation.md) · [Stair Climber](Mock_Test_6/Q2_Medium_Stair_Climber.md) |
| Game theory | Q1–Q3 | [292](../Math/292.Nim_Game.md) · [1406](../Math/1406.Stone_Game_III.md) · [Coin Piles](Mock_Test_5/Q1_Easy_Coin_Piles.md) |
| Graphs — BFS, bipartite & shortest paths | Q2–Q3 | [200](../Graphs/200.Number_of_Islands.md) · [994](../Graphs/994.Rotting_Oranges.md) · [542](../Graphs/542.01_Matrix.md) · [127](../Graphs/127.Word_Ladder.md) · [743](../Graph_Shortest_Path/743.Network_Delay_Time.md) · [787](../Graph_Shortest_Path/787.Cheapest_Flights_Within_K_Stops.md) · [1631](../Graph_Shortest_Path/1631.Path_With_Minimum_Effort.md) · [1368](../Graph_Shortest_Path/1368.Minimum_Cost_to_Make_at_Least_One_Valid_Path_in_a_Grid.md) · [1334](../Graph_Shortest_Path/1334.Find_the_City_With_the_Smallest_Number_of_Neighbors_at_a_Threshold_Distance.md) · [Toll Pass](Mock_Test_2/Q2_Medium_Toll_Pass.md) · [785](../Graphs/785.Is_Graph_Bipartite.md) · [886](../Graphs/886.Possible_Bipartition.md) · [Rival Teams](Mock_Test_4/Q2_Medium_Rival_Teams.md) |
| Graphs — topo sort, DSU, MST, SCC, bridges, cut vertices | Q2–Q3 | [207](../Graphs/207.Course_Schedule.md) · [210](../Graphs/210.Course_Schedule_II.md) · [1857](../Graphs/1857.Largest_Color_Value_in_a_Directed_Graph.md) · [684](../Graph_Advanced/684.Redundant_Connection.md) · [1319](../Graph_Advanced/1319.Number_of_Operations_to_Make_Network_Connected.md) · [1584](../Graph_Advanced/1584.Min_Cost_to_Connect_All_Points.md) · [1192](../Graph_Advanced/1192.Critical_Connections_in_a_Network.md) · [Gold Roads](Mock_Test_4/Q3_Hard_Gold_Roads.md) · [Critical Routers](Mock_Test_5/Q3_Hard_Critical_Routers.md) |
| Segment tree, Fenwick tree & sparse table | Q3 | [307](../Range_Queries/307.Range_Sum_Query_Mutable.md) · [699](../Range_Queries/699.Falling_Squares.md) · [2407](../Range_Queries/2407.Longest_Increasing_Subsequence_II.md) · [315](../Range_Queries/315.Count_of_Smaller_Numbers_After_Self.md) · [493](../Range_Queries/493.Reverse_Pairs.md) · [327](../Range_Queries/327.Count_of_Range_Sum.md) · [1649](../Range_Queries/1649.Create_Sorted_Array_through_Instructions.md) · [Stock Ticker Queries](Mock_Test_1/Q3_Hard_Stock_Ticker_Queries.md) · [Price Spread](Mock_Test_5/Q2_Medium_Price_Spread.md) · [Rising Streaks](Mock_Test_6/Q3_Hard_Rising_Streaks.md) |
| Trees — LCA & binary lifting | Q2–Q3 | [236](../Trees/236.Lowest_Common_Ancestor_of_a_Binary_Tree.md) · [1483](../Trees/1483.Kth_Ancestor_of_a_Tree_Node.md) · [2846](../Trees/2846.Minimum_Edge_Weight_Equilibrium_Queries_in_a_Tree.md) (LCA + path counts) · [2836](../Trees/2836.Maximize_Value_of_Function_in_a_Ball_Passing_Game.md) (lifting on a functional graph) |
| Strings (KMP, Z-function, rolling hash, Manacher), trie, bits | Q2–Q3 | [28](../Strings/28.Find_the_Index_of_the_First_Occurrence_in_a_String.md) · [214](../Strings/214.Shortest_Palindrome.md) · [1392](../Strings/1392.Longest_Happy_Prefix.md) · [208](../Trie/208.Implement_Trie_Prefix_Tree.md) · [421](../Trie/421.Maximum_XOR_of_Two_Numbers_in_an_Array.md) · [2223](../Strings/2223.Sum_of_Scores_of_Built_Strings.md) · [1044](../Strings/1044.Longest_Duplicate_Substring.md) · [187](../Strings/187.Repeated_DNA_Sequences.md) · [647](../Strings/647.Palindromic_Substrings.md) |
| Monotonic stack | Q2 | [84](../Stack/84.Largest_Rectangle_in_Histogram.md) · [907](../Stack/907.Sum_of_Subarray_Minimums.md) |
| Backtracking & geometry | Q1–Q2 | [51](../Backtracking/51.N-Queens.md) · [79](../Backtracking/79.Word_Search.md) · [836](../Math/836.Rectangle_Overlap.md) |

---

## 🔹 Python Survival Rules

* **Input:** `data = sys.stdin.buffer.read().split()` once, then walk an index. `input()` in a loop is slow for 10⁵ lines.
* **Recursion:** the default limit is 1000. Prefer iterative DFS/BFS (see 124, 337, 968, 1192 in this repo) or the threading fallback in the template.
* **Modulo:** reduce after every `+` / `*`; `pow(a, b, MOD)` for powers; `pow(a, MOD - 2, MOD)` for division.
* **Built-ins:** `heapq` (min-heap; negate for max), `deque`, `bisect`, `defaultdict`, `Counter`, `lru_cache`, `math.isqrt`, `math.comb`.
* **Precompute once** (sieve, factorials, BFS distances) outside the query loop.
* **Output:** collect answers in a list and print once with `"\n".join(...)`.

---

## 🔹 Sources (unofficial)

* [Great Learning — Infosys SP & DSE Interview Guide 2026](https://www.mygreatlearning.com/blog/infosys-sp-dse-interview-guide-2026/)
* [LeetCode Discuss — Infosys Specialist Programmer L3 experience](https://leetcode.com/discuss/post/8433956/infosys-specialist-programmer-l3-intervi-mes3/)
* [Medium — HackWithInfy guide: rounds, questions, DSE role](https://medium.com/@pravallikaseshasai/hackwithinfy-guide-rounds-questions-how-i-landed-the-dse-role-bc4f64db465d)
* [PrepInsta — Infosys SP and DSE placement papers](https://prepinsta.com/?p=975993)
