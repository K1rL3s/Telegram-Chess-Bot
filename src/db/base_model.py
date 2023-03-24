from sqlalchemy.orm.exc import DetachedInstanceError

from src.db.db_session import SqlAlchemyBase


class BaseModel(SqlAlchemyBase):
    __abstract__ = True

    def __repr__(self):
        return self._repr()

    def _repr(self, **fields) -> str:
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({', '.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"
