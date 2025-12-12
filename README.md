# ipp-maintenance
This integration is based on Home Assistant's IPP integration and adds a button for printing CMYK color blocks. It can be used together with HA scheduled tasks to automatically print CMYK color blocks periodically, helping prevent printhead clogging.

本集成基于homeassistant集成IPP，新增了打印CMYK色块按钮，可配合HA定时任务实现定期自动打印CMYK色块，避免喷头堵塞问题。

## 安装

方法1：下载并复制`custom_components/ipp_maintenance`文件夹到HomeAssistant根目录下的`custom_components`文件夹即可完成安装

方法2：已经安装了HACS，可以点击按钮快速安装 [![通过HACS添加集成](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tianciwudi&repository=ipp-maintenance&category=integration)

## 配置

配置 > 设备与服务 >  集成 >  添加集成 > 搜索`ipp_maintenance`

或者点击: [![添加集成](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=ipp_maintenance)

## 其他
在HP Smart Tank 580-590打印机上测试过可行，打印采用image/pwg-raster格式、ipp协议，应该绝大多数支持网络打印的打印机都支持。

Tested and proven to be feasible on the HP Smart Tank 580-590 printer, using the image/pwg-raster format and IPP protocol for printing. This should be compatible with the vast majority of network-enabled printers.

## 打印图
![打印的CMYK图](cmyk.png)

## Acknowledgments / Credits

This project is based on IPP, and the PWG generation part references the Open Print Stack:

- **Open Print Stack**  
  Repository: <https://github.com/cskau/open-print-stack>  
  Thanks so much. The image/jpeg format does not support pure K printing, while the image/pwg-raster format does, but its generation rules are complex. This had troubled me for a long time, and fortunately this project accomplished it.

- **Home Assistant – IPP Integration**  
  Repository: <https://github.com/home-assistant/core/tree/dev/homeassistant/components/ipp>  
  Used under the Apache License 2.0 and in accordance with the Home Assistant project’s licensing guidelines.

We gratefully acknowledge the original authors and contributors of these projects.

## 致谢 / 版权声明

本项目基于IPP，PWG生成部分引用了Open Print Stack：

- **Open Print Stack**  
  项目地址：<https://github.com/cskau/open-print-stack>  
  非常感谢，image/jpeg格式不支持纯K色打印，image/pwg-raster格式支持，但生成规则复杂，这困扰了我很久，万幸该项目实现了这一点。

- **Home Assistant – IPP 组件**  
  项目地址：<https://github.com/home-assistant/core/tree/dev/homeassistant/components/ipp>  
  依据 Apache License 2.0 及 Home Assistant 项目版权要求使用。

在此对以上项目的原作者及贡献者表示感谢。
