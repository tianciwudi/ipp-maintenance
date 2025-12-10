# ipp-maintenance
A custom component based on IPP that provides a one-click CMYK color blocks print to help prevent nozzle clogging.

本集成基于homeassistant集成IPP，新增了打印CMYK色块按钮，可配合HA定时任务实现定期自动打印CMYK色块，避免喷头堵塞问题。

## 安装

方法1：下载并复制`custom_components/ipp_maintenance`文件夹到HomeAssistant根目录下的`custom_components`文件夹即可完成安装

方法2：已经安装了HACS，可以点击按钮快速安装 [![通过HACS添加集成](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tianciwudi&repository=ipp-maintenance&category=integration)

## 配置

配置 > 设备与服务 >  集成 >  添加集成 > 搜索`ipp_maintenance`

或者点击: [![添加集成](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=ipp_maintenance)


## Acknowledgments / Credits

This project is based on IPP, and the PWG generation part references the Open Print Stack:

- **Open Print Stack**  
  Repository: <https://github.com/cskau/open-print-stack>  
  Used under the terms of its respective license.

- **Home Assistant – IPP Integration**  
  Repository: <https://github.com/home-assistant/core/tree/dev/homeassistant/components/ipp>  
  Used under the Apache License 2.0 and in accordance with the Home Assistant project’s licensing guidelines.

We gratefully acknowledge the original authors and contributors of these projects.

## 致谢 / 版权声明

本项目基于IPP，PWG生成部分引用了Open Print Stack：

- **Open Print Stack**  
  项目地址：<https://github.com/cskau/open-print-stack>  
  遵循其仓库中指定的许可证。

- **Home Assistant – IPP 组件**  
  项目地址：<https://github.com/home-assistant/core/tree/dev/homeassistant/components/ipp>  
  依据 Apache License 2.0 及 Home Assistant 项目版权要求使用。

在此对以上项目的原作者及贡献者表示感谢。
