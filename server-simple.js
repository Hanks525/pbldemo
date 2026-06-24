const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8090;

const mimeTypes = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  let filePath = '.' + req.url;
  if (filePath === './') {
    filePath = './index.html';
  }

  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = mimeTypes[extname] || 'application/octet-stream';

  fs.readFile(filePath, (error, content) => {
    if (error) {
      if(error.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 - 文件未找到</h1>', 'utf-8');
      }
      else {
        res.writeHead(500);
        res.end('服务器错误: ' + error.code);
      }
    }
    else {
      res.writeHead(200, { 'Content-Type': contentType, 'Content-Length': content.length });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(PORT, () => {
  console.log(`服务器运行在 http://localhost:${PORT}/`);
});