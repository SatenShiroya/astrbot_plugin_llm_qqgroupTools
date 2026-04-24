import json, time
from astrbot.core.message.components import Reply
from typing import List, Dict, Any, AsyncGenerator, Optional
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from astrbot.core.star.star_tools import StarTools

from .core.permission_utils import check_group_and_permission

@register(
    "astrbot_plugin_llm_qqgroupTools", "SatenShiroya", "允许LLM自主管理群聊", "v2.3.0"
)
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.data_dir = StarTools.get_data_dir()

        # 开启/关闭踢人功能
        self.open_kick_user = config.get("open_kick_user",False)
        # 允许群主或管理员使用机器人管理功能
        self.allow_groupadmin_use = config.get("allow_groupadmin_use",False)
        # 权限验证开关
        self.Permission_verification = config.get("Permission_verification",True)
        # 结果反馈开关(已去除)
        #self.Result_response_switch = config.get("Result_response_switch",True)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

    @filter.llm_tool(name="set_essence_msg")
    async def set_essence_msg(
        self, event: AiocqhttpMessageEvent
        ) -> dict:
        """将引用消息添加到群精华"""
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()

            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
                
            first_seg = event.get_messages()[0]
            if isinstance(first_seg, Reply):
                await event.bot.set_essence_msg(message_id=int(first_seg.id))
                msg = f"已将消息 {first_seg.id} 添加到群精华"
                return {
                    "status": "success",
                    "message": msg
                }
            else:
                msg = "请引用要设置为精华的消息"
                return {
                    "status": "error",
                    "message": msg
                }
        except Exception as e:    
            logger.error(f"群精华消息添加，失败: {e}")
            msg = f"群精华消息添加失败。可能的原因是权限不足、消息ID错误或API错误。"
            return {
                "status": "error",
                "message": msg
            }
        
    @filter.llm_tool(name="delete_essence_msg")
    async def delete_essence_msg(
        self, event: AiocqhttpMessageEvent
        ) -> dict:
        """通过引用消息的方式将某条消息从群精华中移除"""
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()

            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
            
                
            first_seg = event.get_messages()[0]
            if isinstance(first_seg, Reply):
                await event.bot.delete_essence_msg(message_id=int(first_seg.id))
                msg = f"已将消息 {first_seg.id} 从群精华中移除"
                return {
                    "status": "success",
                    "message": msg
                }
            else:
                msg = "请引用要移除的精华消息"
                return {
                    "status": "error",
                    "message": msg
                }
        except Exception as e:    
            logger.error(f"群精华消息移除，失败: {e}")
            msg = f"群精华消息移除失败。可能的原因是权限不足、消息ID错误或API错误。"
            return {
                "status": "error",
                "message": msg
            }

    @filter.llm_tool(name="delete_essence_msg_by_id")
    async def delete_essence_msg_by_id(
        self, event: AiocqhttpMessageEvent,message_id: str
        ) -> dict:
        """
        通过输入消息id参数来将消息从群精华中移除。
        Args:
            message_id(string): 要移除的精华消息的消息ID，必定为一串数字，如(12345678)
        """
        try:
            operator_name = event.get_sender_name()

            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}

            await event.bot.delete_essence_msg(
                message_id=int(message_id)
            )

            logger.info(f"已将消息 {message_id} 从群精华中移除")
            msg = f"已将消息 {message_id} 从群精华中移除"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:
            logger.error(f"群精华消息移除，失败: {e}")
            msg = f"群精华消息移除失败。可能的原因是权限不足、消息ID错误或API错误。"
            return {
                "status": "error",
                "message": msg
            }        
        
    @filter.llm_tool(name="delete_msg")
    async def delete_msg(
        self, event: AiocqhttpMessageEvent
        ) -> dict:
        """撤回所引用的消息"""
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()

            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
                
            first_seg = event.get_messages()[0]
            if isinstance(first_seg, Reply):
                await event.bot.delete_msg(message_id=int(first_seg.id))
                msg = f"已将消息 {first_seg.id} 撤回"
                return {
                    "status": "success",
                    "message": msg
                }
            else:
                msg = "请引用要撤回的消息"
                return {
                    "status": "error",
                    "message": msg
                }
        except Exception as e:    
            logger.error(f"消息撤回，失败: {e}")
            msg = f"消息撤回失败。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }

    @filter.llm_tool(name="send_like")
    async def set_like_to_user(
        self, event: AiocqhttpMessageEvent, user_id: str, times:int
    ) -> dict:
        """
        点赞用户，最大点赞次数为10次。
        Args:
            user_id(string): 要点赞的用户的QQ账号，必定为一串数字，如(12345678)
            times(number): 点赞的次数，最大为10次
        """
        try:
            times = min(max(1, times), 10)
            await event.bot.send_like(
                user_id=user_id,
                times=times,
            )
            logger.info(f"已点赞用户：{user_id}，次数：{times}")
            msg=f"已点赞用户：{user_id}，次数：{times}"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:
            logger.error(f"点赞用户：{user_id}， 失败: {e}")
            msg=f"点赞用户：{user_id}失败。可能的原因是用户ID错误或API错误。"
            return {
                "status": "error",
                "message": msg
            }
        
    @filter.llm_tool(name="set_group_ban_byself")
    async def set_group_ban_byself(
        self, event: AiocqhttpMessageEvent, user_id: str, duration: int, user_name: str
    ) -> dict:
        """
        自主禁言功能，当机器人自主决定需要在群聊中禁言指定用户时使用。被禁言的用户在禁言期间将无法发送消息。
        Args:
            user_id(string): 要禁言的用户的QQ账号，必定为一串数字，如(12345678)
            user_name(string): 要禁言的用户的QQ昵称，如(小明)
            duration(number): 禁言持续时间（以秒为单位），必须是 60 的倍数（例如：60、180）。设置为 0 即解除禁言
        """
        try:
            group_id = event.get_group_id()
            self_id = event.get_self_id()
            operator_name = event.get_sender_name()
            target_user_id = user_id  # 被禁言的目标用户ID
            target_user_name = user_name  # 被禁言的目标用户昵称
            duration = (duration // 60) * 60
            # 对目标用户执行禁言操作
            await event.bot.set_group_ban(
                group_id=int(group_id), 
                user_id=int(target_user_id),  # 对目标用户执行禁言
                self_id=int(self_id),
                duration=duration
            )

            logger.info(f"BOT自主决定：禁言用户 {target_user_name} ({target_user_id}) {duration}秒")
            msg = f"BOT自主决定：禁言用户 {target_user_name} ({target_user_id}) {duration}秒"
            return{
                "status": "success",
                "message": msg
            }
        except Exception as e:
            logger.error(f"禁言用户 {target_user_id} 失败: {e}")
            msg = f"操作失败：无法禁言用户 {target_user_name}。可能的原因是权限不足或API错误。"
            return{
                "status": "error",
                "message": msg
            }    

    @filter.llm_tool(name="set_group_ban")
    async def set_group_ban(
        self, event: AiocqhttpMessageEvent, user_id: str, duration: int, user_name: str
    ) -> dict:
        """
        当需要听从机器人管理员或者群聊管理员的指令，在群聊中禁言指定用户时使用。被禁言的用户在禁言期间将无法发送消息。
        Args:
            user_id(string): 要禁言的用户的QQ账号，必定为一串数字，如(12345678)
            user_name(string): 要禁言的用户的QQ昵称，如(小明)
            duration(number): 禁言持续时间（以秒为单位），必须是 60 的倍数（例如：60、180）。设置为 0 即解除禁言
        """
        try:
            group_id = event.get_group_id()
            self_id = event.get_self_id()
            operator_name = event.get_sender_name()
            target_user_id = user_id  # 被禁言的目标用户ID
            target_user_name = user_name  # 被禁言的目标用户昵称
            duration = (duration // 60) * 60
            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
            # 对目标用户执行禁言操作
            await event.bot.set_group_ban(
                group_id=int(group_id), 
                user_id=int(target_user_id),  # 对目标用户执行禁言
                self_id=int(self_id),
                duration=duration
            )

            logger.info(f"用户：{target_user_id}在群聊中被：{operator_name}执行禁言{duration}秒")
            msg = f"用户 {target_user_name} 已被{operator_name}执行禁言{duration}秒。"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:
            logger.error(f"{operator_name}禁言用户 {target_user_id} 失败: {e}")
            msg = f"操作失败：{operator_name}无法禁言用户 {target_user_name}。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }

    @filter.llm_tool(name="set_group_kick")
    async def set_group_kick(
        self, event: AiocqhttpMessageEvent, user_id: str, user_name: str
    ) -> dict:
        """
        将用户从群聊中移除。
        Args:
            user_id(string): 要踢出的用户的QQ账号，必定为一串数字，如(12345678)
            user_name(string): 要踢出的用户的QQ昵称，如(小明)
        """
        try:
            group_id = event.get_group_id()
            self_id = event.get_self_id()
            operator_name = event.get_sender_name()
            target_user_id = user_id  # 被踢出的目标用户ID
            target_user_name = user_name  # 被踢出的目标用户昵称
            if not self.open_kick_user:
                msg = f"操作失败：踢人功能未开启，无法踢出用户 {target_user_name}。"
                logger.error(msg)
                return {
                    "status": "error",
                    "message": msg
                }
            
            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
            
            await event.bot.set_group_kick(
                group_id=int(group_id),
                user_id=int(target_user_id),
                reject_add_request=False,
                self_id=int(self_id),
            )
            logger.info(f"用户：{target_user_id}{target_user_name}已在群聊中被bot踢出")
            msg = f"用户 {target_user_name} ({target_user_id}) 群聊中被bot踢出。"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:    
            logger.error(f"踢出用户 {target_user_id} {target_user_name}失败: {e}")
            msg = f"操作失败：无法踢出用户 {target_user_name} ({target_user_id})。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }
        
    @filter.llm_tool(name="set_group_whole_ban")
    async def set_group_whole_ban(
        self, event: AiocqhttpMessageEvent, enable: bool
    ) -> dict:
        """
        全体禁言，即禁言整个群聊。
        Args:
            enable(boolean): 设置为true时开启全体禁言，设置为false时关闭全群禁言，布尔类型参数
        """
        action_text = "开启" if enable else "关闭"
        try:
            group_id = event.get_group_id()
            self_id = event.get_self_id()
            operator_name = event.get_sender_name()
            
            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
            
            await event.bot.set_group_whole_ban(
                group_id=int(group_id),
                enable=enable,
                self_id=int(self_id),
            )

            logger.info(f"已{action_text}全群禁言")
            msg = f"已{action_text}全群禁言"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:    
            logger.error(f"{action_text}全群禁言，失败: {e}")
            msg = f"操作失败：无法{action_text}全群禁言。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }

    @filter.llm_tool(name="set_group_card")
    async def set_group_card(
        self, event: AiocqhttpMessageEvent, user_id: str, card: str
    ) -> dict:
        """
        修改或取消群聊用户的群昵称
        Args:
            user_id(string): 要修改昵称的用户的QQ账号，必定为一串数字，如(12345678)
            card(string): 要修改的昵称，如果为空值则取消群昵称
        """
        try:
            group_id = event.get_group_id()
            self_id = event.get_self_id()
            operator_name = event.get_sender_name()
            
            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
            
            await event.bot.set_group_card(
                group_id=int(group_id),
                self_id=int(self_id),
                user_id=int(user_id),
                card=card,
            )
            logger.info(f"用户：{user_id}的昵称已修改为：{card}")
            
            msg = f"用户 {user_id} 的昵称已修改为：{card}" if card else f"用户 {user_id} 的群昵称已取消"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:    
            logger.error(f"用户：{user_id}的昵称修改，失败: {e}")
            msg = f"操作失败：用户：{user_id}的昵称修改。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }
    
    @filter.llm_tool(name="set_group_special_title")
    async def set_group_special_title(
        self, event: AiocqhttpMessageEvent, user_id: str, special_title: str
    ) -> dict:
        """
        修改或取消群聊用户的群头衔
        Args:
            user_id(string): 要修改头衔的用户的QQ账号，必定为一串数字，如(12345678)
            special_title(string): 要修改的头衔，如果为空值则取消群头衔
        """
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()
            operator_user_id = event.get_sender_id()
            self_id = event.get_self_id()

            if not group_id:
                msg = f"此操作仅可在群聊中进行。"
                return {
                    "status": "error",
                    "message": msg
                }

            bot_member_info = await event.bot.get_group_member_info(
                group_id=group_id,
                user_id=self_id
            )
            bot_role = bot_member_info.get('role', 'member')
            if bot_role not in ['owner']:
                msg = f"机器人权限不足，无法执行操作。请确保机器人在群内具有群主权限。"
                return {
                    "status": "error", 
                    "message": msg
                }

            if self.Permission_verification:
                has_permission = False
                if self.allow_groupadmin_use:
                    try:
                        group_member_info = await event.bot.get_group_member_info(
                            group_id=group_id,
                            user_id=operator_user_id
                        )
                        role = group_member_info.get('role', 'member')
                        if role in ['owner', 'admin']:
                            has_permission = True
                    except Exception:
                            has_permission = False  # 获取失败视为无权限

                if not has_permission and event.is_admin():
                    has_permission = True
                
                if not has_permission:
                    # 检查操作者是否在给自己设置头衔
                    if operator_user_id == user_id:
                        # 注意：这里不需要额外权限，因为是在改自己的头衔
                        has_permission = True
                        logger.info(f"用户 {operator_name} 正在为自己设置头衔（自操作豁免）")
                    else:
                        # 既不是管理员，也不是给自己改，拒绝
                        msg = f"用户 {operator_name} 权限不足，只能修改自己的头衔。"
                        return {
                            "status": "error", 
                            "message": msg
                        }
            
            await event.bot.set_group_special_title(
                group_id=int(group_id),
                user_id=int(user_id),
                special_title=special_title,
            )
            logger.info(f"用户：{user_id}的头衔已修改为：{special_title}")
            
            msg = f"用户 {user_id} 的头衔已修改为：{special_title}" if special_title else f"用户 {user_id} 的群头衔已取消"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:    
            logger.error(f"用户：{user_id}的头衔修改，失败: {e}")
            msg = f"操作失败：用户：{user_id}的头衔修改。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }

    @filter.llm_tool(name="set_group_admin")
    async def set_group_admin(
        self, event: AiocqhttpMessageEvent, user_id: str, enable: bool
    ) -> dict:
        """
        设置或取消群聊用户的群管理员权限
        Args:
            user_id(string): 要修改管理员权限的用户的QQ账号，必定为一串数字，如(12345678)
            enable(bool): 是否启用管理员权限，设置为true时授予管理员权限，设置为false时取消管理员权限，布尔类型参数
        """
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()
            operator_user_id = event.get_sender_id()
            self_id = event.get_self_id()

            if not group_id:
                msg = f"此操作仅可在群聊中进行。"
                return {
                    "status": "error",
                    "message": msg
                }

            bot_member_info = await event.bot.get_group_member_info(
                group_id=group_id,
                user_id=self_id
            )
            bot_role = bot_member_info.get('role', 'member')
            if bot_role not in ['owner']:
                msg = f"机器人权限不足，无法执行操作。请确保机器人在群内具有群主权限。"
                return {
                    "status": "error", 
                    "message": msg
                }

            if self.Permission_verification:
                has_permission = False
                if self.allow_groupadmin_use:
                    try:
                        group_member_info = await event.bot.get_group_member_info(
                            group_id=group_id,
                            user_id=operator_user_id
                        )
                        role = group_member_info.get('role', 'member')
                        if role in ['owner', 'admin']:
                            has_permission = True
                    except Exception:
                            has_permission = False  # 获取失败视为无权限

                if not has_permission and event.is_admin():
                    has_permission = True

                if not has_permission:
                    msg = f"用户 {operator_name} 权限不足，无法执行操作。请确保操作者在群内具有群主或管理员权限。"
                    return {
                        "status": "error",
                        "message": msg
                    }
            
            await event.bot.set_group_admin(
                group_id=int(group_id),
                user_id=int(user_id),
                enable=enable
            )
            logger.info(f"用户：{user_id}的管理员权限已修改为：{enable}")
            
            msg = f"用户 {user_id} 的管理员权限已修改为：{enable}"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:    
            logger.error(f"用户：{user_id}的管理员权限修改，失败: {e}")
            msg = f"操作失败：用户：{user_id}的管理员权限修改。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }
    
    @filter.llm_tool(name="send_group_at_all")
    async def send_group_at_all(self, event: AstrMessageEvent, reason: str) -> dict:
        """
        用于向群聊发送 @全体成员 的指令。
        Args:
            reason(string): 发送 @全体成员 消息的理由，LLM需要将理由作为参数传入，以便在发送消息时附加说明,留空则不附加理由。
        """
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()
            if not group_id:
                return {"status": "error", "message": "当前环境不是群聊"}

            if not isinstance(event, AiocqhttpMessageEvent):
                return {"status": "error", "message": f"不支持的平台: {event.get_platform_name()}"}

            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}

            message_data = [
                {
                    "type": "at", # 消息类型：艾特
                    "data": {
                        "qq": "all", # 关键点：这里是字符串 "all"，不是数字
                        "name": "全体成员" # 备用显示名称
                    }
                },
                {
                "type": "text",
                "data": {
                    "text": f" {reason}" if reason else "" # 如果有理由则添加到消息中，前面加个空格分隔
                }
            }
            ]

            await event.bot.send_group_msg(
                group_id=group_id,
                message=message_data # 直接传入构造好的数组
            )

            reason_log = reason if reason else "未填写理由，只是单纯的 @全体成员"
            
            logger.info(f"已向群 {group_id} 发送 @全体成员 消息，理由：{reason_log}")
            
            msg = f"已向群 {group_id} 发送 @全体成员 消息，理由：{reason_log}"
            
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:    
            logger.error(f"发送 @全体成员 消息，失败: {e}")
            msg = f"发送 @全体成员 消息失败。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }

    @filter.llm_tool(name="send_group_notice")
    async def send_group_notice(
        self, event: AiocqhttpMessageEvent, content: str
    ) -> dict:
        """
        发布一条群公告
        Args:
            content(string): 要发送的群公告内容
        """
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()

            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
            
            await event.bot._send_group_notice(
                group_id=int(group_id),
                content=content,
            )
            logger.info(f"群公告已发布：{content}")
            msg = f"群公告已发布：{content}"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:    
            logger.error(f"群公告发布，失败: {e}")
            msg = f"群公告发布失败。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }

    @filter.llm_tool(name="delete_group_notice")
    async def delete_group_notice(
        self, event: AiocqhttpMessageEvent, notice_id: str
    ) -> dict:
        """
        删除一条群公告
        Args:
            notice_id(string): 要删除的群公告ID
        """
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()

            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}

            await event.bot._del_group_notice(
                group_id=int(group_id),
                notice_id=notice_id,
            )
            logger.info(f"群公告已删除：{notice_id}")
            msg = f"群公告已删除：{notice_id}"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:
            logger.error(f"群公告删除，失败: {e}")
            msg = f"群公告删除失败。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }
        
    @filter.llm_tool(name="set_group_name")
    async def set_group_name(
        self, event: AiocqhttpMessageEvent, group_name: str
    ) -> dict:
        """
        修改群名称
        Args:
            group_name(string): 要修改的群名称
        """
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()

            if self.Permission_verification:
                has_perm, error_msg = await check_group_and_permission(
                    event, self.allow_groupadmin_use, operator_name
                )
                if not has_perm:
                    return {"status": "error", "message": error_msg}
            
            await event.bot.set_group_name(
                group_id=int(group_id),
                group_name=group_name,
            )
            logger.info(f"群名称已修改：{group_name}")
            msg = f"群名称已修改为：{group_name}"
            return {
                "status": "success",
                "message": msg
            }
        except Exception as e:    
            logger.error(f"群名称修改，失败: {e}")
            msg = f"群名称修改失败。可能的原因是权限不足或API错误。"
            return {
                "status": "error",
                "message": msg
            }

    @filter.llm_tool(name="get_group_members_info")
    async def get_group_members(self, event: AstrMessageEvent) -> str:
        """
        1.当需要在QQ群聊中进行禁言/解除禁言/踢出用户等操作时，先调用此工具查询群成员信息，然后再执行对应的禁言/解除禁言/踢出用户等请求。
        2.需要知道群里是否有特定成员时，调用此工具。
        3.其中display_name是“群昵称”，username是用户“QQ名”，user_id是用户“QQ账号”
        """
        start_time = time.time()
        
        try:
            group_id = event.get_group_id()
            if not group_id:
                logger.info("用户在非群聊环境中调用群成员查询工具")
                return json.dumps({"error": "这不是群聊"})
            
            if not isinstance(event, AiocqhttpMessageEvent):
                logger.info(f"不支持的平台: {event.get_platform_name()}")
                return json.dumps({"error": f"此功能仅支持QQ群聊(aiocqhttp平台)，当前平台为 {event.get_platform_name()}"})

            # 从API获取
            members_info = await self._get_group_members_internal(event)
            if not members_info:
                logger.info(f"无法获取群 {group_id} 的成员信息")
                return json.dumps({"error": "获取群成员信息失败，可能是权限不足或网络问题"})
            
            processed_members = [
                {
                    "user_id": str(member.get("user_id", "")),
                    "display_name": member.get("card") or member.get("nickname") or f"用户{member.get('user_id')}",
                    "username": member.get("nickname") or f"用户{member.get('user_id')}",  # 新增：用户的QQ昵称
                    "role": member.get("role", "member")
                }
                for member in members_info if member.get("user_id")
            ]
            
            group_info = {
                "group_id": group_id,
                "member_count": len(processed_members),
                "members": processed_members
            }
            
            elapsed_time = time.time() - start_time
            logger.info(f"成功获取群 {group_id} 的 {len(processed_members)} 名成员信息，耗时 {elapsed_time:.2f}s")
            
            return json.dumps(group_info, ensure_ascii=False, indent=2)
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.info(f"获取群成员信息时发生错误: {e}，耗时 {elapsed_time:.2f}s")
            return json.dumps({"error": f"获取群成员信息时发生内部错误: {str(e)}"})

    @filter.llm_tool(name="get_essence_msg_list")
    async def get_essence_msg_list(self, event: AstrMessageEvent) -> str:
        """
        1. 当用户需要查询群聊中的“精华消息”记录时调用此工具。
        2. 返回的数据包含消息ID、发送者、操作者、操作时间以及消息内容。
        3. 注意：此接口仅支持QQ群聊(aiocqhttp平台)。
        """
        start_time = time.time()
        
        try:
            group_id = event.get_group_id()
            if not group_id:
                logger.info("用户在非群聊环境中调用获取精华消息工具")
                return json.dumps({"error": "这不是群聊，无法获取精华消息"})
            
            if not isinstance(event, AiocqhttpMessageEvent):
                logger.info(f"不支持的平台: {event.get_platform_name()}")
                return json.dumps({"error": f"此功能仅支持QQ群聊(aiocqhttp平台)，当前平台为 {event.get_platform_name()}"})

            # 调用内部API获取原始数据
            raw_response = await self._get_essence_msg_list_internal(event)
            
            if not raw_response:
                logger.info(f"群 {group_id} 暂无精华消息")
                # 返回一个空列表的结构，而不是错误
                return json.dumps({
                    "group_id": group_id,
                    "count": 0,
                    "messages": []
                }, ensure_ascii=False, indent=2)

            # 2. 数据清洗与格式化 (列表推导式)
            processed_messages = [
                {
                    "message_id": msg.get("message_id"),
                    "sender_id": str(msg.get("sender_id")),       # ID转字符串，防止精度丢失
                    "sender_nick": msg.get("sender_nick"),
                    "operator_id": str(msg.get("operator_id")),   # ID转字符串
                    "operator_nick": msg.get("operator_nick"),
                    "operator_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg.get("operator_time"))),
                    "content": msg.get("content")
                }
                for msg in raw_response if msg.get("message_id") and msg.get("sender_id") and msg.get("operator_id")
            ]
            
            # 3. 构建最终响应
            processed_data = {
                "group_id": group_id,
                "count": len(processed_messages),
                "messages": processed_messages
            }
            
            elapsed_time = time.time() - start_time
            logger.info(f"成功获取群 {group_id} 的 {len(processed_messages)} 条精华消息，耗时 {elapsed_time:.2f}s")
            
            return json.dumps(processed_data, ensure_ascii=False, indent=2)
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.info(f"获取精华消息时发生错误: {e}，耗时 {elapsed_time:.2f}s")
            return json.dumps({"error": f"获取精华消息时发生内部错误: {str(e)}"})
    
    @filter.llm_tool(name="get_group_notice")
    async def get_group_notice(self, event: AstrMessageEvent) -> str:
        """
        1. 当用户需要查询群聊中的“群公告”记录时调用此工具。
        2. 返回的数据包含公告ID、发送者ID、发送时间以及公告内容。
        3. 注意：此接口仅支持QQ群聊(aiocqhttp平台)。
        """
        start_time = time.time()
        
        try:
            group_id = event.get_group_id()
            if not group_id:
                logger.info("用户在非群聊环境中调用获取群公告工具")
                return json.dumps({"error": "这不是群聊，无法获取群公告"})
            
            if not isinstance(event, AiocqhttpMessageEvent):
                logger.info(f"不支持的平台: {event.get_platform_name()}")
                return json.dumps({"error": f"此功能仅支持QQ群聊(aiocqhttp平台)，当前平台为 {event.get_platform_name()}"})

            # 调用内部API获取原始数据
            raw_response = await self._get_group_notice(event)

            if not raw_response:
                logger.info(f"群 {group_id} 暂无群公告")
                # 返回一个空列表的结构，而不是错误
                return json.dumps({
                    "group_id": group_id,
                    "count": 0,
                    "messages": []
                }, ensure_ascii=False, indent=2)

            # 2. 数据清洗与格式化 (列表推导式)
            processed_messages = []
            for msg in raw_response:
                if not (msg.get("notice_id") and msg.get("sender_id") and msg.get("publish_time")):
                    continue

                # 处理图片列表
                images = msg.get("message", {}).get("image")
                if isinstance(images, list):
                    image_data = [
                        {
                            "id": img.get("id"),
                            "height": img.get("height"),
                            "width": img.get("width")
                        }
                        for img in images if img.get("id")   # 只保留有效项
                    ]
                else:
                    image_data = []

                processed_messages.append({
                    "notice_id": msg.get("notice_id"),
                    "sender_id": str(msg.get("sender_id")),   # 转为字符串，防止精度丢失
                    "publish_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg.get("publish_time"))),
                    "message": {
                        "text": msg.get("message", {}).get("text", ""),
                        "images": image_data               # 使用 images (复数) 返回列表
                    }
                })
            
            # 3. 构建最终响应
            processed_data = {
                "group_id": group_id,
                "count": len(processed_messages),
                "messages": processed_messages
            }
            
            elapsed_time = time.time() - start_time
            logger.info(f"成功获取群 {group_id} 的 {len(processed_messages)} 条群公告，耗时 {elapsed_time:.2f}s")
            
            return json.dumps(processed_data, ensure_ascii=False, indent=2)
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.info(f"获取群公告时发生错误: {e}，耗时 {elapsed_time:.2f}s")
            return json.dumps({"error": f"获取群公告时发生内部错误: {str(e)}"})


    async def _get_group_members_internal(self, event: AiocqhttpMessageEvent) -> Optional[List[Dict[str, Any]]]:
        """
        内部函数，用于调用API获取群成员列表
        
        Args:
            event: AiocqhttpMessageEvent实例
            
        Returns:
            群成员列表，失败时返回None
        """
        try:
            group_id = event.get_group_id()
            if not group_id:
                return None

            client = event.bot
            params = {"group_id": group_id}
            return await client.api.call_action('get_group_member_list', **params)
        except Exception as e:
            logger.info(f"API调用失败: {e}")
            return None

    async def _get_essence_msg_list_internal(self, event: AiocqhttpMessageEvent) -> Optional[List[Dict[str, Any]]]:
        """
        内部函数，用于调用API获取群精华消息列表
        
        Args:
            event: AiocqhttpMessageEvent实例
            
        Returns:
            精华消息列表，失败时返回None
        """
        try:
            group_id = event.get_group_id()
            if not group_id:
                return None

            client = event.bot

            params = {"group_id": group_id}
               
            return await client.api.call_action('get_essence_msg_list', **params)
        except Exception as e:
            logger.info(f"API调用失败: {e}")
            return None

    async def _get_group_notice(self, event: AiocqhttpMessageEvent) -> Optional[List[Dict[str, Any]]]:
        """
        内部函数，用于调用API获取群公告列表
        
        Args:
            event: AiocqhttpMessageEvent实例
            
        Returns:
            群公告列表，失败时返回None
        """
        try:
            group_id = event.get_group_id()
            if not group_id:
                return None

            client = event.bot

            params = {"group_id": group_id}
               
            return await client.api.call_action('_get_group_notice', **params)
        except Exception as e:
            logger.info(f"API调用失败: {e}")
            return None
