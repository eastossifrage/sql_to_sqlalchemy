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
    from_date（主管任期开始时间）, to_date（主管任期结束时间）
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

'''----------------------------------------------第二例-----------------------------------------------
    功能说明：
    查询 1999 年时期，部门、主管及部门员工的详细信息，需 Department, DeptManager, Employees, Title, DeptEmp 
    五个表联合查询，其中对 Employees, Title 两个表进行了两次查询，多次查询的时候注意设置别名。
    结果是： 返回字段为 	dp.dept_no（部门编号）， dept_name（部门名称）， dm_emp_no（主管编号），
    dm_title（主管头衔）， dm_birth_date（主管生日），dm_first_name（主管第一名称），
    dm_last_name（主管姓氏）， dm_gender（主管性别）， dm_hire_date（主管聘任日期）， 
    dm_from_date（主管任期开始时间）， dm_to_date（主管任期结束时间），emp_no（员工编号），title（员工头衔），
    t_from_date（头衔授予时间）， t_to_date（头衔结束时间），birth_date（员工生日）, 
    first_name（员工第一名称）， last_name（员工姓氏）， gender（员工性别）， hire_date（员工聘任日期）, 
    from_date（员工在本部门任期开始时间）， to_date（员工在本部门任期结束时间）
'''

'''使用 sql 语句方式进行查询'''
sql = """
        SELECT
            e.emp_no,
            d.dept_no,
            d.dept_name,
            em.emp_no AS dm_emp_no,
            t1.title AS dm_title,
            em.birth_date AS dm_birth_date,
            em.first_name AS dm_first_name,
            em.last_name AS dm_last_name,
            em.gender AS dm_gender,
            em.hire_date AS dm_hire_date,
            dm.from_date AS dm_from_date,
            dm.to_date AS dm_to_date,            
            t2.title,
            t2.from_date AS t_from_date,
            t2.to_date AS t_to_date,
            e.birth_date,
            e.first_name,
            e.last_name,
            e.gender,
            e.hire_date,
            de.from_date,
            de.to_date
        FROM
            employees e
        JOIN dept_emp de ON de.emp_no = e.emp_no
        JOIN departments d ON d.dept_no = de.dept_no
        JOIN dept_manager dm ON dm.dept_no = d.dept_no
        JOIN employees em ON dm.emp_no = em.emp_no
        JOIN titles t1 ON t1.emp_no = em.emp_no
        AND t1.from_date = dm.from_date 
        AND t1.to_date = dm.to_date
        JOIN titles t2 ON t2.emp_no = e.emp_no
        WHERE
            (
                '1999' BETWEEN YEAR (de.from_date)
                AND YEAR (de.to_date)
            )
        AND (
            '1999' BETWEEN YEAR (dm.from_date)
            AND YEAR (dm.to_date)
        )
        AND (
            '1999' BETWEEN YEAR (t2.from_date)
            AND YEAR (t2.to_date)
        )
        GROUP BY
            e.emp_no,
            d.dept_no,
            d.dept_name,
            em.emp_no,
            t1.title,
            em.birth_date,
            em.first_name,
            em.last_name,
            em.gender,
            em.hire_date,
            dm.from_date,
            dm.to_date,
            t2.title,
            t2.from_date,
            t2.to_date,
            e.birth_date,
            e.first_name,
            e.last_name,
            e.gender,
            e.hire_date,
            de.from_date,
            de.to_date
         LIMIT 10
"""
sql_data = [(d.emp_no, d.dept_no, d.dept_name, d.dm_emp_no, d.dm_title, d.dm_birth_date, d.dm_first_name, d.dm_last_name,
             d.dm_gender, d.dm_hire_date, d.dm_from_date, d.dm_to_date, d.title, d.t_from_date, d.t_to_date,
             d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date, d.from_date, d.to_date)
            for d in session.execute(sql)]


'''使用 sqlalchemy 方式进行查询'''
e1 = aliased(Employee)
e2 = aliased(Employee)
t1 = aliased(Title)
t2 = aliased(Title)
alchemy_data = session.query(e2.emp_no, Department.dept_no, Department.dept_name, e1.emp_no.label("dm_emp_no"),
                             t1.title.label("dm_title"), e1.birth_date.label("dm_birth_date"),
                             e1.first_name.label("dm_first_name"), e1.last_name.label("dm_last_Name"),
                             e1.gender.label("dm_gender"), e1.hire_date.label("dm_hire_date"),
                             DeptManager.from_date.label("dm_from_date"), DeptManager.to_date.label("dm_to_date"),
                             t2.title, t2.from_date.label("t_from_date"), t2.to_date.label("t_to_date"),
                             e2.birth_date, e2.first_name, e2.last_name, e2.gender, e2.hire_date, DeptEmp.from_date,
                             DeptEmp.to_date).\
    join(DeptEmp, DeptEmp.emp_no==e2.emp_no).\
    join(Department, Department.dept_no==DeptEmp.dept_no).\
    join(DeptManager, DeptManager.dept_no==Department.dept_no).\
    join(e1, e1.emp_no==DeptManager.emp_no).\
    join(t1, and_(t1.emp_no==e1.emp_no,
                     t1.from_date==DeptManager.from_date,
                     t1.to_date==DeptManager.to_date)).\
    join(t2, t2.emp_no==e2.emp_no).\
    filter(func.year('1999-01-01').between(func.year(DeptEmp.from_date), func.year(DeptEmp.to_date)),
           func.year('1999-01-01').between(func.year(DeptManager.from_date), func.year(DeptManager.to_date)),
           func.year('1999-01-01').between(func.year(t2.from_date), func.year(t2.to_date)),).\
    group_by(e2.emp_no, Department.dept_no, Department.dept_name, e1.emp_no, t1.title, e1.birth_date, e1.first_name,
             e1.last_name, e1.gender, e1.hire_date, DeptManager.from_date, DeptManager.to_date, t2.title, t2.from_date,
             t2.to_date, e2.birth_date, e2.first_name, e2.last_name, e2.gender, e2.hire_date, DeptEmp.from_date,
             DeptEmp.to_date).limit(10).all()

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第二例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''第二例内容总结：使用 sqlalchemy 的时候，要注意 query 的字段顺序，该字段所在的表的顺序与要转换为 SQL 语句中的
 FROM 后面的表的顺序是一致的'''
'''-------------------------------------------------------------------------------------------------'''

session.commit()
session.close()