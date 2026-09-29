# Spirula 本地运行手册

实测版本 v2026.9.24（183b2c6），Windows RTX 3090 24GB。程序来自官方 release；下载后核对 release digest。不要自动下载新权重或接受模型条款来扩展本次任务。

以下大写标记都是需按当前任务设置的路径或名称。输出写入新的任务目录，保留旧结果。新版本先查 help，不机械沿用参数。

## 抽帧和遮罩

```text
spirula sam extract INPUT.insv --out DATA/images --skip 24 --keep 12 --sync --threads 4 --lang en
spirula sam mask DATA/images --preview MASK_PREVIEW.png --lang en
```

本次视频 24fps，skip=24 对应约每秒一组，keep=12 为附近候选选择；文件序号对应原始帧，不是精确秒标签。检查 cam0/cam1 数量一致、起止范围与图像清晰度。上述 mask 是边界处理，不可报告为已完成人物分割。

## 鱼眼定位

```text
spirula sfm auto DATA/images -o DATA/recon --camera-model opencv-fisheye --rig dual-fisheye=cam0,cam1 --sequence cam0,cam1 --data-type video --quality high --pairs prefilter --prefilter-sequential --max-image-size 1920 --max-features 8192 --lang en
```

输入应是 images/，避免从同时含 masks/ 的父目录枚举出重复图。曾遇 auto 对 780 图安排穷举匹配；检查候选对数量及预计资源后再决定是否改预筛。停止任务前核实 PID 与命令行，不能影响其他工作。

对齐后核对 sparse 模型数量、注册图数、每个镜头覆盖及未注册时间段。日志 reprojection error 与导出文件字段可能不同：本次某些导出误差字段为 0，不应取代日志的 0.610 px。rig 可补推部分位姿，注册不等于视觉校验通过。

## 训练

```text
spirula train 360-camera --data DATA --colmap-recon-dir recon/sparse/0 --output-dir-prefix RUNS --output-dir-name RUN_NAME --num-iterations 30000 --cap-max 2000000 --train-resolution-divisor 1 --distraction-robustness mild --eval-mode interval --eval-interval 16 --save-eval-images 1 --save-full-checkpoint 1 --disable-viewer 1 --keep-viewer-alive 0 --lang en
```

检查 config.json 中 warp_to_pinhole、warp_face_fit、warp_back_face，以及日志中 splitting 数量。本次 706 张注册图分为 661 训练、45 评估；五面展开为 3,305 和 225 视图。颜色校正前后指标分开报告。没有运行 geometry 就不报告深度、法线辅助。

完成条件：进程正常结束，日志明确 training complete，最终 checkpoint 的 PLY 存在可读，metrics 与评估图已生成。训练阶段耗时不冒充总流程耗时。

## 查看与恢复

使用 ReSpace README 的本地数据接口；npm 依赖安装到项目自身，不借用无关项目的 node_modules。generated/ 包含本地视点，应被 Git 忽略。现阶段 SuperSplat 假设模型 Z-up，需同时转换视点。

曾遇 Windows PowerShell 对无 BOM 的中文脚本解析失败：需确定执行 shell 的编码兼容性，修复后检查实际发布文件和 HTTP，不仅确认进程启动。内置浏览器可能拒绝 pointer lock，提供按住鼠标转向的替代。

AWS 全景模块的既有探测只接受预期 ERP 格式，不能把方形双鱼眼直接当 ERP。不要据此声称完整 AWS 重建可用。
