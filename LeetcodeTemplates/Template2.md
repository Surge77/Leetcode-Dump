# 🔹 Problem Name: [Title] ([Category], Difficulty)

**🔗 Link:** [LeetCode Problem URL]

## **🔹 Approach**

- **Key Idea:** (1-2 sentence summary of how you solved it)
- **Algorithm Used:** (DP, Sliding Window, Two Pointers, etc.)
- **Why This Works?** (Brief explanation)

## **🔹 Pattern**

- **Concept Type:** (Sliding Window, Greedy, Recursion, etc.)
- **Similar Problems:** (List of problems that use the same pattern)

## **🔹 Complexity Analysis**

- **Time Complexity:** O(?)
- **Space Complexity:** O(?)

## **🔹 Mistakes I Made**

- ❌ (Mistake 1)
- ❌ (Mistake 2)

## **🔹 Code Snippet (Optimized)**

```python
# Your clean, minimal code here
```

# Example Entry

# 🔹 Problem Name: Longest Substring Without Repeating Characters (Sliding Window, Medium)

**🔗 Link:** [https://leetcode.com/problems/longest-substring-without-repeating-characters/](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

## **🔹 Approach**

- **Key Idea:** Use a **sliding window** to dynamically track unique characters.
- **Algorithm Used:** Sliding Window + HashSet
- **Why This Works?** Expanding and shrinking the window ensures optimal traversal.

## **🔹 Pattern**

- **Concept Type:** Sliding Window
- **Similar Problems:** Longest Subarray with Sum K, Maximum Consecutive Ones

## **🔹 Complexity Analysis**

- **Time Complexity:** O(N)
- **Space Complexity:** O(N)

## **🔹 Mistakes I Made**

- ❌ Forgot to remove the **left pointer character** when shrinking the window.
- ❌ Initially tried **brute force O(N²) instead of optimizing**.

## **🔹 Code Snippet (Optimized)**

```python
def lengthOfLongestSubstring(s):
    seen = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        while s[right] in seen:
            seen.remove(s[left])
            left += 1
        seen.add(s[right])
        max_length = max(max_length, right - left + 1)

    return max_length
```
