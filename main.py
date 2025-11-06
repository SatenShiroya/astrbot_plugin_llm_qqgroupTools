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
    "astrbot_plugin_llm_qqgroupTools", "SatenShiroya", "允许LLM自主管理群聊", "v1.1.2"
)
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.data_dir = StarTools.get_data_dir()

        # 开启/关闭踢人功能
        self.open_kick_user = config.get("open_kick_user",False)
        # 允许群主或管理员使用机器人管理功能
        self.allow_groupadmin_use = config.get("allow_groupadmin_use",False)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

    @filter.llm_tool(name="set_essence_msg")
    async def set_essence_msg(self, event: AiocqhttpMessageEvent):
        """将引用消息添加到群精华"""
        first_seg = event.get_messages()[0]
        if isinstance(first_seg, Reply):
            await event.bot.set_essence_msg(message_id=int(first_seg.id))
            await event.send(event.plain_result("已设为精华消息"))
            event.stop_event()
        else:
            await event.send(event.plain_result("请引用要设置为精华的消息"))
            event.stop_event()

    @filter.llm_tool(name="set_group_ban")
    async def set_group_ban(
        self, event: AiocqhttpMessageEvent, user_id: str, duration: int, user_name: str
    ) -> MessageEventResult:
        """
        在群聊中禁言某用户。被禁言的用户在禁言期间将无法发送消息。
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
            
            # 检查是否在群聊中以及操作者权限
            async for result in check_group_and_permission(event, self.allow_groupadmin_use, operator_name):
                yield result
                return

            # 对目标用户执行禁言操作
            await event.bot.set_group_ban(
                group_id=group_id, 
                user_id=target_user_id,  # 对目标用户执行禁言
                duration=duration, 
                self_id=self_id
            )

            logger.info(f"用户：{target_user_id}在群聊中被：{operator_name}执行禁言{duration}秒")
            yield event.plain_result(f"用户 {target_user_name} 已被禁言。")
            return
        except Exception as e:
            logger.error(f"禁言用户 {target_user_id} 失败: {e}")
            yield event.plain_result(f"操作失败：无法禁言用户 {target_user_name}。可能的原因是权限不足或API错误。")
            return


    @filter.llm_tool(name="set_group_kick")
    async def set_group_kick(
        self, event: AiocqhttpMessageEvent, user_id: str, user_name: str
    ) -> MessageEventResult:
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
                yield event.plain_result("当前未开启踢人功能，无法执行该操作。")
                return
            
            # 检查是否在群聊中以及操作者权限
            async for result in check_group_and_permission(event, self.allow_groupadmin_use, operator_name):
                yield result
                return
            
            await event.bot.set_group_kick(
                group_id=group_id,
                user_id=target_user_id,
                reject_add_request=False,
                self_id=self_id,
            )
            logger.info(f"用户：{user_id}在群聊中被：{self_id}踢出")
            yield event.plain_result(f"用户 {target_user_name} 已被踢出群聊。")
            return
        except Exception as e:    
            logger.error(f"踢出用户 {user_id} 失败: {e}")
            yield event.plain_result(f"操作失败：无法踢出用户 {target_user_name}。可能的原因是功能未开启或权限不足或API错误。")
            return

    @filter.llm_tool(name="set_group_whole_ban")
    async def set_group_whole_ban(
        self, event: AiocqhttpMessageEvent, enable: bool
    ) -> MessageEventResult:
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
            
            # 检查是否在群聊中以及操作者权限
            async for result in check_group_and_permission(event, self.allow_groupadmin_use, operator_name):
                yield result
                return
            
            await event.bot.set_group_whole_ban(
                group_id=group_id,
                enable=enable,
                self_id=self_id,
            )

            logger.info(f"已{action_text}全群禁言")
            yield event.plain_result(f"已{action_text}全群禁言。")
            return
        except Exception as e:    
            logger.error(f"{action_text}全群禁言，失败: {e}")
            yield event.plain_result(f"操作失败：{action_text}全群禁言。可能的原因是权限不足或API错误。")
            return

    @filter.llm_tool(name="set_group_card")
    async def set_group_card(
        self, event: AiocqhttpMessageEvent, user_id: str, card: str
    ) -> MessageEventResult:
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
            
            # 检查是否在群聊中以及操作者权限
            async for result in check_group_and_permission(event, self.allow_groupadmin_use, operator_name):
                yield result
                return
            
            await event.bot.set_group_card(
                group_id=group_id,
                self_id=self_id,
                user_id=user_id,
                card=card,
            )
            logger.info(f"用户：{user_id}的昵称已修改为：{card}")
            yield event.plain_result(f"用户：{user_id}的昵称被修改为：{card}")
            return
        except Exception as e:    
            logger.error(f"用户：{user_id}的昵称修改，失败: {e}")
            yield event.plain_result(f"操作失败：用户：{user_id}的昵称修改。可能的原因是权限不足或API错误。")
            return

    @filter.llm_tool(name="send_group_notice")
    async def send_group_notice(
        self, event: AiocqhttpMessageEvent, content: str
    ) -> MessageEventResult:
        """
        发布一条群公告
        Args:
            content(string): 要发送的群公告内容
        """
        try:
            group_id = event.get_group_id()
            operator_name = event.get_sender_name()
            # 检查是否在群聊中以及操作者权限
            async for result in check_group_and_permission(event, self.allow_groupadmin_use, operator_name):
                yield result
                return
            
            await event.bot._send_group_notice(
                group_id=group_id,
                content=content,
            )
            logger.info(f"群公告已发布：{content}")
            yield event.plain_result(f"群公告已发布")
            return
        except Exception as e:    
            logger.error(f"群公告发布，失败: {e}")
            yield event.plain_result(f"群公告发布失败。可能的原因是权限不足或API错误。")
            return

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

    @filter.command("测试群成员", alias={"test_members"})
    async def test_group_members(self, event: AstrMessageEvent) -> AsyncGenerator[MessageEventResult, None]:
        """测试指令：手动触发群成员查询并显示格式化结果（限制显示前300个成员）"""
        if not event.get_group_id():
            yield event.plain_result("此指令仅在群聊中可用")
            return
        start_time = time.time()

        logger.info("手动触发群成员查询测试")
        result_str = await self.get_group_members(event)
        
        try:
            result_data = json.loads(result_str)
            if "error" in result_data:
                yield event.plain_result(f"查询失败: {result_data['error']}")
                return
            
            members = result_data.get("members", [])
            if not members:
                yield event.plain_result("群成员列表为空")
                return
            
            # 限制显示数量，避免消息过长
            display_limit = 300
            display_members = members[:display_limit]
            elapsed_time = time.time() - start_time

            # 格式化输出：群昵称(用户名)(userid)[身份]
            formatted_members = []
            for member in display_members:
                display_name = member.get("display_name", "未知")
                username = member.get("username", "未知")  # 新增：显示用户名
                user_id = member.get("user_id", "未知")
                role = member.get("role", "member")
                
                # 角色中文化
                role_map = {
                    "owner": "群主",
                    "admin": "管理", 
                    "member": "成员"
                }
                role_cn = role_map.get(role, role)
                
                formatted_members.append(f"{display_name}({username})({user_id})[{role_cn}]")
            
            # 构建结果消息
            result_text = f"该命令仅用于测试工具可用性\n工具调用耗时 {elapsed_time:.2f}s\n\n群成员信息 (共{len(members)}人，显示前{len(display_members)}人):\n" + "\n".join(formatted_members)
            
            if len(members) > display_limit:
                result_text += f"\n\n注：群成员过多，仅显示前{display_limit}人。该命令仅用于测试工具可用性\n工具调用耗时 {elapsed_time:.2f}s"
            
            yield event.plain_result(result_text)
            
        except json.JSONDecodeError:
            yield event.plain_result(f"数据解析失败，原始数据：\n{result_str}")
