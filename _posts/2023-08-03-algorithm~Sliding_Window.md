---
layout: single
title: "[algorithm]Sliding Window"
categories: dsa
tag: [algorithm, data structure, dsa]
toc: true
author_profile: false
typora-root-url: ../
sidebar:
  nav: "counts"
---

<nav class="cods"><h2>algorithm posts</h2><ol><li><a href="/dsa/algorithm~Binary_Search">Binary Search</a></li><li><p>(current) Sliding Window</p></li></ol></nav>

## What is a Sliding Window?

### Before Start

Recently, I was solving problems on LeetCode and came across one that required the 'sliding window' algorithm.

This post shares my understanding of the sliding window algorithm. But, as I'm still learning, there might be mistakes. If you find any, I'd appreciate your feedback. 

### Definition

The sliding window technique is a method that involves creating a "window" or sub-array over an array or list and moving this window over the data to examine different portions of it. This technique is used to reduce the time complexity of problems by leveraging the fact that the computations of overlapping subproblems can be used to solve a larger problem.

### When to Use

This algorithm is generally useful when:

1. The problem involves a data structure such as an array or a string.
2. There are overlapping sub-problems that are more efficiently solved by reusing partial results from previous computations instead of recomputing them.

Problems involving maximum/minimum, longest, shortest, or target sum/subarray or substring are good candidates for sliding window.

## Examples

### 1. **Maximum Sum Subarray of Size K**

Problem: Given an array of positive numbers and a positive number ‘k’, find the maximum sum of any contiguous subarray of size ‘k’.

#### Without Sliding Window

Without sliding window, you may have to calculate the sum of each subarray of size 'k', resulting in O(N*k) time complexity. 

```python
def max_sub_array_of_size_k(k, arr):
    max_sum = 0
    for i in range(len(arr) - k + 1):
        current_sum = 0
        for j in range(i, i+k):
            current_sum += arr[j]
        max_sum = max(max_sum, current_sum)
    return max_sum
```

#### With Sliding Window

With sliding window, you can re-use the sum from the previous subarray and slide the window through. This reduces the time complexity to O(N).

```python
def max_sub_array_of_size_k(k, arr):
    max_sum = 0
    window_sum = 0

    window_start = 0
    for window_end in range(len(arr)):
        window_sum += arr[window_end]  # add the next element
        # slide the window, we don't need to slide if we've not hit the required window size of 'k'
        if window_end >= k-1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]  # subtract the element going out
            window_start += 1  # slide the window ahead
    return max_sum
```

### 1. **Longest Substring with K Distinct Characters**

Problem: Given a string, find the length of the longest substring in it with no more than K distinct characters.

#### Without Sliding Window

Without sliding window, you would have to find all substrings of the string and check the condition, which can result in a time complexity of O(N^2).

```python
def longest_substring_with_k_distinct(str, k):
    max_length = 0
    for i in range(len(str)):
        distinct_chars = set()
        for j in range(i, len(str)):
            distinct_chars.add(str[j])
            if len(distinct_chars) <= k:
                max_length = max(max_length, j - i + 1)
            else:
                break
    return max_length
```

#### With Sliding Window

With sliding window, we can use a hashmap to track the unique characters within the window and adjust the window accordingly, which results in a time complexity of O(N).

```python
def longest_substring_with_k_distinct(str, k):
    window_start = 0
    max_length = 0
    char_frequency = {}

    # in the following loop we'll try to extend the range [window_start, window_end]
    for window_end in range(len(str)):
        right_char = str[window_end]
        if right_char not in char_frequency:
            char_frequency[right_char] = 0
        char_frequency[right_char] += 1

        # shrink the sliding window, until we are left with 'k' distinct characters in the char_frequency
        while len(char_frequency) > k:
            left_char = str[window_start]
            char_frequency[left_char] -= 1
            if char_frequency[left_char] == 0:
                del char_frequency[left_char]
            window_start += 1  # shrink the window
        # remember the maximum length so far
        max_length = max(max_length, window_end-window_start + 1)
    return max_length
```

