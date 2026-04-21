<div align="center">

# _AstrBot Admin Tools Plugin_

![views](https://count.getloli.com/get/@astrbot_plugin_llm_qqgroupTools?theme=booru-jaypee)<br>

_✨ 作者：[SatenShiroya](https://github.com/SatenShiroya)✨_

[![Plugin Version](https://img.shields.io/badge/Version-V2.0.0-blue.svg)](https://github.com/SatenShiroya/astrbot_plugin_llm_qqgroupTools)
[![AstrBot](https://img.shields.io/badge/AstrBot-Plugin-ff69b4)](https://github.com/AstrBotDevs/AstrBot)
[![License](https://img.shields.io/badge/License-AGPL%203.0-green.svg)](LICENSE)

</div>

## ✨ _介绍_

- 这是一个 AstrBot 管理工具插件，通过调用接口使AI能听从管理员命令管理群聊或自主实现禁言功能
- 功能包括：禁言和解禁、全群禁言、踢人、改名、发群公告、消息设精，更多内容实现中
- 拥有权限控制，在配置项选择是否开启权限验证（默认开启）和是否只有AI管理员能命令还是群主和群管理也可用，以及最重要的踢人功能开关

## ⌨️ _使用说明_

- 推荐在Astrbot人格中暗示AI本身有相应的功能(详情看下方Tools函数)，以便更好使用
   - 请一定要在人格设置中区分两个禁言工具的使用场景，否则LLM模型调用功能时可能会有概率混淆
- 建议：搭配好感度插件使用，让AI更像个有脾气的小鬼管理员（为所欲为）
- 不建议：开启T人功能，以免一觉醒来臭脾气AI把人都踢掉了

## 📦 _安装_

- 可以直接在Astrbot的插件市场搜索astrbot_plugin_llm_qqgrouptools，点击安装，耐心等待安装完成即可
- 或者下载zip文件到本地，在Astrbot中通过压缩包手动安装  

## 📌 _效果_

- 搭配好感度插件可实现如下图效果

<div align="center">
  <img src="images/1.jpg" alt="看到这行字说明图片失效了！请访问插件仓库查看效果！">
  <img src="images/2.jpg" alt="看到这行字说明图片失效了！请访问插件仓库查看效果！"><br>
  <img src="images/3.jpg" alt="看到这行字说明图片失效了！请访问插件仓库查看效果！">
  <img src="images/4.jpg" alt="看到这行字说明图片失效了！请访问插件仓库查看效果！"><br>
</div>

## 📜 _功能列表_

- 下方所有功能均可用通过口语化使用，或者AI自己判断使用

| 功能 | 功能描述 | Tools函数 | 
|------|----------|----------|
| 禁言 | 让AI禁言某用户，时间可以口语化指定，当然也可用让AI解除禁言 | 'set_group_ban' |
| 自主禁言 | AI自主决定禁言某用户， | 'set_group_ban_byself' |
| 撤回 | 撤回一条消息，必须引用一条消息 | 'delete_msg' |
| 踢人 | 从群聊移除某人 | 'set_group_kick' |
| 全群禁言 | 开启或关闭本群的全体禁言 | 'set_group_whole_ban' |
| 发布群公告 | 在本群发公告，内容可以让AI自拟 | 'send_group_notice' |
| 改群名片 | 修改群用户昵称 | 'set_group_card' |
| 改群名 | 修改群聊名称 | 'set_group_name' |
| 改用户头衔 | 修改群用户头衔 | 'set_group_special_title' |
| 设精 | 群发言设精华，必须引用一条消息 | 'set_essence_msg' |
| 取消设精 | 取消群精华消息，必须引用一条消息 | 'delete_essence_msg' |
| 通过描述取消设精 | 通过描述消息内容或者消息所属成员又或者设精消息的人员来取消群精华消息 | 'delete_essence_msg_by_id' |
| @全体成员 | @全体成员并发送原因，留空则不发送原因 | 'send_group_at_all' |
| 点赞 | 点赞某用户的名片 | 'send_like' |

## 📝 _版本变更履历_
<details>
<summary style="padding-left: 1.6em;"><em>点此展开显示</em></summary>

- ### _V 2.0.0_ 解决ISSUE：[SatenShiroya/astrbot_plugin_llm_qqgroupTools#5](https://github.com/SatenShiroya/astrbot_plugin_llm_qqgroupTools/issues/5)  
  - 新增设置群聊名称功能
  - 新增获取群精华API，以及通过引用或者描述内容的方式来取消群精华消息的功能
  - 新增修改群成员头衔的功能
  - 新增通过引用来撤回消息的功能
  - 新增@全体成员 的功能，单纯的@或者@后让bot附上理由都可以

- ### _V 1.4.0_
  - 优化代码结构，修复原本LLM调用工具，结果直接发送给用户而未返回给LLM的问题
  - 去除了工具调用后是否返回信息的配置开关，因为LLM收到工具调用结果后会触发回复
  
- ### _V 1.3.0_
  - 新增自主禁言工具'set_group_ban_byself'，已修复原本失效的自主禁言功能。需要用户在AI人格设定中强调和原本禁言功能的区别和使用场景。
  - 新增功能使用反馈开关，用户可以自行决定AI成功使用功能后是否进行反馈，但功能使用失败时依旧会进行反馈。

- ### _V 1.2.0_
  - 由于Astrbot更新导致AI自主禁言失效，这边新增权限验证开关来最大限度还原原本的效果表现
  
- ### _V 1.1.3_
  - 新增点赞用户功能，非管理员也可用
  - 新增设精功能，需要引用消息

- ### _V 1.1.2_
  - 新增发布群公告功能

- ### _V 1.1.1_
  - 新增小版本号
  - 新增允许群聊管理和群主使唤bot的功能开关
  - 用yield重新编写了函数返回
  - 重新构建以及封装函数使得代码更美观

- ### _V 1.1_
  - 新增设置群成员名片功能；
  - 新增处理失败抛出异常；
  - 错误返回去除user_id内容，提高安全性；

- ### _V 1.0_
  - 首次修改发布

</details>

## 🔗 _相关链接_

- 机器人框架：[AstrBot 官方文档](https://astrbot.app)
- 客户端使用：[Napcat 官方文档](https://napcat.napneko.icu/)
- 初期参考项：[**ctrlkk**](https://github.com/ctrlkk/astrbot_plugin_admin_tools)

## 👥 _贡献指南_

- ⭐️&nbsp; Star 这个项目！（点右上角的星星，感谢支持！）
- 🐞&nbsp; 提交 Issue 报告问题
- 🔧&nbsp; 提交 Pull Request 改进代码
- 🧠&nbsp; 提出新功能建议