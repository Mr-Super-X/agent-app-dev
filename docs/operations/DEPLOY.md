# 部署文档

> 本教程是 VitePress 静态站，部署成本极低。本文档列出 3 种部署方案。

## 方案 1：GitHub Pages（推荐，零成本）

适用：开源项目、公开教程

### 步骤

1. 推送到 GitHub
   ```bash
   git remote add origin git@github.com:<user>/agent-tutorial.git
   git push -u origin main
   ```

2. 在 GitHub repo Settings → Pages → Source 选 "GitHub Actions"

3. 每次推 main 自动部署到 `https://<user>.github.io/agent-tutorial/`

### 优点
- 零成本
- 与 git workflow 集成
- GitHub Actions 免费额度（公开仓库无限）

### 缺点
- 仅静态站点
- 国内访问慢（需配 CDN）

## 方案 2：Vercel（最简单，零配置）

适用：快速上线、自动 HTTPS、全球 CDN

### 步骤

1. 推送到 GitHub（同上）
2. 访问 https://vercel.com → Import Project → 选仓库
3. Vercel 自动识别 VitePress，构建命令 `pnpm docs:build`，输出 `docs/.vitepress/dist`
4. 点击 Deploy，几分钟后上线

### 优点
- 零配置
- 全球 CDN
- 自动 HTTPS
- 预览部署（每个 PR 一个预览链接）

### 缺点
- 免费额度有限（个人项目够用）
- 国内访问不稳定

## 方案 3：自建服务器（完全控制）

适用：内部团队、国内访问、合规要求

### 步骤

1. 服务器装 Nginx
2. 配置 Nginx 指向 `docs/.vitepress/dist/`
3. 配 systemd 定时拉 git + 重建
4. 配 HTTPS（Let's Encrypt / acme.sh）

### 优点
- 完全控制
- 国内访问快
- 无第三方依赖

### 缺点
- 需要运维
- 需要备案（国内服务器）

## 当前 deploy 配置

本仓库已配 GitHub Actions deploy workflow：`.github/workflows/deploy.yml`。

推 main 即自动部署到 GitHub Pages。
