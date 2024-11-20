#! /usr/bin/python

import sys
import csv

prefectures = ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県","茨城県","栃木県","群馬県",
               "埼玉県","千葉県","東京都","神奈川県","新潟県","富山県","石川県","福井県","山梨県","長野県",
               "岐阜県","静岡県","愛知県","三重県","滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県",
               "鳥取県","島根県","岡山県","広島県","山口県","徳島県","香川県","愛媛県","高知県","福岡県",
               "佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"]


class Node:
    def __init__(self, key):
        self.key = key
        self.value = None
        self.count = 0
        self.children = [None] * 10
        self.others = []

    def append(self, key, value):
        if self.key == key:
            if len(self.others) > 0:
                node = Node(key)
                node.value = value
                node.count = 1
                self.others.append(node)
            elif self.value is None:
                self.value = value
                self.count = 1
            elif self.value == value:
                self.count += 1
            else:
                node = Node(key)
                node.value = self.value
                node.count = self.count
                self.others.append(node)
                self.value = None
                self.count = 0
                node = Node(key)
                node.value = value
                node.count = 1
                self.others.append(node)
        elif len(key) <= len(self.key):
            node = Node(key)
            node.value = value
            node.count = 1
            self.others.append(node)
        else:
            next = key[:len(self.key) + 1]
            n = int(next[-1])
            if self.children[n] is None:
                node = Node(next)
                self.children[n] = node
            self.children[n].append(key, value)

    def shrink(self):
        for child in self.children:
            if child is not None:
                child.shrink()
        if len(self.key) < 2:
            return
        children = {}
        for child in self.children:
            if child is not None:
                if child.value in children:
                    children[child.value].append(child)
                else:
                    children[child.value] = [child]
        max = None
        for value in children.keys():
            if max is None or len(children[max]) < len(children[value]):
                max = value
        for value in children.keys():
            if max != value:
                for child in children[value]:
                    self.others += child.others
                    child.others = []
                    self.others.append(child)
            elif len(children[value]) == 1 and len(children) > 1:
                for child in children[value]:
                    self.others += child.others
                    child.others = []
                    self.others.append(child)
            else:
                self.value = max
                for child in children[max]:
                    self.count += child.count
                    self.others += child.others
        self.children = [None] * 10

    def print(self):
        for node in self.others:
            node.print()
        for child in self.children:
            if child is not None:
                child.print()
        if self.value is not None:
            print("%s\t%s\t%d" % (self.key, self.value, self.count))

    def sum(self):
        count = self.count
        for node in self.others:
            count += node.sum()
        for child in self.children:
            if child is not None:
                count += child.sum()
        return count

def main(utf_ken_all):
    root = Node('')
    with open(utf_ken_all, "r") as f:
        for row in csv.reader(f):
            root.append(row[2], row[6])
    root.shrink()
    root.print()
    print("SUM: %d" % (root.sum()))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python %s <utf_ken_all.csv>" % (sys.argv[0]))
    else:
        main(sys.argv[1])
