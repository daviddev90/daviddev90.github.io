---
layout: single
title: "[LeetCode Javascript]9 - Palindrome Number"
categories: dsa
tag: [algorithm, data structure, dsa, javascript]
toc: true
author_profile: false
typora-root-url: ../
sidebar:
  nav: "counts"
---

<nav class="cods"><h2>LeetCode Javascript posts</h2><ol><li><a href="/dsa/LeetCode_Javascript~1_-_Two_Sum">1 - Two Sum</a></li><li><a href="/dsa/LeetCode_Javascript~2_-_Add_Two_Numbers">2 - Add Two Numbers</a></li><li><a href="/dsa/LeetCode_Javascript~3_-_Longest_Substring_Without_Repeating_Characters">3 - Longest Substring Without Repeating Characters</a></li><li><a href="/dsa/LeetCode_Javascript~4_-_Median_of_Two_Sorted_Arrays">4 - Median of Two Sorted Arrays</a></li><li><a href="/dsa/LeetCode_Javascript~5_-_Longest_Palindromic_Substring">5 - Longest Palindromic Substring</a></li><li><a href="/dsa/LeetCode_Javascript~6_-_Zigzag_Conversion">6 - Zigzag Conversion</a></li><li><a href="/dsa/LeetCode_Javascript~7_-_Reverse_Integers">7 - Reverse Integers</a></li><li><a href="/dsa/LeetCode_Javascript~8_-_MyAtoI">8 - MyAtoI</a></li><li><p>9 - Palindrome Number (current)</p></li></ol></nav>


## Problem

https://leetcode.com/problems/palindrome-number/submissions/

Given an integer `x`, return `true` *if* `x` *is a* **palindrome**, return `true`,  and `false` *otherwise*.

**Example 1:**

```
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.
```

**Example 2:**

```
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
```

## Solution

### My Original Solution 

```javascript
const isPalindrome = function(x) {
    x = x + ""
    let y = '';
    for (let i = x.length - 1; i >=0; i--){
        y += x[i];
    }
    return (x === y)
};
```

![image-20230808010134944](/images/typora/image-20230808010134944.png)

I don't think an explanation is needed.