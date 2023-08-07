---
layout: single
title: "[LeetCode Javascript]6 - Zigzag Conversion"
categories: dsa
tag: [algorithm, data structure, dsa, javascript]
toc: true
author_profile: false
typora-root-url: ../
sidebar:
  nav: "counts"
---

<nav class="cods"><h2>LeetCode Javascript posts</h2><ol><li><a href="/dsa/LeetCode_Javascript~1_-_Two_Sum">1 - Two Sum</a></li><li><a href="/dsa/LeetCode_Javascript~2_-_Add_Two_Numbers">2 - Add Two Numbers</a></li><li><a href="/dsa/LeetCode_Javascript~3_-_Longest_Substring_Without_Repeating_Characters">3 - Longest Substring Without Repeating Characters</a></li><li><a href="/dsa/LeetCode_Javascript~4_-_Median_of_Two_Sorted_Arrays">4 - Median of Two Sorted Arrays</a></li><li><a href="/dsa/LeetCode_Javascript~5_-_Longest_Palindromic_Substring">5 - Longest Palindromic Substring</a></li><li><p>6 - Zigzag Conversion (current)</p></li><li><a href="/dsa/LeetCode_Javascript~7_-_Reverse_Integers">7 - Reverse Integers</a></li><li><a href="/dsa/LeetCode_Javascript~8_-_MyAtoI">8 - MyAtoI</a></li></ol></nav>


## Problem

Well, I don't think this is a good question.
Downvote is twice as much as upvote.

I didn't solve this problem personally.
But I'll share a good solution. Please check the description at the link.

## Solution

https://leetcode.com/problems/zigzag-conversion/solutions/3522/intuitive-javascript-solution/

```javascript
var convert = function(s, numRows) {
    // return original string if can't zigzag
    if (numRows === 1 || s.length < numRows) return s;

    let rows = []
    let converted = '';
    let reverse = false;
    let count = 0

    // prepare rows
    for (let i = 0; i < numRows; i++) rows[i] = [];
    // reverse the push flow when reaching turning points
    for (let i = 0; i < s.length; i++) {
        rows[count].push(s[i]);
        reverse ? count-- : count++;
        if (count === numRows - 1 || count === 0) reverse = !reverse;
    }
    // put together converted string
    return rows.reduce((converted, cur) => converted + cur.join(''), '');
};
```



