FROM nonebot/nb-cli:latest

# 设置工作目录
WORKDIR /MaiMBot

# 先复制依赖列表
COPY requirements.txt .

# 安装依赖（这层会被缓存直到requirements.txt改变）
RUN pip install --upgrade -r requirements.txt

# 然后复制项目代码
COPY . .

VOLUME [ "/MaiMBot/config" ]
VOLUME [ "/MaiMBot/data" ]
EXPOSE 8080
ENTRYPOINT [ "nb","run" ]