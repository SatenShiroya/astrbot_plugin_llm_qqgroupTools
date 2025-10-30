# permissions_utils.py
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from astrbot.api.event import MessageEventResult
from typing import AsyncGenerator

async def check_group_and_permission(
    event: AiocqhttpMessageEvent,
    allow_groupadmin_use: bool,
    operator_name: str
) -> AsyncGenerator[MessageEventResult, None]:
    """
    检查当前是否在群聊中，并验证操作者是否具有执行管理操作的权限。
    
    权限来源：
    1. 如果 allow_groupadmin_use 开启，则群主或管理员有权限。
    2. 机器人管理员始终有权限。
    
    Args:
        event: 消息事件对象
        allow_groupadmin_use: 是否允许群管理员使用此功能
        operator_name: 操作者的昵称（用于返回错误信息）

    Yields:
        MessageEventResult 如果不在群聊或无权限，则返回相应提示并终止。
    """
    group_id = event.get_group_id()
    if not group_id:
        yield event.plain_result("此操作仅可在群聊中进行。")
        return

    operator_user_id = event.get_sender_id()
    has_permission = False

    if allow_groupadmin_use:
        try:
            group_member_info = await event.bot.get_group_member_info(
                group_id=group_id,
                user_id=operator_user_id
            )
            role = group_member_info.get('role', 'member')
            if role in ['owner', 'admin']:
                has_permission = True
        except Exception as e:
            # 获取成员信息失败时，视为无权限（防止误判）
            pass

    # 如果尚未获得权限，检查是否为机器人管理员
    if not has_permission and event.is_admin():
        has_permission = True

    if not has_permission:
        yield event.plain_result(f"用户 {operator_name} 权限不足")
        return

    # 所有校验通过，不 yield 任何内容，表示成功