---
layout: post
title: "使用Python绘制图表(转)"
date: 2017-02-06
comments: true
categories: [ "Python" ]
---

*本文转载自[使用Python绘制图表](https://m.hellobi.com/post/6195)*。

在使用Python绘制图表前，我们需要先安装两个库文件numpy和matplotlib。

Numpy是Python开源的数值计算扩展，可用来存储和处理大型矩阵，比Python自身数据结构要高效；matplotlib是一个Python的图像框架，使用其绘制出来的图形效果和MATLAB下绘制的图形类似。

下面介绍如何使用 Python绘图。

**注意**：  
1）使用notebook绘图时需要就加入一句`%pylab inline`以在页面内显示所绘制图形。    
2）使用`import matplotlib.pyplot as plt`导入绘图库。  
3）使用`plt.show() `显示图形。  
4）使用`plt.savefig('images/line.eps', format='eps')`保存图形到指定格式并显示图形。format可取值为jpg、png、eps等。  
5）使用`plt.savefig`时不要使用`plt.show `。


## 一、图形绘制


```python
%pylab inline
```


#### 直方图


```python
import matplotlib.pyplot as plt

import numpy as np

mu = 100

sigma = 20

x = mu + sigma * np.random.randn(20000)  # 样本数量

plt.hist(x,bins=100,color='green',normed=True)   # bins显示中存在几个直方,normed是否对数据进行标准化

# plt.show() # 显示图形，使用了plt.savefig时不要再使用plt.show

plt.savefig('images/line.eps', format='eps') # 保存图形到指定格式
```


![png](/images/posts/matplotlib/output_8_0.png)


#### 条形图


```python
import matplotlib.pyplot as plt

import numpy as np

y = [20,10,30,25,15]

index = np.arange(5)

plt.bar(left=index, height=y, color='green', width=0.5)

plt.show()

```


![png](/images/posts/matplotlib/output_10_0.png)

#### 柱状图

```python
import matplotlib.pyplot as plt
import numpy as np
plt.rc('font', family='Arial', size=9)
 
num = np.array([13325, 9403, 9227, 8651])
ratio = np.array([0.75, 0.76, 0.72, 0.75])
men = num * ratio
women = num * (1-ratio)
x = ['A','B','C\nC','D']
 
width = 0.5
idx = np.arange(len(x))
plt.bar(idx, men, width, color='red', label='Male')
plt.bar(idx, women, width, bottom=men, color='yellow', label='Female')
plt.xlabel('Type')
plt.ylabel('Distribution')
plt.xticks(idx+width/2, x, rotation=40)
plt.legend()
plt.savefig('images/bar.eps', format='eps',dpi=1000)
```

![png](/images/posts/matplotlib/output_34_0.png)

#### 折线图


```python
import matplotlib.pyplot as plt

import numpy as np

x = np.linspace(-10,10,100)

y = x**3

plt.plot(x,y,linestyle='--',color='green',marker=',')

plt.show()
```


![png](/images/posts/matplotlib/output_12_0.png)


#### 散点图


```python
import matplotlib.pyplot as plt

import numpy as np

x = np.random.randn(1000)

y = x+np.random.randn(1000)*0.5

plt.scatter(x,y,s=5,marker='<')  # s表示面积，marker表示图形

plt.show()

```


![png](/images/posts/matplotlib/output_14_0.png)


#### 饼状图


```python
import matplotlib.pyplot as plt

import numpy as np

labels = 'A','B','C','D'

fracs = [15,30,45,10]

plt.axes(aspect=1)  #使x y轴比例相同

explode = [0,0.05,0,0]  # 突出某一部分区域

plt.pie(x=fracs, labels=labels, autopct='%.1f%%', explode=explode)  #autopct显示百分比

plt.show()
```


![png](/images/posts/matplotlib/output_16_0.png)


#### 箱形图

主要用于显示数据的分散情况。图形分为上边缘、上四分位数、中位数、下四分位数、下边缘。外面的点是异常值。


```python
import matplotlib.pyplot as plt

import numpy as np

np.random.seed(100)

data = \
np.random.normal(size=(1000,4),loc=0,scale=1)

labels = ['A','B','C','D']

plt.boxplot(data,labels=labels)

plt.show()

```


![png](/images/posts/matplotlib/output_19_0.png)


## 二、图像的调整

#### 1、20余种点形状

> `"."  point     ","  pixel     "o" circle      "v" triangle_down`

> `"^"  triangle_up     "<" triangle_left     ">" triangle_right     "1"  tri_down`

> `"2"  tri_up       "3"  tri_left      "4"  tri_right       "8"  octagon`

> `"s"  square     "p"  pentagon     "*"  star     "h"  hexagon1     "H"  hexagon2`

> `"+"  plus     "x"  x      "D"  diamond      "d"  thin_diamond`

#### 2、8种內建默认颜色的缩写

> `b:blue         g:green       r:red       c:cyan`

> `m:magenta      y:yellow      k:black     w:white`

#### 3、4种线性

> `- 实线     --虚线      -.点划线   ：点线`

#### 4、一张图上绘制子图


```python
import matplotlib.pyplot as plt

import numpy as np

x=np.arange(1,100)

plt.subplot(221)  # 2行2列第1个图

plt.plot(x,x,'r-*')

plt.subplot(222)

plt.plot(x,-x,'g--.')

plt.subplot(223)

plt.plot(x,x*x,'b-.+')

plt.subplot(224)

plt.plot(x,np.log(x),'y:^')

plt.show()
```


![png](/images/posts/matplotlib/output_28_0.png)


#### 5、生成网格


```python
import matplotlib.pyplot as plt

import numpy as np

y=np.arange(1,5)

plt.plot(y,y,'r-p')
plt.plot(y,y*2,'g--s')
plt.plot(y,y*3,'b-..')
plt.plot(y,y*4,'k:x')

plt.grid(True,color='g',linestyle='--',linewidth='1')

plt.show()
```


![png](/images/posts/matplotlib/output_30_0.png)


#### 6、生成图例


```python
import matplotlib.pyplot as plt

import numpy as np

x=np.arange(1,11,1)

plt.plot(x,x*2)

plt.plot(x,x*3)

plt.plot(x,x*4)

plt.legend(['Normal','Fast','Faster'])

plt.show()

```


![png](/images/posts/matplotlib/output_32_0.png)

