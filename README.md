<div align="center">

# _AstrBot Admin Tools Plugin_

![views](https://count.getloli.com/get/@astrbot_plugin_llm_qqgroupTools?theme=booru-jaypee)<br>

_✨ 作者：[SatenShiroya](https://github.com/SatenShiroya)✨_

[![Plugin Version](https://img.shields.io/badge/Version-V1.1.3-blue.svg)](https://github.com/SatenShiroya/astrbot_plugin_llm_qqgroupTools)
[![AstrBot](https://img.shields.io/badge/AstrBot-Plugin-ff69b4)](https://github.com/AstrBotDevs/AstrBot)
[![License](https://img.shields.io/badge/License-AGPL%203.0-green.svg)](LICENSE)

</div>

## ✨ _介绍_

- 这是一个 AstrBot 管理工具插件，通过调用接口使AI能自主或听从管理员命令管理群聊
- 功能包括：禁言和解禁、全群禁言、踢人、改名、发群公告、消息设精，更多内容实现中
- 拥有权限控制，在配置项选择是否只有AI管理员能命令还是群主和群管理也可用，以及最重要的踢人功能开关

## ⌨️ _使用说明_

- 推荐在Astrbot人格中暗示AI本身有相应的功能(详情看下方Tools函数)，以便更好使用
- 建议：搭配好感度插件使用，让AI更像个有脾气的小鬼管理员（为所欲为）
- 不建议：开启T人功能，以免一觉醒来臭脾气AI把人都踢掉了

## 📦 _安装_

- 可以直接在Astrbot的插件市场搜索astrbot_plugin_llm_qqgrouptools，点击安装，耐心等待安装完成即可
- 或者下载zip文件到本地，在Astrbot中通过压缩包手动安装  

## 📌 _效果_

- 搭配好感度插件可实现如下图效果

    ![看到这行字说明图片失效了！请访问插件仓库查看效果！](images/1.jpg)
    ![看到这行字说明图片失效了！请访问插件仓库查看效果！](images/2.jpg)<br>
    ![看到这行字说明图片失效了！请访问插件仓库查看效果！](images/3.jpg)
    ![看到这行字说明图片失效了！请访问插件仓库查看效果！](images/4.jpg)<br>


## 📜 _功能列表_

- 下方所有功能均可用通过口语化使用，或者AI自己判断使用

| 功能 | 功能描述 | Tools函数 | 
|------|----------|----------|
| 禁言 | 禁言某用户，时间可以口语化指定，当然也可用让AI解除禁言 | 'set_group_ban' |
| 踢人 | 从群聊移除某人 | 'set_group_kick' |
| 全群禁言 | 开启或关闭本群的全体禁言 | 'set_group_whole_ban' |
| 发布群公告 | 在本群发公告，内容可以让AI自拟 | 'send_group_notice' |
| 改群名片 | 修改用户昵称 | 'set_group_card' |
| 设精 | 群发言设精华，必须引用一条消息 | 'set_essence_msg' |
| 点赞 | 点赞某用户的名片 | 'send_like' |

## 📝 _版本变更履历_

### _V 1.1.3_
 - 新增点赞用户功能，非管理员也可用
 - 新增设精功能，需要引用消息

### _V 1.1.2_
 - 新增发布群公告功能

### _V 1.1.1_
 - 新增小版本号
 - 新增允许群聊管理和群主使唤bot的功能开关
 - 用yield重新编写了函数返回
 - 重新构建以及封装函数使得代码更美观

### _V 1.1_
- 新增设置群成员名片功能；
- 新增处理失败抛出异常；
- 错误返回去除user_id内容，提高安全性；

### _V 1.0_
- 首次修改发布

## 🔗 _相关链接_

- 机器人框架：[AstrBot 官方文档](https://astrbot.app)
- 客户端使用：[Napcat 官方文档](https://napcat.napneko.icu/)
- 初期参考项：[**ctrlkk**](https://github.com/ctrlkk/astrbot_plugin_admin_tools)

## 👥 _贡献指南_

- ⭐️&nbsp; Star 这个项目！（点右上角的星星，感谢支持！）
- 🐞&nbsp; 提交 Issue 报告问题
- 🔧&nbsp; 提交 Pull Request 改进代码
- 🧠&nbsp; 提出新功能建议