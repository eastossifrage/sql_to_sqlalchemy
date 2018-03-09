# -*- coding:utf-8 -*-
__author__ = '东方鹗'
__blog__ = 'http://www.os373.cn'

from models import session, Employee, Department, DeptEmp, DeptManager, Salary, Title
import operator
from sqlalchemy import func, and_, or_, text
from sqlalchemy.orm import aliased


'''===========================================联合查询实例==========================================='''

'''----------------------------------------------第一例-----------------------------------------------
    功能说明：
    查询部门及主管的信息，需 Department, DeptManager, Employees, Title 四个表联合查询。
    结果是： 返回字段为 	dp.dept_no（部门编号）, dept_name（部门名称）, title（头衔）, 
    t_from_date（头衔开始时间）, t_to_date（头衔结束时间）, birth_date（主管生日）, 
    first_name（主管第一名称）, last_name（主管姓氏）, gender（主管性别）, hire_date（聘任日期）, 
    from_date（开始时间）, to_date（结束时间）
'''

'''使用 sql 语句方式进行查询'''
sql = """
        SELECT
            dp.dept_no,
            dp.dept_name,
            t.title,
            t.from_date AS t_from_date,
            t.to_date AS t_to_date,
            e.birth_date,
            e.first_name,
            e.last_name,
            e.gender,
            e.hire_date,
            dm.from_date,
            dm.to_date
        FROM
            departments dp
        JOIN dept_manager dm ON dp.dept_no = dm.dept_no
        JOIN employees e ON e.emp_no = dm.emp_no
        JOIN titles t ON t.emp_no = e.emp_no
         AND t.from_date = dm.from_date
         AND t.to_date = dm.to_date
        GROUP BY
            dp.dept_no,
            dm.from_date,
            dm.to_date,
            dp.dept_name,
            t.title,
            t.from_date,
            t.to_date,
            e.birth_date,
            e.first_name,
            e.last_name,
            e.gender,
            e.hire_date
"""
sql_data = [(d.dept_no, d.dept_name, d.title, d.t_from_date, d.t_to_date, d.birth_date, d.first_name, d.last_name,
             d.gender, d.hire_date, d.from_date, d.to_date)
            for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
alchemy_data = session.query(Department.dept_no, Department.dept_name, Title.title,
                             Title.from_date.label("t_from_date"), Title.to_date.label("t_to_date"),
                             Employee.birth_date, Employee.first_name, Employee.last_name, Employee.gender,
                             Employee.hire_date, DeptManager.from_date, DeptManager.to_date).\
    join(DeptManager, Department.dept_no==DeptManager.dept_no).\
    join(Employee, Employee.emp_no==DeptManager.emp_no).\
    join(Title, and_(Title.emp_no==Employee.emp_no,
                     Title.from_date==DeptManager.from_date,
                     Title.to_date==DeptManager.to_date)).\
    group_by(Department.dept_no, DeptManager.from_date, DeptManager.to_date, Department.dept_name,
             Title.title, Title.from_date, Title.to_date, Employee.birth_date,
             Employee.first_name, Employee.last_name, Employee.gender, Employee.hire_date).all()

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第一例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

session.commit()
session.close()