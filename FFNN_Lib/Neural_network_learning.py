# neural network class definition 神经网络类定义
import numpy
from scipy.special import expit
import matplotlib.pyplot
import pylab
import time
import pickle


class Neural_network:

    # initialise the neural network 初始化神经网络
    def __init__(self, input_nodes_in, hidden_nodes_in, output_nodes_in, learning_rate_in, weights_in=False,
                 wih_in=None, who_in=None):
        # set number of nodes in each input, hidden, output layer
        self.i_nodes = input_nodes_in
        self.h_nodes = hidden_nodes_in
        self.o_nodes = output_nodes_in

        # link weight matrices, wih and who 链接权重矩阵，wih和who
        # weights inside the arrays are w_i_j, where link is from node i to node j in the next layer
        # 数组中的权重为w_i_j，其中链接从节点i到下一层中的节点j
        # w11 w21
        # w12 w22 etc
        if weights_in:
            self.wih = wih_in
            self.who = who_in
        else:
            self.wih = numpy.random.normal((1.0 - 1.0), pow(self.h_nodes, -0.5), (self.h_nodes, self.i_nodes))
            self.who = numpy.random.normal((1.0 - 1.0), pow(self.o_nodes, -0.5), (self.o_nodes, self.h_nodes))

        # learning rate 学习率
        self.lr = learning_rate_in

        # activation function is the sigmoid function
        # 激活函数是sigmoid函数
        # Sigmoid函数 :Sigmoid函数是一个在生物学中常见的S型函数，也称为S型生长曲线。
        # 在信息科学中，由于其单增以及反函数单增等性质，Sigmoid函数常被用作神经网络的激活函数，将变量映射到0,1之间。
        self.activation_function = lambda x: expit(x)
        # 图像如下
        """
        import numpy as np
        import matplotlib.pyplot as plt
        def sigmoid(x):
            return 1.0 / (1 + np.exp(-x))

        sigmoid_inputs = np.arange(-10, 10, 0.1)
        sigmoid_outputs = sigmoid(sigmoid_inputs)
        print("Sigmoid Function Input :: {}".format(sigmoid_inputs))
        print("Sigmoid Function Output :: {}".format(sigmoid_outputs))

        plt.plot(sigmoid_inputs, sigmoid_outputs)
        plt.xlabel("Sigmoid Inputs")
        plt.ylabel("Sigmoid Outputs")
        plt.show()
        """

        pass

    # train the neural network 训练神经网络

    def train(self, inputs_list, targets_list):
        # convert inputs list to 2d array 将输入列表转换为二维数组
        inputs_in = numpy.array(inputs_list, ndmin=2).T
        targets_in = numpy.array(targets_list, ndmin=2).T

        # calculate signals into hidden layer 将信号计算到隐藏层中
        hidden_inputs = numpy.dot(self.wih, inputs_in)
        # calculate the signals emerging from hidden layer 计算隐藏层中出现的信号
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer 将信号计算到最终输出层
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer 计算来自最终输出层的信号
        final_outputs = self.activation_function(final_inputs)
        # output layer error is the (target - actual) 输出层错误是（目标-实际）
        output_errors = targets_in - final_outputs
        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        # hidden layer error是输出_错误，按权重分割，在隐藏节点处重新组合
        hidden_errors = numpy.dot(self.who.T, output_errors)

        # update the weights for the links between the hidden and output layers
        # 更新隐藏层和输出层之间链接的权重
        self.who += self.lr * numpy.dot((output_errors * final_outputs * (1.0 - final_outputs)),
                                        numpy.transpose(hidden_outputs))

        # update the weights for the links between the input and hidden layers
        # 更新输入层和隐藏层之间链接的权重
        self.wih += self.lr * numpy.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)),
                                        numpy.transpose(inputs_in))
        pass

    # query the neural network 查询神经网络

    def query(self, input_list):
        # convert inputs list to 2d array 将输入列表转换为二维数组
        inputs_in = numpy.array(input_list, ndmin=2).T

        # calculate signals into hidden layer 将信号计算到隐藏层中
        hidden_inputs = numpy.dot(self.wih, inputs_in)
        # calculate the signals emerging from hidden layer 计算隐藏层中出现的信号
        hidden_outputs = self.activation_function(hidden_inputs)

        # calculate signals into final output layer 将信号计算到最终输出层
        final_inputs = numpy.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer 计算来自最终输出层的信号
        final_outputs = self.activation_function(final_inputs)
        return final_outputs

    def get_weights(self):
        return {"wih": self.wih, "who": self.who}


t1 = time.time()
with open("weight.pkl", 'rb') as r:
    threshold = 1e6
    numpy.set_printoptions(threshold=int(threshold))
    weights_read = dict(pickle.load(r))
# number of input, hidden and output nodes 输入、隐藏和输出节点数
input_nodes = 784
hidden_nodes = 200
output_nodes = 10

# learning rate 学习率
learning_rate = 0.1

# create instance of neural network 神经网络实例的创建
n = Neural_network(input_nodes, hidden_nodes, output_nodes, learning_rate, True, weights_read.get("wih"),
                   weights_read.get("who"))

learn = str(input("训练？"))
if learn == "":
    pass
else:

    network_data_input_count = 20000
    # load the mnist training data csv file into a list 将mnist培训数据csv文件加载到列表中
    with open("data/mnist_train.csv", 'r') as r:  # data/mnist_train.csv
        training_data_list = r.readlines()[:network_data_input_count]

    # train the neural network 训练神经网络

    # epochs is the number if times the training data set is used for training
    # epochs是训练数据集用于训练的次数
    epochs = 15

    for e in range(epochs):
        # go through all records in the training data set
        # 检查培训数据集中的所有记录
        for record in training_data_list:
            # split the record by the ',' commas 将记录拆分为“，”逗号
            all_values = record.split(",")
            # scale and shift the inputs 缩放和移动输入
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            # create the target output values (all 0.01, except the desired label which is 0.99)
            # 创建目标输出值（除所需标签为0.99外，所有值均为0.01）
            targets = numpy.zeros(output_nodes) + 0.01
            # all_values[0] is the target label for this record
            # 所有_值[0]都是此记录的目标标签
            targets[int(all_values[0])] = 0.99
            n.train(inputs, targets)
            pass
        pass

network_data_test_count = 1000
# load the mnist test data csv file into a list 将mnist测试数据csv文件加载到列表中
with open("data/mnist_test.csv", 'r') as r:  # data/mnist_test.csv
    test_data_list = r.readlines()[:network_data_test_count]

# test the neural network 测试神经网络

# scorecard for how well the network performs, initially empty 网络表现的记分卡，最初为空
scorecard = []
show_picture = False

# go through all the records in the test data set 检查测试数据集中的所有记录
for record in test_data_list:
    # split the record by the ',' commas 将记录拆分为“，”逗号
    all_values = record.split(",")
    if show_picture:
        image_array = numpy.asfarray(all_values[1:]).reshape((28, 28))
        matplotlib.pyplot.imshow(image_array, cmap='Greys', interpolation="None")
        pylab.show()
    # correct answer is first value 正确答案是第一个值
    correct_label = int(all_values[0])
    # scale and shift the inputs 缩放和移动输入
    inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
    # query the network 查询网络
    outputs = n.query(inputs)
    # the index of the highest value corresponds to the label 最高值的索引对应于标签
    label = numpy.argmax(outputs)
    print(label)
    # append correct or incorrect to list 在列表中添加正确或不正确的内容
    if label == correct_label:
        # network's answer matches correct answer, add 1 to scorecard 网络的答案与正确答案匹配，将1添加到记分卡
        scorecard.append(1)
    else:
        # network's answer doesn't match correct answer, add 0 to scorecard 网络的答案与正确答案不匹配，请将0添加到记分卡
        scorecard.append(0)
        pass

    pass

# calculate the performance score, the fraction of correct answer 计算成绩分数，正确答案的分数
scorecard_array = numpy.asarray(scorecard)
print("performance = ", scorecard_array.sum() / scorecard_array.size)
t2 = time.time()
print(t2 - t1)
is_save = str(input("save?"))
if is_save == "" or is_save == "no" or is_save == "false" or is_save == "n" or is_save == "f":
    pass
else:
    threshold = 1e6
    with open("weight.pkl", 'wb') as w:
        numpy.set_printoptions(threshold=int(threshold))
        thing = n.get_weights()
        pickle.dump(thing, w)
