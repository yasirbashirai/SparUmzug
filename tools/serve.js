// Local preview server with SPA fallback (mirrors .htaccess / vercel.json behaviour)
const http=require('http'),fs=require('fs'),path=require('path');
const root=path.join(__dirname,'..','website');
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml','.ico':'image/x-icon','.xml':'application/xml','.txt':'text/plain'};
http.createServer((req,res)=>{
  let p=decodeURIComponent(req.url.split('?')[0]);
  let f=path.join(root,p);
  if(fs.existsSync(f)&&fs.statSync(f).isDirectory()){ if(!p.endsWith('/')){res.writeHead(301,{Location:p+'/'});return res.end();} f=path.join(f,'index.html'); }
  if(!fs.existsSync(f)) f=path.join(root,'index.html');
  res.writeHead(200,{'Content-Type':types[path.extname(f)]||'application/octet-stream'});
  fs.createReadStream(f).pipe(res);
}).listen(8765,()=>console.log('http://localhost:8765'));
