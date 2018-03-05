# -*- coding:utf-8 -*-
__author__ = '东方鹗'
__blog__ = 'http://www.os373.cn'

from models import session, Employee, Department, DeptEmp, DeptManager, Salary, Title
import operator
from sqlalchemy import func, and_, or_

'''===========================================联合查询实例==========================================='''

'''----------------------------------------------第一例-----------------------------------------------
    功能说明：
    查询主键为 10004 的员工的所有年薪，需 Employees，Salaries 两个表联合查询。
    结果是： 返回字段为 emp_no, birth_date, first_name, last_name, gender, hire_date, times, salary
'''

'''使用 sql 语句方式进行查询'''
sql = "SELECT " + \
            "emp.*, " + \
            "CONCAT_WS('--', s.from_date, s.to_date) AS 'times', " + \
            "s.salary " + \
        "FROM " + \
            "employees emp " + \
        "JOIN salaries s ON emp.emp_no = s.emp_no " + \
        "WHERE " + \
            "emp.emp_no = 10004 "
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date, d.times, d.salary)
            for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
alchemy_data = session.query(Employee.emp_no, Employee.birth_date, Employee.first_name,
                  Employee.last_name, Employee.gender, Employee.hire_date,
                  func.concat_ws('--', Salary.from_date, Salary.to_date).label('times'), Salary.salary).\
    filter(Employee.emp_no==10004, Salary.emp_no==10004).all()

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第一例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''----------------------------------------------第二例-----------------------------------------------
    功能说明：
    查询主键为 10004 的员工的所有年薪，需 Employees，Salaries，Title 三个表联合查询。
    结果是： 返回字段为 emp_no, birth_date, first_name, last_name, gender, hire_date, 
    title(新增字段，需联表 Title), times， salary
'''

'''使用 sql 语句方式进行查询'''
sql = "SELECT " + \
            "emp.*, t.title, " + \
            "CONCAT_WS('--', s.from_date, s.to_date) AS 'times', " + \
            "s.salary " + \
        "FROM " + \
            "employees emp " + \
        "JOIN titles t ON emp.emp_no = t.emp_no " + \
        "JOIN salaries s ON emp.emp_no = s.emp_no " + \
        "WHERE " + \
            "emp.emp_no = 10004 " + \
        "AND (" + \
            "s.from_date BETWEEN t.from_date " + \
            "AND t.to_date" + \
        ")"
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date, d.title, d.times, d.salary)
            for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
alchemy_data = session.query(Employee.emp_no, Employee.birth_date, Employee.first_name,
                                 Employee.last_name, Employee.gender, Employee.hire_date, Title.title,
                                 func.concat_ws('--', Salary.from_date, Salary.to_date).label('times'),
                                 Salary.salary).\
    filter(Employee.emp_no == 10004, Salary.emp_no == 10004, Title.emp_no == 10004,
           Salary.from_date.between(Title.from_date, Title.to_date)).all()

print(alchemy_data)

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第二例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''
session.commit()
session.close()
