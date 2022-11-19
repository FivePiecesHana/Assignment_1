import pandas as pd
import csv


class Geometry:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class Point(Geometry):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


class Line(Geometry):
    def __init__(self, name, Point_1, Point_2):
        super().__init__(name)
        self.__Point_1 = Point_1
        self.__Point_2 = Point_2

    def get_point(self):
        line_point = [self.__Point_1, self.__Point_2]
        return line_point


class Polygon(Geometry):
    def __init__(self, name, Points):
        super().__init__(name)
        self.__Points = Points

    def get_points(self):
        return self.__Points

    def get_lines(self):
        res = []
        ps = self.get_points()
        Point_A = ps[0]
        for Point_B in ps[1:]:
            res.append(Line(Point_A.get_name()+'-'+Point_B.get_name(), Point_A, Point_B))
            Point_A = Point_B
        res.append(Line(Point_A.get_name()+'-'+ps[0].get_name(), Point_A, ps[0]))
        return res

    def get_rec_boundary(self):
        # boundary = [min_x(left), max_x(right), min_y(bottom), max_y(top)]
        left = self.__Points[0].get_x()
        right = left
        bottom = self.__Points[0].get_y()
        top = bottom
        for point_iter in self.__Points[1:]:
            if point_iter.get_x() < left:
                left = point_iter.get_x()
            if point_iter.get_x() > right:
                right = point_iter.get_x()
            if point_iter.get_y() < bottom:
                bottom = point_iter.get_y()
            if point_iter.get_y() > top:
                top = point_iter.get_y()
        boundary = [left, right, bottom, top]
        return boundary

    def mbr_algo(self, pnt):
        boundary = self.get_rec_boundary()
        if boundary[0] <= pnt.get_x() <= boundary[1] and boundary[2] <= pnt.get_y() <= boundary[3]:
            print('It is in the MBL.')
            return True
        else:
            print('It is not in the MBL.')
            return False

    def near_line(self, pnt):
        nr_line = []
        poly_line = self.get_lines()
        for line_iter in poly_line[0:]:
            line_x_list = [line_iter.get_point()[0].get_x(), line_iter.get_point()[1].get_x()]
            line_y_list = [line_iter.get_point()[0].get_y(), line_iter.get_point()[1].get_y()]
            if min(line_y_list) <= pnt.get_y() <= max(line_y_list):
                if max(line_x_list) >= pnt.get_x():
                    nr_line.append(line_iter)
        return nr_line

    def is_boundary(self, pnt):
        nr_line = self.near_line(pnt)
        for line_iter in nr_line[0:]:
            # 判断是否是端点1
            if pnt.get_x() == line_iter.get_point()[0].get_x() and pnt.get_y() == line_iter.get_point()[0].get_y():
                print('Boundary:point')
                return True
            # 判断是否是端点2
            elif pnt.get_x() == line_iter.get_point()[1].get_x() and pnt.get_y() == line_iter.get_point()[1].get_y():
                print('Boundary: point')
                return True
            # 判断是否是竖线
            elif line_iter.get_point()[0].get_x() == line_iter.get_point()[1].get_x() == pnt.get_x():
                print('Boundary: 1')
                return True
            # 判断是否在线上
            else:
                k_1 = (pnt.get_y()-line_iter.get_point()[0].get_y())/(pnt.get_x()-line_iter.get_point()[0].get_x())
                k_2 = (pnt.get_y()-line_iter.get_point()[1].get_y())/(pnt.get_x()-line_iter.get_point()[1].get_x())
                if k_1 == k_2:
                    print('Boundary:lines')
                    return True
        print('not boundary')
        return False

    def rca_algo(self, pnt):
        nr_line = self.near_line(pnt)
        count = 0
        for line_iter in nr_line[0:]:
            line_y_list = [line_iter.get_point()[0].get_y(), line_iter.get_point()[1].get_y()]
            if pnt.get_y() != max(line_y_list):
                count += 1
        print(count)
        if count % 2 == 0:
            res = 'outside'
            print('outside')
            return res
        else:
            res = 'inside'
            print('inside')
            return res

    def judge_position(self, pnt):
        if self.mbr_algo(pnt):
            print('it is in mbr')
            if self.is_boundary(pnt):
                print('it is boundary')
                res = 'boundary'
                return res
            else:
                return self.rca_algo(pnt)
        else:
            res = 'outside'
            print('outsides')
            return res


def load_points(roots):
    points_list = []
    data = pd.read_csv(roots)
    for index, row in data.iterrows():
        id, x, y = row['id'], row['x'], row['y']
        pt = Point(str(id), x, y)
        points_list.append(pt)
    return points_list


Input_Points = load_points('input.csv')
Polygon_A = Polygon('polygon', load_points('polygon.csv'))

result = []
for point_iter in Input_Points[0:]:
    print('Now is the '+point_iter.get_name()+'point')
    row = (point_iter.get_name(), Polygon_A.judge_position(point_iter))
    result.append(row)

header = ['id', 'category']
with open('output_1.csv', 'w', encoding='utf-8', newline='') as file_obj:
    # 创建对象
    writer = csv.writer(file_obj)
    # 写表头
    writer.writerow(header)
    # 遍历，将每一行的数据写入csv
    for point in result:
        writer.writerow(point)

'''
1. Test how Point, Line, Polygon class work 
point_A = Point('A', 0, 0)
point_B = Point('B', 0, 1)
point_C = Point('C', 1, 1)
point_D = Point('D', 1, 0)
points = [point_A, point_B, point_C, point_D, point_A]

Line_AB = Line('A-B', point_A, point_B)
polygon_ABCD = Polygon('ABCD', points)
print(polygon_ABCD.get_lines()[0].get_name())
'''

'''
2. Test CSV files import
data = pd.read_csv("polygon.csv")
print(data.iloc[1][0])
'''

'''
3. test the csv iterrows
Point_List = []
data = pd.read_csv("polygon.csv")
for index, row in data.iterrows():
    id, x, y = row['id'], row['x'], row['y']
    pt = Point(id, x, y)
    Point_List.append(pt)
# get the length of csv file
print(len(data))  
Input_point_List = Load_Points("polygon.csv")
print(Input_point_List[6].get_x())
'''

'''
4. test the MBR algo
Polygon_A = Polygon('polygon', load_points('polygon.csv'))
# print(Polygon_A.get_rec_boundary())
Polygon_A.mbr_algo()
'''

'''
5. test the boundary algo
point_A = Point('A', 2.5, 0)
Polygon_A = Polygon('polygon', load_points('polygon.csv'))
Polygon_A.is_boundary(point_A)
'''

'''
6. test the rca algo
point_A = Point('A', 0.5, 1)
Polygon_A = Polygon('polygon', load_points('polygon.csv'))
Polygon_A.judge_position(point_A)
'''