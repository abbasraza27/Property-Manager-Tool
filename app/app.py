import reflex as rx
from app.states.state import PropertyManagementState
from app.components.sidebar import sidebar
from app.components.dashboard import dashboard_content
from app.components.units import units_content
from app.components.tenants import tenants_content
from app.components.maintenance import maintenance_content


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.match(
                PropertyManagementState.active_section,
                ("dashboard", dashboard_content()),
                ("units", units_content()),
                ("tenants", tenants_content()),
                ("maintenance", maintenance_content()),
                rx.el.div("Select a section"),
            ),
            class_name="flex-1 h-screen overflow-y-auto bg-gray-50",
        ),
        class_name="flex font-['Lato'] bg-white text-gray-800",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)