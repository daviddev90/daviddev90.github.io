2023-08-06

## Problem

https://leetcode.com/problems/string-to-integer-atoi/description/

Implement the `myAtoi(string s)` function, which converts a string to a 32-bit signed integer (similar to C/C++'s `atoi` function).

The algorithm for `myAtoi(string s)` is as follows:

1. Read in and ignore any leading whitespace.
2. Check if the next character (if not already at the end of the string) is `'-'` or `'+'`. Read this character in if it is either. This determines if the final result is negative or positive, respectively. Assume the result is positive if neither is present.
3. Read in the next characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored.
4. Convert these digits into an integer (i.e., `"123" -> 123`, `"0032" -> 32`). If no digits were read, then the integer is `0`. Change the sign as necessary (from step 2).
5. If the integer is out of the 32-bit signed integer range `[-231, 231 - 1]`, then clamp the integer so that it remains in the range. Specifically, integers less than `-231` should be clamped to `-231`, and integers greater than `231 - 1` should be clamped to `231 - 1`.
6. Return the integer as the final result.

## Solution

### My Original Solution 

First, I just wanted to understand the question, so I wrote straightforward code.

#### Full Code

```javascript
const myAtoi = function(s) {
    s = s.trim();
    let multiplier = 1;
    let numberString = '';
    if (s[0] === '-'){
        multiplier = -1;
        s = s.substring(1);
    } else if (s[0] === '+'){
        s = s.substring(1);
    }
    
    for(let i = 0; i < s.length; i++){
        const c = s[i];
        if(!isNaN(c*1) && c !==" "){
            numberString += c;
        } else{
            break;
        }
    }
    if(numberString === ''){
        return 0;
    }
    let output = numberString * multiplier;
    if(output > 2**31 - 1){
        return 2**31 - 1;
    }
    if(output < -(2**31)){
        return -(2**31)
    }
    return output
};
```

#### Explain

```javascript
s = s.trim();
```

In the first line, I trimmed whitespaces to deal with leading whitespaces.

```javascript
if (s[0] === '-'){
    multiplier = -1;
    s = s.substring(1);
} else if (s[0] === '+'){
    s = s.substring(1);
}
```

I use **else if** because there are the cases like **'-+83'**, in which the return value should be **0**.

```javascript
if(output > 2**31 - 1){
    return 2**31 - 1;
}
if(output < -(2**31)){
    return -(2**31)
}
```

The return value should be a 32-bit signed integer. So I added the above code, but I wish it was cleaner.

#### Result and Time Complexity.

![image-20230808003730830](../../../../images/typora/image-20230808003730830.png)

Time complexity is $O(n)$. Because there is only one loop.
