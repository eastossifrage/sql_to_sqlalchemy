# sql to sqlalchemy 实例教程——使用 MySQL 示例 employees 数据库

---

> 在Python项目中，经常需要操作数据库，而 sqlalchemy 提供了 SQL 工具包及对象关系映射(ORM)工具，大大提高了编程开发的效率。为了更好的提升自己的 sql 以及使用 sqlachemy 水平，可以使用 MySQL 自带的示范数据库 employees 进行练习。

## 安装 MySQL 示例 employees 数据库

### 1 下载地址

MySQL 提供了一个联系用的示范数据库 employees。可以从 Employees DB on Lanunchpad（https://launchpad.net/test-db）中下载，建议下载 “**employees\_db\_full\_1.0.6**”。
empployees 示例数据库一共有 6 张表，约 400 万条记录，包含 160M 数据。

### 2 选择默认引擎

默认导入数据是 InnoDB 引擎，如果需要指定其它引擎，可以修改 employees.sql 文件，取消注释响应的引擎，命令如下：

```
set storage_engine = InnoDB;
-- set storage_engine = MyISAM;
-- set storage_engine = FaIcon;
-- set storage_engine = PBXT;
-- set storage_engine = Maria;
```
### 3 导入数据

使用 MySQL 命令将数据导入到实例中。

```
mysql -t < employees.sql
```

通过以下命令验证范例数据导入是否正确。

```
time mysql -t < test_employees_sha.sql
```

![](http://www.os373.cn/admin/pictures/dijkstra/employees.png)

### 4 修正错误 1

安装时报错：

```
ERROR 1193 (HY000) at line 38: Unknown system variable 'storage_engine'
```

这是因为下载的数据没有跟着mysql版本升级改变，mysql5.7.5以后，这个变量被移除了，改用default\_storage\_engine就可以了

```
set default_storage_engine = InnoDB;
-- set default_storage_engine = MyISAM;
-- set default_storage_engine = Falcon;
-- set default_storage_engine = PBXT;
-- set default_storage_engine = Maria;

select CONCAT('storage engine: ', @@default_storage_engine) as INFO;
```

### 5 修正错误 2

The source command is not a MySQL statement, but something only handled by the MySQL client. MySQL Workbench does not handle this (as it is focused on pure MySQL code).

To import the entire set remove the source commands from the main file and then manually import these files like you did with the main dump. A bit tedious, but at least a way to load all files.

[https://stackoverflow.com/questions/45227599/mysql-syntax-error-source-source-is-not-valid-input-at-this-position](https://stackoverflow.com/questions/45227599/mysql-syntax-error-source-source-is-not-valid-input-at-this-position)

## 建立 sqlalchemy 开发环境

### 安装 pymysql

python3 连接 MySQL 数据库需要使用 pymysql

```
(env)$ pip install pymysql
```

### 安装 sqlacodegen

安装该包是为了自动生成 models.py

```
(env)$ pip install sqlacodegen
```

无需再安装 sqlalchemy， 已经进行了依赖安装。
由于使用了 python3 ，需要在 sqlacodegen 的 \_\_init\_\_.py 文件里加上如下内容：

```
import pymysql

pymysql.install_as_MySQLdb()
```

### 生成 models.py

```
sqlacodegen mysql://username:password@127.0.0.1:3306/employees > models.py
```

### 初始化数据库连接

在生成的 models.py 文件下面添加如下内容：

```
# 初始化数据库连接:
engine = create_engine('mysql+pymysql://root:password@127.0.0.1:3306/employees', echo=True)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()
```

## 课程目录

- [利用 sqlacodegen 生成的 models.py ](https://github.com/eastossifrage/sql_to_sqlalchemy/blob/master/models.py)
- [基础查询功能](https://github.com/eastossifrage/sql_to_sqlalchemy/blob/master/chapter001/employees.py)


-----
## 欢迎大家提供需要转变为 sqlalchemy 语法的 sql 语句。

如有需求，请加入 QQ群：291521082

<a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=d8c6eea26733f58dc2874a05a1c42dcfc8204fa71597077ce90348c6ca011f66">
<img border="0" src="//pub.idqqimg.com/wpa/images/group.png" alt="藕丝空间--认真的编程" title="藕丝空间--认真的编程"></a>
