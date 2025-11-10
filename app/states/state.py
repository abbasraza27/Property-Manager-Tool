import reflex as rx
from typing import TypedDict, Literal
import logging


class Property(TypedDict):
    id: int
    name: str
    address: str
    occupancy: tuple[int, int]
    status: Literal["occupied", "vacant", "maintenance"]
    image_url: str


class Unit(TypedDict):
    id: int
    property_name: str
    unit_number: str
    rent_amount: int
    tenant_name: str | None
    rent_status: Literal["Paid", "Overdue", "Vacant"]
    lease_end: str | None
    archived: bool


class Tenant(TypedDict):
    id: int
    name: str
    email: str
    phone: str
    property_name: str
    unit_number: str
    lease_document_url: str


class MaintenanceRequest(TypedDict):
    id: int
    property_name: str
    unit: str
    description: str
    priority: Literal["Low", "Medium", "High"]
    status: Literal["Open", "In Progress", "Completed"]
    vendor: str | None


class PropertyManagementState(rx.State):
    active_section: str = "dashboard"
    add_unit_form_open: bool = False
    edit_unit_form_open: bool = False
    edit_unit_id: int | None = None
    new_unit_property: str = ""
    new_unit_number: str = ""
    new_unit_rent_amount: str = ""
    new_unit_tenant_name: str = ""
    new_unit_rent_status: str = "Vacant"
    new_unit_lease_end: str = ""
    edit_unit_property: str = ""
    edit_unit_number: str = ""
    edit_unit_rent_amount: str = ""
    edit_unit_tenant_name: str = ""
    edit_unit_rent_status: str = ""
    edit_unit_lease_end: str = ""
    unit_filter: str = "All"
    maintenance_filter: str = "All"
    new_request_property: str = ""
    new_request_unit: str = ""
    new_request_description: str = ""
    new_request_priority: str = "Low"
    new_request_vendor: str = ""
    available_vendors: list[str] = [
        "General Maintenance Co.",
        "QuickFix Plumbing",
        "ACME HVAC Services",
        "Sparky Electricians",
        "The Paint Squad",
    ]
    properties: list[Property] = [
        {
            "id": 1,
            "name": "Sunset Apartments",
            "address": "123 Ocean View, LA",
            "occupancy": (18, 20),
            "status": "occupied",
            "image_url": "/placeholder.svg",
        },
        {
            "id": 2,
            "name": "Downtown Lofts",
            "address": "456 Main St, Metropolis",
            "occupancy": (28, 30),
            "status": "occupied",
            "image_url": "/placeholder.svg",
        },
        {
            "id": 3,
            "name": "Green Valley Homes",
            "address": "789 Country Rd, Smallville",
            "occupancy": (10, 15),
            "status": "vacant",
            "image_url": "/placeholder.svg",
        },
        {
            "id": 4,
            "name": "Sunrise Towers",
            "address": "101 Dawn Ave, Gotham",
            "occupancy": (45, 50),
            "status": "maintenance",
            "image_url": "/placeholder.svg",
        },
    ]
    units: list[Unit] = [
        {
            "id": 1,
            "property_name": "Sunset Apartments",
            "unit_number": "A101",
            "rent_amount": 1650,
            "tenant_name": "Alice Johnson",
            "rent_status": "Paid",
            "lease_end": "2024-12-31",
            "archived": False,
        },
        {
            "id": 2,
            "property_name": "Sunset Apartments",
            "unit_number": "B203",
            "rent_amount": 1600,
            "tenant_name": None,
            "rent_status": "Vacant",
            "lease_end": None,
            "archived": False,
        },
        {
            "id": 3,
            "property_name": "Downtown Lofts",
            "unit_number": "5B",
            "rent_amount": 2100,
            "tenant_name": "Bob Williams",
            "rent_status": "Overdue",
            "lease_end": "2025-06-30",
            "archived": False,
        },
    ]
    tenants: list[Tenant] = [
        {
            "id": 1,
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "phone": "555-0101",
            "property_name": "Sunset Apartments",
            "unit_number": "A101",
            "lease_document_url": "#",
        },
        {
            "id": 2,
            "name": "Bob Williams",
            "email": "bob@example.com",
            "phone": "555-0102",
            "property_name": "Downtown Lofts",
            "unit_number": "5B",
            "lease_document_url": "#",
        },
    ]
    maintenance_requests: list[MaintenanceRequest] = [
        {
            "id": 1,
            "property_name": "Sunset Apartments",
            "unit": "#102",
            "description": "Leaky faucet in kitchen",
            "priority": "Medium",
            "status": "Open",
            "vendor": "QuickFix Plumbing",
        },
        {
            "id": 2,
            "property_name": "Downtown Lofts",
            "unit": "#305",
            "description": "Broken window pane",
            "priority": "High",
            "status": "Open",
            "vendor": None,
        },
    ]

    @rx.var
    def total_units(self) -> int:
        return sum((prop["occupancy"][1] for prop in self.properties))

    @rx.var
    def occupied_units(self) -> int:
        return sum((prop["occupancy"][0] for prop in self.properties))

    @rx.var
    def occupancy_rate(self) -> float:
        if self.total_units == 0:
            return 0.0
        return self.occupied_units / self.total_units * 100

    @rx.var
    def vacant_units(self) -> int:
        return self.total_units - self.occupied_units

    @rx.var
    def monthly_income(self) -> int:
        return self.occupied_units * 1500

    @rx.var
    def upcoming_maintenance(self) -> int:
        return len(
            [req for req in self.maintenance_requests if req["status"] == "Open"]
        )

    @rx.var
    def property_names(self) -> list[str]:
        return sorted([prop["name"] for prop in self.properties])

    @rx.var
    def filtered_units(self) -> list[Unit]:
        if self.unit_filter == "All":
            return [u for u in self.units if not u["archived"]]
        if self.unit_filter == "Archived":
            return [u for u in self.units if u["archived"]]
        return [
            u
            for u in self.units
            if u["rent_status"] == self.unit_filter and (not u["archived"])
        ]

    @rx.var
    def filtered_maintenance_requests(self) -> list[MaintenanceRequest]:
        if self.maintenance_filter == "All":
            return sorted(
                self.maintenance_requests,
                key=lambda r: (r["status"] != "Open", r["status"] != "In Progress"),
            )
        return [
            r
            for r in self.maintenance_requests
            if r["status"] == self.maintenance_filter
        ]

    @rx.event
    def set_active_section(self, section: str):
        self.active_section = section

    @rx.event
    def set_unit_filter(self, status: str):
        self.unit_filter = status

    @rx.event
    def set_maintenance_filter(self, status: str):
        self.maintenance_filter = status

    def _reset_new_unit_form(self):
        self.new_unit_property = ""
        self.new_unit_number = ""
        self.new_unit_rent_amount = ""
        self.new_unit_tenant_name = ""
        self.new_unit_rent_status = "Vacant"
        self.new_unit_lease_end = ""

    @rx.event
    def open_add_unit_form(self):
        self._reset_new_unit_form()
        self.add_unit_form_open = True

    @rx.event
    def close_add_unit_form(self):
        self.add_unit_form_open = False
        self._reset_new_unit_form()

    @rx.event
    def add_unit(self, form_data: dict):
        property_name = form_data.get("property_name")
        unit_number = form_data.get("unit_number")
        rent_amount_str = form_data.get("rent_amount")
        if not all([property_name, unit_number, rent_amount_str]):
            return rx.toast.error("Property, Unit #, and Rent are required.")
        try:
            rent = int(rent_amount_str)
        except (ValueError, TypeError) as e:
            logging.exception(f"Error converting rent to int: {e}")
            return rx.toast.error("Rent amount must be a valid number.")
        new_id = max((u["id"] for u in self.units)) + 1 if self.units else 1
        unit = Unit(
            id=new_id,
            property_name=property_name,
            unit_number=unit_number,
            rent_amount=rent,
            tenant_name=form_data.get("tenant_name") or None,
            rent_status=form_data.get("rent_status", "Vacant"),
            lease_end=form_data.get("lease_end") or None,
            archived=False,
        )
        self.units.append(unit)
        self.add_unit_form_open = False
        self._reset_new_unit_form()
        return rx.toast.success(f"Unit {unit['unit_number']} added successfully!")

    def _reset_new_request_form(self):
        self.new_request_property = ""
        self.new_request_unit = ""
        self.new_request_description = ""
        self.new_request_priority = "Low"
        self.new_request_vendor = ""

    @rx.event
    def add_maintenance_request(self, form_data: dict):
        if not all(
            [
                form_data.get("property_name"),
                form_data.get("unit"),
                form_data.get("description"),
            ]
        ):
            return rx.toast.error("Property, Unit, and Description are required.")
        new_id = (
            max((r["id"] for r in self.maintenance_requests)) + 1
            if self.maintenance_requests
            else 1
        )
        request = MaintenanceRequest(
            id=new_id,
            property_name=form_data["property_name"],
            unit=form_data["unit"],
            description=form_data["description"],
            priority=form_data.get("priority", "Low"),
            status="Open",
            vendor=form_data.get("vendor") or None,
        )
        self.maintenance_requests.append(request)
        self._reset_new_request_form()
        return rx.toast.success("Maintenance request added!")

    @rx.event
    def open_edit_unit_form(self, unit_id: int):
        unit = next((u for u in self.units if u["id"] == unit_id), None)
        if unit:
            self.edit_unit_id = unit["id"]
            self.edit_unit_property = unit["property_name"]
            self.edit_unit_number = unit["unit_number"]
            self.edit_unit_rent_amount = str(unit["rent_amount"])
            self.edit_unit_tenant_name = unit["tenant_name"] or ""
            self.edit_unit_rent_status = unit["rent_status"]
            self.edit_unit_lease_end = unit["lease_end"] or ""
            self.edit_unit_form_open = True

    @rx.event
    def close_edit_unit_form(self):
        self.edit_unit_form_open = False
        self.edit_unit_id = None

    @rx.event
    def set_edit_unit_property(self, value: str):
        self.edit_unit_property = value

    @rx.event
    def set_edit_unit_rent_status(self, value: str):
        self.edit_unit_rent_status = value

    @rx.event
    def update_unit(self, form_data: dict):
        if self.edit_unit_id is None:
            return rx.toast.error("No unit selected for editing.")
        unit_number = form_data.get("unit_number")
        rent_amount_str = form_data.get("rent_amount")
        if not all([self.edit_unit_property, unit_number, rent_amount_str]):
            return rx.toast.error("Property, Unit #, and Rent are required.")
        try:
            rent = int(rent_amount_str)
        except (ValueError, TypeError) as e:
            logging.exception(f"Error converting rent to int: {e}")
            return rx.toast.error("Rent amount must be a valid number.")
        for i, unit in enumerate(self.units):
            if unit["id"] == self.edit_unit_id:
                self.units[i]["property_name"] = self.edit_unit_property
                self.units[i]["unit_number"] = unit_number
                self.units[i]["rent_amount"] = rent
                self.units[i]["tenant_name"] = form_data.get("tenant_name") or None
                self.units[i]["rent_status"] = self.edit_unit_rent_status
                self.units[i]["lease_end"] = form_data.get("lease_end") or None
                break
        else:
            return rx.toast.error("Unit not found.")
        self.edit_unit_form_open = False
        return rx.toast.info(f"Unit {unit_number} updated successfully!")

    @rx.event
    def update_maintenance_status(self, request_id: int, status: str):
        for i, req in enumerate(self.maintenance_requests):
            if req["id"] == request_id:
                self.maintenance_requests[i]["status"] = status
                return rx.toast.info(f"Request status updated to {status}.")

    @rx.event
    def update_maintenance_vendor(self, request_id: int, vendor: str):
        for i, req in enumerate(self.maintenance_requests):
            if req["id"] == request_id:
                self.maintenance_requests[i]["vendor"] = vendor
                return rx.toast.info(
                    f"Vendor for request #{request_id} updated to {vendor}."
                )

    @rx.event
    def toggle_unit_archive(self, unit_id: int):
        for i, unit in enumerate(self.units):
            if unit["id"] == unit_id:
                self.units[i]["archived"] = not self.units[i]["archived"]
                status = "archived" if self.units[i]["archived"] else "restored"
                return rx.toast.success(f"Unit {unit['unit_number']} {status}.")
        return