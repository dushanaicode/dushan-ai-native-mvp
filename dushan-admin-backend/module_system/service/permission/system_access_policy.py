from framework.starter_di.public import Inject, service
from framework.starter_security.public import SecurityContext, SecurityErrorCodes, SecurityException
from module_system.config.system_settings import SystemSettings
from module_system.dal.mapper.permission.menu_mapper import MenuMapper


@service()
class SystemAccessPolicy:
    OWNER_PAGES = frozenset({"system/menu/index", "infra/redis-cache/index"})
    settings: SystemSettings = Inject()
    security: SecurityContext = Inject()
    menus: MenuMapper = Inject()

    def is_owner(self, user_id: int | str) -> bool:
        return str(user_id) == self.settings.owner_user_id

    def is_current_owner(self) -> bool:
        return self.is_owner(self.security.require().account_id)

    def require_owner(self) -> None:
        if not self.is_current_owner():
            raise SecurityException(
                SecurityErrorCodes.DENIED, detail="仅作者超级管理员可执行此操作"
            )

    def protect_owner_account(self, user_id: int | str) -> None:
        if self.is_owner(user_id):
            self.require_owner()

    async def menu_ids(self, user_id: int | str) -> set[int]:
        """普通管理员只能获授可委派菜单，平台维护入口始终由实例所有者操作。"""
        menus = await self.menus.select_list()
        if self.is_owner(user_id):
            return {menu.id for menu in menus}
        return {
            menu.id
            for menu in menus
            if not any(character in menu.permission for character in "*?[")
            and menu.component not in self.OWNER_PAGES
            and not menu.permission.startswith("system:permission:menu:")
            and not (
                menu.permission.startswith("infra:cache:")
                and menu.permission != "infra:cache:get-monitor-info"
            )
        }
