# Redis配置
REDIS_HOST = "192.168.142.128"  # Redis服务器地址
REDIS_PORT = 6379         # Redis端口
REDIS_DB = 0              # Redis数据库编号
NONCE_EXPIRE_SECONDS = 300  # nonce过期时间（秒）
REDIS_PASSWORD = "656634739"

# MySQL数据库配置
MYSQL_HOST = "192.168.142.128"      # MySQL服务器地址
MYSQL_PORT = 3306             # MySQL端口
MYSQL_USER = "background_user"      # MySQL用户名
MYSQL_PASSWORD = "Gaolei%25656634739"  # MySQL密码 %转义%25
MYSQL_DB = "background"          # 数据库名

# 密码加密相关
PASSWORD_HASH_ITERATIONS = 100000  # pbkdf2迭代次数 

# JWT令牌相关
SECRET_KEY = "d9s2v5k3j8l6m2n9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 4320

# 模型配置
DEFAULT_MODEL = "qwen2.5-coder-14b-instruct"  # 默认使用的模型

MODEL_CONFIG = {
    "qwen2.5-coder-14b-instruct": {
        "base_url": "http://192.168.31.22:12345",  # 模型服务地址
        "model_name": "qwen2.5-coder-14b-instruct",  # 模型名称
        "timeout": 180,  # 请求超时时间（秒）
        "max_tokens": 4096,  # 最大token数
        "temperature": 0.7  # 温度参数
    },
    "qwen2.5-coder-32b-instruct": {
        "base_url": "http://192.168.31.22:12345",  # 模型服务地址
        "model_name": "qwen2.5-coder-32b-instruct",  # 模型名称
        "timeout": 360,  # 请求超时时间（秒）
        "max_tokens": 8192,  # 最大token数
        "temperature": 0.7  # 温度参数
    }
}