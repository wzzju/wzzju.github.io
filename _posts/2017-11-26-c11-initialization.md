---
layout: post
title: C++11统一初始化
date: 2017-11-26
comments: true
toc: true
categories: [ "C++", "C++11" ]
---

> 本文第一次编写于2017年11月26日，在深入理解`C++11统一初始化`后，于2022年5月3日进行完善。

## 统一初始化的用法

在C++11之前，我们多值填充初始化一个vector列表，需要书写如下的冗余代码：

```cpp
vector<int> i;

// populate the vector
i.push_back(1);
i.push_back(2);
i.push_back(3);
i.push_back(4);
```

C++11提供了一个名为“Uniform Initialization”的特征，它的目的就是为了解决上述的问题，上面的代码在C++11中改变如下：

```cpp
vector<int> i{1,2,34};
```

`Uniform Initialization`所带来的方便不仅如此，让我们再看一个例子。因为`person`类定义了一个包含三个参数（`first_name,`）的构造器，我们可以通过`Uniform Initialization`去设置这三个变量。

```cpp
// declare the person class
class person {
  public:
    person(void) = default;
    person(const string& fn, const string &ln, const int a) 
      : first_name(fn), last_name(ln), age(a) { }
    virtual ~person(void) = default;

  private:
    string first_name, last_name;
    int age;
};

// initialize a person
person p { "John", "Smith", 25 };

// initialize a vector of people
vector<person> people { {"Mary", "Brown", 21},
                        {"Joe", "Jones", 35},
                        p,
                        {"Sally", "Green", 32} };
```
这个语法适用于任何枚举类型的容器。例如，下面的代码利用`person`类声明了一个名为employees的map：
```
map<int, person> employees {
  {1, {"Mary", "Brown", 21}},
  {2, {"Joe", "Jones", 35}},
  {3, {"John", "Smith", 25}},
  {4, {"Sally", "Green", 32}}
};
```

正如那你所看到的，该语法使得初始化过程在C++中变得更加友好。

## 统一初始化的优缺点
C++11中提出的统一初始化语法仅是一种理想情况下的统一。因为它的实现是基于大括号，所以称其为大括号初始化更为确切。
### 大括号初始化的优点
大括号初始化的优点描述如下：
* 可使用初始化列表直接初始化容器：`std::vector<int> v{1, 3, 5}`。
* 可用于设置类成员变量的默认初始值（也可以使用`=`，但不能使用`()`）。
  ```cpp
  class Widget {
  // ...
  private:
    int x{0};  // x的默认初始值为0
    int y = 0; // 同上
    int z(0);  // 报错
  };
  ```
* 不可拷贝对象(如`std::atomic`)可以用`{}`和`()`初始化，但不能用`=`。
  ```cpp
  std::atomic<int> x{0};  // 可以
  std::atomic<int> y(0);  // 可以
  std::atomic<int> z = 0; // 报错
  ```
* 当大括号初始化应用于内置类型变量时，隐式的窄化转换将被禁止。
  ```cpp
  double ld = 3.14;
  int x {ld}; // 警告：窄化转换
  int y (ld); // 正确
  ```
* 令人烦恼的语法解析规则：*任何可以被解析为声明的东西都必须被解释为一个声明*。使用小括号语法调用无参构造时，会被解析为一个函数声明语句，而不是对象创语句。然而，使用大括号初始化语法则不会。
  ```cpp
  Widget w1(); // 令人头痛的语法解析歧义：声明了一个名为w1，不接受任何参数，返回值类型为Widget的函数
  Widget w2;   // 正确：w2是个默认初始化的对象
  Widget w3{}; // 无歧义
  ```

### 大括号初始化的缺点

构造函数的重载类型中，只要不含有形参为`std::initializer_list<T>`的原型，圆括号和大括号行为是一致的。然而，若构造函数中存在形参为`std::initializer_list<T>`的重载类型，则使用大括号初始化语法调用构造函数时会强制使用带`std::initializer_list<T>`参数的重载构造函数。即使是拷贝构造或移动构造会被带有`std::initializer_list<T>`的构造函数劫持。具体规则描述如下：

* 只要大括号内的值可以被转换为`std::initializer_list<T>`中的元素类型`T`，即使带有`std::initializer_list<T>`参数的构造函数是无法调用的或者没有其他版本的构造函数类型匹配精准，编译器也会忽略其他版本的构造函数。
* 只有当大括号内的值无法被转换为`std::initializer_list<T>`中的元素类型`T`时，编译器才会考虑使用其他版本的构造函数。
* 一个例外：大括号内无参，调用的是**默认构造函数**。因为一个空的大括号代表没有参数，而非一个空的`std::initializer_list`对象。备注：可使用一个空的list来调用带`std::initializer_list<T>`参数的构造函数。

示例1：

```cpp
#include <bits/stdc++.h>

using namespace std;

class Widget {
 public:
  Widget() { cout << "Default ctor\n"; }
  Widget(int i, bool b) { cout << "Widget(int i, bool b)\n"; }
  Widget(int i, double b) { cout << "Widget(int i, double b)\n"; }
  Widget(initializer_list<long double> il) {
    cout << "Widget(initializer_list<long double> il)\n";
  }
  Widget(const Widget& w) { cout << "Widget(const Widget& w)\n"; }
  Widget(Widget&& w) { cout << "Widget(Widget&& w)\n"; }
  operator float() const {
    cout << "operator float()\n";
    return 1.f;
  }
};

int main() {
  Widget w1(10, true);
  Widget w2{10, true};
  Widget w3(10, 5.0);
  Widget w4{10, 5.0};
  Widget w5(w1);
  Widget w6{w1};
  Widget w7(move(w1));
  Widget w8{move(w1)};
  // `{}`调用默认构造函数
  Widget w9{};
  // 使用一个空的list来调用带std::initializer_list构造函数
  Widget w10({});
  return 0;
}
// Output:
// Widget(int i, bool b)
// Widget(initializer_list<long double> il)
// Widget(int i, double b)
// Widget(initializer_list<long double> il)
// Widget(const Widget& w)
// operator float()
// Widget(initializer_list<long double> il)
// Widget(Widget&& w)
// operator float()
// Widget(initializer_list<long double> il)
// Default ctor
// Widget(initializer_list<long double> il)
```

示例2：

```cpp
std::vector<int> v1(10, 20);  // 使用不带std::initializer_list的构造函数
                              // 创建10个元素初始值为20的vector

std::vector<int> v2{10, 20};  // 使用带std::initializer_list的构造函数
                              // 创建2个元素的vector，元素值分别为10和20
```

## 参考资料
* [Uniform Initialization with C++11](http://tuttlem.github.io/2013/01/17/uniform-initialization-with-c-11.html)

* [Effective Modern C++: Item 7](https://www.amazon.com/Effective-Modern-Specific-Ways-Improve/dp/1491903996)
