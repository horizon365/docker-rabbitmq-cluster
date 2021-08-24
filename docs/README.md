根据model文件生成Table操作步骤：


    pip安装依赖包 sphinx，sphinxcontrib_django2
    新建目录 docs，进入目录后执行 sphinx-quickstart ，第一项选择Y（source与build独立目录），其它项按需填写。删除source/index.rst文件的以下部分：

    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`


    进入新生成的source目录，下载main.py文件放到目录 main.py

    编辑main.py文件，设定django包路径，以及想要导出的Models。
    sys.path.insert(0, os.path.abspath('../../website'))  # so sphinx can find modules, and also to allow django to set up
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
    django.setup()
     
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    from mydoc.models import *
    运行python main.py 在当前目录生成rst文件和对应的csv文件。
    退回到docs目录，执行`sphinx-build source/ build/` 将在build目录生成html文件，打开index.html并拷贝表格至confluence。

根据注释生成api接口文档：

   1.进入docs目录，执行sphinx-apidoc -o source/ ../website/mydoc/ 生成 mydoc.models.rst等rst文件。
   2. 补充index.rst 文件。
   3. 进入docs目录，执行sphinx-build source/ build/

自动编号相关：

index.rst中 
.. toctree::
   :numbered: 4

子文件头：
.. sectnum::
https://docutils.sourceforge.io/docs/ref/rst/directives.html#sectnum

参考文献： https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html

技术储备：

用 Django REST Framework 撰寫 RESTful API 並生成 Swagger 文檔
https://zoejoyuliao.medium.com/%E7%94%A8-django-rest-framework-%E6%92%B0%E5%AF%AB-restful-api-%E4%B8%A6%E7%94%9F%E6%88%90-swagger-%E6%96%87%E6%AA%94-7cbef7c8e8d6

第 16 篇：别再手动管理接口文档了
https://zhuanlan.zhihu.com/p/214054224