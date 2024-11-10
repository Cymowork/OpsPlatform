#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Annotated
#  Annotated 是 Python 3.9+ 中引入的类型提示（Type Hints）特性，位于 typing 模块中。
# 它用于在函数参数或返回值上添加额外的元数据或注解。
# 主要作用
    # 类型注解增强
    # 允许为类型提示添加额外的元数据
    # 不影响运行时的类型检查
    # 主要用于静态类型检查器和文档生成

from fastapi import APIRouter, Depends, Request, Response
# Depends 是 FastAPI 框架中的一个依赖注入函数，用于将依赖项注入到路由处理函数中。
# 它允许你在处理函数中使用其他函数或服务，从而实现依赖注入模式。        
# Request 和 Response 是 FastAPI 框架中的请求和响应对象，用于处理 HTTP 请求和响应。 
# 它们提供了对请求和响应的访问和操作，包括请求头、请求体、响应状态码、响应头等。    
# APIRouter 是 FastAPI 框架中的一个类，用于定义和管理 API 路由。
# 它允许你将相关的路由分组在一起，并添加各种元数据和配置，从而创建更结构化和可维护的 API 端点。

from fastapi.security import HTTPBasicCredentials
# HTTPBasicCredentials 是 FastAPI 框架中的一个类，用于处理 HTTP 基本认证（Basic Authentication）的凭证。    
# 它提供了对 HTTP 基本认证请求的访问和操作，包括用户名和密码。

from fastapi_limiter.depends import RateLimiter
# RateLimiter 是 FastAPI 框架中的一个依赖项，用于实现速率限制功能。
# 它允许你在路由处理函数上添加速率限制，从而控制请求的频率和数量。

from starlette.background import BackgroundTasks
# BackgroundTasks 是 FastAPI 框架中的一个类，用于处理后台任务。
# 它允许你在处理函数中执行一些后台任务，而不阻塞主线程。        

from backend.app.admin.schema.token import GetSwaggerToken
# GetSwaggerToken 是 FastAPI 框架中的一个类，用于处理 Swagger 调试专用登录的响应。
# 它定义了 Swagger 调试专用登录的响应格式，包括 access_token 和 user。

from backend.app.admin.schema.user import AuthLoginParam
# AuthLoginParam 是 FastAPI 框架中的一个类，用于处理用户登录的参数。
# 它定义了用户登录的参数格式，包括用户名、密码等。

from backend.app.admin.service.auth_service import auth_service 
# auth_service 是 FastAPI 框架中的一个服务，用于处理认证相关的逻辑。
# 它提供了用户登录、登出、创建新 token 等功能。

from backend.common.response.response_schema import ResponseModel, response_base
# ResponseModel 是 FastAPI 框架中的一个类，用于定义响应的格式。
# response_base 是 FastAPI 框架中的一个模块，用于定义通用的响应格式。

from backend.common.security.jwt import DependsJwtAuth
# DependsJwtAuth 是 FastAPI 框架中的一个依赖项，用于处理 JWT 认证。
# 它允许你在路由处理函数中添加 JWT 认证，从而保护 API 端点。    

router = APIRouter()
# router 是 FastAPI 框架中的一个类，用于定义和管理 API 路由。
# 它允许你将相关的路由分组在一起，并添加各种元数据和配置，从而创建更结构化和可维护的 API 端点。

@router.post('/login/swagger', summary='swagger 调试专用', description='用于快捷获取 token 进行 swagger 认证')
# 定义了一个 POST 请求的路由，用于处理 Swagger 调试专用登录。
# summary 用于描述路由的简短摘要。
# description 用于描述路由的详细描述。
async def swagger_login(obj: Annotated[HTTPBasicCredentials, Depends()]) -> GetSwaggerToken:
    token, user = await auth_service.swagger_login(obj=obj)
    return GetSwaggerToken(access_token=token, user=user)  # type: ignore


@router.post(
    '/login',
    summary='用户登录',
    description='json 格式登录, 仅支持在第三方api工具调试, 例如: postman',
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def user_login(
    request: Request, response: Response, obj: AuthLoginParam, background_tasks: BackgroundTasks
) -> ResponseModel:
    data = await auth_service.login(request=request, response=response, obj=obj, background_tasks=background_tasks)
    return response_base.success(data=data)


@router.post('/token/new', summary='创建新 token', dependencies=[DependsJwtAuth])
async def create_new_token(request: Request, response: Response) -> ResponseModel:
    data = await auth_service.new_token(request=request, response=response)
    return response_base.success(data=data)


@router.post('/logout', summary='用户登出', dependencies=[DependsJwtAuth])
async def user_logout(request: Request, response: Response) -> ResponseModel:
    await auth_service.logout(request=request, response=response)
    return response_base.success()
