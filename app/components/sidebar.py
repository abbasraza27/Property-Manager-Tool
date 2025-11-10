import reflex as rx
from app.states.state import PropertyManagementState

NAV_ITEMS = [
    {"label": "Dashboard", "icon": "layout-grid", "section": "dashboard"},
    {"label": "Units", "icon": "building", "section": "units"},
    {"label": "Tenants", "icon": "users", "section": "tenants"},
    {"label": "Maintenance", "icon": "wrench", "section": "maintenance"},
]


def nav_item(item: dict) -> rx.Component:
    return rx.el.a(
        rx.icon(item["icon"], size=20),
        rx.el.span(item["label"], class_name="font-medium"),
        on_click=lambda: PropertyManagementState.set_active_section(item["section"]),
        class_name=rx.cond(
            PropertyManagementState.active_section == item["section"],
            "flex items-center gap-3 rounded-lg bg-gray-100 px-3 py-2 text-purple-600 transition-all hover:text-purple-700 cursor-pointer",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 cursor-pointer",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("home", size=28, class_name="text-purple-600"),
                    rx.el.h3("PropManage", class_name="text-xl font-bold"),
                    class_name="flex items-center gap-2",
                ),
                class_name="flex h-16 items-center border-b px-6",
            ),
            rx.el.nav(
                rx.foreach(NAV_ITEMS, nav_item),
                class_name="flex-1 flex flex-col gap-1 p-4 text-sm font-medium",
            ),
            class_name="flex-1 overflow-auto",
        ),
        class_name="h-screen w-64 border-r bg-white flex flex-col",
    )