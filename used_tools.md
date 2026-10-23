## fastapi
### Response
是底层响应对象 用来
### query
用 Query() 是为了加校验和元数据，比如 ge、le、min_length、max_length、pattern、alias、description。没给默认值就是必填，给了默认值就是可选
## pydantic

## postgresql
是一个功能很强大的关系型数据库。
可以使用pgadmin或者shell作为客户端与后端进行交互。
“连接”表示 pgAdmin 与正在运行的 PostgreSQL 服务建立通信，并通过数据库账号认证。保存连接配置只是记录地址、端口等信息；建立连接后，才能发送查询、创建数据库等命令。这里连接的是 PostgreSQL，不是你写的 FastAPI。
数据库实例和数据库不是一回事。实例指运行中的 PostgreSQL 服务及其管理的数据；一个实例可以包含多个数据库，每个数据库里面又可以包含多张表。创建数据库不会因此新建一个运行中的服务实例。
## uvicorn
是一个ASGI服务器。它实现了一套标准接口规范（ASGI），用于连接web服务器和应用框架程序，实现异步请求处理和相应。
是一个Asynchronous Server Gateway Interface，异步服务器网关接口。
做的事情：网络请求不断到达，他拿到这个请求，将他按照http协议进行解析。解析完了之后交给fastapi进行处理 但是怎么交给fastapi 按照什么格式，fastapi完成之后怎么通知·uvincorn ，这个需要一个协议 也就是使用的ASGI。
同时将任务交给fastapi之后 uvicorn不能在这里干等，因为还有各种任务到来。那么实际就会将这个请求注册成任务，交给调度器，然后立刻接受新请求。这个调度器是事件循环，维护多个任务的多部执行。
一个任务处理完了之后，再交给uvicorn，他再写回网络。
（FastAPI 处理完之后，不是“通知”Uvicorn，而是 FastAPI 主动调用 Uvicorn 传给它的 send 函数，把响应事件发回去。ASGI 给应用两个函数：receive 用来收请求体等事件，send 用来发响应事件。FastAPI 内部调用 send({"type": "http.response.start", ...}) 发状态码和头，再调用 send({"type": "http.response.body", ...}) 发响应体。Uvicorn 收到这些事件，再按 HTTP 协议写回网络）
### 什么是事件循环
注意这里 ASGI服务器不是给每个任务开一个线程 而是使用事件循环，只有当同步任务占住了调度器才会将他作为一个单独的线程。
## http
实际http是应用层协议 应用层协议 规定 什么是信息边界 什么编码解码 怎么进行交互 发来信息之后我应该怎么处理 他告诉我做什么事情 我能够理解 并按照他想要的操作去做（这是不是对应上：get put delete等） 怎么建立连接 怎么算信息传递结束 怎么返回处理的信息的结果 这是应用层要考虑的事情。但是hTTP 帮助双方理解请求的通用意图；具体操作仍由你的应用定义、实现。
而下面几层 比如传输层 考虑的是 怎么把包进行端到端传输 怎么找到相应的端口 怎么用唯一标识找到源主机 目标主机 并把包发给相应的端口？ 可能还要考虑可靠性 重传等
ip层 主要考虑怎么一跳一跳进行点到点传输 怎么经过路由器将包送到目标主机
链路层 主要考虑怎么在这个链路上 怎样完成当前这一跳的传递？

注意：http只是应用层协议的一种 实际任何应用都能设计他自己的应用层协议 。例如游戏可以采用：自定义游戏协议 → UDP → IP。
HTTP 可以获取静态资源，也可以调用动态业务接口。静态资源获取例如GET取文件 但也可能调用动态接口：先处理请求 再生成结果。

为什么应用层协议http 规定了大类例如get put 为什么在这些后面 还能定位以及找到程序的接口呢 GET /tasks/42 这具体是怎么实现的？
实际是使用fastapi 这个框架 使用它提前在程序里登记了路径与函数的对应关系。fastapi将这个函数与路径的对应关系登记到fastapi的路由表中。
请求方法：GET
请求路径：/tasks/42

如果自己实现 那么首先就是解析请求（按照http规则）。之后得到method=GET path=/task 之后就是条件判断 解析出来方法和路径之后 做判断 如果符合条件语句就调用这个函数等这样。如果接口越来越多，那么条件判断就很臃肿 可以将条件判断变成一个列表或者字典之类的，（叫做路由表），请求来了之后，解析，然后遍历路由表。
之后还可以再提供一个用于登记路由的函数：接收路径以及函数，保存到路由表，或者直接将这个登记过程包装成装饰器。大概就是这样。

http有哪些方法：
GET：获取资源，参数一般在 URL 查询串，安全且幂等，不改变服务器状态。
POST：提交数据、创建资源、触发处理，参数在请求体，不幂等。
PUT：整体替换资源，客户端提供完整新表示，幂等。
PATCH：部分更新资源，只传要改的字段，通常不幂等。
DELETE：删除资源，幂等，删多次最终状态一样。
HEAD：和 GET 一样，但只返回响应头，不返回响应体，用来检查资源是否存在、拿 Content-Length 等。
OPTIONS：询问服务器支持哪些方法，也用于 CORS 预检。
TRACE：回显请求，调试用，很多服务器默认关闭。
CONNECT：建立隧道，HTTPS 代理常用，比如 CONNECT example.com:443。
## getpass
getpass是一个python的标准库 他的核心功能是再命令行程序中安全读取密码。主要实现了当你输入密码时 不回显到屏幕上。

## psycopg
这个包实现了Python 的 DB-API 2.0 规范  能够在python中直接写sql语句
cursor.execute() 里面写的字符串，就是直接发给 PostgreSQL 服务器执行的原生 SQL。
注意 ILIKE：不区分大小写 LIKE：区分大小写

## .env是什么文件
是一个用于存放项目环境变量的纯文本配置文件。#开头的这行是注释，每一行以键值对的形式出现。在 Python 生态中，通常借助 python-dotenv 这个库来读取 .env 文件，它会将文件里的键值对加载为系统的环境变量。
.env 不是 Python 专属，也不是 python-dotenv 发明的。它是一种跨语言、跨工具的事实约定格式，本质上就是“一堆 KEY=VALUE 的纯文本”，没有正式的 RFC 或标准委员会，但因为足够简单，被大量语言和工具各自实现了解析器。

## Literal typing
 是 typing 模块里的类型注解，用来限定一个变量只能取某几个字面量值。status: Literal["todo", "in_progress", "done"] 的意思是：status 这个字段只允许是这三个字符串之一，写别的值就是非法。注意 他严格区分大小写
typing是python的标准库，提供类型注解的语法和工具，pydantic 是第三方库，它读取这些类型注解，在运行时做校验和转换。

## @router.get("/{task_id}", response_model=TaskRead) 这是啥意思 为啥装饰器还能有参数
其实也就相当于：register_route = router.get(
    "/{task_id}",
    response_model=TaskRead,
)
def get_task(task_id: int):
在函数里再定义一个函数。python完全允许

## logging
logging 模块在 Python 启动时其实已经自带了一个叫 root logger 的单例对象，你不需要自己实例化它。logging.basicConfig() 是模块级函数，内部操作的就是这个 root logger，给它加 handler、设级别、设格式。logging.info()、logging.warning() 这些模块级快捷函数也是直接往 root logger 写日志。所以你看到“没实例化”，是因为实例化在模块内部早就完成了，你调用的函数只是配置和操作它。

## 什么是异常
异常对象是某个类的实例，括号里传的是错误信息 这个对象带着类型和信息，沿着调用栈向上传播。
raise做的事情：立即中断当前函数的执行 创建异常对象 把这个对象抛出去，如果这个层的try exept接住之后 就在这层调用解决了，如果没有 就沿着调用栈把异常抛给调用者， 直到有人except，或者到最顶层，程序打印traceback之后终止。

raise直接抛出一个异常对象，但是也有没有显示抛出的对象？可能是使用的库，在库的实现中已经抛出了这个相应的异常了。大量异常都不是你手写 raise 抛出来的，而是底层库、Python 解释器甚至操作系统帮你抛的。

注意 如果一个异常被raise了 只要在调用栈有一个except接住了这个异常 异常就被处理了 处理方法是except里的代码块，只要 except 块里没有新的 raise，这个异常就到此为止，不会再传播给上层调用者。
except 块执行完之后，程序会继续往下走，而不是回到 raise 那一行。

## logger.execption()
logging.exception() 会自动获取并记录 当前异常的完整堆栈跟踪信息 (stack trace)。级别是error 不处理这个异常 但是会将这个异常信息进行日志化。它等价于 logging.error(..., exc_info=True)，必须在 except 块里调用

## 调试信息 .vscode/launch.json
如果你只是写了一个简单的 main.py，里面全是 print，VS Code 是允许你直接点“运行”或按 F5 调试的。因为 VS Code它默认会帮你执行 python main.py。

但你的项目是一个 FastAPI 后端。你平时启动它的命令不是 python main.py，而是类似于：
uvicorn app.main:app --host 127.0.0.1 --port 8000

这时候 VS Code 就不知道该怎么办了：它不知道你要用 uvicorn 启动，不知道入口是 app.main:app，也不知道要加端口号。如果你直接按 F5，它可能只会去跑 main.py，然后瞬间报错或者直接退出，你的断点根本来不及生效。
.vscode/launch.json 的作用，就是给 VS Code 写一份“启动说明书”。你在这个文件里告诉 VS Code：“请用我指定的 Python 解释器，在指定的目录下，替我执行这行长长的 uvicorn 启动命令，然后再开始调试”。

## yeild
yield 是 Python 语法：交出一个值，并暂停函数。这个值使用完之后 恢复这个函数，让它退出 with，完成数据库连接的清理。

## 依赖注入
fast.Depends是一种实现方式，就是这个依赖不是自己准备，而是交给别人去做别人做完之后注入到这里。
FastAPI 转头去看看 get_db 是个什么函数，然后主动替你执行 get_db()。
get_db 里面通常会帮你连上数据库，然后把连接对象 yield（交）给 FastAPI。
FastAPI 把拿到手的连接对象，塞进你的 connection 参数里。
等你函数执行完、把结果返回给前端后，FastAPI 还会自动回去执行 get_db 剩下的收尾代码（通常是关闭连接）。
## fastapi.depends
fastapi.Depends（依赖注入）的核心用法就一句话：在路由函数的参数里声明“我需要什么”，并告诉 FastAPI 去哪个函数里拿，FastAPI 就会在运行你的代码前自动去执行那个函数，并把结果塞给你。
因为 FastAPI 的依赖注入机制。你只要写了 Depends(get_current_user)，FastAPI 就会在运行你的 read_current_user 函数之前，自动去执行 get_current_user()。
执行完之后，把返回的用户对象，自动塞到你参数里的 current_user 上。
为什么 get_current_user 后面没有括号 ()？
这是 Python 函数作为参数传递的语法。你传的是函数对象本身

## psycopg.Connection
是这个数据库连接对象

## 数据库 什么是schema
Schema 在 PostgreSQL 里叫“模式”（或者叫命名空间），你可以把它理解成数据库里的“文件夹”。
一个作用是防止重名 就是可以在一个数据库里创建不同的shcema 这些schema属于不同的命名空间 然后不同命名空间可以有相同的表名。
如果不建schema 那么public'就是默认的命名空间 。
如果建了schema 那么找表时需要带上这个schema的名字。SELECT * FROM hr.employees，不带的时候 默认从public里找。

## schema
在这个文件夹中 值得意思是：模式 结构定义  具体就是这个接口数据的结构定义。
在 PostgreSQL 中，schema 是数据库内部用于组织表、视图、函数等对象的“命名空间”


## pwdlib[argon2]
是个加密库,将用户密码不明文存到数据库中，而是随即盐+密码 进行哈希之后 存这串乱码。当然盐也需要存。
密码不存明文、不作解密，而是将“明文密码+随机盐”经过故意变慢的单向哈希算法算成密文；校验时只是把输入重新算一遍比对——因为不可逆且单次计算成本极高，所以即使黑客拿到盐和规则，也绝对无法反向破解或批量穷举

## pyJWT--JSON Web Token

PyJWT 的核心功能只有两个，正好对应你认证流程中的两个关键步骤：
jwt.encode()：签发 Token。用户登录成功后，你把用户 ID、过期时间等信息（Payload）和服务器密钥，交给 jwt.encode()，它会生成一串看起来像乱码的字符串（Token）返回给前端。
jwt.decode()：验证 Token。用户后续携带 Token 访问受保护接口时，你用 jwt.decode() 和同一把密钥去验证它。如果 Token 被篡改或过期，会直接抛出异常，验证失败。

算法（比如 SHA256）是完全公开的，全世界的人都知道。JWT 的内容（包含用户 ID 和有效期 exp）是明文，只是被 Base64 编码了一下，谁都能解开看。
如果只靠算法，会发生什么可怕的事情？
黑客截获了你的 Token，把里面的有效期从“今天到期”改成“2099年到期”，然后拿公开的算法重新算一遍，发回给服务器。
因为服务器只用算法验证，算出来的结果是对的，服务器就会放行！黑客就能永远登录你的账号。
所以，光有算法绝对不行。你必须有一样“只有你知道，别人不知道”的东西，把它混在算法里一起去算。 这个东西就是 SECRET_KEY。
（在代码中配置的：）backend\pyproject.toml
服务器生成 Token 时：签名 = 算法(Token内容 + SECRET_KEY)。
黑客篡改内容后，想重新计算签名，但他没有 SECRET_KEY，所以算出的签名绝对对不上。服务器一比对，就知道被篡改了。

## pydantic-settings
是一个专门用于应用配置管理的库，它能让你用一种类型安全、自动化的方式，从环境变量或文件中加载和管理配置。只需创建一个继承自 BaseSettings 的类，并声明字段和类型。实例化时，它会自动从环境变量中查找并加载匹配的值。
除了直接读取系统的环境变量，它原生支持从各种格式的文件中读取配置，最常用的就是 .env 文件，同时也支持 JSON、YAML 和 TOML 等格式。

## fastapi.HTTPException
是 FastAPI 专门用来主动向前端返回 HTTP 错误状态码（比如 404、401、400）的异常类。
它的三个核心参数：
status_code：必填。标准的 HTTP 状态码，比如 400（请求错误）、401（未登录）、403（无权限）、404（找不到）、409（冲突）。
detail：必填。返回给前端的错误信息。可以是一个字符串，也可以是一个列表或字典。
headers：选填。如果你需要返回一些特殊的响应头（比如 401 未授权时，通常需要带 WWW-Authenticate: Bearer 头）。

异常类的传参，就是为了把错误的具体细节（谁、在哪、为什么、当前是什么值）打包传递出去，方便外层的 except 捕获后，能根据这些信息做出正确的处理（比如打印日志、重试、或者像 FastAPI 那样转成 JSON 返回给前端）。