## Problem

Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to `target`*.

You may assume that each input would have ***exactly\* one solution**, and you may not use the *same* element twice.

You can return the answer in any order.

 

**Example 1:**

```javascript
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

**Example 2:**

```javascript
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

**Example 3:**

```javascript
Input: nums = [3,3], target = 6
Output: [0,1]
```

 

**Constraints:**

- `2 <= nums.length <= 104`
- `-109 <= nums[i] <= 109`
- `-109 <= target <= 109`
- **Only one valid answer exists**



## Solve

### My Original Answer

``` javascript
/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
var twoSum = function(nums, target) {
    const max = nums.length

    for (let i = 0; i < max; i++){
        const num1 = nums[i];
        for (let j = i + 1; j < max; j++){
            const num2 = nums[j]
            if (num1 + num2 === target){
                return [i, j]
            }
        }
    }
};
```

I am a six-year front-end developer who has never studied data structures, algorithms, etc. While studying machine learning, I need this knowledge and study for the first time.

It's my first time solving leetcode, so I just tried number one.
When I saw the problem, I felt, "Oh, that's easy."

### Result of First Answer

![스크린샷 2023-07-31 오후 6.04.31](../../../images/typora/스크린샷 2023-07-31 오후 6.04.31.png)

