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

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第二例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''----------------------------------------------第三例-----------------------------------------------
    功能说明：
    查询主键为 10004, 10001, 10006, 10003 的四位员工在 1997-12-01 时期的年薪及上年年薪，
    需 Employees，Salaries，Title 三个表联合查询。
    结果是： 返回字段为 emp_no, birth_date, first_name, last_name, gender, hire_date, 
    title(新增字段，需联表 Title), from_date, to_date, salary, last_salary
    提示：该实例很复杂，重点如下：
        1、if else 三目运算符的使用。
        2、func.date_sub 的使用。
        3、text 可以使用原始的 sql 语句。
        4、对 salaries 表同时进行两次及以上查询，用到了 aliased
'''

'''使用 sql 语句方式进行查询'''
sql = "SELECT " + \
        "emp.*, t.title, " + \
        "s.from_date, " + \
        "s.to_date, " + \
        "s.salary, " + \
        "IF ( " + \
            "ISNULL( " + \
                "( " + \
                    "SELECT " + \
                        "s.salary " + \
                    "FROM " + \
                        "salaries s " + \
                    "WHERE " + \
                        "s.emp_no = emp.emp_no " + \
                    "AND ( " + \
                        "DATE_SUB( " + \
                            "DATE('1997-12-01'), " + \
                            "INTERVAL 1 YEAR " + \
                        ") BETWEEN s.from_date " + \
                        "AND s.to_date " + \
                    ") " + \
                ") " + \
            "), " + \
            "0, " + \
            "s.salary - ( " + \
                "SELECT " + \
                    "s.salary " + \
                "FROM " + \
                    "salaries s " + \
                "WHERE " + \
                    "s.emp_no = emp.emp_no " + \
                "AND ( " + \
                    "DATE_SUB( " + \
                        "DATE('1997-12-01'), " + \
                        "INTERVAL 1 YEAR " + \
                    ") BETWEEN s.from_date " + \
                    "AND s.to_date " + \
                ") " + \
            ") " + \
        ") AS last_salary " + \
        "FROM " + \
            "employees emp " + \
        "JOIN titles t ON emp.emp_no = t.emp_no " + \
        "JOIN salaries s ON emp.emp_no = s.emp_no " + \
        "WHERE " + \
            "( " + \
                "emp.emp_no = 10004 " + \
                "OR emp.emp_no = 10001 " + \
                "OR emp.emp_no = 10006 " + \
                "OR emp.emp_no = 10003 " + \
            ") " + \
        "AND ( " + \
            "DATE('1997-12-01') BETWEEN s.from_date " + \
            "AND s.to_date " + \
        ") " + \
        "AND ( " + \
            "DATE('1997-12-01') BETWEEN t.from_date " + \
            "AND t.to_date " + \
        ")"
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date, d.title, d.from_date, d.to_date,
             d.salary, d.last_salary)
            for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
s1 = aliased(Salary)
s2 = aliased(Salary)
alchemy_data = session.query(Employee.emp_no, Employee.birth_date, Employee.first_name,
                                 Employee.last_name, Employee.gender, Employee.hire_date, Title.title,
                                 s1.from_date, s1.to_date, s1.salary, (0 if not
                                        session.query(s2.salary).filter(s2.emp_no==Employee.emp_no,
                                        func.date_sub(text("date('1997-12-01'), interval 1 year")).
                                        between(s2.from_date, s2.to_date))
                             else (s1.salary - (session.query(s2.salary).
        filter(s2.emp_no==Employee.emp_no, func.date_sub(text("date('1997-12-01'), interval 1 year")).
               between(s2.from_date, s2.to_date))))).label("last_salary")).\
    filter(Employee.emp_no==s1.emp_no , Title.emp_no==s1.emp_no,
           or_(Employee.emp_no==10004,
               Employee.emp_no==10001,
               Employee.emp_no==10006,
               Employee.emp_no==10003),
           func.date('1997-12-01').between(s1.from_date, s1.to_date),
           func.date('1997-12-01').between(Title.from_date, Title.to_date)).all()

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第三例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''
session.commit()
session.close()
