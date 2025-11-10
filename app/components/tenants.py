import reflex as rx
from app.states.state import PropertyManagementState, Tenant


def tenant_card(tenant: Tenant) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={tenant['name']}",
                    class_name="h-12 w-12 rounded-full",
                ),
                rx.el.div(
                    rx.el.h3(tenant["name"], class_name="font-semibold text-lg"),
                    rx.el.p(
                        f"{tenant['property_name']}, Unit {tenant['unit_number']}",
                        class_name="text-sm text-gray-500",
                    ),
                ),
            ),
            rx.el.a(
                rx.icon("file-text", size=16, class_name="mr-2"),
                "View Lease",
                href=tenant["lease_document_url"],
                class_name="inline-flex items-center text-sm font-medium text-purple-600 hover:text-purple-800",
                target="_blank",
            ),
            class_name="flex items-center justify-between",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("mail", size=14, class_name="text-gray-400"),
                rx.el.p(tenant["email"], class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.icon("phone", size=14, class_name="text-gray-400"),
                rx.el.p(tenant["phone"], class_name="text-sm text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col sm:flex-row gap-4 mt-4 pt-4 border-t",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def tenants_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Tenant Portal", class_name="text-3xl font-bold"),
            rx.el.p(
                "Read-only view of current tenants and their information.",
                class_name="text-gray-500 mt-1",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.foreach(PropertyManagementState.tenants, tenant_card),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        class_name="p-6",
    )