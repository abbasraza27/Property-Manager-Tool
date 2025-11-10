import reflex as rx
from app.states.state import PropertyManagementState, Unit


def rent_status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.match(
        status,
        (
            "Paid",
            rx.el.div(
                rx.icon("square_check", size=14),
                "Paid",
                class_name="flex items-center gap-1.5 w-fit text-xs font-medium px-2 py-1 rounded-full bg-green-100 text-green-700",
            ),
        ),
        (
            "Overdue",
            rx.el.div(
                rx.icon("badge_alert", size=14),
                "Overdue",
                class_name="flex items-center gap-1.5 w-fit text-xs font-medium px-2 py-1 rounded-full bg-red-100 text-red-700",
            ),
        ),
        (
            "Vacant",
            rx.el.div(
                rx.icon("home", size=14),
                "Vacant",
                class_name="flex items-center gap-1.5 w-fit text-xs font-medium px-2 py-1 rounded-full bg-gray-100 text-gray-600",
            ),
        ),
        rx.el.div("Unknown"),
    )


def archived_badge() -> rx.Component:
    return rx.el.div(
        rx.icon("archive", size=14),
        "Archived",
        class_name="flex items-center gap-1.5 w-fit text-xs font-medium px-2 py-1 rounded-full bg-gray-100 text-gray-600",
    )


def unit_card(unit: Unit) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(f"Unit {unit['unit_number']}", class_name="font-semibold"),
                rx.el.p(unit["property_name"], class_name="text-sm text-gray-500"),
            ),
            rx.cond(
                unit["archived"],
                archived_badge(),
                rent_status_badge(unit["rent_status"]),
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Tenant", class_name="text-xs text-gray-500"),
                rx.el.p(unit["tenant_name"].to_string(), class_name="font-medium"),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.p("Lease End", class_name="text-xs text-gray-500"),
                rx.el.p(unit["lease_end"].to_string(), class_name="font-medium"),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.p("Rent", class_name="text-xs text-gray-500"),
                rx.el.p(
                    f"${unit['rent_amount'].to_string()}", class_name="font-medium"
                ),
                class_name="flex-1",
            ),
            class_name="flex gap-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("pencil", size=14, class_name="mr-1.5"),
                "Edit",
                on_click=lambda: PropertyManagementState.open_edit_unit_form(
                    unit["id"]
                ),
                class_name="text-xs font-medium text-gray-600 hover:text-black flex items-center",
            ),
            rx.el.button(
                rx.cond(unit["archived"], "Restore", "Archive"),
                on_click=lambda: PropertyManagementState.toggle_unit_archive(
                    unit["id"]
                ),
                class_name="text-xs font-medium text-gray-600 hover:text-black flex items-center",
            ),
            class_name="flex items-center gap-4 mt-4 pt-4 border-t border-gray-100",
        ),
        class_name="p-4 bg-white border border-gray-200 rounded-xl shadow-sm",
    )


def filter_button(label: str, status: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: PropertyManagementState.set_unit_filter(status),
        class_name=rx.cond(
            PropertyManagementState.unit_filter == status,
            "px-3 py-1 text-sm font-medium rounded-md bg-purple-100 text-purple-700",
            "px-3 py-1 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-100",
        ),
    )


def _unit_form(state: rx.State, handler: rx.event.EventHandler) -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.div(
                rx.el.label("Property", class_name="text-sm font-medium"),
                rx.el.select(
                    rx.foreach(
                        state.property_names,
                        lambda name: rx.el.option(name, value=name),
                    ),
                    name="property_name",
                    default_value=state.new_unit_property.to_string(),
                    on_change=state.set_new_unit_property,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                    required=True,
                ),
                class_name="col-span-2",
            ),
            rx.el.div(
                rx.el.label("Unit Number", class_name="text-sm font-medium"),
                rx.el.input(
                    name="unit_number",
                    default_value=state.new_unit_number,
                    key=state.new_unit_number,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                    required=True,
                ),
            ),
            rx.el.div(
                rx.el.label("Rent Amount ($)", class_name="text-sm font-medium"),
                rx.el.input(
                    type="number",
                    name="rent_amount",
                    default_value=state.new_unit_rent_amount,
                    key=state.new_unit_rent_amount,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                    required=True,
                ),
            ),
            rx.el.div(
                rx.el.label("Tenant Name", class_name="text-sm font-medium"),
                rx.el.input(
                    name="tenant_name",
                    default_value=state.new_unit_tenant_name,
                    key=state.new_unit_tenant_name,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                ),
            ),
            rx.el.div(
                rx.el.label("Rent Status", class_name="text-sm font-medium"),
                rx.el.select(
                    rx.el.option("Paid", value="Paid"),
                    rx.el.option("Overdue", value="Overdue"),
                    rx.el.option("Vacant", value="Vacant"),
                    name="rent_status",
                    default_value=state.new_unit_rent_status,
                    on_change=state.set_new_unit_rent_status,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                ),
            ),
            rx.el.div(
                rx.el.label("Lease End Date", class_name="text-sm font-medium"),
                rx.el.input(
                    type="date",
                    name="lease_end",
                    default_value=state.new_unit_lease_end,
                    key=state.new_unit_lease_end,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                ),
                class_name="col-span-2",
            ),
            class_name="grid grid-cols-2 gap-4",
        ),
        on_submit=handler,
    )


def add_unit_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("plus", size=16, class_name="mr-2"),
                "Add Unit",
                on_click=PropertyManagementState.open_add_unit_form,
                class_name="flex items-center bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700 transition-colors",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Add New Unit"),
            _unit_form(PropertyManagementState, PropertyManagementState.add_unit),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=PropertyManagementState.close_add_unit_form,
                        class_name="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200",
                    )
                ),
                rx.el.button(
                    "Save Unit",
                    type_="submit",
                    form="_unit_form",
                    class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700",
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
            id="_unit_form",
        ),
        open=PropertyManagementState.add_unit_form_open,
    )


def edit_unit_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Edit Unit"),
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
                            default_value=PropertyManagementState.edit_unit_property,
                            on_change=PropertyManagementState.set_edit_unit_property,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                            required=True,
                        ),
                        class_name="col-span-2",
                    ),
                    rx.el.div(
                        rx.el.label("Unit Number", class_name="text-sm font-medium"),
                        rx.el.input(
                            name="unit_number",
                            default_value=PropertyManagementState.edit_unit_number,
                            key=PropertyManagementState.edit_unit_number,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Rent Amount ($)", class_name="text-sm font-medium"
                        ),
                        rx.el.input(
                            type="number",
                            name="rent_amount",
                            default_value=PropertyManagementState.edit_unit_rent_amount,
                            key=PropertyManagementState.edit_unit_rent_amount,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                            required=True,
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Tenant Name", class_name="text-sm font-medium"),
                        rx.el.input(
                            name="tenant_name",
                            default_value=PropertyManagementState.edit_unit_tenant_name,
                            key=PropertyManagementState.edit_unit_tenant_name,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Rent Status", class_name="text-sm font-medium"),
                        rx.el.select(
                            rx.el.option("Paid", value="Paid"),
                            rx.el.option("Overdue", value="Overdue"),
                            rx.el.option("Vacant", value="Vacant"),
                            name="rent_status",
                            default_value=PropertyManagementState.edit_unit_rent_status,
                            on_change=PropertyManagementState.set_edit_unit_rent_status,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Lease End Date", class_name="text-sm font-medium"),
                        rx.el.input(
                            type="date",
                            name="lease_end",
                            default_value=PropertyManagementState.edit_unit_lease_end,
                            key=PropertyManagementState.edit_unit_lease_end,
                            class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm",
                        ),
                        class_name="col-span-2",
                    ),
                    class_name="grid grid-cols-2 gap-4",
                ),
                on_submit=PropertyManagementState.update_unit,
                id="edit_unit_form",
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=PropertyManagementState.close_edit_unit_form,
                        class_name="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-medium hover:bg-gray-200",
                    )
                ),
                rx.el.button(
                    "Update Unit",
                    type_="submit",
                    form="edit_unit_form",
                    class_name="bg-purple-600 text-white px-4 py-2 rounded-lg font-medium hover:bg-purple-700",
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
        open=PropertyManagementState.edit_unit_form_open,
    )


def units_content() -> rx.Component:
    return rx.el.div(
        add_unit_dialog(),
        edit_unit_dialog(),
        rx.el.div(
            rx.el.h1("Unit Management", class_name="text-3xl font-bold"),
            rx.el.div(
                filter_button("All", "All"),
                filter_button("Paid", "Paid"),
                filter_button("Overdue", "Overdue"),
                filter_button("Vacant", "Vacant"),
                filter_button("Archived", "Archived"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(
            rx.foreach(PropertyManagementState.filtered_units, unit_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
        ),
        class_name="p-6",
    )