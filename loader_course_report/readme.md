# loader_course_report

## Testing

To test this function locally, create a `.env` file with the following:

```
PSQL_DB_CREATION_STRING="host='localhost' user='<username>' password='<password>' "
PSQL_CONNECTIONSTRING="host='localhost' user='<username>' password='<password>' dbname='test_course_report'"
```

## Functions

There are two functions which handle the main logic of table creation in app.py: `load_course_report_into_db` and `load_course_skills_into_db`, which are named respectively for the tables they create. These are conditionally triggered in `__init__.py` depending on the blob that enters storage.
