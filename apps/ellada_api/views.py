from django.http import HttpResponse, JsonResponse, Http404
from .models import *
import sqlite3
import os
import json

DB_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ellada.db')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def api(request, table, id):
    conn = sqlite3.connect(DB_path)
    conn.row_factory = dict_factory
    c = conn.cursor()
    try:
        if(table == 'gallery'):
            if id:
                c.execute(f"SELECT * FROM gallery WHERE _id_glossary = '{id}'")
                return JsonResponse(c.fetchone())
            else:
                c.execute(f"SELECT * FROM glossary ORDER BY glossary.name")
                return JsonResponse(c.fetchone())
        else:
            c.execute(f"SELECT * FROM {table} WHERE _id_glossary = '{id}'")
            return JsonResponse(c.fetchone())
    except Exception as ex:
        return JsonResponse({'foo': json.dumps(ex)})

    # c.execute(f"SELECT * FROM {table} WHERE _id_glossary = '{id}'")
    # return JsonResponse(c.fetchone())