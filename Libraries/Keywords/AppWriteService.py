from robot.api.deco import keyword
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.query import Query
import time


class AppWriteService:
    def __init__(self, endpoint, project_id, api_key):
        self.client = Client()
        self.client.set_endpoint(endpoint)
        self.client.set_project(project_id)
        self.client.set_key(api_key)
        self.databases = Databases(self.client)

    @keyword("Create Database")
    def create_database(self, database_id = None, name = None):
        """Create a database

        Arguments:
        - database_id: Optional database ID (uses unique ID if not provided)
        - name: Optional database name (uses "My Database" if not provided)

        Returns the created database object
        """
        try:
            db_id = database_id if database_id else ID.unique()
            db_name = name if name else "My Database"
            result = self.databases.create(
                database_id = db_id,
                name = db_name
            )
            return result
        except Exception as e:
            raise e

    @keyword("List Databases")
    def list_databases(self):
        """List all databases

        Returns list of all databases
        """
        try:
            result = self.databases.list()
            return result
        except Exception as e:
            raise e

    @keyword("Delete Database")
    def delete_database(self, database_id):
        """Delete a database

        Arguments:
        - database_id: ID of the database to delete

        Returns delete result
        """
        try:
            result = self.databases.delete(database_id = database_id)
            return result
        except Exception as e:
            raise e

    @keyword("Create Collection")
    def create_collection(self, database_id, collection_id = None, name = None):
        """Create a collection

        Arguments:
        - database_id: Database ID where collection will be created
        - collection_id: Optional collection ID (uses unique ID if not provided)
        - name: Optional collection name (uses "My Collection" if not provided)

        Returns the created collection object
        """
        try:
            coll_id = collection_id if collection_id else ID.unique()
            coll_name = name if name else "My Collection"
            result = self.databases.create_collection(
                database_id = database_id,
                collection_id = coll_id,
                name = coll_name
            )
            return result
        except Exception as e:
            raise e

    @keyword("List Collections")
    def list_collections(self, database_id):
        """List all collections in a database

        Arguments:
        - database_id: Database ID to list collections from

        Returns list of collections
        """
        try:
            result = self.databases.list_collections(database_id = database_id)
            return result
        except Exception as e:
            raise e

    @keyword("Delete Collection")
    def delete_collection(self, database_id, collection_id):
        """Delete a collection

        Arguments:
        - database_id: Database ID containing the collection
        - collection_id: Collection ID to delete

        Returns delete result
        """
        try:
            result = self.databases.delete_collection(
                database_id = database_id,
                collection_id = collection_id
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create String Attribute")
    def create_string_attribute(self, database_id, collection_id, key, size, required = False, default = None,
                                array = False):
        """Create a string attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - size: String size limit
        - required: Whether attribute is required (default: False)
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_string_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                size = size,
                required = required,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Integer Attribute")
    def create_integer_attribute(self, database_id, collection_id, key, required = False, min_val = None,
                                 max_val = None, default = None, array = False):
        """Create an integer attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - required: Whether attribute is required (default: False)
        - min_val: Minimum value
        - max_val: Maximum value
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_integer_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                required = required,
                min = min_val,
                max = max_val,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Float Attribute")
    def create_float_attribute(self, database_id, collection_id, key, required = False, min_val = None, max_val = None,
                               default = None, array = False):
        """Create a float attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - required: Whether attribute is required (default: False)
        - min_val: Minimum value
        - max_val: Maximum value
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_float_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                required = required,
                min = min_val,
                max = max_val,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Boolean Attribute")
    def create_boolean_attribute(self, database_id, collection_id, key, required = False, default = None,
                                 array = False):
        """Create a boolean attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - required: Whether attribute is required (default: False)
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_boolean_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                required = required,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Datetime Attribute")
    def create_datetime_attribute(self, database_id, collection_id, key, required = False, default = None,
                                  array = False):
        """Create a datetime attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - required: Whether attribute is required (default: False)
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_datetime_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                required = required,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Email Attribute")
    def create_email_attribute(self, database_id, collection_id, key, required = False, default = None, array = False):
        """Create an email attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - required: Whether attribute is required (default: False)
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_email_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                required = required,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create URL Attribute")
    def create_url_attribute(self, database_id, collection_id, key, required = False, default = None, array = False):
        """Create a URL attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - required: Whether attribute is required (default: False)
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_url_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                required = required,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create IP Attribute")
    def create_ip_attribute(self, database_id, collection_id, key, required = False, default = None, array = False):
        """Create an IP attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - required: Whether attribute is required (default: False)
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_ip_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                required = required,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Enum Attribute")
    def create_enum_attribute(self, database_id, collection_id, key, elements, required = False, default = None,
                              array = False):
        """Create an enum attribute in collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key
        - elements: List of allowed values
        - required: Whether attribute is required (default: False)
        - default: Default value
        - array: Whether attribute is an array (default: False)

        Returns the created attribute object
        """
        try:
            result = self.databases.create_enum_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                elements = elements,
                required = required,
                default = default,
                array = array
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Relationship Attribute")
    def create_relationship_attribute(self, database_id, collection_id, related_collection_id, relation_type,
                                      two_way = False, key = None, two_way_key = None, on_delete = "restrict"):
        """Create a relationship attribute between collections

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - related_collection_id: Related collection ID
        - relation_type: Type of relationship
        - two_way: Whether relationship is two-way (default: False)
        - key: Attribute key
        - two_way_key: Two-way attribute key
        - on_delete: Delete behavior (default: "restrict")

        Returns the created attribute object
        """
        try:
            result = self.databases.create_relationship_attribute(
                database_id = database_id,
                collection_id = collection_id,
                related_collection_id = related_collection_id,
                type = relation_type,
                two_way = two_way,
                key = key,
                two_way_key = two_way_key,
                on_delete = on_delete
            )
            return result
        except Exception as e:
            raise e

    @keyword("List Attributes")
    def list_attributes(self, database_id, collection_id):
        """List all attributes in a collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID

        Returns list of attributes
        """
        try:
            result = self.databases.list_attributes(
                database_id = database_id,
                collection_id = collection_id
            )
            return result
        except Exception as e:
            raise e

    @keyword("Delete Attribute")
    def delete_attribute(self, database_id, collection_id, key):
        """Delete an attribute from collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key to delete

        Returns delete result
        """
        try:
            result = self.databases.delete_attribute(
                database_id = database_id,
                collection_id = collection_id,
                key = key
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Index")
    def create_index(self, database_id, collection_id, key, type, attributes, orders = None):
        """Create an index for a collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Index key
        - type: Index type
        - attributes: List of attributes to index
        - orders: List of order directions (default: None)

        Returns the created index object
        """
        try:
            result = self.databases.create_index(
                database_id = database_id,
                collection_id = collection_id,
                key = key,
                type = type,
                attributes = attributes,
                orders = orders
            )
            return result
        except Exception as e:
            raise e

    @keyword("List Indexes")
    def list_indexes(self, database_id, collection_id):
        """List all indexes in a collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID

        Returns list of indexes
        """
        try:
            result = self.databases.list_indexes(
                database_id = database_id,
                collection_id = collection_id
            )
            return result
        except Exception as e:
            raise e

    @keyword("Delete Index")
    def delete_index(self, database_id, collection_id, key):
        """Delete an index from collection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Index key to delete

        Returns delete result
        """
        try:
            result = self.databases.delete_index(
                database_id = database_id,
                collection_id = collection_id,
                key = key
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Document")
    def create_document(self, database_id, collection_id, data, document_id = None, permissions = None):
        """Create a document in AppWrite

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - data: Document data
        - document_id: Optional document ID (uses unique ID if not provided)
        - permissions: Optional permissions list

        Returns the created document object
        """
        try:
            doc_id = document_id if document_id else ID.unique()
            result = self.databases.create_document(
                database_id = database_id,
                collection_id = collection_id,
                document_id = doc_id,
                data = data,
                permissions = permissions if permissions else [ ]
            )
            return result
        except Exception as e:
            raise e

    @keyword("Get Document")
    def get_document(self, database_id, collection_id, document_id):
        """Get a document from AppWrite

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - document_id: Document ID to retrieve

        Returns the document object
        """
        try:
            result = self.databases.get_document(
                database_id = database_id,
                collection_id = collection_id,
                document_id = document_id
            )
            return result
        except Exception as e:
            raise e

    @keyword("Update Document")
    def update_document(self, database_id, collection_id, document_id, data, permissions = None):
        """Update a document in AppWrite

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - document_id: Document ID to update
        - data: Updated data
        - permissions: Optional permissions list

        Returns the updated document object
        """
        try:
            result = self.databases.update_document(
                database_id = database_id,
                collection_id = collection_id,
                document_id = document_id,
                data = data,
                permissions = permissions
            )
            return result
        except Exception as e:
            raise e

    @keyword("Delete Document")
    def delete_document(self, database_id, collection_id, document_id):
        """Delete a document from AppWrite

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - document_id: Document ID to delete

        Returns delete result
        """
        try:
            result = self.databases.delete_document(
                database_id = database_id,
                collection_id = collection_id,
                document_id = document_id
            )
            return result
        except Exception as e:
            raise e

    @keyword("List Documents")
    def list_documents(self, database_id, collection_id, queries = None):
        """List documents from AppWrite with optional queries

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - queries: Optional query list

        Returns list of documents
        """
        try:
            result = self.databases.list_documents(
                database_id = database_id,
                collection_id = collection_id,
                queries = queries if queries else [ ]
            )
            return result
        except Exception as e:
            raise e

    @keyword("Query Documents")
    def query_documents(self, database_id, collection_id, field, operator, value):
        """Query documents with specific conditions

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - field: Field to query
        - operator: Query operator
        - value: Query value

        Returns queried documents
        """
        try:
            query = [ Query.equal(field, value) ]

            if operator == "not_equal":
                query = [ Query.not_equal(field, value) ]
            elif operator == "less_than":
                query = [ Query.less_than(field, value) ]
            elif operator == "less_than_equal":
                query = [ Query.less_than_equal(field, value) ]
            elif operator == "greater_than":
                query = [ Query.greater_than(field, value) ]
            elif operator == "greater_than_equal":
                query = [ Query.greater_than_equal(field, value) ]
            elif operator == "search":
                query = [ Query.search(field, value) ]
            elif operator == "is_null":
                query = [ Query.is_null(field) ]
            elif operator == "is_not_null":
                query = [ Query.is_not_null(field) ]
            elif operator == "between":
                query = [ Query.between(field, value[ 0 ], value[ 1 ]) ]
            elif operator == "starts_with":
                query = [ Query.starts_with(field, value) ]
            elif operator == "ends_with":
                query = [ Query.ends_with(field, value) ]
            elif operator == "contains":
                query = [ Query.contains(field, value) ]

            result = self.databases.list_documents(
                database_id = database_id,
                collection_id = collection_id,
                queries = query
            )
            return result
        except Exception as e:
            raise e

    @keyword("Complex Query")
    def complex_query(self, database_id, collection_id, queries_list):
        """Execute complex queries with multiple conditions

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - queries_list: List of query objects

        Returns queried documents
        """
        try:
            result = self.databases.list_documents(
                database_id = database_id,
                collection_id = collection_id,
                queries = queries_list
            )
            return result
        except Exception as e:
            raise e

    @keyword("Query With Params")
    def query_with_params(self, database_id, collection_id, queries = None, limit = 25, offset = 0, order_field = None,
                          order_type = "ASC"):
        """Query documents with additional parameters

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - queries: Optional query list
        - limit: Maximum number of documents (default: 25)
        - offset: Skip this number of documents (default: 0)
        - order_field: Field to order by
        - order_type: Order direction ("ASC" or "DESC", default: "ASC")

        Returns queried documents
        """
        try:
            query_list = queries if queries else [ ]

            if limit:
                query_list.append(Query.limit(limit))
            if offset:
                query_list.append(Query.offset(offset))
            if order_field:
                if order_type.upper() == "ASC":
                    query_list.append(Query.order_asc(order_field))
                else:
                    query_list.append(Query.order_desc(order_field))

            result = self.databases.list_documents(
                database_id = database_id,
                collection_id = collection_id,
                queries = query_list
            )
            return result
        except Exception as e:
            raise e

    @keyword("Query With Select")
    def query_with_select(self, database_id, collection_id, select_fields, queries = None):
        """Query documents with field selection

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - select_fields: List of fields to select
        - queries: Optional query list

        Returns queried documents with selected fields
        """
        try:
            query_list = queries if queries else [ ]

            if select_fields:
                query_list.append(Query.select(select_fields))

            result = self.databases.list_documents(
                database_id = database_id,
                collection_id = collection_id,
                queries = query_list
            )
            return result
        except Exception as e:
            raise e

    @keyword("Create Documents Batch")
    def create_documents_batch(self, database_id, collection_id, documents_data):
        """Create multiple documents in batch

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - documents_data: List of document data objects

        Returns list of results
        """
        results = [ ]
        for data in documents_data:
            try:
                result = self.create_document(database_id, collection_id, data)
                results.append(result)
            except Exception as e:
                results.append({ "error": str(e), "data": data })
        return results

    @keyword("Update Documents Batch")
    def update_documents_batch(self, database_id, collection_id, documents_updates):
        """Update multiple documents in batch

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - documents_updates: List of update objects with document_id and data

        Returns list of results
        """
        results = [ ]
        for update in documents_updates:
            try:
                result = self.update_document(
                    database_id,
                    collection_id,
                    update[ 'document_id' ],
                    update[ 'data' ],
                    update.get('permissions')
                )
                results.append(result)
            except Exception as e:
                results.append({ "error": str(e), "document_id": update[ 'document_id' ] })
        return results

    @keyword("Wait For Attribute")
    def wait_for_attribute(self, database_id, collection_id, key, timeout = 30):
        """Wait for attribute to be available

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Attribute key to wait for
        - timeout: Maximum wait time in seconds (default: 30)

        Returns True if attribute becomes available, False if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                attributes = self.list_attributes(database_id, collection_id)
                for attr in attributes[ 'attributes' ]:
                    if attr[ 'key' ] == key and attr[ 'status' ] == 'available':
                        return True
                time.sleep(1)
            except Exception:
                time.sleep(1)
        return False

    @keyword("Wait For Index")
    def wait_for_index(self, database_id, collection_id, key, timeout = 30):
        """Wait for index to be available

        Arguments:
        - database_id: Database ID
        - collection_id: Collection ID
        - key: Index key to wait for
        - timeout: Maximum wait time in seconds (default: 30)

        Returns True if index becomes available, False if timeout
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                indexes = self.list_indexes(database_id, collection_id)
                for index in indexes[ 'indexes' ]:
                    if index[ 'key' ] == key and index[ 'status' ] == 'available':
                        return True
                time.sleep(1)
            except Exception:
                time.sleep(1)
        return False
