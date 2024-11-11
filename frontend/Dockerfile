# 使用 Node 作為第一階段（build stage）
FROM node:18 AS builder

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json 進入工作目錄
COPY package*.json ./

# 安裝相依的 packages
RUN npm install

# 複製所有源碼
COPY . .

ENV VITE_API_URL=http://localhost:1234

# 構建 React 應用（會將輸出放在 build/ 資料夾）
RUN npm run build

# 使用 Nginx 作為第二階段（production stage）
FROM nginx:stable-alpine


# 複製構建的文件到 Nginx 的預設靜態文件目錄
COPY --from=builder /app/dist /usr/share/nginx/html

# 暴露端口 80
EXPOSE 80

# 啟動 Nginx
CMD ["nginx", "-g", "daemon off;"]
