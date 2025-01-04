from ..database.operations import DatabaseOperations


class BaseModel:
    table_name = None
    fields = []

    @classmethod
    def create(self, **kwargs):
        """Creates a new record"""
        return DatabaseOperations.create_record(self.table_name, kwargs)

    @classmethod
    def get(self, id):
        """Retrieves a single record by ID"""
        return DatabaseOperations.read_records(self.table_name, conditions=f"id = {id}")[0]

    @classmethod
    def get_all(self):
        """Retrieves all records"""
        return DatabaseOperations.read_records(self.table_name)

    @classmethod
    def update(self, id, **kwargs):
        """Updates an existing record"""
        return DatabaseOperations.update_record(self.table_name, kwargs, f"id = {id}")

    @classmethod
    def delete(self, id):
        """Deletes a record"""
        return DatabaseOperations.delete_record(self.table_name, f"id = {id}")
