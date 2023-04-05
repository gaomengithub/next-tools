import multiprocessing

# 监听内网端口8000
bind = "0.0.0.0:8000"
# 并行工作进程数
workers = multiprocessing.cpu_count() * 2 + 1
# 监听队列
backlog = 2048
# 工作模式协程。
worker_class = "uvicorn.workers.UvicornWorker"
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# worker_connections最大客户端并发数量，默认情况下这个值为1000。
worker_connections = 2000
# 设置日志记录水平
loglevel = 'info'
# supervisor管理gunicorn 日志输出到supervisor日志文件
errorlog = '-'
accesslog = '-'
# 日志格式
logconfig_dict = {
    'formatters': {
        "generic": {
            "format": "%(process)d %(asctime)s %(levelname)s %(message)s",  # 打日志的格式
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",  # 时间显示方法
            "class": "logging.Formatter"
        }
    }
}
