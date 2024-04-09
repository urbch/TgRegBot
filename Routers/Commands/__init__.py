__all__ = ("router",)

from aiogram import Router #commit

from .base_commands import router as base_commands_router
from .user_commands import router as user_commands_router
from .reg_handler import router as reg_handler_router

router = Router(name=__name__)

router.include_routers(base_commands_router, user_commands_router, reg_handler_router)