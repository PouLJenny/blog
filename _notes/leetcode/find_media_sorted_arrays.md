# 寻找两个有序数组的中位数

https://leetcode.cn/problems/median-of-two-sorted-arrays/solutions/258842/xun-zhao-liang-ge-you-xu-shu-zu-de-zhong-wei-s-114/?source=vscode

有A,B两个有序数组

A的长度为m
B的长度为n

在任意位置i将A划分为两个部分 left : A[0] ~ A[i - 1] , right: A[i] ~ A[m - 1]
在任意位置j将B划分为两个部分 left : B[0] ~ B[j - 1] , right: B[j] ~ B[n - 1]

len(left_A)=i,len(right_A)=m−i

len(left_B)=j,len(right_B)=n−j


当 A 和 B 的总长度是偶数时，如果可以确认：

- len(left_part)=len(right_part)
- max(left_part)≤min(right_part)


当 A 和 B 的总长度是奇数时，如果可以确认：

- len(left_part)=len(right_part)+1
- max(left_part)≤min(right_part)

当m +n 是偶数时：
- i + j = m - i + n - j 
当m +n 是奇数时：
- i + j = m - i + n - j + 1

所以可以得到 (i + j) = (m + n + 1) / 2



