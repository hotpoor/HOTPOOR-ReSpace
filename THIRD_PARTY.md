# 第三方组件

依赖由 npm 安装，不将依赖发布包及生成 bundle 纳入 Git。分发构建产物时保留相应许可证和版权声明。

| 组件 | 当前版本 | 许可证 | 来源 |
|---|---|---|---|
| Three.js | 0.170.0 | MIT | https://github.com/mrdoob/three.js |
| GaussianSplats3D | 0.4.7 | MIT | https://github.com/mkkellogg/GaussianSplats3D |
| SuperSplat Viewer | 1.36.0 | MIT | https://github.com/playcanvas/supersplat-viewer |

SuperSplat 官方 bundle 包含 PlayCanvas 引擎，使用时保留上游声明。

Spirula Studio v2026.9.24（183b2c6）是外部重建工具，未捆绑：https://github.com/harry7557558/spirula-studio 。使用或分发它时独立遵守其许可。

鱼眼演示自行实现 OPENCV_FISHEYE 投影与采样，五个轴向对应正前、右、下、左、上。核对 Spirula 的轴向和流程不代表包含其训练源码。

本项目自有代码暂未指定开源许可证。公开可见不等于已授权任意再分发；第三方组件保持各自许可。
