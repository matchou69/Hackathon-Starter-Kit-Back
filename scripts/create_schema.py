from graphql.utils import schema_printer
from schema import schema

my_schema_str = schema_printer.print_schema(schema)
with open("schema.graphql", "w") as fp:
    fp.write(my_schema_str)
