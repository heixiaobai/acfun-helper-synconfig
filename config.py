# -*- coding:utf-8 -*-

"""
后端服务运行配置信息
开发阶段测试文件，正式上线后应移除后根据实际情况重新设置
"""

SESSION_TYPE = "redis"

# 上线后需要根据需求重设Redis
REDIS_URL = "redis://@localhost:6379/0"

# 上线时需要设置将密钥替换为128位以上的随机字符串
SECRET_KEY = "Dev Test"
# session存活时间，单位秒
SESSION_LIFETIME = 60
