# permission_utils.py

from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from typing import Tuple

async def check_group_and_permission(
    event: AiocqhttpMessageEvent,
    allow_groupadmin_use: bool,
    operator_name: str
) -> Tuple[bool, str | None]:
    """
    检查当前是否在群聊中，并验证操作者是否具有执行管理操作的权限。

    Returns:
        (has_permission: bool, error_message: str | None)
        - 如果有权限，返回 (True, None)
        - 如果无权限或不在群聊，返回 (False, "错误信息")
    """
    group_id = event.get_group_id()
    if not group_id:
        return False, "此操作仅可在群聊中进行。"

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
        except Exception:
            pass  # 获取失败视为无权限

    if not has_permission and event.is_admin():
        has_permission = True

    if not has_permission:
        return False, f"用户 {operator_name} 权限不足"

    return True, None