"""项目配置。

职责：集中管理 API Key、Base URL、模型名称等配置项。
"""
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

if not API_KEY:
    raise ValueError("没有配置 API_KEY")

if not BASE_URL:
    raise ValueError("没有配置 BASE_URL")

if not MODEL:
    raise ValueError("没有配置 MODEL")