# 网络认证助手
# 主要功能
**对"YMUN"网络网关进行实时监测，当识别到对应网关IP地址时，通过requests提交带参数的请求，配合系统自带的"任务计划程序"，即可实现接入YMUN网络时自动连接**

# 相关参数（在config.ini中设置）
id：登录账号/n
password：登录密码  
try_times：登录失败时重登次数  
try_interval：登录失败时重登时间间隔（秒）  
connect_detect_interval：网络检测间隔（秒）

### 为避免对认证服务器造成压力，请合理设置try_times和try_interval
### 软件仅供交流学习使用，请勿用于非法用途。
