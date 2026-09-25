from uuid import UUID

import pytest
from faker import Faker

from src.core.domain import EntityValidationError
from tests.fakes import FakeEntity, FakeEvent


class TestEntity:
    """Test suite for entity"""

    def test_entity_initialization(self) -> None:
        """Test validation method at entity initialization"""
        fake = Faker()
        entity_id = fake.uuid4(cast_to=None)
        description = fake.name()

        fake_entity = FakeEntity(id=entity_id, description=description)

        assert fake_entity.id == entity_id
        assert fake_entity.description == description

    def test_create_entity_without_description_raises_error(self) -> None:
        """Test validation method at entity initialization"""
        fake = Faker()
        entity_id = fake.uuid4(cast_to=None)

        with pytest.raises(expected_exception=EntityValidationError) as exc_info:
            FakeEntity(id=entity_id, description="")

        assert "Description must be a non-empty string." in str(exc_info)

    def test_create_entity_without_id_successfully(self) -> None:
        """Teste if a entity can be created without id"""
        fake = Faker()

        fake_entity = FakeEntity(description=fake.name())

        assert fake_entity.id is not None
        assert isinstance(fake_entity.id, UUID)

    def test_entity_can_record_domain_events(self) -> None:
        """Test if the entity correctly registers domain events."""
        fake = Faker()
        fake_entity = FakeEntity(description=fake.name())

        event1 = FakeEvent(payload="event 1")
        event2 = FakeEvent(payload="event 2")

        fake_entity.add_domain_event(event1)
        fake_entity.add_domain_event(event2)

        events = fake_entity.list_domain_events()
        assert len(events) == 2
        assert event1 in events
        assert event2 in events

    def test_entity_can_clear_domain_events(self) -> None:
        """Test if the entity correctly clears and returns registered domain events."""
        fake = Faker()
        fake_entity = FakeEntity(description=fake.name())

        event = FakeEvent(payload="test payload")
        fake_entity.add_domain_event(event)

        dispatched_events = fake_entity.clear_domain_events()

        assert len(dispatched_events) == 1
        assert dispatched_events[0] == event
        assert len(fake_entity.list_domain_events()) == 0

    def test_domain_events_are_independent_between_instances(self) -> None:
        """Test if different entity instances do not share the same event list."""
        fake = Faker()
        entity_a = FakeEntity(description=fake.name())
        entity_b = FakeEntity(description=fake.name())

        entity_a.add_domain_event(FakeEvent(payload="event A"))

        assert len(entity_a.list_domain_events()) == 1
        assert len(entity_b.list_domain_events()) == 0

    def test_entity_representation(self) -> None:
        """Test __str__ and __repr__ methods of the entity."""
        fake = Faker()
        entity_id = fake.uuid4(cast_to=None)

        fake_entity = FakeEntity(id=entity_id, description=fake.name())

        expected_repr = f"<FakeEntity id={entity_id}>"
        expected_str = f"FakeEntity (id={entity_id})"

        assert repr(fake_entity) == expected_repr
        assert str(fake_entity) == expected_str

    def test_entity_instance_equality_and_id(self) -> None:
        """Test entity instance equality"""
        fake = Faker()
        entity_id = fake.uuid4(cast_to=None)

        fake_entity_a = FakeEntity(id=entity_id, description=fake.name())
        fake_entity_b = FakeEntity(id=entity_id, description=fake.name())

        assert fake_entity_a == fake_entity_b

    def test_entity_instance_equality_with_different_ids(self) -> None:
        """Test entity instance equality"""
        fake = Faker()

        fake_entity_a = FakeEntity(
            id=fake.uuid4(cast_to=None),
            description="Same Description",
        )
        fake_entity_b = FakeEntity(
            id=fake.uuid4(cast_to=None),
            description="Same Description",
        )

        assert fake_entity_a != fake_entity_b

    def test_entity_instance_equality_between_different_classes(self) -> None:
        """Test entity instance equality"""

        class AnotherFakeClass:
            """Another fake class for equality test"""

        fake_entity_a = FakeEntity(description="Original Class")
        fake_entity_b = AnotherFakeClass()

        assert fake_entity_a != fake_entity_b

    def test_entity_repr_fields(self) -> None:
        """Test the protected _repr_fields method directly."""
        fake = Faker()
        entity_id = fake.uuid4(cast_to=None)

        fake_entity = FakeEntity(id=entity_id, description=fake.name())

        # pylint: disable=protected-access
        assert fake_entity._repr_fields() == f"id={entity_id}"

    def test_entity_str_fields(self) -> None:
        """Test the protected _str_fields method directly."""
        fake = Faker()
        entity_id = fake.uuid4(cast_to=None)

        fake_entity = FakeEntity(id=entity_id, description=fake.name())

        # pylint: disable=protected-access
        assert fake_entity._str_fields() == f"id={entity_id}"
