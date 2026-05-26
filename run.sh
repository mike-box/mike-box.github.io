#!/bin/bash
# save as fix.sh, then chmod +x fix.sh && ./fix.sh

echo "=== 清理旧依赖 ==="
rm -rf node_modules package-lock.json

echo "=== 重新安装 ==="
npm install

echo "=== 处理不兼容插件 ==="
npm uninstall hexo-calendar hexo-pdf
npm install hexo-generator-calendar --save  # 替换日历插件
npm install hexo-pdf --save  # 重装 pdf 插件

echo "=== 验证 ==="
hexo clean
hexo generate
