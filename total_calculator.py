#完全版的计算器，加减乘除都有--基于链表实现的
#小部件的实例--不用当参数传递给函数
from tkinter import *
import tkinter as tk
import re

root = Tk()
root.title("total calculator")

#显示器显示数字--这个逻辑需要在最后出现
number = Entry(root,width = 45,borderwidth = 5)
number.grid(row=0,column=0, columnspan= 3, padx=10,pady=5)

#按键效果--将按键对应值放到Entry，并检测是否符合语法
def button_math(text):
    test_symbol = ["+","-","*","/","="]
    test = number.get()

#一个错误，运算符出现在第一个位置
    if (text in test_symbol) and (len(test) == 0):
        print("语法错误，请重新输入")
        return None
#连续两个运算符？
    elif (text in test_symbol) and (test[len(test)-1] in test_symbol):
        print("语法错误，请重新输入")
        return None
    number.insert(tk.END,text)

    #检测是否为=，开始进入计算
    if text == "=":
        meet_equal_cal()

    return True
    
    
#clear的用法
def clear_entry():
    number.delete(0, tk.END)
#取消所有的文本
    
#描述等号的作用，分有加号，没有加号-哪些情况属于语法错误？检测手段
#语法错误-连续输入加减乘除和=，从左到右-提示重新输入，并清除最后一个符号 
#语法正确-只有=输入才开始计算。因为没有括号的因素-将元素分解后，设计成双端链表-到了乘除，前端后端运算，与下一个运算符相连接。
    #属于经常删减，较少访问的情况，就用链表-- 如果修改，访问都很频繁呢？什么数据结构适合--该符号是等号的话，aft是none
    #遇见等号的话-直接return self.pre



class Number_link:
    def __init__(self,pre,aft,data):
        self.data = data 
        self.pre = pre
        self.aft = aft
    
    #融合链表--类的方法定义临时变量
    def merge(self):
        self.aft = self.aft.aft
        self.aft.pre = self

        if(self.pre.pre != None):
            self.pre = self.pre.pre
            self.pre.aft = self
        else:
            self.pre.aft = None
            self.pre = None
        

    #当该data是运算符号时,改变字符
    def math_symbol(self):
    #已经做过检测后,不用再检测语法,链接数据---容易犯的错误：没有转化字符串为Int
        a = int(self.aft.data)
        b = int(self.pre.data)
        if self.data == "+":
            self.data = a + b
        elif self.data == "-":
            self.data = a - b
        elif self.data == "*":
            self.data = a * b
        elif self.data == "/":
            self.data = a / b
        
        self.merge()

#专门的计算程序-基于不带括号的+-*/ --- num是链表的开始
def math_cal(num):
    #先第一遍清理所有的*/运算--如果第一个头结点被消除，Num就空了，因此要注意，如果每次消除涉及第一个，即point.pre.pre==None
    #就需要把它移到目前的位置。
    point = num
    while point.data != "=":
        if point.data == "*" or point.data == "/":
            point.math_symbol()
            if point.pre == None: #此时合并后，成为第一个头结点
                num = point#要把该节点盯紧
        point = point.aft
    #如果此时运算结束

    #第二遍是+-运算 
    point = num
    
    while point.data != "=":
        if point.data == "+" or point.data == "-":
            point.math_symbol()
        point = point.aft

    return point.pre.data

#当遇到=开始运算最终结果后，合成一个链表，使用方法计算。并清空显示数值，附上合成的结果-这里已经检测过了
def meet_equal_cal():
    member_list = []
    e = number.get()

    #写入列表,创建了一个包含运算符的列表
    member_list = re.split(r'(\+|\-|\*|\/|\=)', e)
    #创建链表,第一个表达式开始--一个完整的表达式
    start = Number_link(None,None,member_list[0])
    #删除最后一个空白
    del member_list[len(member_list)-1]
    f_point = start
    s_point = start
    #创建双端链表,返回链表头引用

    for i in range(len(member_list)):
        if member_list[i] != "=":
            s_point = Number_link(f_point,None,member_list[i+1])
            f_point.aft = s_point
            f_point = s_point
        else:
            break
    value = math_cal(start)
    clear_entry()
    number.insert(tk.END,value)
    return start
       

#按钮设置，13个button的位置--Q: 每个按钮一个Button？
number_button = []

#用列表存储，再和显示数值联系--command使用lambda 潜在传递参数
for i in range(10):
    
    number_button.append(Button(root, text=i, padx=40,pady=20, command = lambda t=i:button_math(t)))

number_button.append(Button(root, text="clear", padx=40,pady=20,width = 18,command = clear_entry))
number_button.append(Button(root, text="+", padx=40,pady=20, command = lambda :button_math("+")))
number_button.append(Button(root, text="=", padx=40,pady=20, command = lambda :button_math("="),width = 18))
number_button.append(Button(root, text="-", padx=40,pady=20, command = lambda :button_math("-")))
number_button.append(Button(root, text="*", padx=40,pady=20, command = lambda :button_math("*")))
number_button.append(Button(root, text="/", padx=40,pady=20, command = lambda :button_math("/")))

#安排按钮位置
i = 0
for i in range(3):
    number_button[i*3].grid(row=i+1,column=0,pady=5)
    number_button[i*3+1].grid(row=i+1,column=1,pady=5)
    number_button[i*3+2].grid(row=i+1,column=2,pady=5)
number_button[9].grid(row=4,column=0,pady=5)
number_button[10].grid(row=4,column=1,pady=5,columnspan = 2)
number_button[11].grid(row=5,column=0,pady=5)
number_button[12].grid(row=5,column=1,pady=5,columnspan = 2)
number_button[13].grid(row=6,column=0,pady=5)
number_button[14].grid(row=6,column=1,pady=5)
number_button[15].grid(row=6,column=2,pady=5)

root.mainloop()
