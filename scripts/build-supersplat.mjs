import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import {renderViewerHtml,js} from '@playcanvas/supersplat-viewer';
import {defaultSettings,validateSettings} from '@playcanvas/supersplat-viewer/settings';
import {resolve} from 'node:path';
const base=resolve(process.env.RESPACE_DATA_DIR||'data')+'/';
const output=resolve('generated/supersplat')+'/';mkdirSync(output,{recursive:true});
for(const model of ['full','sample']){
 if(!existsSync(base+model+'-views.json')){console.log('Skipping unconfigured model: '+model);continue;}
 const v=JSON.parse(readFileSync(base+model+'-views.json','utf8'))[0];
 const transform=p=>[p[0],p[2],-p[1]];
 const settings=defaultSettings(); settings.tonemapping='none'; settings.animTracks=[]; settings.startMode='default'; settings.cameras=[{initial:{position:transform(v.position),target:transform(v.target),fov:85}}]; validateSettings(settings);
 const page=renderViewerHtml({bootstrap:{contentUrl:'/'+model+'.ply',settings},baseHref:'/supersplat/',inlineCss:true,bodyStartExtras:`<div style="position:fixed;top:12px;left:12px;z-index:9999;background:#152321ed;color:white;padding:10px 14px;border-radius:9px;font:14px system-ui"><b>SuperSplat · ${model==='full'?'完整视频版':'30 秒样片'}</b><div style="margin-top:6px"><a style="color:#a6e4ca" href="/?model=${model}">切回原播放器</a> · <a style="color:#a6e4ca" href="/supersplat/${model==='full'?'sample':'full'}.html?lang=zh-CN">切换模型</a></div><small>同一份 PLY · 本地加载 · 未压缩 / 未启用 LOD</small></div>`,headExtras:'<script>const u=new URL(location.href);u.searchParams.set("noanim","");history.replaceState(null,"",u);window.firstFrame=()=>{const e=window.app?.root.findByName("gsplat");if(e){e.setLocalEulerAngles(-90,0,0);window.app.renderNextFrame=true;}};</script>'});
 writeFileSync(output+model+'.html',page);
}
writeFileSync(output+'index.js',js);
console.log('Generated both local viewer pages');
