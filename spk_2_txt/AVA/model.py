from flask import current_app
from google.cloud import datastore

builtin_list = list

def init_app(app):
    pass


def get_client():
    return datastore.Client(current_app.config['PROJECT_ID'])


def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, builtin_list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity

def list(limit=10,cursor=None):
    ds = get_client()

    query = ds.query(kind='File')
    query_itterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_itterator.pages)

    entities = builtin_list(map(from_datastore, page))
    next_cursor = (
        query_itterator.next_page_token.decode('utf-8')
        if query_itterator.next_page_token else None)

    return entities, next_cursor


def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key("File", int(id))
    else:
        key = ds.key("File")

    entity = datastore.Entity(key=key)
    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


create = update

def delete(id):
    ds = get_client()
    key = ds.key("File", int(id))
    ds.delete(key=key)