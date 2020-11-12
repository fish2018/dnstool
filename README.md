## 背景
项目生产环境分批切K8s时，由于官网在使用一级域名，所以无法直接泛域名解析到Ingress Controller；
只能对每个ingress的域名进行单独配置records

## 功能
#### 1、阿里云private_zone批量添加record
#### 2、windows DNS批量添加record

## 安装依赖
```
pip install -r requirements.txt
```

## 修改配置信息
配置文件: `config.py`

## 运行
入口文件`run.py`
```
python3 run.py
```