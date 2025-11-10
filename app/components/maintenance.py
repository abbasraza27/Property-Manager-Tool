import reflex as rx
from app.states.state import PropertyManagementState, MaintenanceRequest


def priority_badge(priority: rx.Var[str]) -> rx.Component:
    return rx.match(
        priority,
        (
            "High",
            rx.el.div(
                "High",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-red-100 text-red-700",
            ),
        ),
        (
            "Medium",
            rx.el.div(
                "Medium",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-yellow-100 text-yellow-700",
            ),
        ),
        (
            "Low",
            rx.el.div(
                "Low",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-blue-100 text-blue-700",
            ),
        ),
        rx.el.div("Unknown"),
    )


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.match(
        status,
        (
            "Open",
            rx.el.div(
                "Open",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-green-100 text-green-700",
            ),
        ),
        (
            "In Progress",
            rx.el.div(
                "In Progress",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-purple-100 text-purple-700",
            ),
        ),
        (
            "Completed",
            rx.el.div(
                "Completed",
                class_name="w-fit text-xs font-medium px-2 py-1 rounded-full bg-gray-100 text-gray-600",
            ),
        ),
        rx.el.div("Unknown"),
    )


def maintenance_card(req: MaintenanceRequest) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(req["description"], class_name="font-semibold"),
                rx.el.p(
                    f"{req['property_name']}, Unit {req['unit']}",
                    class_name="text-sm text-gray-500",
                ),
            ),
            rx.el.div(
                priority_badge(req["priority"]),
                status_badge(req["status"]),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between items-start",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Assigned Vendor", class_name="text-xs text-gray-500"),
                rx.el.p(
                    rx.cond(req["vendor"], req["vendor"], "Not Assigned"),
                    class_name="font-medium",
                ),
            ),
            class_name="mt-4 pt-4 border-t border-gray-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    "In Progress",
                    on_click=lambda: PropertyManagementState.update_maintenance_status(
                        req["id"], "In Progress"
                    ),
                    disabled=req["status"] == "In Progress",
                    class_name="text-xs font-medium bg-purple-100 text-purple-700 px-2 py-1 rounded-md hover:bg-purple-200 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                rx.el.button(
                    "Completed",
                    on_click=lambda: PropertyManagementState.update_maintenance_status(
                        req["id"], "Completed"
                    ),
                    disabled=req["status"] == "Completed",
                    class_name="text-xs font-medium bg-green-100 text-green-700 px-2 py-1 rounded-md hover:bg-green-200 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                rx.el.button(
                    "Re-open",
                    on_click=lambda: PropertyManagementState.update_maintenance_status(
                        req["id"], "Open"
                    ),
                    disabled=req["status"] == "Open",
                    class_name="text-xs font-medium bg-red-100 text-red-700 px-2 py-1 rounded-md hover:bg-red-200 disabled:opacity-50 disabled:cursor-not-allowed",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.select(
                rx.el.option("Assign Vendor", value="", disabled=True),
                rx.foreach(
                    PropertyManagementState.available_vendors,
                    lambda v: rx.el.option(v, value=v),
                ),
                on_change=lambda vendor: PropertyManagementState.update_maintenance_vendor(
                    req["id"], vendor
                ),
                default_value=req["vendor"].to_string(),
                key=f"vendor-select-{req['id']}",
                class_name="text-xs rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500",
            ),
            class_name="flex items-center justify-between mt-4 pt-4 border-t border-gray-100",
        ),
        class_name="p-4 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


def filter_button(label: str, status: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: PropertyManagementState.set_maintenance_filter(status),
        class_name=rx.cond(
            PropertyManagementState.maintenance_filter == status,
            "px-3 py-1 text-sm font-medium rounded-md bg-purple-100 text-purple-700",
            "px-3 py-1 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-100",
        ),
    )


def add_request_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("plus", size=16, class_name="mr-2"),
                "New Request",
                class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700 transition-colors",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("New Maintenance Request"),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Property", class_name="text-sm font-medium"),
                        rx.el.select(
                            rx.foreach(
                                PropertyManagementState.property_names,
                                lambda name: rx.el.option(name, value=name),
                            ),
                            name="property_name",
                            default_value=PropertyManagementState.new_request_property,
                            on_change=PropertyManagementState.set_new_request_property,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                            required=True,
                        ),
                        class_name="col-span-1",
                    ),
                    rx.el.div(
                        rx.el.label("Unit Number", class_name="text-sm font-medium"),
                        rx.el.input(
                            name="unit",
                            key=PropertyManagementState.new_request_unit,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Description", class_name="text-sm font-medium"),
                        rx.el.textarea(
                            name="description",
                            key=PropertyManagementState.new_request_description,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                            required=True,
                        ),
                        class_name="col-span-2",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label("Priority", class_name="text-sm font-medium"),
                            rx.el.select(
                                rx.el.option("Low", value="Low"),
                                rx.el.option("Medium", value="Medium"),
                                rx.el.option("High", value="High"),
                                name="priority",
                                default_value=PropertyManagementState.new_request_priority,
                                on_change=PropertyManagementState.set_new_request_priority,
                                class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Assign Vendor", class_name="text-sm font-medium"
                            ),
                            rx.el.select(
                                rx.el.option("Select a vendor", value=""),
                                rx.foreach(
                                    PropertyManagementState.available_vendors,
                                    lambda v: rx.el.option(v, value=v),
                                ),
                                name="vendor",
                                default_value=PropertyManagementState.new_request_vendor,
                                on_change=PropertyManagementState.set_new_request_vendor,
                                class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                            ),
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4",
                ),
                on_submit=PropertyManagementState.add_maintenance_request,
                id="maintenance_form",
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        class_name="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200",
                    )
                ),
                rx.el.button(
                    "Save Request",
                    type_="submit",
                    form="maintenance_form",
                    class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700",
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
    )


def maintenance_content() -> rx.Component:
    return rx.el.div(
        add_request_dialog(),
        rx.el.div(
            rx.el.h1("Maintenance Tracking", class_name="text-3xl font-bold"),
            rx.el.div(
                filter_button("All", "All"),
                filter_button("Open", "Open"),
                filter_button("In Progress", "In Progress"),
                filter_button("Completed", "Completed"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.foreach(
                PropertyManagementState.filtered_maintenance_requests, maintenance_card
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
        ),
        class_name="p-6",
    )