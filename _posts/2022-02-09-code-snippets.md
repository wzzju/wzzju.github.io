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

## 字符串分割

* 【分割最精准】使用正则表达式分割字符串，且分割的结果中包括空白字符

```cpp
void split(const string& str, const string& del, vector<string>& vals) {
  regex reg(del);
  // -1表示返回未匹配的部分
  vals.assign(sregex_token_iterator(str.begin(), str.end(), reg, -1),
              sregex_token_iterator());
}
```
> **注意：**
>
> 1) 假设分割符为`#`：对于字符串`"#1#2##3#"`，使用上述基于正则表达式的字符串分割函数split所得结果为`{,1,2,,3}`，结果size为5。**最前面有一个空串，最后面却没有空串，中间存在空串。**
>
> 2）假设分割符为`#`：对于空串`""`，使用上述基于正则表达式的字符串分割函数split所得结果为`{}`，结果size为1，**即包括一个空串**。


* 分割的结果中包括空白字符

```cpp
// There will be blanks in the result.
void split(const string& str, char del, vector<string>& vals) {
  istringstream is(str);
  string val;
  while (getline(is, val, del)) {
    vals.emplace_back(move(val));
  }
}
```

* 分割的结果中不包括空白字符，且目标串str中不含有del中的任何字符

```cpp
// There is no blank in the result.
void split(const string& str, const string& del, vector<string>& vals) {
  auto beg = str.find_first_not_of(del, 0);
  auto end = str.find_first_of(del, beg);
  while (beg != string::npos || end != string::npos) {
    vals.emplace_back(str.substr(beg, end - beg));
    beg = str.find_first_not_of(del, end);
    end = str.find_first_of(del, beg);
  }
}
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

## C++万能头文件
`<bits/stdc++.h>`仅适用于GNU g++，但它不属于GNU C++库的标准头文件，在部分情况下可能会导入失败。该头文件主要用于竞赛中的代码编写，可以节约时间和减少记忆成本。然而，**在实际工程项目中切勿使用该头文件。**

```cpp
// 下面两条语句仅用于竞赛中的代码编写
#include <bits/stdc++.h>
using namespace std;
```

## 打印STL容器内容
[adah1972/output_range](https://github.com/adah1972/output_range)基于c++17标准提供了一套可打印STL容器和原生数组内容的header-only代码，内容摘录如下：

```cpp
// output_range.h

#include <iterator>     // std::begin/end
#include <ostream>      // std::ostream
#include <tuple>        // std::tuple
#include <type_traits>  // std::false_type/true_type/decay_t/is_same_v/remove_...
#include <utility>      // std::declval/forward/pair

namespace output_range {

using std::begin;
using std::end;

template <class Rng>
auto adl_begin(Rng&& rng) -> decltype(begin(rng)) {
  // Intentionally not using std::forward, as std::begin does not
  // accept an rvalue reference.
  return begin(rng);
}

template <class Rng>
auto adl_end(Rng&& rng) -> decltype(end(rng)) {
  // Intentionally not using std::forward, as std::end does not
  // accept an rvalue reference.
  return end(rng);
}

}  // namespace output_range

// Type trait to detect std::pair
template <typename T>
struct is_pair : std::false_type {};
template <typename T, typename U>
struct is_pair<std::pair<T, U>> : std::true_type {};
template <typename T>
inline constexpr bool is_pair_v = is_pair<T>::value;

// Type trait to detect whether an output function already exists
template <typename T>
struct has_output_function {
  template <class U>
  static auto output(U* ptr)
      -> decltype(std::declval<std::ostream&>() << *ptr, std::true_type());
  template <class U>
  static std::false_type output(...);
  static constexpr bool value = decltype(output<T>(nullptr))::value;
};
#ifndef OUTPUT_RANGE_NO_ARRAY_OUTPUT
template <typename T, std::size_t N>
struct has_output_function<T[N]> : std::false_type {};
template <std::size_t N>
struct has_output_function<char[N]> : std::true_type {};
#endif
template <typename T>
inline constexpr bool has_output_function_v = has_output_function<T>::value;

// Output function for std::pair
template <typename T, typename U>
std::ostream& operator<<(std::ostream& os, const std::pair<T, U>& pr);

// Output function for std::tuple
template <typename... Args>
std::ostream& operator<<(std::ostream& os, const std::tuple<Args...>& args);

// Element output function for containers that define a key_type and
// have its value type as std::pair
template <typename T, typename Rng>
auto output_element(std::ostream& os, const T& element, const Rng&,
                    std::true_type)
    -> decltype(std::declval<typename Rng::key_type>(), os);
// Element output function for other containers
template <typename T, typename Rng>
auto output_element(std::ostream& os, const T& element, const Rng&, ...)
    -> decltype(os);

// Main output function, enabled only if no output function already exists
template <typename Rng, typename = std::enable_if_t<!has_output_function_v<
                            std::remove_cv_t<std::remove_reference_t<Rng>>>>>
auto operator<<(std::ostream& os, Rng&& rng)
    -> decltype(output_range::adl_begin(std::forward<Rng>(rng)),
                output_range::adl_end(std::forward<Rng>(rng)), os) {
  using std::decay_t;
  using std::is_same_v;

  using element_type =
      decay_t<decltype(*output_range::adl_begin(std::forward<Rng>(rng)))>;
  constexpr bool is_char_v = is_same_v<element_type, char>;
  if constexpr (!is_char_v) {
    os << '{';
  }
  auto end = output_range::adl_end(std::forward<Rng>(rng));
  bool on_first_element = true;
  for (auto it = output_range::adl_begin(std::forward<Rng>(rng)); it != end;
       ++it) {
    if constexpr (is_char_v) {
      if (*it == '\0') {
        break;
      }
    } else {
      if (!on_first_element) {
        os << ", ";
      } else {
        os << ' ';
        on_first_element = false;
      }
    }
    output_element(os, *it, std::forward<Rng>(rng), is_pair<element_type>());
  }
  if constexpr (!is_char_v) {
    if (!on_first_element) {  // Not empty
      os << ' ';
    }
    os << '}';
  }
  return os;
}

template <typename T, typename Rng>
auto output_element(std::ostream& os, const T& element, const Rng&,
                    std::true_type)
    -> decltype(std::declval<typename Rng::key_type>(), os) {
  os << element.first << " => " << element.second;
  return os;
}

template <typename T, typename Rng>
auto output_element(std::ostream& os, const T& element, const Rng&, ...)
    -> decltype(os) {
  os << element;
  return os;
}

template <typename T, typename U>
std::ostream& operator<<(std::ostream& os, const std::pair<T, U>& pr) {
  os << '(' << pr.first << ", " << pr.second << ')';
  return os;
}

template <typename Tup, std::size_t... Is>
void output_tuple_members(std::ostream& os, const Tup& tup,
                          std::index_sequence<Is...>) {
  ((os << (Is != 0 ? ", " : "") << std::get<Is>(tup)), ...);
}

template <typename... Args>
std::ostream& operator<<(std::ostream& os, const std::tuple<Args...>& args) {
  os << '(';
  output_tuple_members(os, args, std::index_sequence_for<Args...>{});
  os << ')';
  return os;
}
```

若在某个命名空间中对`operator<<`进行了重载，这将会隐藏全局定义的`::operator<<`，进而可能会导致编译失败。通过在相应命名空间中使用`using ::operator<<;`，参数依赖查找（ADL）规则可以正确找到全局定义的`::operator<<`。更多关于[名字隐藏（name hiding）](https://www.ibm.com/docs/en/zos/2.2.0?topic=scope-name-hiding-c-only)规则的内容详见[Argument-Dependent Lookup](https://blog.csdn.net/qq_17550379/article/details/80007769)。示例代码如下：
{% raw %}
```cpp
#include <iostream>
#include <string>
#include <vector>
// output_range.h包含打印STL容器和原生数组内容的header-only代码
#include "output_range.h"

using namespace std;

namespace output {
struct P {
  string name{"Tom"};
  int age{10};
};

// name hiding规则将会隐藏全局定义的`::operator<<`
ostream& operator<<(ostream& os, const P& p) {
  os << "{ name: " << p.name << ", age: " << p.age << " }";
  return os;
}

void Print() {
  using ::operator<<; // 不使用此语句将导致编译失败
  vector<P> vals{{"Tom", 18}, {"Mike", 26}};
  // 即使将`vector<P>`换成`vector<int>`，不使用`using ::operator<<;`，
  // 这里也会导致编译失败。
  cout << vals << endl;
}
}  // namespace output

int main() {
  output::Print();
  return 0;
}
```
{% endraw %}
