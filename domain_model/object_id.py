from __future__ import annotations
from uuid import UUID, uuid4


class ObjectID:
    def __init__(self, id_: UUID | None):
        self._initial_id = id_
        self._id = id_ or uuid4()

    @property
    def value(self) -> UUID:
        return self._id

    @property
    def is_new(self) -> bool:
        return self._initial_id is None

    def __eq__(self, other: ObjectID | UUID | None) -> bool:
        if isinstance(other, UUID):
            return self._id == other
        elif isinstance(other, ObjectID):
            return self._id == other._id
        # I'm not sure about this one - it's a bit unclear why comparison to `None` can return `True`.
        # However, it's quite useful in tests.
        elif other is None:
            return self._initial_id is None

        raise ValueError(f'Cannot compare ObjectID with {type(other)}')

    def __hash__(self) -> int:
        return hash(self._id)
