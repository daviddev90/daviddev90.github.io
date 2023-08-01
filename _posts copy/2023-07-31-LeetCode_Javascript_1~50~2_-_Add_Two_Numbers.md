---
layout: single
title: "[LeetCode Javascript 1~50]2 - Add Two Numbers"
categories: leetcode
tag: [python, leetcode]
toc: true
author_profile: false
typora-root-url: ../
sidebar:
  nav: "counts"
---

<nav class="cods"><h2>LeetCode Javascript 1~50 Posts</h2><ol><li><a href="/leetcode/LeetCode_Javascript_1~50~1_-_Two_Sum/">1 - Two Sum</a></li><li><p>(current) 2 - Add Two Numbers</p></li></ol></nav>

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



## Solve 

### Attempt 1

#### My Solution

Shamefully, I thought 'wow, is there "ListNode" type in javascript? that's new to me, but maybe it's same as Array'
And I tried to submit my solution and got error message.

And turns out, ListNode is just a function they made.
They wrote about it in comment, and I missed it. 
That's my fault.

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

I missed the commented ListNode Function declare part, so I had to refer to other people's correct answers.

https://leetcode.com/problems/add-two-numbers/solutions/1020/javascript-solution/

I saw the solution of the link above.
I tried to submit my own solution, but I ended up writing a code almost same as above solution.
From the next question, I will read the comments carefully and solve the problem.

Anyway, my answer is this:

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



#### Result

![image-20230731205751610](/images/typora/image-20230731205751610.png)

The results were very good, but I wasn't very happy because this isn't a code I wrote on my own.