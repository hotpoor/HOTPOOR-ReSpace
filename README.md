# HOTPOOR ReSpace

把真实空间，带进浏览器。

本地优先的空间重建验证项目，包含高斯模型漫游、播放器对比和鱼眼投影教学演示。目前是验证版本，尚不是一键重建产品。

沿 X5 全景相机的线索，我们发现 Spirula 和 AWS 工具箱，并先跑通 Spirula。本项目希望让 agent 能参与中间步骤：检查日志与产物、调整流程、验证结果，把经验保存到文档和 SKILL，供下一次任务继续使用。

## 已有功能

- Three.js + GaussianSplats3D：WASD 移动、Q/E 升降、Shift 加速、中键原地转向、拍摄位置跳转。
- 本地 SuperSplat Viewer：同一份 PLY 对比显示，可切回原查看器。
- 鱼眼演示：一个镜头的图片转换为五个透视方向，显示像素对应关系。
- 服务仅监听本机 127.0.0.1；真实素材与生成结果保留在外部数据目录。

## 启动

需要 Node.js 20+、Python 3.10+。Python 无第三方依赖。

```powershell
npm ci
$env:RESPACE_DATA_DIR = 'D:/your-local/reconstruction'
npm run build
python server.py
```

打开 http://127.0.0.1:8768/?model=full 。SuperSplat 在 `/supersplat/full.html?lang=zh-CN`，鱼眼演示在 `/fisheye-demo`。服务器可用 `--port` 和 `--data-dir` 设置。构建与服务器应指向同一数据目录。

没有本地数据时，查看器显示配置提示；构建跳过缺少视点文件的模型。仓库不提供私人素材或自动下载场景。

## 数据接口（第一版）

本版保留 sample/full 两个槽位。完整版需要 `full-model.json`、`full-views.json` 和清单指定的 PLY。

清单 `full-model.json`：

```json
{"name":"完整视频版","summary":"我的空间","scope":"未经清理的重建结果","file":"models/full.ply"}
```

视点 `full-views.json`（至少一个）：

```json
[{"name":"起始位置","position":[0,0,1],"target":[0,1,1],"up":[0,0,1]}]
```

`file` 必须位于数据目录内。当前 SuperSplat 适配针对 Z-up 模型：模型和相机同时绕 X 轴旋转 -90° 对应 Y-up。其他坐标约定须调整适配器。原始 PLY 不变。

样片兼容路径：`sample-views.json`、`training/spirula-x5-30s-eval/step-000006000.ckpt/splat.ply`。

鱼眼演示是固定标定样例：读取 `x5-full/images/cam0/00022.jpg` 和 `x5-full/masks/cam0/00022.png`，遮罩白色为有效区。换素材时须同步替换页面中的镜头参数。它不是通用转换器，也不逐像素复刻训练内部的裁边。

## 项目文档

- [路线与实施策略](docs/IMPLEMENTATION_STRATEGY.md)
- [开发者日志](docs/DEVELOPMENT_LOG.md)
- [开发传记与产品判断](docs/DEVELOPMENT_STORY.md)
- [可复用 SKILL](skills/hotpoor-respace-360/SKILL.md)
- [第三方组件](THIRD_PARTY.md)

## 开发验证

```powershell
npm run check
python -m unittest discover -s tests
```

`web/` 存放页面；`scripts/` 生成 SuperSplat 页面；`server.py` 只提供明确列出的资源路由。`generated/` 含本地视点，已排除 Git。

Spirula 是独立的第三方重建工具。本仓库不捆绑其二进制、权重或源码，尚无自动训练调度。当前没有压缩、LOD 或碰撞模型；播放器不能自动修复重建缺损。
