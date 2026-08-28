const fs = require('fs');
const path = require('path');

const postsDir = 'source/_posts';

function fixImagePaths(dir) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      fixImagePaths(filePath);
    } else if (file.endsWith('.md')) {
      let content = fs.readFileSync(filePath, 'utf8');
      
      // 修复 Typora 本地路径
      content = content.replace(
        /!\[([^\]]*)\]\([^)]*?typora-user-images[^)]*?\)/g,
        (match, alt) => {
          const imgName = match.match(/([^\\\/]+\.(?:png|jpg|jpeg|gif))\)/)[1];
          return `![${alt}](/images/${imgName})`;
        }
      );
      
      // 修复 .com// 格式
      content = content.replace(/\.com\/\//g, '.com/');
      
      fs.writeFileSync(filePath, content);
      console.log(`Fixed: ${filePath}`);
    }
  });
}

fixImagePaths(postsDir);
