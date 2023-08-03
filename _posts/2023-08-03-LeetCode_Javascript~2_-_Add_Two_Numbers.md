---
layout: single
title: "[LeetCode Javascript]2 - Add Two Numbers"
categories: dsa
tag: [algorithm, data structure, dsa, javascript]
toc: true
author_profile: false
typora-root-url: ../
sidebar:
  nav: "counts"
---

<nav class="cods"><h2>LeetCode Javascript posts</h2><ol><li><a href="/dsa/LeetCode_Javascript~1_-_Two_Sum">1 - Two Sum</a></li><li><p>(current) 2 - Add Two Numbers</p></li><li><a href="/dsa/LeetCode_Javascript~3_-_Longest_Substring_Without_Repeating_Characters">3 - Longest Substring Without Repeating Characters</a></li><li><a href="/dsa/LeetCode_Javascript~4_-_Median_of_Two_Sorted_Arrays">4 - Median of Two Sorted Arrays</a></li></ol></nav>

## Problem

You are given two **non-empty** linked lists representing two non-negative integers. The digits are stored in **reverse order**, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

**Example 1:**

```
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
```

**Example 2:**

```
Input: l1 = [0], l2 = [0]
Output: [0]
```

**Example 3:**

```
Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]
```



## Solution

Shamefully, I thought, 'Wow, is there a "ListNode" type in javascript? that's new to me.'
And I tried to submit my solution and got an error message.

And turns out, ListNode is just a function they made. And here's the definition:

```javascript
/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
```

I missed this comment, so I had no idea, so I had to refer to other people's correct answers.

https://leetcode.com/problems/add-two-numbers/solutions/1020/javascript-solution/

I tried to submit my own solution, but I ended up writing code almost the same as the above solution.

Anyway, my solution(which is already the perfect solution because I referred to the best solution) is this:

```javascript
let addTwoNumbers = function(l1, l2) {
    let sum = 0;
    const answer = new ListNode(0);
    let current = answer;

    while(l1 || l2 || sum > 0){
        if (l1){
            sum += l1.val;
            l1 = l1.next;
        }
        if (l2){
            sum += l2.val;
            l2 = l2.next;
        }
        if (sum >= 10){
            current.next = new ListNode(sum - 10);
            current = current.next
            sum = 1;
        } else{
            current.next = new ListNode(sum);
            current = current.next
            sum = 0;
        }
    }

    return answer.next;
};
```

![image-20230731205751610](/images/typora/image-20230731205751610.png)
