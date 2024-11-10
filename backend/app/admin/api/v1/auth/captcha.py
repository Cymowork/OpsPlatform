#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fast_captcha import img_captcha
# 图片验证码和文字验证工具
# https://pypi.org/project/fast_captcha/
# from fast_captcha import img_captcha (原代码里面写的)

from fastapi import APIRouter, Depends, Request
# fastapi 是 FastAPI 框架的核心库，用于构建和运行 Web 应用程序。    
# Depends 是 FastAPI 中的一个装饰器，用于将依赖注入到路由处理函数中。
# Request 是 FastAPI 中的一个类，用于表示 HTTP 请求。
# APIRouter 是 FastAPI 中的一个类，用于定义 API 路由。
# from fastapi import APIRouter, Depends, Request(这是原代码写的)

from fastapi_limiter.depends import RateLimiter 
# fastapi_limiter 是 FastAPI 的一个扩展库，用于实现速率限制。
# RateLimiter 是用于限制API访问频率的类，可以设置在指定时间内允许的最大请求次数。
# depends 是 fastapi_limiter 中的一个模块，用于将依赖注入到路由处理函数中。
# from fastapi_limiter.depends import RateLimiter(这是原代码写的)

from starlette.concurrency import run_in_threadpool
# starlette.concurrency 是 Starlette 框架中的一个模块，用于处理并发任务。
# run_in_threadpool 是用于在多线程环境中运行阻塞代码的函数，可以提高性能。
# from starlette.concurrency import run_in_threadpool(这是原代码写的)

from backend.app.admin.conf import admin_settings   
# backend.app.admin.conf 是后端应用的配置模块，用于获取管理员相关的配置。(项目内的路径)
# admin_settings 是配置模块中的一个类，用于获取管理员相关的配置。
# from backend.app.admin.conf import admin_settings(这是原代码写的)

from backend.common.response.response_schema import ResponseModel, response_base
# backend.common.response.response_schema 是后端应用的响应模块，用于定义响应的结构。(项目内的路径)
# ResponseModel 是响应模块中的一个类，用于定义响应的结构。
# response_base 是响应模块中的一个类，用于定义响应的结构。  
# from backend.common.response.response_schema import ResponseModel, response_base(这是原代码写的)

from backend.database.db_redis import redis_client  
# backend.database.db_redis 是后端应用的Redis数据库模块，用于与Redis数据库进行交互。(项目内的路径)
# redis_client 是数据库模块中的一个类，用于与Redis数据库进行交互。
# from backend.database.db_redis import redis_client(这是原代码写的)

router = APIRouter()
# APIRouter 是 FastAPI 中的一个类，用于定义API路由。
# router = APIRouter()(这是原代码写的)
# router 本身就是路由的意思，可以理解为路由器。
# 按功能命名
    # auth_router = APIRouter()  # 认证相关的路由
    # user_router = APIRouter()  # 用户相关的路由
    # product_router = APIRouter()  # 产品相关的路由

@router.get(
    '',
    summary='获取登录验证码',
    # summary 是用于描述API的路径和功能的字符串。   (fastapi框架的接口文档功能)

    dependencies=[Depends(RateLimiter(times=5, seconds=10))],   
    # dependencies 是用于定义API的依赖关系。
    # RateLimiter 是用于限制API访问频率的类，可以设置在指定时间内允许的最大请求次数。
    # times=5, seconds=10 表示在10秒内最多允许5次请求。
    # 1.最内层 - RateLimiter(times=5, seconds=10)
        # RateLimiter(times=5, seconds=10)  # 创建限流器实例
        # times=5: 允许的请求次数
        # seconds=10: 时间窗口（10秒）
        # 意思是：10秒内最多允许5次请求
    # 2.中间层 - Depends()
        # Depends(RateLimiter(...))  # 将限流器包装为FastAPI的依赖项
        # Depends: FastAPI的依赖注入系统
        # 使组件能够被FastAPI正确识别和处理
    # 3.最外层 - dependencies=[Depends(...)]
        # dependencies=[Depends(...)]  # 将限流器包装为FastAPI的依赖项   
        # 可以添加多个依赖：dependencies=[Depends(A), Depends(B)]
        # 所有依赖都会在请求处理前执行  
    # 就像一个安检流程：
        # RateLimiter(times=5, seconds=10) 是安检规则（10秒内最多5人）
        # Depends() 是将这个规则注册为正式安检项
        # dependencies=[...] 是安检点的检查项目清单

)
async def get_captcha(request: Request) -> ResponseModel:
    # 获取验证码    
    # 拆解为三个部分：
        # 函数名：get_captcha
            # 表示这是一个获取验证码的函数
            # 命名符合功能描述
        # 参数部分：(request: Request)
            # request 是参数名
            # : 后面的 Request 是类型注解
            # 表示这个参数必须是 Request 类型
        # 返回值：-> ResponseModel
            # -> 是 Python 3.5+ 引入的类型注解（Type Hints）语法
            # 表示这个函数返回一个 ResponseModel 类型的值
            # 返回值的类型注解：-> ResponseModel
            # 表示这个函数返回一个 ResponseModel 类型的数据
    # 这就像写一份合同：
        # 函数名说明这是做什么的（获取验证码）
        # 参数部分说明需要什么输入（请求对象）
        # 返回值类型说明会得到什么结果（响应模型）
    img_type: str = 'base64'
    # 图片类型  
    img, code = await run_in_threadpool(img_captcha, img_byte=img_type)
    # 生成图片和验证码
    # 1.解构赋值：
        # img, code = ...  同时获取两个返回值
        # img: 生成的验证码图片（base64格式）
        # code: 验证码文本内容 
    # 2.异步操作：
        # await run_in_threadpool(...)
            # 将阻塞操作（img_captcha）放入线程池中执行
            # 提高性能，避免阻塞    
        # await: 等待异步操作完成   
        # run_in_threadpool: 将阻塞操作（img_captcha）放入线程池中执行
    # 3. 函数调用：
        # img_captcha(img_byte=img_type)  # 调用验证码生成函数
        # img_captcha: 验证码生成函数
        # img_byte='base64': 指定返回base64格式的图片
    # 完整的工作流程：
        # 调用 img_captcha 生成验证码
        # 在线程池中执行以避免阻塞
        # 等待执行完成
        # 获取图片和验证码文本
    # 就像：
        # 去照相馆拍照（img_captcha）
        # 让专业人员处理照片（run_in_threadpool）
        # 等待处理完成（await）
        # 最后得到照片和电子文件（img, code）
    
    ip = request.state.ip
    # 从请求对象中获取客户端的 IP 地址
    # 组成部分：
        # request: 请求对象（FastAPI的Request类）
        # state: request的状态属性，用于存储请求级别的状态数据
        # ip: 存储在state中的IP地址值
    # 就像：
        # request 是一个信封
        # state 是信封上的备注栏
        # ip 是在备注栏中记录的寄件人地址
    # 这样设计的好处：
        # 可以在整个请求过程中传递数据
        # 避免重复获取IP地址
        # 方便进行IP相关的操作（如限流、日志等）

    await redis_client.set(
        # 将验证码文本存储在Redis中
        # 1. Redis操作
            # redis_client: Redis客户端实例
            # .set(): Redis的设置值命令
            # await: 因为是异步操作，需要等待完成
        
         f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{ip}', code, ex=admin_settings.CAPTCHA_LOGIN_EXPIRE_SECONDS
            # 第一个参数：键名
                #f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{ip}'  
                # 使用f-string格式化字符串
                # 可能生成的键名如：'captcha:login:192.168.1.1'
            # 第二个参数：值
                # code  # 验证码内容    
            # 第三个参数：过期时间
                # ex=admin_settings.CAPTCHA_LOGIN_EXPIRE_SECONDS  # 多少秒后过期
            #就像：
                # 在Redis这个大仓库里
                # 放入一个标记了IP的盒子（键）
                # 里面装着验证码（值）
                # 并设置5分钟后自动销毁（过期时间）
    )
    return response_base.success(data={'image_type': img_type, 'image': img})   
    # 返回响应
        # response_base.success(): 返回成功的响应
        # data: 响应的数据
            # image_type: 图片类型
            # image: 图片内容   
    # 就像：
        # response_base.success() 是一个标准信封模板
        # data={...} 是信封里装的具体内容
        # 内容包括：
            # 图片的格式说明（image_type）
            # 图片本身（image）



# @router.get(
#     '',
#     summary='获取登录验证码',
#     dependencies=[Depends(RateLimiter(times=5, seconds=10))],
# )
# async def get_captcha(request: Request) -> ResponseModel:
#     """
#     此接口可能存在性能损耗，尽管是异步接口，但是验证码生成是IO密集型任务，使用线程池尽量减少性能损耗
#     """
#     img_type: str = 'base64'
#     img, code = await run_in_threadpool(img_captcha, img_byte=img_type)
#     ip = request.state.ip
#     await redis_client.set(
#         f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{ip}', code, ex=admin_settings.CAPTCHA_LOGIN_EXPIRE_SECONDS
#     )
#     return response_base.success(data={'image_type': img_type, 'image': img})
