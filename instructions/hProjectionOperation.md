# hProjectionOperation

垂直投影的逻辑，及使用文档。

### 1.逻辑

#### 1.1基础

如下，图一为原五线谱，图二为hProjection(后文简写hPjc)
![示例](https://foruda.gitee.com/images/1665837632184286024/41fd901f_10062986.png "test0.png")
图二：
![示例](https://foruda.gitee.com/images/1665837490950593627/117e6b50_10062986.png "hProjection2.png")
不难从图二看出，这个操作的目的，是非常简易的通过算法来确定五线谱的大体位置。
而这个投影函数的实现则是把灰度图的黑像素移至右边，白像素移至左边。

这个函数`getHProjection()`在`tool_functions.py`中可以找到。

#### 1.2读取顺序

这里会说到读取的逻辑，包括配合其他操作出来的数据。

##### 1.2.1 hProjection连续性扫描

在获取到每一行的black pix count后，应对每一行进行扫描，扫描之后要把白色区间和黑色区间返回。

这个函数`lineO_hProjectionContinuousScanning()`在`lineOperation.py`中可以找到，用法如下：
> `lineO_hProjectionContinuousScanning(inL: numpy.ndarray) -> list:`
> 
> 返回连续像素范围
> 
> `:param inL 输入的数组`
> 
> `:return 一个list 如下：`
> 
> `[{'white': [0, 152]}, {'black': [153, 246]}, {'white': [247, 255]}, ..., {'black': [2203, 2224]}, 
    {'white': [2225, 2338]}]`

