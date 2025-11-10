import reflex as rx
from app.states.state import PropertyManagementState, Property


def metric_card(icon: str, title: str, value: rx.Var, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, size=24, class_name=f"text-{color}-500"),
            class_name=f"p-3 rounded-lg bg-{color}-100 w-fit",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.h4(value, class_name="text-2xl font-bold"),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 p-4 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


def property_status_badge(status: rx.Var) -> rx.Component:
    return rx.match(
        status,
        (
            "occupied",
            rx.el.div(
                "Occupied",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-green-100 text-green-700",
            ),
        ),
        (
            "vacant",
            rx.el.div(
                "Vacant",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-yellow-100 text-yellow-700",
            ),
        ),
        (
            "maintenance",
            rx.el.div(
                "Maintenance",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-blue-100 text-blue-700",
            ),
        ),
        rx.el.div("Unknown"),
    )


def property_card(property: Property) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=property["image_url"],
            height="180px",
            width="100%",
            class_name="object-cover rounded-t-xl",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(property["name"], class_name="font-semibold text-lg"),
                property_status_badge(property["status"]),
                class_name="flex justify-between items-start",
            ),
            rx.el.p(property["address"], class_name="text-sm text-gray-500"),
            rx.el.div(
                rx.icon("users", size=14, class_name="text-gray-500"),
                rx.el.p(
                    f"{property['occupancy'][0]}/{property['occupancy'][1]} Units Occupied",
                    class_name="text-sm text-gray-600",
                ),
                class_name="flex items-center gap-2 mt-2",
            ),
            class_name="p-4 flex flex-col gap-2",
        ),
        class_name="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md transition-shadow",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Dashboard", class_name="text-3xl font-bold mb-6"),
        rx.el.div(
            metric_card(
                "building",
                "Occupancy Rate",
                f"{PropertyManagementState.occupancy_rate.to_string()}%",
                "purple",
            ),
            metric_card(
                "dollar-sign",
                "Monthly Income",
                f"${PropertyManagementState.monthly_income.to_string()}",
                "green",
            ),
            metric_card(
                "wrench",
                "Upcoming Maintenance",
                PropertyManagementState.upcoming_maintenance,
                "orange",
            ),
            class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
        ),
        rx.el.h2("Properties Overview", class_name="text-2xl font-bold mb-4"),
        rx.el.div(
            rx.foreach(PropertyManagementState.properties, property_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
        ),
        class_name="p-6",
    )