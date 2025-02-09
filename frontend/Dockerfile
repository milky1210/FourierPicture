FROM nginx:alpine
# index.html などの静的ファイルを配置
COPY index.html /usr/share/nginx/html/
# カスタム Nginx 設定ファイルを上書き
COPY default.conf /etc/nginx/conf.d/default.conf
