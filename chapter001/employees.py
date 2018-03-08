# -*- coding:utf-8 -*-
__author__ = '东方鹗'
__blog__ = 'http://www.os373.cn'

from models import session, Employee, Department, DeptEmp, DeptManager, Salary, Title
import operator


'''----------------------------------------------第一例-----------------------------------------------
    功能说明：
    使用主键对 employees 表进行查询，结果是： 返回该主键对应的单条数据！
'''

'''使用 sql 语句方式进行查询'''
sql = "select * from employees where emp_no = 10006"
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
d = session.query(Employee).get(10006)
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)]

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第一例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第二例--------------------------------------------------
    功能说明：
    对 employees 表进行查询，结果是：从第 4 行开始查询，返回之后的 10 行数据！值为一个列表。
'''

'''使用 sql 语句方式进行查询'''
sql = "select * from employees limit 10 offset 4"
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)
                for d in session.query(Employee).limit(10).offset(4).all()]

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第二例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第三例--------------------------------------------------
    功能说明：
    使用一个精确参数对 employees 表进行查询(搜索字段 last_name 为 'Nooteboom' 的内容)，
    结果是： 返回该参数对应的第一条数据！仅仅是第一条数据！
'''

'''使用 sql 语句方式进行查询'''
sql = "select * from employees where last_name = 'Nooteboom' limit 1"
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
d = session.query(Employee).filter_by(last_name='Nooteboom').first()
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)]

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第三例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第四例--------------------------------------------------
    功能说明：
    使用一个精确参数对 employees 表进行查询(搜索字段 last_name 为 'Nooteboom' 的内容)，
    结果是： 返回该参数对应的所有数据！所有数据！值为一个列表。
'''

'''使用 sql 语句方式进行查询'''
sql = "select * from employees where last_name = 'Nooteboom'"
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''

'''方法一
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)
                for d in session.query(Employee).filter_by(last_name='Nooteboom').all()]
'''

'''方法二如下'''
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)
                for d in session.query(Employee.emp_no, Employee.birth_date, Employee.first_name,
                Employee.last_name, Employee.gender, Employee.hire_date
                ).filter_by(last_name='Nooteboom').all()]


'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第四例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第五例--------------------------------------------------
    功能说明：
    使用两个及以上的精确参数对 employees 表进行查询(搜索字段 last_name 为 'Nooteboom' 
    并且字段 first_name 为 'Pohua' 的内容)，
    结果是： 返回参数对应的所有数据！所有数据！值为一个列表。
'''

'''使用 sql 语句方式进行查询'''
sql = "select * from employees where last_name = 'Nooteboom' and first_name = 'Pohua'"
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''

'''方法一
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)
                for d in session.query(Employee).
                    filter_by(last_name='Nooteboom', first_name='Pohua').all()]
'''
'''方法二如下'''
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)
                for d in session.query(Employee).filter(Employee.last_name=='Nooteboom').
                    filter(Employee.first_name=='Pohua').all()]

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第五例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第六例--------------------------------------------------
    功能说明：
    使用一个模糊参数对 employees 表进行查询，结果是： 返回该参数对应的所有数据！所有数据！值为一个列表。
    提示：
        1、sqlalchemy 提供了 like, endswith, startswith 函数结合通配符来进行模糊查询。
           对于 like, endswith, startswith ，见字如面，请按照英文字面意思理解。
        2、本例的重点是使用且仅一个模糊参数, 主要是为了展示 like 函数。
'''

'''使用 sql 语句方式进行查询'''
sql = "select * from employees where last_name like 'N%te_%'"
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''

alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)
                for d in session.query(Employee).filter(Employee.last_name.like('N%te_%')).all()]

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第六例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第七例--------------------------------------------------
    功能说明：
    使用两个及以上模糊参数对 employees 表进行查询，查询字段 last_name 近似于 'N%te_%'，
    并且字段 first_name 在 ('Jaewon', 'os373.cn') 里，同时，
    字段 birth_date 是以 1955 开头，且字段 hire_date 是以 05-30 结束的员工信息。
    结果是： 返回参数对应的所有数据！所有数据！值为一个列表。
    提示：
        1、sqlalchemy 提供了 like, endswith, startswith 函数结合通配符来进行模糊查询。
           对于 like, endswith, startswith ，见字如面，请按照英文字面意思理解。
        2、本例的重点是展示 like, endswith, startswith 函数以及 and_, or_, in_ 逻辑运算符函数的用法。
    彩蛋：思考一下 not in， not equal，is NULL，is not NULL 的用法。
'''

'''使用 sql 语句方式进行查询'''
sql = """
        SELECT
            *
        FROM
            employees
        WHERE
            last_name LIKE 'N%te_%'
        AND first_name IN ('Jaewon', 'os373.cn')
        AND birth_date LIKE '1955%'
        AND hire_date LIKE '%05-30'
"""
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
from sqlalchemy import and_, or_
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)
                for d in session.query(Employee).filter(and_(Employee.last_name.like('N%te_%'),
                                                             Employee.first_name.in_(['Jaewon','os373.cn']),
                                                             Employee.birth_date.startswith('1955'),
                                                             Employee.hire_date.endswith('05-30'))).all()]

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第七例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第八例--------------------------------------------------
    功能说明：
    使用两个及以上模糊参数对 employees 表进行查询，查询字段 last_name 近似于 'N%te_%'，
    并且字段 first_name 在 ('Jaewon', 'os373.cn') 里的员工信息，或者是，
    字段 birth_date 是以 1955 开头，且字段 hire_date 是以 05-30 结束的员工信息的个数。
    结果是： 返回一个数字。
    提示：
        1、sqlalchemy 提供了 like, endswith, startswith 函数结合通配符来进行模糊查询。
           对于 like, endswith, startswith ，见字如面，请按照英文字面意思理解。
        2、本例的重点是展示 like, endswith, startswith 函数以及 and_, or_, in_ 逻辑运算符函数的用法。
        3、func 函数可以执行数据库所支持的函数，本例中是为了执行 MySQL 的 count 函数。
        4、scalar() 函数是为了返回单项数据，与 first(), one() 函数类似，
           但是前者返回的是单项数据，后两者返回的是 tuple。
'''

'''使用 sql 语句方式进行查询'''
sql = """
        SELECT
            count(*)
        FROM
            employees
        WHERE
            (
                last_name LIKE 'N%te_%'
                AND first_name IN ('Jaewon', 'os373.cn')
            )
        OR (
            birth_date LIKE '1955%'
            AND hire_date LIKE '%05-30'
        )
"""
sql_data = [d for d in session.execute(sql)][0][0]

'''使用 sqlalchemy 方式进行查询'''
from sqlalchemy import and_, or_

'''方法一
alchemy_data = session.query(Employee).filter(or_(and_(Employee.last_name.like('N%te_%'),
                                                       Employee.first_name.in_(['Jaewon','os373.cn'])),
                                                  and_(Employee.birth_date.startswith('1955'),
                                                       Employee.hire_date.endswith('05-30')))).count()
                                                       '''

'''方法二'''
from sqlalchemy import func
alchemy_data = session.query(func.count("*")).filter(or_(and_(Employee.last_name.like('N%te_%'),
                                                       Employee.first_name.in_(['Jaewon','os373.cn'])),
                                                  and_(Employee.birth_date.startswith('1955'),
                                                       Employee.hire_date.endswith('05-30')))).scalar()

'''比较两个结果，应该是True'''
print(sql_data, alchemy_data)
print('第八例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第九例--------------------------------------------------
    功能说明：
    使用两个及以上模糊参数对 employees 表进行查询，查询字段 last_name 近似于 'N%te_%'，
    并且字段 first_name 在 ('Jaewon', 'os373.cn') 里的员工信息，或者是，
    字段 birth_date 是以 1955 开头，且字段 hire_date 是以 05-30 结束的员工信息，
    并按照字段 last_name 进行排序。
    结果是： 返回参数对应的所有数据！所有数据！值为一个列表。
    提示：
        1、由于 MySQL 5.7 中的 sql_mode 设置有 only_full_group_by，因此要求 group by 的使用方法像 oracle 
        一样，必须得把要查询出的字段都罗列在 group by 语句之后，聚合函数除外。按照最靠前的字段来进行排序。
'''

'''使用 sql 语句方式进行查询'''
sql = """
        SELECT
            *
        FROM
            employees
        WHERE
            (
                last_name LIKE 'N%te_%'
                AND first_name IN ('Jaewon', 'os373.cn')
            )
        OR (
            birth_date LIKE '1955%'
            AND hire_date LIKE '%05-30'
        )
        GROUP BY
            last_name,
            gender,
            hire_date,
            emp_no,
            birth_date,
            first_name 
"""
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
from sqlalchemy import and_, or_
alchemy_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date)
                for d in session.query(Employee).filter(or_(and_(Employee.last_name.like('N%te_%'),
                                                             Employee.first_name.in_(['Jaewon','os373.cn'])),
                                                            and_(Employee.birth_date.startswith('1955'),
                                                                 Employee.hire_date.endswith('05-30')))).\
    group_by(Employee.last_name, Employee.gender, Employee.hire_date, Employee.emp_no,
             Employee.birth_date, Employee.first_name).all()]

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第九例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''

'''-------------------------------------------第十例--------------------------------------------------
    功能说明：
    查询当前还在职的员工的信息，在职的一个条件是 titles 表中的 to_date 字段为 '9999-01-01'。
    结果是： 返回字段为 emp_no, birth_date, first_name, last_name, gender, 
    hire_date, title, from_date, to_date值为一个列表。
    提示：
        需要用到 employees, titles 两个表联合查询
'''

'''使用 sql 语句方式进行查询'''
sql = """
        SELECT
            e.*, t.title,
            t.from_date,
            t.to_date
        FROM
            employees e
        JOIN titles t ON e.emp_no = t.emp_no
        WHERE
            t.to_date = '9999-01-01'
        LIMIT 10
"""
sql_data = [(d.emp_no, d.birth_date, d.first_name, d.last_name, d.gender, d.hire_date,
             d.title, d.from_date, d.to_date) for d in session.execute(sql)]

'''使用 sqlalchemy 方式进行查询'''
alchemy_data = session.query(Employee.emp_no, Employee.birth_date, Employee.first_name, Employee.last_name,
                             Employee.gender, Employee.hire_date, Title.title, Title.from_date, Title.to_date).\
    join(Title, Employee.emp_no==Title.emp_no).filter(Title.to_date=='9999-01-01').limit(10).all()

'''比较两个结果，应该是True'''
for d in zip(sql_data, alchemy_data):
    print(d)
print('第十例结果是：{}'.format(operator.eq(sql_data, alchemy_data)))

'''-------------------------------------------------------------------------------------------------'''
session.commit()
session.close()
