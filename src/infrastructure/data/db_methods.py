from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModelMixin:
    def save(self, session):
        session.add(self)
        session.commit()
        session.refresh(self)
        return self

    def delete(self, session):
        session.delete(self)
        session.commit()

    def update(self, session, data: dict):
        for key, value in data.items():
            if value is not None:
                setattr(self, key, value)
        session.commit()
        session.refresh(self)

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session, id):
        return session.get(cls, id)

    @classmethod
    def get_by_email(cls, session, email):
        return session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_user_id(cls, session, user_id):
        return session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def get_by_list_task_id(cls, session, id_list_task):
        return session.query(cls).filter(cls.id_list_task == id_list_task).all()
