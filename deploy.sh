hexo gen
# 先清理并重新生成，确保文件完整
git add -A
git commit -m "update"
git push origin master
# 强制重新构建 subtree 历史
git subtree split --prefix=public -b gh-pages-temp
git push origin gh-pages-temp:gh-pages --force
git branch -D gh-pages-temp