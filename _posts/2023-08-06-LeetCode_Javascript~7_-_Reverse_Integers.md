---
layout: single
title: "[LeetCode Javascript]7 - Reverse Integers"
categories: dsa
tag: [algorithm, data structure, dsa, javascript]
toc: true
author_profile: false
typora-root-url: ../
sidebar:
  nav: "counts"
---

<nav class="cods"><h2>LeetCode Javascript posts</h2><ol><li><a href="/dsa/LeetCode_Javascript~1_-_Two_Sum">1 - Two Sum</a></li><li><a href="/dsa/LeetCode_Javascript~2_-_Add_Two_Numbers">2 - Add Two Numbers</a></li><li><a href="/dsa/LeetCode_Javascript~3_-_Longest_Substring_Without_Repeating_Characters">3 - Longest Substring Without Repeating Characters</a></li><li><a href="/dsa/LeetCode_Javascript~4_-_Median_of_Two_Sorted_Arrays">4 - Median of Two Sorted Arrays</a></li><li><a href="/dsa/LeetCode_Javascript~5_-_Longest_Palindromic_Substring">5 - Longest Palindromic Substring</a></li><li><a href="/dsa/LeetCode_Javascript~6_-_Zigzag_Conversion">6 - Zigzag Conversion</a></li><li><p>7 - Reverse Integers (current)</p></li><li><a href="/dsa/LeetCode_Javascript~8_-_MyAtoI">8 - MyAtoI</a></li><li><a href="/dsa/LeetCode_Javascript~9_-_Palindrome_Number">9 - Palindrome Number</a></li></ol></nav>


## Problem

Given a signed 32-bit integer `x`, return `x` *with its digits reversed*. If reversing `x` causes the value to go outside the signed 32-bit integer range `[-231, 231 - 1]`, then return `0`.

**Assume the environment does not allow you to store 64-bit integers (signed or unsigned).** 

**Example 1:**

```
Input: x = 123
Output: 321
```

**Example 2:**

```
Input: x = -123
Output: -321
```

**Example 3:**

```
Input: x = 120
Output: 21
```

**Constraints:**

- `-231 <= x <= 231 - 1`

## Solution

### My Original Solution

```javascript
const reverse = function(x) {
    let output = 0;

    while(x !== 0){
        const last_digit = x % 10;

        output += last_digit;
        x -= last_digit;

        if (x !== 0){
            output = output * 10;
            x = x / 10
        }
    }

    if (output <= - 2147483648 || output >= 2147483647){
        return 0;
    }
    
    return output;
};
```

![image-20230805213528718](/images/typora/image-20230805213528718.png)

Well, I thought it was a straightforward question.
But I found this statement after I start writing this post.

`Assume the environment does not allow you to store 64-bit integers (signed or unsigned). `

Actually, a lot of 'upvoted' solutions failed to meet this condition :)

So, the solution should be like the one below.

### Solution - without 64-bit storing

```javascript
const reverse = function(x) {
    let output = 0;

    while(x !== 0){
        const last_digit = x % 10;

        output += last_digit;
        x -= last_digit;

        if (x !== 0){
          	if (output  <= (-2147483648 - x / 10) / 10 || 
              	output >= (2147483647 - x / 10)  / 10){
              return 0;
            }
            output = output * 10;
            x = x / 10
        }
    }
    
    return output;
};
```

![image-20230805214756996](/images/typora/image-20230805214756996.png)

## Complexity

ChatGPT calculated this for me:

### Time Complexity:

The time complexity is determined by how many times the loop is executed. Since the input x is divided by 10 in each iteration of the loop, the loop will run $log_{10}(∣x∣)$ times, where $|x|$ is the absolute value of $x$. Therefore, the time complexity is $O(log_{10}(|x|)$.

### Space Complexity:

The additional memory determines the space complexity the algorithm uses. In this case, the variables `output`, `last_digit`, and `x` all use a constant amount of space, regardless of the input size. Therefore, the space complexity is $O(1)$