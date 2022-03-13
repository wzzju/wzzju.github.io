---
layout: post
title: C++11统一初始化
date: 2017-11-26
comments: true
toc: false
categories: [ "C++", "C++11" ]
---

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