import pytest
from faker import Faker

from src.inventory.domain.entities import Warehouse
from src.inventory.domain.exceptions import InvalidWarehouseError


class TestWarehouse:
    """Test suite for Warehouse entity"""

    def test_can_create_an_warehouse_successfully(self) -> None:
        """Test if can create an warehouse with all attributes"""

        fake = Faker()

        warehouse_id = fake.uuid4(cast_to=None)
        warehouse_name = fake.name()
        warehouse_location = fake.locale()

        warehouse = Warehouse(
            id=warehouse_id,
            name=warehouse_name,
            location_code=warehouse_location,
            is_active=True,
        )

        assert warehouse is not None
        assert warehouse.id == warehouse_id
        assert warehouse.name == warehouse_name
        assert warehouse.location_code == warehouse_location
        assert warehouse.is_active is True

    def test_if_can_create_warehouse_without_name_raises_error(self) -> None:
        """Test if can create an warehouse without pass name"""

        with pytest.raises(InvalidWarehouseError) as exc_info:
            Warehouse(
                name="",
                location_code="warehouse_location",
                is_active=True,
            )

        assert "Name must be a non-empty string." in str(exc_info)

        with pytest.raises(InvalidWarehouseError) as exc_info:
            Warehouse(
                name=None,  # type: ignore
                location_code="warehouse_location",
                is_active=True,
            )

        assert "Name must be a non-empty string." in str(exc_info)

    def test_if_can_create_warehouse_without_location_code_raises_error(self) -> None:
        """Test if can create an warehouse without pass location code"""

        with pytest.raises(InvalidWarehouseError) as exc_info:
            Warehouse(
                name="warehouse_name",
                location_code="",
                is_active=True,
            )

        assert "Location Code must be a non-empty string." in str(exc_info)

        with pytest.raises(InvalidWarehouseError) as exc_info:
            Warehouse(
                name="warehouse_name",
                location_code=None,  # type: ignore
                is_active=True,
            )

        assert "Location Code must be a non-empty string." in str(exc_info)

    def test_activate_and_deactivate_an_warehouse_successfully(self) -> None:
        """Test if can activate and deactivate an Warehouse"""

        fake = Faker()

        warehouse_id = fake.uuid4(cast_to=None)
        warehouse_name = fake.name()
        warehouse_location = fake.locale()

        warehouse = Warehouse(
            id=warehouse_id,
            name=warehouse_name,
            location_code=warehouse_location,
            is_active=False,
        )

        assert warehouse is not None
        assert warehouse.id == warehouse_id
        assert warehouse.name == warehouse_name
        assert warehouse.location_code == warehouse_location
        assert warehouse.is_active is False

        warehouse.activate()
        assert warehouse.is_active is True

        warehouse.deactivate()
        assert warehouse.is_active is False

    def test_if_activate_an_active_warehouse_raises_error(self) -> None:
        """Test if try to activate an active warehouse raises error"""

        warehouse = Warehouse(
            name="warehouse_name",
            location_code="warehouse_location",
            is_active=True,
        )

        assert warehouse is not None
        assert warehouse.is_active is True

        with pytest.raises(InvalidWarehouseError) as exc_info:
            warehouse.activate()

        assert "Warehouse already active." in str(exc_info)

    def test_if_deactivate_an_inactive_warehouse_raises_error(self) -> None:
        """Test if try to deactivate and inactive warehouse raises error"""

        warehouse = Warehouse(
            name="warehouse_name",
            location_code="warehouse_location",
            is_active=False,
        )

        assert warehouse is not None
        assert warehouse.is_active is False

        with pytest.raises(InvalidWarehouseError) as exc_info:
            warehouse.deactivate()

        assert "Warehouse already inactive." in str(exc_info)
