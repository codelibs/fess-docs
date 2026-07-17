==================
认证与会话 API
==================

概述
====

v2 API 采用基于会话的认证方式。
登录通过 ``POST /auth/login`` 完成，成功后将建立会话并颁发 CSRF 令牌。

修改状态的请求（\ ``POST``\ ）需要携带 ``X-Fess-CSRF-Token`` 头。
有关 CSRF 令牌的获取方式、轮换机制，以及公共响应信封和错误模型，请参阅 :doc:`api-overview`。

本页介绍以下 4 个端点。

.. tabularcolumns:: |p{4cm}|p{4cm}|p{7cm}|
.. list-table:: 端点一览
   :header-rows: 1
   :widths: 25 15 60

   * - 端点
     - 方法
     - 说明
   * - ``/auth/me``
     - GET
     - 获取当前已认证的用户。
   * - ``/auth/login``
     - POST
     - 使用用户名和密码登录。
   * - ``/auth/logout``
     - POST
     - 注销（幂等）。
   * - ``/auth/password``
     - POST
     - 修改当前用户的密码。

.. _api-auth-userpayload:

公共用户信息 (UserPayload)
==========================

``GET /auth/me`` 和 ``POST /auth/login`` 的响应中包含的用户信息，以公共的 ``UserPayload`` 结构返回。
所有数组字段均为非 null；无值时返回空数组。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: UserPayload
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 类型
     - 说明
   * - ``user_id``
     - string
     - 用户 ID。（必填）
   * - ``username``
     - string
     - 供 SPA 账户菜单显示的用户名。目前与 ``user_id`` 相同，但将来后端可能独立提供。（必填）
   * - ``name``
     - string
     - 供 SPA 账户菜单显示的显示名称。目前与 ``user_id`` 相同。（必填）
   * - ``roles``
     - string[]
     - 用户角色的数组。（必填）
   * - ``groups``
     - string[]
     - 用户所属组的数组。（必填）
   * - ``permissions``
     - string[]
     - 用户权限的数组。（必填）
   * - ``editable``
     - boolean
     - 用户信息是否可编辑。（必填）
   * - ``admin``
     - boolean
     - 当用户拥有已配置的 ``authentication.admin.roles`` 中任意一个角色时为 ``true``\ 。控制 SPA 中"Administration"项目的显示。（必填）

获取认证状态
============

请求
----

==================  ====================================================
HTTP 方法            GET
端点                 ``/api/v2/auth/me``
==================  ====================================================

获取当前已认证的用户。
对匿名调用不会报错，而是返回 ``authenticated: false``\ 。
已认证时，\ ``user`` 包含 :ref:`UserPayload <api-auth-userpayload>`。

响应
----

成功时（HTTP 200），返回如下公共信封格式的响应（已认证示例）。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "authenticated": true,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        }
      }
    }

``response`` 各元素说明如下。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 响应信息
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 类型
     - 说明
   * - ``authenticated``
     - boolean
     - 是否已认证。（必填）
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`。仅当 ``authenticated`` 为 ``true`` 时存在。

错误响应
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应
   :header-rows: 1
   :widths: 25 75

   * - 状态码
     - 说明
   * - 405 Method Not Allowed
     - 指定了不支持的 HTTP 方法时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

登录
====

请求
----

==================  ====================================================
HTTP 方法            POST
端点                 ``/api/v2/auth/login``
==================  ====================================================

使用用户名和密码登录。
登录成功时，Servlet 会话 ID 将轮换，颁发新的 CSRF 令牌，并清除调用方 IP 和目标用户的速率限制桶。

速率限制分为两个维度：调用方 IP 单位和用户单位。超过 IP 单位限制时，返回 ``429 Too Many Requests`` 并附带 ``Retry-After`` 头（单位秒）。超过用户单位限制时，为防止外部推测计数器状态，返回与凭据不正确相同的 ``401 Unauthorized``\ （不附带 ``Retry-After`` 头）。

即使已有认证会话，也不会短路，传入的凭据始终会被验证。

``return_to`` 必须是符合 ``^/[A-Za-z0-9_\-/.?&=%:@+~#*!,;]*$`` 的相对路径。
此外，协议相对路径（以 ``//`` 开头）及包含 ASCII 控制字符的路径将被拒绝，并从回显的响应中静默移除。

.. note::

   本端点 **不在 CSRF 验证范围之内**\ （因为登录前令牌不存在）。

.. note::

   与其他状态变更端点不同，本端点会将过大的请求体或不支持的 ``Content-Type`` 统一归为 ``400 invalid_request``\ （其他端点会返回 ``413`` / ``415``\ ）。

.. note::

   登录和密码修改的速率限制可通过以下属性进行配置（括号内为默认值）：

   - ``theme.api.login.rate.limit.per.ip.per.minute`` (``10``): 每个 IP 地址每分钟的最大尝试次数。仅适用于 ``/auth/login``\ 。
   - ``theme.api.login.rate.limit.per.user.per.minute`` (``5``): 每个用户每分钟的最大尝试次数。适用于 ``/auth/login`` 和 ``/auth/password``\ 。
   - ``theme.api.login.lockout.seconds`` (``900``): 超过限制后的锁定时长（秒）。作为 ``Retry-After`` 头的值返回。

请求体 (LoginRequest)
~~~~~~~~~~~~~~~~~~~~~

Content-Type 为 ``application/json``\ （字符集 UTF-8）。请求体大小上限为 4 KiB。

.. tabularcolumns:: |p{3cm}|p{2cm}|p{2cm}|p{7cm}|
.. list-table:: LoginRequest
   :header-rows: 1
   :widths: 20 12 12 56

   * - 字段
     - 类型
     - 必填
     - 说明
   * - ``username``
     - string
     - 是
     - 用户名。\ ``minLength`` 为 1。
   * - ``password``
     - string
     - 是
     - 密码。\ ``minLength`` 为 1。
   * - ``return_to``
     - string
     - 否
     - 登录后的重定向目标。须为符合上述格式的相对路径。

请求示例：

.. code-block:: json

    {
      "username": "taro",
      "password": "secret",
      "return_to": "/search"
    }

响应
----

成功时（HTTP 200，LoginResponse），返回如下公共信封格式的响应。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "user": {
          "user_id": "taro",
          "username": "taro",
          "name": "taro",
          "roles": ["admin"],
          "groups": [],
          "permissions": ["1taro"],
          "editable": true,
          "admin": true
        },
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f",
        "return_to": "/search"
      }
    }

``response`` 各元素说明如下。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 响应信息
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 类型
     - 说明
   * - ``user``
     - object
     - :ref:`UserPayload <api-auth-userpayload>`。
   * - ``csrf_token``
     - string
     - 与新会话绑定的新 CSRF 令牌。（必填）
   * - ``return_to``
     - string
     - 仅当请求值通过允许列表时才回显。

错误响应
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应
   :header-rows: 1
   :widths: 25 75

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求不合法时（包括过大的请求体或不支持的 ``Content-Type``\ ）。
   * - 401 Unauthorized
     - 认证信息不正确时。
   * - 405 Method Not Allowed
     - 指定了不支持的 HTTP 方法时。
   * - 429 Too Many Requests
     - 超过速率限制时。\ ``Retry-After`` 头中会指示需要等待的秒数。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

注销
====

请求
----

==================  ====================================================
HTTP 方法            POST
端点                 ``/api/v2/auth/logout``
==================  ====================================================

注销。此操作是幂等的，即使没有活动会话也会返回 no-op 而不报错。始终返回 ``ok: true``\ 。

需要携带 ``X-Fess-CSRF-Token`` 头。

响应
----

成功时（HTTP 200，OkResponse），返回如下公共信封格式的响应。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true
      }
    }

``response`` 各元素说明如下。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 响应信息
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 类型
     - 说明
   * - ``ok``
     - boolean
     - 始终为 ``true``\ 。（必填）

错误响应
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应
   :header-rows: 1
   :widths: 25 75

   * - 状态码
     - 说明
   * - 403 Forbidden
     - CSRF 令牌缺失或过期时。
   * - 405 Method Not Allowed
     - 指定了 POST 以外的方法时。响应中附带 ``Allow: POST`` 头。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。

修改密码
========

请求
----

==================  ====================================================
HTTP 方法            POST
端点                 ``/api/v2/auth/password``
==================  ====================================================

修改当前用户的密码。
验证 ``current_password``\ ，对 ``new_password`` 应用已配置的密码策略，使当前会话失效，并通过 ``re_login_required: true`` 提示 SPA 重定向至登录页面。

由于会话在服务端被销毁，因此不返回 ``csrf_token``\ 。SPA 须在重新认证后获取新的令牌。

需要携带 ``X-Fess-CSRF-Token`` 头。

本端点应用用户单位速率限制；超过限制时，返回 ``429 Too Many Requests`` 并附带 ``Retry-After`` 头（设置与登录共用）。

请求体 (PasswordChangeRequest)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Content-Type 为 ``application/json``\ （字符集 UTF-8）。请求体大小上限为 4 KiB。

.. tabularcolumns:: |p{3.5cm}|p{2cm}|p{2cm}|p{6.5cm}|
.. list-table:: PasswordChangeRequest
   :header-rows: 1
   :widths: 22 12 12 54

   * - 字段
     - 类型
     - 必填
     - 说明
   * - ``current_password``
     - string
     - 是
     - 当前密码。\ ``minLength`` 为 1。
   * - ``new_password``
     - string
     - 是
     - 新密码。须满足已配置的密码策略（默认最少 8 个字符）。\ ``minLength`` 为 1。
   * - ``confirm_password``
     - string
     - 是
     - 确认密码。须与 ``new_password`` 一致。\ ``minLength`` 为 1。

响应
----

成功时（HTTP 200），返回如下公共信封格式的响应。

.. code-block:: json

    {
      "response": {
        "status": 0,
        "ok": true,
        "re_login_required": true
      }
    }

``response`` 各元素说明如下。

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: 响应信息
   :header-rows: 1
   :widths: 25 15 60

   * - 字段
     - 类型
     - 说明
   * - ``ok``
     - boolean
     - 始终为 ``true``\ 。（必填）
   * - ``re_login_required``
     - boolean
     - 始终为 ``true``\ 。当前会话已在服务端失效。SPA 须重定向至登录页面以获取新的会话和 CSRF 令牌。（必填）

错误响应
--------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: 错误响应
   :header-rows: 1
   :widths: 25 75

   * - 状态码
     - 说明
   * - 400 Bad Request
     - 请求不合法时。
   * - 401 Unauthorized
     - 需要认证，或 ``current_password`` 不正确时。
   * - 403 Forbidden
     - CSRF 令牌缺失或过期时。
   * - 405 Method Not Allowed
     - 指定了不支持的 HTTP 方法时。
   * - 413 Payload Too Large
     - 请求体超过大小限制时。
   * - 415 Unsupported Media Type
     - 不支持的 ``Content-Type`` 时。
   * - 429 Too Many Requests
     - 超过速率限制时。
   * - 500 Internal Server Error
     - 发生服务器内部错误时。
