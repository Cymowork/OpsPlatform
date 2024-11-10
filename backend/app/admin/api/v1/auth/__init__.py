#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter
# APIRouter 是 FastAPI 框架中的一个类，用于定义和管理 API 路由。
# 它允许你将相关的路由分组在一起，并添加各种元数据和配置，从而创建更结构化和可维护的 API 端点。 

from backend.app.admin.api.v1.auth.auth import router as auth_router
# auth_router 是 FastAPI 框架中的一个路由，用于处理授权相关的逻辑。 
# 它包含了用户登录、登出、创建新 token 等功能。

from backend.app.admin.api.v1.auth.captcha import router as captcha_router
# captcha_router 是 FastAPI 框架中的一个路由，用于处理验证码相关的逻辑。
# 它包含了获取验证码、验证验证码等功能。

router = APIRouter(prefix='/auth')
# router 是 FastAPI 框架中的一个类，用于定义和管理 API 路由。
# 它允许你将相关的路由分组在一起，并添加各种元数据和配置，从而创建更结构化和可维护的 API 端点。

router.include_router(auth_router, tags=['授权'])
# 将 auth_router 路由添加到 router 中，并指定标签为 '授权'。
# 同时，将前缀设置为 '/auth'。  

router.include_router(captcha_router, prefix='/captcha', tags=['验证码'])
# 将 captcha_router 路由添加到 router 中，并指定标签为 '验证码'。
# 同时，将前缀设置为 '/captcha'。