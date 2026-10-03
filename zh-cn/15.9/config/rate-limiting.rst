==================================
速率限制配置
==================================

概述
====

|Fess| 具有速率限制功能，用于维护系统的稳定性和性能。
通过此功能，可以保护系统免受过度请求的影响，实现公平的资源分配。

速率限制适用于以下场景:

- 包括搜索API和AI搜索模式API在内的所有HTTP请求（``RateLimitFilter``）
- 爬虫请求（通过爬取设置进行控制）

HTTP请求的速率限制
==========================

可以按IP地址单位限制对 |Fess| 的HTTP请求数。
此限制适用于搜索API、AI搜索模式API、管理界面等所有HTTP请求。

设置
----

``app/WEB-INF/classes/fess_config.properties``:

::

    # 启用速率限制（默认: false）
    rate.limit.enabled=true

    # 每个IP地址每个窗口的最大请求数（默认: 100）
    rate.limit.requests.per.window=100

    # 窗口大小（毫秒）（默认: 60000）
    rate.limit.window.ms=60000

行为
----

- 超过速率限制的请求返回HTTP 429 (Too Many Requests)
- 因超过限制而被阻止的IP地址，以及阻止IP列表中的IP地址的请求返回HTTP 403 (Forbidden)
- 响应体为JSON（429 为 ``{"error":"rate_limit_exceeded",...,"retry_after":60}`` ，403 为 ``{"error":"ip_blocked",...}`` ）。429 附带 ``Retry-After`` 头
- 限制按IP地址单位应用
- 每个IP从首次请求开始计算窗口，窗口期间过后计数重置（固定窗口方式）
- 超过限制时，IP会被阻止 ``rate.limit.block.duration.ms`` 的期间

AI搜索模式的速率限制
====================

AI搜索模式功能具有速率限制，用于控制LLM API的成本和资源消耗。
AI搜索模式除了上述HTTP请求速率限制外，还可以设置AI搜索模式固有的速率限制。

AI搜索模式固有的速率限制设置请参阅 :doc:`rag-chat`。

.. note::
   AI搜索模式的速率限制与LLM提供商端的速率限制分别应用。
   请同时考虑两者的限制进行设置。

爬虫的速率限制
======================

可以设置请求间隔，以避免爬虫对目标站点造成过度负载。

Web爬取设置
---------------

在管理界面的「爬虫」→「Web」中设置以下内容:

- **请求间隔**: 请求间的等待时间（毫秒）
- **线程数**: 并行爬取线程数

推荐设置:

::

    # 一般站点
    intervalTime=1000
    numOfThread=1

    # 大型站点（有授权时）
    intervalTime=500
    numOfThread=3

遵守robots.txt
----------------

|Fess| 默认遵守robots.txt的Crawl-delay指令。

::

    # robots.txt示例
    User-agent: *
    Crawl-delay: 10

robots.txt的处理由 ``app/WEB-INF/classes/fess_config.properties`` 中的 ``crawler.ignore.robots.txt`` 控制（默认值: ``false``）。
将其设置为 ``true`` 可禁用robots.txt的处理，包括Crawl-delay的遵守。

::

    # 忽略robots.txt（默认: false）
    crawler.ignore.robots.txt=false

Crawl-delay 按访问目标（源）分别应用，上限为 60 秒。等待以 URL 为单位进行，因此在增量爬取中，对同一个 URL 发送的 HEAD 和 GET 会连续发送。爬取配置的“间隔”与此分开，作为到下一个 URL 之前的等待时间生效。

robots.txt 按照 RFC 9309 解释。 ``Allow:`` 和 ``Disallow:`` 以最长匹配的规则优先，起始 URL 也会根据 robots.txt 进行检查。被 robots.txt 禁止的 URL 会以 INFO 级别记录到 ``fess-crawler.log``\ ，不会登记为故障 URL。

429/503 响应时的退避
--------------------

当服务器返回 ``429 Too Many Requests`` 或 ``503 Service Unavailable`` 时，会暂时停止对该源的访问，并最多重试该 URL 3 次。等待时间在有 ``Retry-After`` 头时为该值，否则为从 10 秒开始的指数增长时间（最长 5 分钟）。最后一次重试也失败时，会在 ``fess-crawler.log`` 中输出 WARN。

无法获取 robots.txt 时
----------------------

当获取 robots.txt 因 5xx、429 或超时等失败时，该源的 URL 会被放回队列，直到退避结束。首次失败后再重试 3 次仍失败时，在本次爬取期间该源的所有 URL 都不会被爬取，并会在 ``fess-crawler.log`` 中输出一次 WARN。15.8 及更早版本会将无法获取的 robots.txt 一律视为允许。要恢复该行为，请在 Web 爬取配置的“配置参数”中指定以下内容。

::

    client.robotsTxtAllowOnUnavailable=true

要完全禁用 robots.txt 处理，请使用 ``client.robotsTxtEnabled=false`` （按爬取配置）或 ``crawler.ignore.robots.txt=true``\ 。

速率限制的全部配置项
======================

``app/WEB-INF/classes/fess_config.properties`` 中可配置的所有属性。

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - 属性
     - 说明
     - 默认值
   * - ``rate.limit.enabled``
     - 启用速率限制
     - ``false``
   * - ``rate.limit.requests.per.window``
     - 每个窗口的最大请求数
     - ``100``
   * - ``rate.limit.window.ms``
     - 窗口大小（毫秒）
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - 超过限制时的IP阻止期间（毫秒）
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Retry-After响应头的值（秒）
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - 从速率限制中排除的IP地址（逗号分隔）
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - 要阻止的IP地址（逗号分隔）
     - （空）
   * - ``rate.limit.trusted.proxies``
     - 信任的代理IP（从X-Forwarded-For/X-Real-IP获取客户端IP）
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - 清理间隔（请求数，预留）
     - ``1000``

.. note::
   ``rate.limit.cleanup.interval`` 是为将来使用而预留的设置项。
   在当前实现中，请求计数器和被阻止的IP信息会根据内部缓存过期时间（``rate.limit.window.ms`` 和 ``rate.limit.block.duration.ms``）自动清理，因此该值不会被使用。

高级速率限制设置
====================

自定义速率限制
------------------

要根据特定条件应用不同的速率限制逻辑，
需要实现自定义组件。

::

    // RateLimitHelper自定义示例
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // 自定义逻辑
        }
    }

排除设置
========

可以将特定IP地址从速率限制中排除或阻止。

::

    # 白名单IP（从速率限制中排除，逗号分隔）
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # 阻止IP列表（始终阻止，逗号分隔）
    rate.limit.blocked.ips=203.0.113.50

    # 信任的代理IP（逗号分隔）
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   使用反向代理时，请将代理的IP地址设置在 ``rate.limit.trusted.proxies`` 中。
   仅从信任的代理发出的请求，才会从X-Forwarded-For和X-Real-IP头获取客户端IP。

监控与告警
==============

用于监控速率限制状况的设置:

日志输出
--------

应用速率限制时，会记录在日志中:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

故障排除
======================

正常请求被阻止
--------------------------------

**原因**: 限制值过于严格

**解决方法**:

1. 增加 ``rate.limit.requests.per.window``
2. 将特定IP添加到白名单（``rate.limit.whitelist.ips``）
3. 调整窗口大小（``rate.limit.window.ms``）

速率限制不生效
--------------------

**原因**: 设置未正确生效

**确认事项**:

1. 是否设置了 ``rate.limit.enabled=true``
2. 配置文件是否正确加载
3. 是否重启了 |Fess|

性能影响
----------------------

速率限制检查本身影响性能时:

1. 利用白名单跳过信任IP的检查
2. 禁用速率限制（``rate.limit.enabled=false``）

参考信息
========

- :doc:`rag-chat` - AI搜索模式功能配置
- :doc:`../admin/webconfig-guide` - Web爬取配置指南
- :doc:`../api/api-overview` - API概述
