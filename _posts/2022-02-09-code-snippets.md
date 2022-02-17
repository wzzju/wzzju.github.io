---
layout: post
title: 有用的C++程序片段
date: 2022-02-09
comments: true
toc: true
categories: [ "C++" ]
---

## 生成随机数

```cpp
#include <cstdlib>
#include <ctime>

// "int rand(void)" returns a pseudo-random integer
// value between 0 and RAND_MAX (0 and RAND_MAX included).
// RAND_MAX is a constant whose default value
// may vary between implementations, but it is
// granted to be at least 32767.

// Create random numbers in [m, n]:
// 0 <= rand() % (n - m + 1) <= n - m
//                ||
//                \/
// m <= rand() % (n - m + 1) + m <= n
// e.g. 10 <= random <= 30
// srand(static_cast<unsigned>(time(nullptr)));
srand(time(nullptr));
int rn = rand() % (30 - 10 + 1) + 10;

// e.g. 0 <= random <= 1
float rnf = rand() / static_cast<float>(RAND_MAX);
```

## 取数据类型limit

```cpp
#include <cfloat>
#include <climits>

#define FLT_LOWEST (-FLT_MAX)
#define DBL_LOWEST (-DBL_MAX)
#define LDBL_LOWEST (-LDBL_MAX)

#define PRINT_LIMIT(N) LOG(INFO) << #N " = " << N

// int
PRINT_LIMIT(INT_MIN);
PRINT_LIMIT(INT_MAX);
// long
PRINT_LIMIT(LONG_MIN);
PRINT_LIMIT(LONG_MAX);
// long long
PRINT_LIMIT(LONG_LONG_MIN);
PRINT_LIMIT(LONG_LONG_MAX);
// float
PRINT_LIMIT(FLT_LOWEST);
PRINT_LIMIT(FLT_MIN);
PRINT_LIMIT(FLT_MAX);
// double
PRINT_LIMIT(DBL_LOWEST);
PRINT_LIMIT(DBL_MIN);
PRINT_LIMIT(DBL_MAX);
// long double
PRINT_LIMIT(LDBL_LOWEST);
PRINT_LIMIT(LDBL_MIN);
PRINT_LIMIT(LDBL_MAX);
```

* 输出如下：
```shell
INT_MIN = -2147483648
INT_MAX = 2147483647
LONG_MIN = -9223372036854775808
LONG_MAX = 9223372036854775807
LONG_LONG_MIN = -9223372036854775808
LONG_LONG_MAX = 9223372036854775807
FLT_LOWEST = -3.40282e+38
FLT_MIN = 1.17549e-38
FLT_MAX = 3.40282e+38
DBL_LOWEST = -1.79769e+308
DBL_MIN = 2.22507e-308
DBL_MAX = 1.79769e+308
LDBL_LOWEST = -1.79769e+308
LDBL_MIN = 2.22507e-308
LDBL_MAX = 1.79769e+308
```

## Map方式调用成员方法

* (1)和(2)提供了两种以Map的方式存储成员方法，以便后续替代`if`/`switch`的形式进行调用。
* 方式(2)借助了`std::function`，可读性更好。


```cpp
#include <functional>
#include <unordered_map>

enum class Precedences { LOWEST = 1, Middle, Higher };

class Call {
  using FT = void (Call::*)(int); // (1)
  using FN_FT = std::function<void(int)>; // (2)

 public:
  Call() {
    map_.emplace(Precedences::LOWEST, &Call::Add); // (1)
    fn_map_.emplace(Precedences::LOWEST, [this](int val) { Add(val); }); // (2)
    // fn_map_.emplace(Precedences::LOWEST, [this](auto&& val) {
    //   add(std::forward<decltype(val)>(val));
    // });
    // fn_map_.emplace(Precedences::LOWEST,
    //                 std::bind(&Call::add, this, std::placeholders::_1));
  }

  void operator()(Precedences p, int v) {
    (this->*map_.at(p))(v); // (1)
    fn_map_.at(p)(v); // (2)
  }

 private:
  void Add(int v) { val_ += v; }

  std::unordered_map<Precedences, FT> map_; // (1)
  std::unordered_map<Precedences, FN_FT> fn_map_; // (2)
  int val_{};
};

// usage
Call c;
c(Precedences::LOWEST, 2);
```