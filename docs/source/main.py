# coding=utf-8


import os
import sys
import inspect
import django
from django.utils.html import strip_tags
from django.utils.encoding import force_text
from django.db import models
from sphinxcontrib_django2.docstrings.field_utils import get_field_verbose_name, get_field_type
import pdb


sys.path.insert(0, os.path.abspath('../../website'))  # so sphinx can find modules, and also to allow django to set up
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
from mydoc.models import *


def process_docstring(obj):
    # This causes import errors if left outside the function
    # Only look at objects that inherit from Django's base model class
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        # Grab the field list from the meta class
        all_fields = obj._meta.get_fields(include_parents=True)
        rows = []
        for field in all_fields:
            # Skip ManyToOneRel and ManyToManyRel fields which have no 'verbose_name'
            if not hasattr(field, 'verbose_name'):
                verbose_name = get_field_verbose_name(field)
                field_type = get_field_type(field, include_role=False)
                row = {
                    "字段": getattr(field, 'attname', '->'),
                    "数据类型": field_type,
                    "描述": verbose_name,
                    "是否必填": "否",
                    "空值形式": '',
                    "备注": field_type,
                }
                rows.append(row)
                continue

            # Decode and strip any html out of the field's help text
            help_text = strip_tags(force_text(field.help_text))

            # Decode and capitalize the verbose name, for use if there isn't
            # any help text
            verbose_name = force_text(field.verbose_name).capitalize()

            # Add the field's type to the docstring
            if isinstance(field, models.ForeignKey):
                to = field.related_model
                remark = u' %s: %s to :class:`~%s.%s`' % (
                    field.attname, type(field).__name__, to.__module__, to.__name__)
            else:
                remark = help_text
            row = {
                "字段": field.attname,
                "数据类型": f'{type(field).__name__}({field.max_length})' if field.max_length else type(field).__name__,
                "描述": verbose_name,
                "是否必填": "否" if field.null or field.blank else "是",
                "空值形式": field.get_default(),
                "备注": remark,
            }
            rows.append(row)
        writer_csv(obj.__name__, rows)
        writer_rst(obj.__name__)
        writer_index_rst(obj.__name__)


def writer_csv(fn, rowdicts):
    import csv
    filepath = os.path.join(BASE_DIR, fn + '.csv')
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["字段", "数据类型", "描述", "是否必填", "空值形式", "备注"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rowdicts)


def writer_rst(fn):
    template = \
        f'''
表： [{fn}]
============================

.. csv-table:: 
   :header-rows: 1
   :file: ./{fn}.csv
   :widths: 40, 40, 60, 40, 40, 50
'''
    filepath = os.path.join(BASE_DIR, fn + '.rst')
    with open(filepath, 'w', encoding='utf-8') as rstfile:
        rstfile.write(template)


def writer_index_rst(rst):
    template = \
        """
        Models
        ============
        
        .. toctree::
        """
    content = ' ' * 3 + rst + '\n'
    filepath = os.path.join(BASE_DIR, 'index.rst')
    with open(filepath, 'a+') as f:
        end = f.tell()
        f.seek(0)
        if content not in f.readlines():
            f.seek(end)
            f.write(content)


if __name__ == '__main__':
    for obj in list(locals().values()):
        process_docstring(obj)
