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

def api(request, table, id=None):
    conn = sqlite3.connect(DB_path)
    conn.row_factory = dict_factory
    c = conn.cursor()
    try:
        if(table == 'gallery'):
            if id:
                c.execute(f"SELECT * FROM gallery WHERE _id_glossary = '{id}'")
                return JsonResponse(c.fetchall(), safe=False)
            else:
                c.execute(f"SELECT DISTINCT _id_glossary, name FROM gallery ORDER BY gallery.name")
                return JsonResponse(c.fetchall(), safe=False)
        if(table == 'glossary'):
            if id:
                c.execute(f"SELECT name, text, _id FROM glossary WHERE _id = '{id}'")
                return JsonResponse(c.fetchone(), safe=False)
            else:
                c.execute(f"SELECT name, _id FROM glossary ORDER BY glossary.name")
                return JsonResponse(c.fetchall(), safe=False)
        if(table == 'map'):
            if id:
                c.execute(f"SELECT * FROM map WHERE _id = '{id}'")
                return JsonResponse(c.fetchone(), safe=False)
            else:
                c.execute(f"SELECT name, _id FROM map ORDER BY map.name")
                return JsonResponse(c.fetchall(), safe=False)
        if(table == 'source'):
            if id:
                c.execute(f"SELECT name, text, _id FROM source WHERE _id = '{id}'")
                return JsonResponse(c.fetchone(), safe=False)
            else:
                c.execute(f"SELECT author._id, author.name, author.image, source.name AS sourse_name, source._id AS sourse_id FROM source INNER JOIN author ON author.id = source.id_author ORDER BY author.name")
                return JsonResponse(c.fetchall(), safe=False)
        if(table == 'author'):
            if id:
                c.execute(f"SELECT author.name, author.text, author._id, publication.text AS publication_text FROM author INNER JOIN publication ON publication.id_author=author.id WHERE author ._id='{id}'")
                return JsonResponse(c.fetchall(), safe=False)
            else:
                c.execute(f"SELECT * FROM author ORDER BY author.name")
                return JsonResponse(c.fetchall(), safe=False)        
        else:
            c.execute(f"SELECT * FROM {table} WHERE _id = '{id}'")
            return JsonResponse(c.fetchall(), safe=False)
    except Exception as ex:
        return JsonResponse({'error': str(ex)})

    # c.execute(f"SELECT * FROM {table} WHERE _id_glossary = '{id}'")
    # return JsonResponse(c.fetchone())