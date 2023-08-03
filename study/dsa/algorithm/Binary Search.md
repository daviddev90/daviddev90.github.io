## What is Binary Search

The algorithm checks the middle element to determine if it's greater than, less than, or equal to the value being searched for.

- If it's equal, you've found your value. 
- If it's less, you know the value must be in the upper half of the array. 
- If it's greater, the value must be in the lower half of the array. 

This process is repeated on the correct half of the array, essentially reducing the search space by half each time. This is why it's called a "binary" search. It's an efficient way to search for a value in a sorted array, with a time complexity of $O(log(n))$.

### Restrictions

Binary search can only be used when the array or list is sorted. 
If the data is not sorted, you would need to sort it first before using binary search, which can be expensive for large data sets.

### Benefits

1. **Efficiency**: Binary search has a time complexity of $O(log (n))$, making it much faster than linear search, which has a time complexity of $O(n)$ especially for large data sets.
2. **Less Comparisons**: In binary search, the number of comparisons decreases with each step, as the search space is halved. This reduces the total number of comparisons needed to find the target.
3. **Doesn't Require Extra Space**: Binary search doesn't require any extra space, as it works on the original data structure. This makes it a space-efficient algorithm.
4. **Versatility**: Binary search isn't just used for searching. It's also used in a variety of other algorithms and problem-solving approaches, including finding the square root of a number, checking if a number is a perfect square, and solving more complex problems like the median of two sorted arrays, as we've seen in this example.

## Binary Search, Simple Usecase

```javascript
const array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const target = 7;
```

The array is already sorted, and we want to find the target numer 7 in the array.

```javascript
function binarySearch(array, target) {
    let start = 0;
    let end = array.length - 1;

    while (start <= end) {
        let mid = Math.floor((start + end) / 2);

        if (array[mid] === target) {
            return mid;
        } else if (array[mid] < target) {
            start = mid + 1;
        } else {
            end = mid - 1;
        }
    }
    return -1;
}
```

This function starts by initializing two pointers, **start** and **end**, to the beginning and end of the array, respectively. Then it enters a loop that continues until **start** is greater than **end**.

In each iteration of the loop, the function calculates the midpoint of the current search space and checks if the target number is at that position in the array. If it is, the function returns the index of the target number.

If the target number is not at the midpoint, the function checks if the target number is greater than the number at the midpoint. If it is, the **start** pointer is moved to the right of the midpoint for the next iteration. If the target number is less than the number at the midpoint, the **end** pointer is moved to the left of the midpoint.

The loop continues, halving the search space in each iteration, until the target number is found or until the search space is empty (i.e., **start > end**), at which point the function returns **-1** to indicate that the target number is not in the array.

## Binary Search, More Complicated Usecase

### Problem(leetcode no.4)

https://leetcode.com/problems/median-of-two-sorted-arrays/submissions/

Given two sorted arrays `nums1` and `nums2`. return **the median** of the two sorted arrays.

**Example 1:**

```
Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
```

**Example 2:**

```
Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
```

### Solution: Full Code

```javascript
const findMedianSortedArrays = function(nums1, nums2) {
    if (nums1.length > nums2.length) {
        [nums1, nums2] = [nums2, nums1];
    }
    
    let x = nums1.length;
    let y = nums2.length;
    
    let start = 0;
    let end = x;
    
    while (start <= end) {
        let partitionX = (start + end) >> 1;
        let partitionY = ((x + y + 1) >> 1) - partitionX;
        
        let maxLeftX = (partitionX === 0) ? -Infinity : nums1[partitionX - 1];
        let minRightX = (partitionX === x) ? Infinity : nums1[partitionX];
        
        let maxLeftY = (partitionY === 0) ? -Infinity : nums2[partitionY - 1];
        let minRightY = (partitionY === y) ? Infinity : nums2[partitionY];
        
        if (maxLeftX <= minRightY && maxLeftY <= minRightX) {
            if ((x + y) & 1) {
                return Math.max(maxLeftX, maxLeftY);
            } else {
                return (Math.max(maxLeftX, maxLeftY) + Math.min(minRightX, minRightY)) / 2;
            }
        } else if (maxLeftX > minRightY) {
            end = partitionX - 1;
        } else {
            start = partitionX + 1;
        }
    }
};
```



### Solution: Break Down

#### 1. Define Loop

```javascript
 while (start <= end) {
        let partitionX = (start + end) >> 1;
        let partitionY = ((x + y + 1) >> 1) - partitionX;
```

The binary search is performed in a `while` loop. The algorithm calculates `partitionX` and `partitionY` to divide `nums1` and `nums2` into left and right halves, respectively. The sum of the elements on the left side should be equal to or one more than the sum on the right side.

#### 2. Define maxLeft, maxRight for X and Y

```javascript
let maxLeftX = (partitionX === 0) ? -Infinity : nums1[partitionX - 1];
        let minRightX = (partitionX === x) ? Infinity : nums1[partitionX];
        
        let maxLeftY = (partitionY === 0) ? -Infinity : nums2[partitionY - 1];
        let minRightY = (partitionY === y) ? Infinity : nums2[partitionY];
```

The `maxLeftX`, `minRightX`, `maxLeftY`, and `minRightY` variables represent the border elements of the partitions in `nums1` and `nums2`. If a partition has no elements on the left or right side, it uses `-Infinity` or `Infinity`, respectively, to allow comparisons to be performed correctly.

#### 3. Check the partition

```javascript
if (maxLeftX <= minRightY && maxLeftY <= minRightX) {
```

Here, the algorithm checks whether the current partition is correct. It's correct if the largest element on the left side of the partition in `nums1` (`maxLeftX`) is not greater than the smallest element on the right side of the partition in `nums2` (`minRightY`), and the largest element on the left side of the partition in `nums2` (`maxLeftY`) is not greater than the smallest element on the right side of the partition in `nums1` (`minRightX`).

If this condition is met, it means all the elements on the left side of the partition are less than or equal to the elements on the right side, which is the property of a sorted array that the algorithm leverages to find the median.

#### 4. Return median

```javascript
if ((x + y) & 1) {
    return Math.max(maxLeftX, maxLeftY);
} else {
    return (Math.max(maxLeftX, maxLeftY) + Math.min(minRightX, minRightY)) / 2;
}
```

Once the correct partition is found, the median is calculated and returned. If the total number of elements in `nums1` and `nums2` (`x + y`) is odd, the median is the maximum element on the left side of the partition. If the total number of elements is even, the median is the average of the maximum element on the left side and the minimum element on the right side.

#### 5. Adjust the search space

```javascript
} else if (maxLeftX > minRightY) {
    end = partitionX - 1;
} else {
    start = partitionX + 1;
}
```
