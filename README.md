# AstrBot Admin Tools Plugin

- 这是一个 AstrBot 管理工具插件，使LLM能自主或听从管理员命令管理群聊
- 推荐在人格提示词中暗示AI本身有相应的功能，以便更好使用

## 功能

### 群聊管理
- **set_group_ban**: 群聊禁言用户
- **set_group_kick**: 群聊踢出用户
- **set_group_whole_ban**：群聊全群禁言
- **set_group_card**：设置群成员名片
- **get_group_members_info**：获取群成员信息

## 版本变更履历

## V1.1.1
 - 新增小版本号
 - 新增允许群聊管理和群主使唤bot的功能开关
 - 用yield重新编写了函数返回
 - 重新构建以及封装函数使得代码更美观

## V1.1
- 新增设置群成员名片功能；
- 新增处理失败抛出异常；
- 错误返回去除user_id内容，提高安全性；

## V1.0
- 首次修改发布

参考用户**ctrlkk**项目制作：https://github.com/ctrlkk/astrbot_plugin_admin_tools
