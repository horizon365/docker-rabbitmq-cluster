.. sectnum::
   :depth: 4

Milkyway-Assert-Database(v2.0.0)
================================
描述
-------------
以数据库资产为主题资源的API。

资源实例
--------------
Y：是；N：否；-：该声明不适用于此属性字段。

.. csv-table::
   :header-rows: 1
   :file: ./Role.csv
   :widths: 40, 40, 60, 40, 40, 50

表头说明：

    * 可创建：表明该属性字段可用作POST参数。
    * 可更新：表明该属性字段可用作PUT/PATCH的目标更新字段参数（data中属性）。
    * 可展示：表明该属性字段可用于GET/POST/PUT/PATCH的响应数据；对于GET，也限制了fields的值域（当支持fields参数功能时）。
    * 可检索：表明该属性字段可用作GET的检索字段（field的取值）。
    * 系统生成：表明该属性字段既非由用户直接填写，也非由需求方提供的数据填入，而是由系统逻辑自动生成或边界效应进行填写和更新。

URL
------------
http://domain/milkyway/api/databases/

HTTP方法
-------------
GET
~~~~~~~~~~
描述
''''''''
获取数据库资产列表。

请求
''''''''''
权限要求
^^^^^^^^^^^^^^^^^^^^
登录用户。

参数
^^^^^^^^^^^^^^^^^^^^

Y：是；N：否；-：没有相关内容。

表头说明：

    * 名称：参数名称。
    * 类型：参数类型。
    * 存在：表明是否该参数不论有没有值，都必须发送到后端。
    * 必填：表明当该参数被发送到后端时，是否必须对应类型的非空值。
    * 值域：该参数的取值范围。
    * 前端验证：只需要前端进行验证的逻辑。
    * 后端验证：只需要后端进行验证的逻辑。
    * 前后端验证：前后端都必须进行验证的逻辑。
    * 描述：参数描述。

示例
^^^^^^^^^^^^^^^^^^^^

无示例。

.. code-block:: javascript

    {
        "query": "query_keyword",
        "filters": [
            {
                "field": "fieldname1",
                "rule": "contain",
                "value": "value1",
                "operator": "and"
            },
            {
                "field": "fieldname2",
                "rule": "exact",
                "value": "value2",
                "operator": "and"
            }
        ],
        "fields": ["fieldname1", "fieldname2"],
        "pagination": {
            "page": 13,
            "per_page": 10,
            "sort": [
                {
                    "field": "fieldname3",
                    "rule": "desc"
                },
                {
                    "field": "fieldname7",
                    "rule": "asc"
                }
            ]
        },
        "accept": "text/comma-separated-values"
    }

响应
''''''''''
400
^^^^^^^^^^^^^^^^^^^^

描述：参数错误。

数据体：需要，响应相关的参数错误信息。

数据体示例：

.. code-block:: javascript

    {
        "error": {
            "query": "query错误码",  // 枚举值：请罗列枚举值。
            "filters": "filters级别错误码",  // 枚举值：请罗列枚举值。
            // 或者：
            "filters": [
                "",  // 第一项没有错误。
                "元素级别错误码",  // 枚举值：请罗列枚举值。
                {
                    "field": "field错误码",  // 枚举值：请罗列枚举值。
                    "rule": "rule错误码",  // 枚举值：请罗列枚举值。
                    "value": "value错误码",  // 枚举值：请罗列枚举值。
                    "operator": "operator错误码"  // 枚举值：请罗列枚举值。
                },
                ...
            ],
            "fields": "fields级别错误码",  // 枚举值：请罗列枚举值。
            // 或者：
            "fields": [
                "",  // 第一项没有错误。
                "元素级别错误码",  // 枚举值：请罗列枚举值。
                ...
            ],
            "pagination": "pagination级别错误码",  // 枚举值：请罗列枚举值。
            // 或者：
            "pagination": {
                "page": "page错误码",  // 枚举值：请罗列枚举值。
                "per_page": "per_page错误码",  // 枚举值：请罗列枚举值。
                "sort": "sort级别错误码"  // 枚举值：请罗列枚举值。
                // 或者
                "sort": [
                    "",  // 第一项没有错误。
                    "元素级别错误码",  // 枚举值：请罗列枚举值。
                    {
                        "sort": "sort错误码",  // 枚举值：请罗列枚举值。
                        "rule": "rule错误码"  // 枚举值：请罗列枚举值。
                    },
                    ...
                ]
            },
            "accept": "accept错误码",  // 枚举值：请罗列枚举值。
            "{field}": "invalidField"  // 适用于所有非法参数名称。
        }
    }


#. This is the first item of the list
#. This is the second one

   * The second item has a nested list with two items
   * this is the last item of the nested list

#. The parent list continues with its third item
