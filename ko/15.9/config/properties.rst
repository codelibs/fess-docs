=============================
Fess Configuration Properties
=============================

Every configuration property Fess reads, with its description and its default value.
The values themselves live in ``fess_config.properties``; see :doc:`crawler-advanced`
for how to override them.

The tables below are generated from ``fess_config.properties``. To correct a
description, change the comment above the property in the Fess repository. To translate
one, fill in ``properties.po`` beside this file.

.. GENERATED-BEGIN: properties -- from fess_config.properties via tools/update_properties_doc.sh
.. DO NOT EDIT. Descriptions and headings come from fess_config.properties in the
.. fess repository; translations come from properties.po beside this file.
.. Regenerate with tools/update_properties_doc.sh.

코어
----

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - domain.title
    - 로깅과 표시에 사용하는 도메인의 제목.
    - ``Fess``

.. list-table:: 검색 엔진
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - search_engine.type
    - 검색 엔진 백엔드의 유형입니다. 사용 가능한 값: default(CodeLibs 플러그인이 있는 OpenSearch), vanilla(CodeLibs 플러그인이 없는 OpenSearch), aws(AWS 전용 처리를 더한 vanilla). cloud는 vanilla의 지원 중단 예정 별칭입니다.
    - ``default``
  * - search_engine.http.url
    - 검색 엔진 HTTP 엔드포인트의 URL입니다. IPv6 환경에서는 IPv6 주소를 대괄호로 감싸십시오(예: http://[::1]:9200)
    - ``http://localhost:9200``
  * - search_engine.http.ssl.certificate_authorities
    - 보안 HTTP 연결에 사용하는 SSL 인증 기관의 경로.
    - (empty)
  * - search_engine.username
    - 검색 엔진 인증에 사용하는 사용자 이름.
    - (empty)
  * - search_engine.password
    - 검색 엔진 인증에 사용하는 비밀번호.
    - (empty)
  * - search_engine.heartbeat_interval
    - 검색 엔진에 대한 하트비트 확인 간격(밀리초).
    - ``10000``
  * - app.cipher.algorithm
    - 암호화에 사용하는 암호 알고리즘.
    - ``aes``
  * - app.cipher.key
    - 암호화용 비밀 키(운영 환경에서는 이 값을 변경하십시오).
    - ``___change__me___``
  * - app.digest.algorithm
    - 다이제스트 계산용 알고리즘.
    - ``sha256``
  * - app.password.algorithm
    - 비밀번호 해싱(새로운 방식, Spring Security v5.8 호환) 지원: bcrypt(현 시점에서는 bcrypt만)
    - ``bcrypt``
  * - app.password.bcrypt.cost
    - BCrypt 코스트(로그 라운드)입니다. 10은 Spring Security v5.8의 기본값과 같습니다. 범위: 4-31.
    - ``10``
  * - app.password.upgrade.enabled
    - 레거시 해시에 대해 로그인 성공 시 수행하는 지연 재해싱.
    - ``true``
  * - app.encrypt.property.pattern
    - 참고: app.digest.algorithm 은 레거시 비밀번호 검증 전용으로 유지됩니다(업그레이드 이전의 {id} 접두사가 없는 해시). 새 비밀번호에는 사용하지 마십시오. 암호화할 프로퍼티의 정규 표현식 패턴입니다.
    - ``.*password|.*key|.*token|.*secret``
  * - app.log.sensitive.property.pattern
    - 디버그 로그에서 마스킹할 민감한 값의 정규 표현식 패턴(프로퍼티/환경 변수 키에 대해 대소문자를 구분하지 않고 일치 판정).
    - ``.*password.*|.*secret.*|.*key.*|.*token.*|.*credential.*|.*auth.*|.*private.*``
  * - app.extension.names
    - 애플리케이션 커스터마이즈용 확장 이름.
    - (empty)
  * - app.audit.log.format
    - 감사 로그 형식.
    - (empty)
  * - script.audit.log.enabled
    - 스크립트 감사 로그 설정.
    - ``true``
  * - script.audit.log.max.length
    - 스크립트 감사 로그 항목에 보관하는 스크립트 텍스트의 최대 문자 수이며, 이보다 긴 텍스트는 잘립니다.
    - ``100``
  * - jvm.crawler.options
    - 크롤러 프로세스용 JVM 옵션.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Dhttp.maxConnections=20``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx512m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:-OmitStackTraceInFastThrow``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=5``
      | ``-Djcifs.client.responseTimeout=30000``
      | ``-Djcifs.client.soTimeout=35000``
      | ``-Djcifs.client.connTimeout=60000``
      | ``-Djcifs.client.sessionTimeout=60000``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j.skipJansi=true``
      | ``-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider``
      | ``-Dorg.apache.pdfbox.rendering.UsePureJavaCMYKConversion=true``
  * - jvm.suggest.options
    - 서제스트 생성기 자식 프로세스에 전달하는 JVM 옵션(줄바꿈 구분).
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx256m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=30``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
  * - jvm.chunk.options
    - 청크 벡터 인덱서 프로세스용 JVM 옵션입니다. 힙 예산. 이 자식 JVM은 "Content Chunk Vector Indexer" 작업이 실행되는 동안에만 시작되므로, 콘텐츠 청킹이 꺼져 있으면 넉넉한 -Xmx를 지정해도 비용이 들지 않습니다. 라이브 세트는 처리 중인 배치가 대부분을 차지하며, 각 배치는 문서마다 전체 _source, 문서의 청크 문자열, 문서의 임베딩 벡터를 유지합니다: content_chunker.job.bulk_size (기본값 20) x content_chunker.max_chunks_per_document (기본값 1000) x content_chunker.embedding.dimension (기본값 768) x float당 4바이트 x content_chunker.job.concurrency (기본값 2) = 청크 문자열과 문서 소스를 제외하고 벡터만으로 약 117 MB입니다. 제공되는 기본값에서 최악의 경우 라이브 세트는 약 190-250 MB이며(dimension=1536에서는 벡터만으로 약 235 MB), 이는 GC 여유를 두면 256 MB 힙에 들어가지 않습니다. bulk_size, max_chunks_per_document, concurrency 또는 임베딩 차원을 올리는 경우에는 -Xmx를 더 올리십시오.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx1g``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=30``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
  * - jvm.thumbnail.options
    - 썸네일 프로세스용 JVM 옵션.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx256m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:-OmitStackTraceInFastThrow``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=4m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=50``
      | ``-Djcifs.client.responseTimeout=30000``
      | ``-Djcifs.client.soTimeout=35000``
      | ``-Djcifs.client.connTimeout=60000``
      | ``-Djcifs.client.sessionTimeout=60000``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
      | ``-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider``
      | ``-Dorg.apache.pdfbox.rendering.UsePureJavaCMYKConversion=true``

.. list-table:: 작업
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - job.system.job.ids
    - 스케줄된 작업의 시스템 작업 ID.
    - ``default_crawler``
  * - job.template.title.web
    - 웹 크롤러 작업 제목 템플릿.
    - ``Web Crawler - {0}``
  * - job.template.title.file
    - 파일 크롤러 작업 제목 템플릿.
    - ``File Crawler - {0}``
  * - job.template.title.data
    - 데이터 크롤러 작업 제목 템플릿.
    - ``Data Crawler - {0}``
  * - job.template.script
    - 작업 실행용 스크립트 템플릿.
    - ``return container.getComponent("crawlJob").logLevel("info").webConfigIds([{0}]).fileConfigIds([{1}]).dataConfigIds([{2}]).jobExecutor(executor).execute();``
  * - job.max.crawler.processes
    - 크롤러 프로세스의 최대 수.
    - ``0``
  * - job.default.script
    - 작업의 기본 스크립트 언어.
    - ``javascript``
  * - job.system.property.filter.pattern
    - 작업용 시스템 프로퍼티를 필터링하는 패턴.
    - (empty)
  * - processors
    - 사용할 프로세서 수.
    - ``0``
  * - java.command.path
    - Java 명령의 경로.
    - ``java``
  * - python.command.path
    - Python 명령의 경로.
    - ``python``
  * - path.encoding
    - 파일 경로의 인코딩.
    - ``UTF-8``
  * - use.own.tmp.dir
    - 전용 임시 디렉터리 사용 여부.
    - ``true``
  * - max.log.output.length
    - 로그 출력의 최대 길이.
    - ``4000``
  * - adaptive.load.control
    - 적응형 부하 제어 값.
    - ``50``
  * - web.load.control
    - 웹 요청 부하 제어용 CPU 임계값(%)입니다. CPU가 이 값 이상이면 429를 반환합니다. (100: 비활성화)
    - ``100``
  * - api.load.control
    - API 요청 부하 제어용 CPU 임계값(%)입니다. CPU가 이 값 이상이면 429를 반환합니다. (100: 비활성화)
    - ``100``
  * - load.control.monitor.interval
    - OpenSearch CPU 부하를 모니터링하는 간격(초).
    - ``1``
  * - supported.languages
    - 지원하는 언어.
    - ``ar,bg,bn,ca,ckb_IQ,cs,da,de,el,en_IE,en,es,et,eu,fa,fi,fr,gl,gu,he,hi,hr,hu,hy,id,it,ja,ko,lt,lv,mk,ml,nl,no,pa,pl,pt_BR,pt,ro,ru,si,sq,sv,ta,te,th,tl,tr,uk,ur,vi,zh_CN,zh_TW,zh``
  * - api.access.token.length
    - API 액세스 토큰의 길이.
    - ``60``
  * - api.access.token.request.parameter
    - API 액세스 토큰 요청 파라미터.
    - (empty)
  * - api.admin.access.permissions
    - API 관리 액세스용 권한.
    - ``Radmin-api``
  * - api.search.accept.referers
    - API 검색에서 허용하는 리퍼러.
    - (empty)
  * - api.search.scroll
    - API 검색의 스크롤 활성화 여부.
    - ``false``
  * - api.search.export
    - /api/v2/documents/export 에서 최종 사용자가 검색 결과(CSV/JSON)를 내보내는 기능의 활성화 여부.
    - ``false``
  * - api.search.export.max.size
    - 검색 결과 내보내기 1회에서 출력하는 문서의 최대 수.
    - ``1000``
  * - api.search.export.fields
    - 검색 결과 내보내기에서 출력하는 필드(쉼표 구분)입니다. API 응답 필드가 아닌 필드는 무시됩니다.
    - ``title,url_link,last_modified,content_length,filetype``
  * - api.search.export.rate.limit.per.minute
    - 사용자별(게스트는 클라이언트 IP별) 1분당 검색 결과 내보내기의 최대 횟수입니다. 0 이하이면 제한이 비활성화됩니다.
    - ``10``
  * - api.json.response.headers
    - API JSON 응답용 헤더입니다. Access-Control-\* 및 Timing-Allow-Origin 은 여기서 무시됩니다(CORS는 api.cors.\* / CorsFilter 로 제어됩니다). Vary는 설정하지 마십시오.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.json.response.exception.included
    - API JSON 응답의 예외 포함 여부.
    - ``false``
  * - api.gsa.response.headers
    - API GSA 응답용 헤더입니다. Access-Control-\* 및 Timing-Allow-Origin 은 여기서 무시됩니다(CORS는 api.cors.\* / CorsFilter 로 제어됩니다). Vary는 설정하지 마십시오.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.gsa.response.exception.included
    - API GSA 응답의 예외 포함 여부.
    - ``false``
  * - api.dashboard.response.headers
    - API 대시보드 응답용 헤더입니다. Access-Control-\* 및 Timing-Allow-Origin 은 여기서 무시됩니다(CORS는 api.cors.\* / CorsFilter 로 제어됩니다). Vary는 설정하지 마십시오.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.cors.allow.origin
    - CORS에서 허용하는 오리진입니다. "\*"를 지정하면 리터럴 "\*"를 반환하며(요청의 Origin은 결코 반영되지 않습니다) 자격 증명이 비활성화됩니다. 자격 증명을 포함한 크로스 오리진 액세스를 허용하려면 명시적인 오리진(줄바꿈 또는 쉼표 구분)을 지정하십시오.
    - ``*``
  * - api.cors.allow.methods
    - CORS에서 허용하는 HTTP 메서드.
    - ``GET, POST, OPTIONS, DELETE, PUT``
  * - api.cors.max.age
    - CORS 프리플라이트 요청의 최대 유효 기간.
    - ``3600``
  * - api.cors.allow.headers
    - CORS 프리플라이트에서 허용하는 요청 헤더입니다. 고정 목록을 반환합니다(Access-Control-Request-Headers는 반영되지 않습니다). CSRF 토큰을 보내는 크로스 오리진 SPA를 위해 X-Fess-CSRF-Token을 포함합니다.
    - ``Origin, Content-Type, Accept, Authorization, X-Requested-With, X-Fess-CSRF-Token``
  * - api.cors.allow.credentials
    - CORS 자격 증명 허용 여부입니다. 명시적인 Origin과 정확히 일치하는 경우에만 적용되며, api.cors.allow.origin 이 "\*"이면 무시됩니다.
    - ``true``
  * - api.jsonp.enabled
    - API의 JSONP 활성화 여부.
    - ``false``
  * - api.ping.search_engine.fields
    - 검색 엔진으로의 API ping용 필드.
    - ``status,timed_out``

속도 제한
---------

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rate.limit.enabled
    - 속도 제한 활성화 여부.
    - ``false``
  * - rate.limit.requests.per.window
    - 윈도우당 허용되는 최대 요청 수.
    - ``100``
  * - rate.limit.window.ms
    - 윈도우 크기(밀리초).
    - ``60000``
  * - rate.limit.block.duration.ms
    - 제한 초과 시 IP를 블록하는 기간(밀리초).
    - ``300000``
  * - rate.limit.retry.after.seconds
    - Retry-After 헤더 값(초).
    - ``60``
  * - rate.limit.whitelist.ips
    - 화이트리스트에 등록된 IP의 쉼표 구분 목록(예: 127.0.0.1,::1).
    - ``127.0.0.1,::1``
  * - rate.limit.blocked.ips
    - 블록된 IP의 쉼표 구분 목록.
    - (empty)
  * - rate.limit.trusted.proxies
    - 신뢰하는 프록시 IP의 쉼표 구분 목록입니다. 이 IP로부터 오는 X-Forwarded-For/X-Real-IP만 신뢰합니다.
    - ``127.0.0.1,::1``
  * - rate.limit.cleanup.interval
    - 메모리 누수를 방지하기 위한 클린업 작업 간의 요청 수.
    - ``1000``
  * - virtual.host.headers
    - 가상 호스트: Host:fess.codelibs.org=fess
    - (empty)
  * - http.proxy.host
    - HTTP 프록시 서버의 호스트명.
    - (empty)
  * - http.proxy.port
    - HTTP 프록시 서버의 포트 번호(예: 8080).
    - ``8080``
  * - http.proxy.username
    - HTTP 프록시 인증용 사용자 이름.
    - (empty)
  * - http.proxy.password
    - HTTP 프록시 인증용 비밀번호.
    - (empty)
  * - http.fileupload.max.size
    - HTTP 파일 업로드의 최대 크기(바이트).
    - ``262144000``
  * - http.fileupload.threshold.size
    - HTTP 파일 업로드 버퍼링의 임계 크기(바이트).
    - ``262144``
  * - http.fileupload.max.file.count
    - HTTP 업로드 1회당 허용되는 최대 파일 수.
    - ``10``

인덱스
------

.. list-table:: 크롤러 공통
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.http.thread_pool.size
    - HTTP 크롤링용 스레드 수.
    - ``0``
  * - crawler.data.serializer
    - 크롤러 데이터의 시리얼라이저 타입(예: kryo).
    - ``kryo``
  * - crawler.document.max.site.length
    - 문서 내 사이트 이름의 최대 길이.
    - ``100``
  * - crawler.document.site.encoding
    - 문서 내 사이트 이름의 인코딩.
    - ``UTF-8``
  * - crawler.document.unknown.hostname
    - 문서에서 호스트명을 알 수 없을 때 사용하는 호스트명.
    - ``unknown``
  * - crawler.document.use.site.encoding.on.english
    - 영어 문서의 사이트 인코딩 사용 여부.
    - ``false``
  * - crawler.document.append.data
    - 문서에 데이터 추가 여부.
    - ``true``
  * - crawler.document.append.filename
    - 문서에 파일명 추가 여부.
    - ``false``
  * - crawler.document.max.alphanum.term.size
    - 문서 내 영숫자 단어의 최대 크기.
    - ``20``
  * - crawler.document.max.symbol.term.size
    - 문서 내 기호 단어의 최대 크기.
    - ``10``
  * - crawler.document.duplicate.term.removed
    - 문서 내 중복 단어 제거 여부.
    - ``false``
  * - crawler.document.space.chars
    - 문서 파싱용 유니코드 공백 문자.
    - ``u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6``
  * - crawler.document.fullstop.chars
    - 문서 파싱용 유니코드 마침표 문자.
    - ``u002eu06d4u2e3cu3002``
  * - crawler.crawling.data.encoding
    - 크롤링 데이터의 인코딩.
    - ``UTF-8``
  * - crawler.web.protocols
    - 크롤링에서 지원하는 웹 프로토콜.
    - ``http,https``
  * - crawler.file.protocols
    - 크롤링에서 지원하는 파일 프로토콜.
    - ``file,smb,smb1,ftp``
  * - crawler.data.env.param.key.pattern
    - 크롤링 데이터 내 환경 변수 키의 패턴.
    - ``^FESS_ENV_.*``
  * - crawler.ignore.robots.txt
    - 크롤링 중 robots.txt 무시 여부.
    - ``false``
  * - crawler.ignore.robots.tags
    - 크롤링 중 robots 메타 태그 무시 여부.
    - ``false``
  * - crawler.ignore.content.exception
    - 크롤링 중 콘텐츠 예외 무시 여부.
    - ``true``
  * - crawler.failure.url.status.codes
    - 장애 URL로 간주하는 HTTP 상태 코드.
    - ``404,403,410``
  * - crawler.system.monitor.interval
    - 크롤링 중 시스템 모니터링 간격(초).
    - ``60``
  * - crawler.hotthread.ignore_idle_threads
    - 핫 스레드 모니터링에서 유휴 스레드 무시 여부.
    - ``true``
  * - crawler.hotthread.interval
    - 핫 스레드 모니터링 간격(예: 500ms).
    - ``500ms``
  * - crawler.hotthread.snapshots
    - 핫 스레드 모니터링의 스냅샷 수.
    - ``10``
  * - crawler.hotthread.threads
    - 핫 스레드 모니터링의 스레드 수.
    - ``3``
  * - crawler.hotthread.timeout
    - 핫 스레드 모니터링의 타임아웃(예: 30s).
    - ``30s``
  * - crawler.hotthread.type
    - 핫 스레드 모니터링의 타입(예: cpu).
    - ``cpu``
  * - crawler.metadata.content.excludes
    - 문서 콘텐츠에서 제외할 메타데이터 필드.
    - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*``
  * - crawler.metadata.name.mapping
    - 문서 메타데이터 이름의 매핑.
    - | ``title=title:string``
      | ``Title=title:string``
      | ``dc:title=title:string``
      | ``frontmatter.title=title:string``

.. list-table:: 크롤러 HTML
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.html.content.xpath
    - HTML 문서에서 주요 콘텐츠를 추출하는 XPath.
    - ``//BODY``
  * - crawler.document.html.lang.xpath
    - HTML 문서에서 언어 속성을 추출하는 XPath.
    - ``//HTML/@lang``
  * - crawler.document.html.digest.xpath
    - HTML 문서에서 다이제스트(설명)를 추출하는 XPath.
    - ``//META[@name='description']/@content``
  * - crawler.document.html.canonical.xpath
    - HTML 문서에서 표준 URL을 추출하는 XPath.
    - ``//LINK[@rel='canonical'][1]/@href``
  * - crawler.document.html.pruned.tags
    - 문서 처리 중에 프루닝(제거)할 HTML 태그.
    - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
  * - crawler.document.html.max.digest.length
    - HTML 문서에서 추출하는 다이제스트의 최대 길이.
    - ``120``
  * - crawler.document.html.default.lang
    - HTML 문서의 기본 언어.
    - (empty)
  * - crawler.document.html.default.include.index.patterns
    - HTML 인덱스 처리에 포함할 패턴.
    - (empty)
  * - crawler.document.html.default.exclude.index.patterns
    - HTML 인덱스 처리에서 제외할 패턴.
    - ``(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)``
  * - crawler.document.html.default.include.search.patterns
    - HTML 검색 처리에 포함할 패턴.
    - (empty)
  * - crawler.document.html.default.exclude.search.patterns
    - HTML 검색 처리에서 제외할 패턴.
    - (empty)

.. list-table:: 크롤러 파일
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.file.name.encoding
    - 문서 내 파일명의 인코딩.
    - (empty)
  * - crawler.document.file.no.title.label
    - 파일에 제목이 없을 때 사용하는 라벨.
    - ``No title.``
  * - crawler.document.file.ignore.empty.content
    - 내용이 빈 파일 무시 여부.
    - ``false``
  * - crawler.document.file.max.title.length
    - 문서 내 파일 제목의 최대 길이.
    - ``100``
  * - crawler.document.file.max.digest.length
    - 문서 내 파일 다이제스트의 최대 길이.
    - ``200``
  * - crawler.document.file.append.meta.content
    - 파일의 메타 콘텐츠 추가 여부.
    - ``true``
  * - crawler.document.file.append.body.content
    - 파일의 본문 콘텐츠 추가 여부.
    - ``true``
  * - crawler.document.file.default.lang
    - 파일 문서의 기본 언어.
    - (empty)
  * - crawler.document.file.default.include.index.patterns
    - 파일 인덱스 처리에 포함할 패턴.
    - (empty)
  * - crawler.document.file.default.exclude.index.patterns
    - 파일 인덱스 처리에서 제외할 패턴.
    - (empty)
  * - crawler.document.file.default.include.search.patterns
    - 파일 검색 처리에 포함할 패턴.
    - (empty)
  * - crawler.document.file.default.exclude.search.patterns
    - 파일 검색 처리에서 제외할 패턴.
    - (empty)
  * - crawler.document.file.owner.enabled
    - 크롤링한 파일(SMB, 로컬 파일 시스템, FTP)의 소유자를 인덱싱할지 여부입니다. 크롤링 설정 파라미터 config.owner.enabled 가 이를 오버라이드합니다.
    - ``true``
  * - crawler.document.file.last.modifier.enabled
    - 크롤링한 파일의 최종 수정자를 인덱싱할지 여부입니다. 문서 메타데이터에서 읽으며, 없으면 파일 소유자로 폴백합니다. 크롤링 설정 파라미터 config.last.modifier.enabled 가 이를 오버라이드합니다.
    - ``true``

.. list-table:: 크롤러 캐시
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.cache.enabled
    - 문서 캐시 활성화 여부.
    - ``true``
  * - crawler.document.cache.max.size
    - 문서 캐시의 최대 크기(바이트).
    - ``2621440``
  * - crawler.document.cache.supported.mimetypes
    - 문서 캐시에서 지원하는 MIME 타입.
    - ``text/html``
  * - crawler.document.cache.html.mimetypes
    - ,text/plain,application/xml,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation HTML 문서 캐시용 MIME 타입.
    - ``text/html``
  * - crawler.document.mimetype.extension.overrides
    - MIME 타입 감지를 위한 확장자에서 MIME 타입으로의 오버라이드 매핑(한 줄에 하나: .ext=mime/type).
    - (empty)
  * - crawler.document.ocr.enabled
    - Tesseract OCR로 이미지와 스캔한 PDF에서 텍스트를 추출할지 여부(tesseract 명령 필요).
    - ``false``
  * - crawler.document.ocr.language
    - '+'로 연결한 Tesseract OCR 언어(예: jpn+eng).
    - ``eng``
  * - crawler.document.ocr.timeout
    - Tesseract OCR 1회 실행의 타임아웃(초).
    - ``120``

.. list-table:: 인덱서
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - indexer.thread.dump.enabled
    - 인덱서의 스레드 덤프 활성화 여부.
    - ``true``
  * - indexer.unprocessed.document.size
    - 인덱서의 미처리 문서 최대 수.
    - ``1000``
  * - indexer.click.count.enabled
    - 인덱서의 클릭 수 추적 활성화 여부.
    - ``true``
  * - indexer.favorite.count.enabled
    - 인덱서의 즐겨찾기 수 추적 활성화 여부.
    - ``true``
  * - indexer.webfs.commit.margin.time
    - 인덱서의 webfs용 커밋 마진 시간(밀리초).
    - ``5000``
  * - indexer.webfs.max.empty.list.count
    - 인덱서의 webfs용 빈 목록의 최대 수.
    - ``3600``
  * - indexer.webfs.update.interval
    - 인덱서의 webfs용 업데이트 간격(밀리초).
    - ``10000``
  * - indexer.webfs.max.document.cache.size
    - 인덱서의 webfs용 문서 캐시 최대 크기.
    - ``10``
  * - indexer.webfs.max.document.request.size
    - 인덱서의 webfs용 문서 요청 최대 크기(바이트).
    - ``1048576``
  * - indexer.data.max.document.cache.size
    - 인덱서의 데이터용 문서 캐시 최대 크기.
    - ``10000``
  * - indexer.data.max.document.request.size
    - 인덱서의 데이터용 문서 요청 최대 크기(바이트).
    - ``1048576``
  * - indexer.data.max.delete.cache.size
    - 인덱서의 데이터용 삭제 캐시 최대 크기.
    - ``100``
  * - indexer.data.max.redirect.count
    - 인덱서의 데이터용 최대 리디렉션 횟수.
    - ``10``
  * - indexer.language.fields
    - 인덱서에서 언어 감지에 사용하는 필드.
    - ``content,important_content,title``
  * - indexer.language.detect.length
    - 인덱서의 언어 감지용 텍스트 길이.
    - ``1000``
  * - indexer.max.result.window.size
    - 인덱서의 최대 결과 윈도우 크기.
    - ``10000``
  * - indexer.max.search.doc.size
    - 인덱서의 검색 문서 최대 수.
    - ``50000``

.. list-table:: 인덱스 설정
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.codec
    - 인덱스의 코덱 타입.
    - ``default``
  * - index.number_of_shards
    - 인덱스의 프라이머리 샤드 수.
    - ``5``
  * - index.auto_expand_replicas
    - 인덱스의 레플리카 자동 확장 설정.
    - ``0-1``
  * - index.id.digest.algorithm
    - 인덱스 ID용 다이제스트 알고리즘.
    - ``SHA-512``
  * - index.user.initial_password
    - 인덱스 사용자의 초기 비밀번호.
    - ``admin``

.. list-table:: 필드명
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.field.favorite_count
    - 인덱스의 즐겨찾기 수 필드명.
    - ``favorite_count``
  * - index.field.click_count
    - 인덱스의 클릭 수 필드명.
    - ``click_count``
  * - index.field.config_id
    - 인덱스의 설정 ID 필드명.
    - ``config_id``
  * - index.field.expires
    - 인덱스의 만료일 필드명.
    - ``expires``
  * - index.field.url
    - 인덱스의 URL 필드명.
    - ``url``
  * - index.field.doc_id
    - 인덱스의 문서 ID 필드명.
    - ``doc_id``
  * - index.field.id
    - 인덱스의 내부 ID 필드명.
    - ``_id``
  * - index.field.version
    - 인덱스의 버전 필드명.
    - ``_version``
  * - index.field.seq_no
    - 인덱스의 시퀀스 번호 필드명.
    - ``_seq_no``
  * - index.field.primary_term
    - 인덱스의 프라이머리 텀 필드명.
    - ``_primary_term``
  * - index.field.lang
    - 인덱스의 언어 필드명.
    - ``lang``
  * - index.field.has_cache
    - 인덱스의 캐시 상태 필드명.
    - ``has_cache``
  * - index.field.last_modified
    - 인덱스의 최종 수정일 필드명.
    - ``last_modified``
  * - index.field.etag
    - 인덱스의 크롤링한 문서의 ETag 응답 헤더 필드명.
    - ``etag``
  * - index.field.owner
    - 인덱스의 크롤링한 파일의 소유자 필드명.
    - ``owner``
  * - index.field.last_modifier
    - 인덱스의 크롤링한 파일의 최종 수정자 필드명.
    - ``last_modifier``
  * - index.field.anchor
    - 인덱스의 앵커 필드명.
    - ``anchor``
  * - index.field.segment
    - 인덱스의 세그먼트 필드명.
    - ``segment``
  * - index.field.role
    - 인덱스의 역할 필드명.
    - ``role``
  * - index.field.boost
    - 인덱스의 부스트 값 필드명.
    - ``boost``
  * - index.field.created
    - 인덱스의 생성일 필드명.
    - ``created``
  * - index.field.timestamp
    - 인덱스의 타임스탬프 필드명.
    - ``timestamp``
  * - index.field.label
    - 인덱스의 라벨 필드명.
    - ``label``
  * - index.field.tag
    - 인덱스의 문서 사용자 태그 필드명.
    - ``tag``
  * - index.field.mimetype
    - 인덱스의 MIME 타입 필드명.
    - ``mimetype``
  * - index.field.parent_id
    - 인덱스의 부모 ID 필드명.
    - ``parent_id``
  * - index.field.important_content
    - 인덱스의 중요 콘텐츠 필드명.
    - ``important_content``
  * - index.field.content
    - 인덱스의 콘텐츠 필드명.
    - ``content``
  * - index.field.content_minhash_bits
    - 인덱스의 콘텐츠 minhash 비트 필드명.
    - ``content_minhash_bits``
  * - index.field.cache
    - 인덱스의 캐시 필드명.
    - ``cache``
  * - index.field.digest
    - 인덱스의 다이제스트 필드명.
    - ``digest``
  * - index.field.title
    - 인덱스의 제목 필드명.
    - ``title``
  * - index.field.host
    - 인덱스의 호스트 필드명.
    - ``host``
  * - index.field.site
    - 인덱스의 사이트 필드명.
    - ``site``
  * - index.field.content_length
    - 인덱스의 콘텐츠 길이 필드명.
    - ``content_length``
  * - index.field.filetype
    - 인덱스의 파일 타입 필드명.
    - ``filetype``
  * - index.field.filename
    - 인덱스의 파일명 필드명.
    - ``filename``
  * - index.field.thumbnail
    - 인덱스의 썸네일 필드명.
    - ``thumbnail``
  * - index.field.virtual_host
    - 인덱스의 가상 호스트 필드명.
    - ``virtual_host``
  * - response.field.content_title
    - 응답의 콘텐츠 제목 필드명.
    - ``content_title``
  * - response.field.content_description
    - 응답의 콘텐츠 설명 필드명.
    - ``content_description``
  * - response.field.url_link
    - 응답의 URL 링크 필드명.
    - ``url_link``
  * - response.field.site_path
    - 응답의 사이트 경로 필드명.
    - ``site_path``
  * - response.max.title.length
    - 응답 내 콘텐츠 제목의 최대 길이.
    - ``50``
  * - response.max.site.path.length
    - 응답 내 사이트 경로의 최대 길이.
    - ``100``
  * - response.highlight.content_title.enabled
    - 응답의 콘텐츠 제목 하이라이트 활성화 여부.
    - ``true``
  * - response.inline.mimetypes
    - 응답의 인라인 MIME 타입.
    - ``application/pdf,text/plain``
  * - response.headers
    - 응답용 HTTP 헤더입니다. Access-Control-\* 및 Timing-Allow-Origin 은 무시됩니다(CORS는 api.cors.\* / CorsFilter 로 제어됩니다). 여기서는 Vary를 설정하지 마십시오.
    - | ``text/html=X-XSS-Protection: 1; mode=block``
      | ``text/html=X-Frame-Options: SAMEORIGIN``

.. list-table:: 문서 인덱스
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.document.search.index
    - 검색 문서의 인덱스 이름.
    - ``fess.search``
  * - index.document.update.index
    - 업데이트 문서의 인덱스 이름.
    - ``fess.update``
  * - index.document.suggest.index
    - 서제스트 문서의 인덱스 이름.
    - ``fess``
  * - index.document.crawler.index
    - 크롤러 문서의 인덱스 이름.
    - ``fess_crawler``
  * - index.document.crawler.queue.number_of_shards
    - 크롤러 큐 인덱스의 프라이머리 샤드 수.
    - ``10``
  * - index.document.crawler.data.number_of_shards
    - 크롤러 데이터 인덱스의 프라이머리 샤드 수.
    - ``10``
  * - index.document.crawler.filter.number_of_shards
    - 크롤러 필터 인덱스의 프라이머리 샤드 수.
    - ``10``
  * - index.document.crawler.queue.number_of_replicas
    - 크롤러 큐 인덱스의 레플리카 수.
    - ``1``
  * - index.document.crawler.data.number_of_replicas
    - 크롤러 데이터 인덱스의 레플리카 수.
    - ``1``
  * - index.document.crawler.filter.number_of_replicas
    - 크롤러 필터 인덱스의 레플리카 수.
    - ``1``
  * - index.config.index
    - 설정 데이터의 인덱스 이름.
    - ``fess_config``
  * - index.user.index
    - 사용자 데이터의 인덱스 이름.
    - ``fess_user``
  * - index.log.index
    - 로그 데이터의 인덱스 이름.
    - ``fess_log``
  * - index.dictionary.prefix
    - 사전 인덱스 이름의 접두사.
    - (empty)

.. list-table:: 문서 관리
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.admin.array.fields
    - 인덱스의 관리용 배열 타입 필드.
    - ``lang,role,label,anchor,virtual_host``
  * - index.admin.date.fields
    - 인덱스의 관리용 날짜 타입 필드.
    - ``expires,created,timestamp,last_modified``
  * - index.admin.integer.fields
    - 인덱스의 관리용 정수 타입 필드.
    - (empty)
  * - index.admin.long.fields
    - 인덱스의 관리용 Long 타입 필드.
    - ``content_length,favorite_count,click_count``
  * - index.admin.float.fields
    - 인덱스의 관리용 Float 타입 필드.
    - ``boost``
  * - index.admin.double.fields
    - 인덱스의 관리용 Double 타입 필드.
    - (empty)
  * - index.admin.required.fields
    - 인덱스의 관리용 필수 필드.
    - ``url,title,role,boost``

.. list-table:: 타임아웃
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.search.timeout
    - 인덱스 검색 작업의 타임아웃.
    - ``3m``
  * - index.scroll.search.timeout
    - 스크롤 검색 작업의 타임아웃.
    - ``3m``
  * - index.index.timeout
    - 인덱스 작업의 타임아웃.
    - ``3m``
  * - index.bulk.timeout
    - 벌크 인덱스 작업의 타임아웃.
    - ``3m``
  * - index.delete.timeout
    - 인덱스의 삭제 작업 타임아웃.
    - ``3m``
  * - index.health.timeout
    - 인덱스 헬스 체크의 타임아웃.
    - ``10m``
  * - index.indices.timeout
    - 인덱스 indices 작업의 타임아웃.
    - ``1m``

.. list-table:: 파일 타입
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.filetype
    - 인덱싱용 MIME 타입과 filetype 라벨의 매핑.
    - | ``text/html=html``
      | ``application/msword=word``
      | ``application/vnd.openxmlformats-officedocument.wordprocessingml.document=word``
      | ``application/vnd.ms-excel=excel``
      | ``application/vnd.ms-excel.sheet.2=excel``
      | ``application/vnd.ms-excel.sheet.3=excel``
      | ``application/vnd.ms-excel.sheet.4=excel``
      | ``application/vnd.ms-excel.workspace.3=excel``
      | ``application/vnd.ms-excel.workspace.4=excel``
      | ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet=excel``
      | ``application/vnd.ms-powerpoint=powerpoint``
      | ``application/vnd.openxmlformats-officedocument.presentationml.presentation=powerpoint``
      | ``application/vnd.oasis.opendocument.text=odt``
      | ``application/vnd.oasis.opendocument.spreadsheet=ods``
      | ``application/vnd.oasis.opendocument.presentation=odp``
      | ``application/pdf=pdf``
      | ``application/x-fictionbook+xml=fb2``
      | ``application/e-pub+zip=epub``
      | ``application/x-ibooks+zip=ibooks``
      | ``text/plain=txt``
      | ``application/rtf=rtf``
      | ``application/vnd.ms-htmlhelp=chm``
      | ``application/zip=zip``
      | ``application/x-7z-comressed=7z``
      | ``application/x-bzip=bz``
      | ``application/x-bzip2=bz2``
      | ``application/x-tar=tar``
      | ``application/x-rar-compressed=rar``
      | ``video/3gp=3gp``
      | ``video/3g2=3g2``
      | ``video/x-msvideo=avi``
      | ``video/x-flv=flv``
      | ``video/mpeg=mpeg``
      | ``video/mp4=mp4``
      | ``video/ogv=ogv``
      | ``video/quicktime=qt``
      | ``video/x-m4v=m4v``
      | ``audio/x-aif=aif``
      | ``audio/midi=midi``
      | ``audio/mpga=mpga``
      | ``audio/mp4=mp4a``
      | ``audio/ogg=oga``
      | ``audio/x-wav=wav``
      | ``image/webp=webp``
      | ``image/bmp=bmp``
      | ``image/x-icon=ico``
      | ``image/x-icon=ico``
      | ``image/png=png``
      | ``image/svg+xml=svg``
      | ``image/tiff=tiff``
      | ``image/jpeg=jpg``
  * - index.reindex.size
    - 재인덱싱 작업 1회당 처리할 문서 수.
    - ``100``
  * - index.reindex.body
    - 재인덱싱 작업의 요청 본문 템플릿.
    - ``{"source":{"index":"__SOURCE_INDEX__","size":__SIZE__},"dest":{"index":"__DEST_INDEX__"},"script":{"source":"__SCRIPT_SOURCE__"}}``
  * - index.reindex.requests_per_second
    - 재인덱싱 작업의 초당 요청 수("adaptive"이면 자동).
    - ``adaptive``
  * - index.reindex.refresh
    - 재인덱싱 후 인덱스 리프레시 여부.
    - ``false``
  * - index.reindex.timeout
    - 재인덱싱 작업의 타임아웃.
    - ``1m``
  * - index.reindex.scroll
    - 재인덱싱 작업의 스크롤 타임아웃.
    - ``5m``
  * - index.reindex.max_docs
    - 재인덱싱 작업의 최대 문서 수.
    - (empty)

.. list-table:: 쿼리
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.max.length
    - 검색 쿼리의 최대 길이.
    - ``1000``
  * - query.timeout
    - 검색 쿼리의 타임아웃(밀리초).
    - ``10000``
  * - query.timeout.logging
    - 쿼리 타임아웃 또는 샤드 실패로 결과가 불완전한 검색의 로그 기록 여부.
    - ``true``
  * - query.track.total.hits
    - 쿼리에서 추적할 총 히트 건수의 최대 수입니다. 양수 또는 true만 지원합니다. false를 지정하면 응답에 히트 건수가 포함되지 않으며, 여기서든 검색 파라미터로든 히트 건수를 요청하는 검색은 거부됩니다.
    - ``10000``
  * - query.geo.fields
    - 지리 검색 쿼리에 사용하는 필드.
    - ``location``
  * - query.browser.lang.parameter.name
    - 쿼리의 브라우저 언어 파라미터 이름.
    - ``browser_lang``
  * - query.replace.term.with.prefix.query
    - 단어의 접두사 쿼리 치환 여부.
    - ``true``
  * - query.orsearch.min.hit.count
    - OR 검색 쿼리의 최소 히트 건수.
    - ``-1``
  * - query.highlight.terminal.chars
    - 쿼리 하이라이트용 유니코드 종단 문자.
    - ``u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61``
  * - query.highlight.fragment.size
    - 쿼리 하이라이트의 프래그먼트 크기.
    - ``60``
  * - query.highlight.number.of.fragments
    - 쿼리 하이라이트의 프래그먼트 수.
    - ``2``
  * - query.highlight.type
    - 쿼리 하이라이트의 타입.
    - ``fvh``
  * - query.highlight.tag.pre
    - 하이라이트된 텍스트 앞에 사용하는 태그.
    - ``<strong>``
  * - query.highlight.tag.post
    - 하이라이트된 텍스트 뒤에 사용하는 태그.
    - ``</strong>``
  * - query.highlight.boundary.chars
    - 쿼리 하이라이트의 경계 문자.
    - ``u0009u000Au0013u0020``
  * - query.highlight.boundary.max.scan
    - 쿼리 하이라이트 경계의 최대 스캔.
    - ``20``
  * - query.highlight.boundary.scanner
    - 쿼리 하이라이트 경계의 스캐너 타입.
    - ``chars``
  * - query.highlight.encoder
    - 쿼리 하이라이트의 인코더 타입.
    - ``default``
  * - query.highlight.force.source
    - 쿼리 하이라이트의 소스 강제 여부.
    - ``false``
  * - query.highlight.fragmenter
    - 쿼리 하이라이트의 프래그멘터 타입.
    - ``span``
  * - query.highlight.fragment.offset
    - 쿼리 하이라이트 프래그먼트의 오프셋.
    - ``-1``
  * - query.highlight.no.match.size
    - 일치 항목이 없을 때의 쿼리 하이라이트 크기.
    - ``0``
  * - query.highlight.order
    - 쿼리 하이라이트 프래그먼트의 순서.
    - ``score``
  * - query.highlight.phrase.limit
    - 쿼리 하이라이트의 프레이즈 제한.
    - ``256``
  * - query.highlight.content.description.fields
    - 쿼리 하이라이트에서 콘텐츠 설명에 사용하는 필드.
    - ``hl_content,digest``
  * - query.highlight.boundary.position.detect
    - 쿼리 하이라이트의 경계 위치 감지 여부.
    - ``true``
  * - query.highlight.text.fragment.type
    - 쿼리 하이라이트의 텍스트 프래그먼트 타입.
    - ``query``
  * - query.highlight.text.fragment.size
    - 쿼리 하이라이트의 텍스트 프래그먼트 크기.
    - ``3``
  * - query.highlight.text.fragment.prefix.length
    - 쿼리 하이라이트의 텍스트 프래그먼트 접두사 길이.
    - ``5``
  * - query.highlight.text.fragment.suffix.length
    - 쿼리 하이라이트의 텍스트 프래그먼트 접미사 길이.
    - ``5``
  * - query.max.search.result.offset
    - 쿼리의 최대 검색 결과 오프셋.
    - ``100000``
  * - query.additional.default.fields
    - 쿼리의 추가 기본 필드.
    - (empty)
  * - query.additional.response.fields
    - 검색 결과를 위해 인덱스에서 가져오는 추가 필드입니다. 여기에 추가한 필드는 query.additional.api.response.fields 에도 나열된 경우에만 검색 API가 반환합니다.
    - (empty)
  * - query.additional.api.response.fields
    - 쿼리의 추가 API 응답 필드입니다. 이 키는 v2 API 응답 허용 목록에 필드를 추가(추가 전용)할 뿐이며 필드를 가져오지는 않습니다. 필드를 가져오는 설정도 필요합니다. 검색 API에는 query.additional.response.fields 에, 스크롤 API에는 query.additional.scroll.response.fields 에 추가하십시오. ACL 또는 내부 필드(예: role, virtual_host)는 추가하지 마십시오. 추가하면 검색 API 응답에 접근 제어 정보가 노출됩니다.
    - (empty)
  * - query.additional.scroll.response.fields
    - 스크롤 검색 결과를 위해 인덱스에서 가져오는 추가 필드입니다. 여기에 추가한 필드는 query.additional.api.response.fields 에도 나열된 경우에만 스크롤 API가 반환합니다.
    - (empty)
  * - query.additional.cache.response.fields
    - 쿼리의 추가 캐시 응답 필드.
    - (empty)
  * - query.additional.highlighted.fields
    - 쿼리의 추가 하이라이트 필드.
    - (empty)
  * - query.additional.search.fields
    - 쿼리의 추가 검색 필드.
    - (empty)
  * - query.additional.facet.fields
    - 쿼리의 추가 패싯 필드.
    - (empty)
  * - query.additional.sort.fields
    - 쿼리의 추가 정렬 필드.
    - (empty)
  * - query.additional.analyzed.fields
    - 쿼리의 추가 분석 필드.
    - (empty)
  * - query.additional.not.analyzed.fields
    - 쿼리의 추가 비분석 필드.
    - (empty)
  * - query.gsa.response.fields
    - 쿼리의 GSA 응답용 필드.
    - ``UE,U,T,RK,S,LANG``
  * - query.gsa.default.lang
    - GSA 쿼리의 기본 언어.
    - ``en``
  * - query.gsa.default.sort
    - GSA 쿼리의 기본 정렬.
    - (empty)
  * - query.gsa.meta.prefix
    - GSA 쿼리의 메타 접두사.
    - ``MT_``
  * - query.gsa.index.field.charset
    - GSA 인덱스 쿼리의 문자셋 필드.
    - ``charset``
  * - query.gsa.index.field.content_type.
    - GSA 인덱스 쿼리의 콘텐츠 타입 필드.
    - ``content_type``
  * - query.collapse.max.concurrent.group.results
    - collapse 쿼리의 최대 동시 그룹 결과 수.
    - ``4``
  * - query.collapse.inner.hits.name
    - collapse 쿼리의 inner hits 이름.
    - ``similar_docs``
  * - query.collapse.inner.hits.size
    - collapse 쿼리의 inner hits 크기.
    - ``0``
  * - query.collapse.inner.hits.sorts
    - collapse 쿼리의 inner hits 정렬.
    - (empty)
  * - query.default.languages
    - 쿼리의 기본 언어.
    - (empty)
  * - query.json.default.preference
    - JSON 쿼리의 기본 프리퍼런스.
    - ``_query``
  * - query.gsa.default.preference
    - GSA 쿼리의 기본 프리퍼런스.
    - ``_query``
  * - query.language.mapping
    - 쿼리의 언어 매핑.
    - | ``ar=ar``
      | ``bg=bg``
      | ``bn=bn``
      | ``ca=ca``
      | ``ckb-iq=ckb-iq``
      | ``ckb_IQ=ckb-iq``
      | ``cs=cs``
      | ``da=da``
      | ``de=de``
      | ``el=el``
      | ``en=en``
      | ``en-ie=en-ie``
      | ``en_IE=en-ie``
      | ``es=es``
      | ``et=et``
      | ``eu=eu``
      | ``fa=fa``
      | ``fi=fi``
      | ``fr=fr``
      | ``gl=gl``
      | ``gu=gu``
      | ``he=he``
      | ``hi=hi``
      | ``hr=hr``
      | ``hu=hu``
      | ``hy=hy``
      | ``id=id``
      | ``it=it``
      | ``ja=ja``
      | ``ko=ko``
      | ``lt=lt``
      | ``lv=lv``
      | ``mk=mk``
      | ``ml=ml``
      | ``nl=nl``
      | ``no=no``
      | ``pa=pa``
      | ``pl=pl``
      | ``pt=pt``
      | ``pt-br=pt-br``
      | ``pt_BR=pt-br``
      | ``ro=ro``
      | ``ru=ru``
      | ``si=si``
      | ``sq=sq``
      | ``sv=sv``
      | ``ta=ta``
      | ``te=te``
      | ``th=th``
      | ``tl=tl``
      | ``tr=tr``
      | ``uk=uk``
      | ``ur=ur``
      | ``vi=vi``
      | ``zh-cn=zh-cn``
      | ``zh_CN=zh-cn``
      | ``zh-tw=zh-tw``
      | ``zh_TW=zh-tw``
      | ``zh=zh``

.. list-table:: 부스트
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.boost.title
    - 쿼리의 제목 필드 부스트 값.
    - ``0.5``
  * - query.boost.title.lang
    - 쿼리의 언어 지정 제목 필드 부스트 값.
    - ``1.0``
  * - query.boost.content
    - 쿼리의 콘텐츠 필드 부스트 값.
    - ``0.05``
  * - query.boost.content.lang
    - 쿼리의 언어 지정 콘텐츠 필드 부스트 값.
    - ``0.1``
  * - query.boost.important_content
    - 쿼리의 중요 콘텐츠 필드 부스트 값.
    - ``-1.0``
  * - query.boost.important_content.lang
    - 쿼리의 언어 지정 중요 콘텐츠 필드 부스트 값.
    - ``-1.0``
  * - query.boost.fuzzy.min.length
    - 쿼리의 퍼지 부스트 최소 길이.
    - ``4``
  * - query.boost.fuzzy.title
    - 퍼지 제목 쿼리의 부스트 값.
    - ``0.01``
  * - query.boost.fuzzy.title.fuzziness
    - 퍼지 제목 쿼리의 퍼지 정도.
    - ``AUTO``
  * - query.boost.fuzzy.title.expansions
    - 퍼지 제목 쿼리의 확장 수.
    - ``10``
  * - query.boost.fuzzy.title.prefix_length
    - 퍼지 제목 쿼리의 접두사 길이.
    - ``0``
  * - query.boost.fuzzy.title.transpositions
    - 퍼지 제목 쿼리의 전치 허용 여부.
    - ``true``
  * - query.boost.fuzzy.content
    - 퍼지 콘텐츠 쿼리의 부스트 값.
    - ``0.005``
  * - query.boost.fuzzy.content.fuzziness
    - 퍼지 콘텐츠 쿼리의 퍼지 정도.
    - ``AUTO``
  * - query.boost.fuzzy.content.expansions
    - 퍼지 콘텐츠 쿼리의 확장 수.
    - ``10``
  * - query.boost.fuzzy.content.prefix_length
    - 퍼지 콘텐츠 쿼리의 접두사 길이.
    - ``0``
  * - query.boost.fuzzy.content.transpositions
    - 퍼지 콘텐츠 쿼리의 전치 허용 여부.
    - ``true``
  * - query.default.query_type
    - 기본 쿼리 타입.
    - ``bool``
  * - query.dismax.tie_breaker
    - dismax 쿼리의 타이 브레이커 값.
    - ``0.1``
  * - query.bool.minimum_should_match
    - 불리언 쿼리의 minimum should match 값.
    - (empty)
  * - query.prefix.expansions
    - 접두사 쿼리의 확장 수.
    - ``50``
  * - query.prefix.slop
    - 접두사 쿼리의 슬롭 값.
    - ``0``
  * - query.fuzzy.prefix_length
    - 퍼지 쿼리의 접두사 길이.
    - ``0``
  * - query.fuzzy.expansions
    - 퍼지 쿼리의 확장 수.
    - ``50``
  * - query.fuzzy.transpositions
    - 퍼지 쿼리의 전치 허용 여부.
    - ``true``

.. list-table:: 패싯
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.facet.fields
    - 패싯 쿼리용 필드.
    - ``label``
  * - query.facet.fields.size
    - 패싯 필드의 크기.
    - ``100``
  * - query.facet.fields.size.max
    - facet.size 의 상한 클램프(검색 초크포인트에서 적용).
    - ``1000``
  * - query.facet.fields.min_doc_count
    - 패싯 필드의 최소 문서 수.
    - ``1``
  * - query.facet.fields.min_doc_count.max
    - facet.minDocCount 의 상한 클램프(검색 초크포인트에서 적용).
    - ``2147483647``
  * - query.facet.fields.sort
    - 패싯 필드의 정렬 순서.
    - ``count.desc``
  * - query.facet.fields.missing
    - 누락된 패싯 필드의 값.
    - (empty)
  * - query.facet.queries
    - 패싯 쿼리 정의.
    - | ``labels.facet_timestamp_title:labels.facet_timestamp_1day=timestamp:[now/d-1d TO *]	labels.facet_timestamp_1week=timestamp:[now/d-7d TO *]	labels.facet_timestamp_1month=timestamp:[now/d-1M TO *]	labels.facet_timestamp_1year=timestamp:[now/d-1y TO *]``
      | ``labels.facet_contentLength_title:labels.facet_contentLength_10k=content_length:[0 TO 9999]	labels.facet_contentLength_10kto100k=content_length:[10000 TO 99999]	labels.facet_contentLength_100kto500k=content_length:[100000 TO 499999]	labels.facet_contentLength_500kto1m=content_length:[500000 TO 999999]	labels.facet_contentLength_1m=content_length:[1000000 TO *]``
      | ``labels.facet_filetype_title:labels.facet_filetype_html=filetype:html	labels.facet_filetype_word=filetype:word	labels.facet_filetype_excel=filetype:excel	labels.facet_filetype_powerpoint=filetype:powerpoint	labels.facet_filetype_odt=filetype:odt	labels.facet_filetype_ods=filetype:ods	labels.facet_filetype_odp=filetype:odp	labels.facet_filetype_pdf=filetype:pdf	labels.facet_filetype_txt=filetype:txt	labels.facet_filetype_others=filetype:others``

.. list-table:: 랭킹
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rank.fusion.window_size
    - Rank Fusion의 윈도우 크기.
    - ``200``
  * - rank.fusion.rank_constant
    - Rank Fusion의 랭크 상수.
    - ``20``
  * - rank.fusion.threads
    - Rank Fusion의 스레드 수.
    - ``-1``
  * - rank.fusion.timeout
    - Fess가 검색기의 결과를 직접 융합할 때(rank.fusion.engine.enabled=false) 메인 검색기 이외의 검색기를 기다리는 최대 시간(밀리초)입니다. 그때까지 응답하지 않은 검색기는 해당 검색에서 제외되며, 결과에는 부분 결과이며 타임아웃되었다는 표시가 붙습니다. 메인 검색기는 항상 기다립니다. 0 이하이면 제한 없이 기다립니다.
    - ``10000``
  * - rank.fusion.score_field
    - Rank Fusion의 스코어 필드.
    - ``rf_score``
  * - rank.fusion.engine.enabled
    - 검색 엔진이 Rank Fusion을 수행할지 여부입니다. true이면 참여할 수 있는 검색기가 자신의 쿼리를 하나의 요청에 제공하므로 패싯과 총 히트 건수는 융합된 결과 집합을 나타냅니다. false이면 Fess가 검색기의 결과를 직접 융합합니다.
    - ``false``
  * - rank.fusion.combination.technique
    - 검색 엔진이 융합된 스코어를 결합하는 방식: rrf, arithmetic_mean, geometric_mean 또는 harmonic_mean.
    - ``rrf``
  * - rank.fusion.normalization.technique
    - 결합하기 전에 스코어를 정규화하는 방식: min_max, l2 또는 z_score. rrf 에서는 무시됩니다. z_score 는 arithmetic_mean 과만 조합할 수 있으며, 그 외의 mean은 거부되고 Fess가 결과를 직접 융합합니다.
    - ``min_max``
  * - rank.fusion.combination.weights
    - 엔진 측 융합에서 검색기별 가중치를 name:weight 쌍으로 지정합니다(예: default:0.7,semantic_chunk:0.3). 가중치의 합은 1.0이어야 하며 참여하는 모든 검색기를 지정해야 합니다. 비워 두면 모든 검색기에 동일한 가중치가 적용됩니다.
    - (empty)
  * - rank.fusion.pagination_depth
    - 엔진 측 융합에서 각 검색기가 샤드별로 제공하는 결과 수입니다. 클라이언트가 페이징할 수 있는 깊이와 엔진이 순위를 매기는 문서 집합의 범위를 모두 제한합니다. 융합된 검색은 이 수만큼의 결과를 페이징하며, indexer.max.result.window.size 를 넘지 않습니다.
    - ``1000``

.. list-table:: ACL
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - smb.role.from.file
    - 파일에서 SMB 역할을 가져올지 여부.
    - ``true``
  * - smb.available.sid.types
    - SMB에서 사용 가능한 SID 타입.
    - ``1,2,4:2,5:1``
  * - file.role.from.file
    - 파일에서 파일 역할을 가져올지 여부.
    - ``true``
  * - ftp.role.from.file
    - 파일에서 FTP 역할을 가져올지 여부.
    - ``true``

.. list-table:: 백업
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.backup.targets
    - 인덱스 백업 대상 파일.
    - ``fess_basic_config.bulk,fess_config.bulk,fess_user.bulk,system.properties,fess.json,doc.json``
  * - index.backup.log.targets
    - 인덱스 백업 대상 로그 파일.
    - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
  * - index.backup.log.load.timeout
    - 인덱스 백업 로그 로딩의 타임아웃.
    - ``60000``

.. list-table:: 로깅
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - logging.app.packages
    - 로깅용 애플리케이션 패키지.
    - ``org.codelibs,org.dbflute,org.lastaflute``
  * - logging.search.docs.enabled
    - 검색 문서 로깅 활성화 여부.
    - ``true``
  * - logging.search.docs.fields
    - 검색 문서에서 로그에 기록할 필드.
    - ``filetype,created,click_count,title,doc_id,url,score,site,filename,host,digest,boost,mimetype,favorite_count,_id,lang,last_modified,content_length,timestamp``
  * - logging.search.use.logfile
    - 검색 로깅의 로그 파일 사용 여부.
    - ``true``
  * - logging.search.max.queue.size
    - 검색 로깅의 최대 큐 크기.
    - ``10000``
  * - logging.click.max.queue.size
    - 클릭 로깅의 최대 큐 크기.
    - ``10000``
  * - logging.chat.max.queue.size
    - 채팅 사용량 로깅의 최대 큐 크기.
    - ``10000``
  * - search.history.enabled
    - 검색 이력을 위해 로그인한 사용자의 검색 조건을 기록할지 여부.
    - ``true``
  * - search.history.size
    - 사용자별로 반환하는 검색 이력 항목의 최대 수.
    - ``10``
  * - user.tag.enabled
    - 로그인한 사용자가 문서에 태그를 지정할 수 있는지 여부입니다. 각 태그는 만든 사용자에게 속합니다.
    - ``false``
  * - user.tag.name.max.length
    - 태그 이름의 최대 길이(코드 포인트 단위).
    - ``50``
  * - user.tag.max.tags
    - 한 사용자가 소유할 수 있는 태그의 최대 수.
    - ``1000``
  * - user.tag.max.paths
    - 하나의 태그를 붙일 수 있는 URL의 최대 수.
    - ``10000``
  * - user.tag.queue.max.size
    - 문서에 적용될 때까지 메모리에 보관하는 대기 중인 태그 변경의 최대 수.
    - ``10000``
  * - user.tag.process.batch.size
    - 태그 변경을 문서에 적용할 때 벌크 요청 1회당 업데이트하는 URL 수.
    - ``100``
  * - user.tag.visible.max.size
    - 검색에서 한 사용자에게 보이는 태그의 최대 수.
    - ``1000``

웹
--

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - form.admin.max.input.size
    - 관리 폼의 최대 입력 크기.
    - ``10000``
  * - form.admin.label.in.config.enabled
    - 관리 설정 폼의 라벨 활성화 여부.
    - ``false``
  * - form.admin.default.template.name
    - 관리 폼의 기본 템플릿 이름.
    - ``__TEMPLATE__``
  * - osdd.link.enabled
    - OSDD 링크(OpenSearch Description Document) 활성화 여부.
    - ``auto``
  * - clipboard.copy.icon.enabled
    - 클립보드 복사 아이콘 활성화 여부.
    - ``true``
  * - authentication.admin.users
    - 인증용 관리자 사용자 이름.
    - ``admin``
  * - authentication.admin.users.ignore.case
    - authentication.admin.users 를 대소문자 구분 없이 일치시킬지 여부입니다: auto, true 또는 false. auto는 ldap.provider.url 이 설정되어 있으면 대소문자를 무시합니다.
    - ``auto``
  * - authentication.admin.roles
    - 인증용 관리자 역할 이름.
    - ``admin``
  * - role.search.default.permissions
    - 검색 역할의 기본 권한.
    - (empty)
  * - role.search.default.display.permissions
    - 검색 역할의 기본 표시 권한.
    - ``{role}guest``
  * - role.search.guest.permissions
    - role.search.guest.permissions 는 비워 두지 마십시오. 이 값은 익명 검색 역할 집합이 비지 않도록 유지하는 게스트 역할의 시드가 됩니다. 확정된 역할 집합이 비어 있으면 역할 필터가 건너뛰어져(fail-open) 역할 기반 접근 제어가 무효화되고 문서가 익명 사용자에게 노출될 수 있습니다. 검색 역할의 게스트 권한입니다.
    - ``{role}guest``
  * - role.search.user.prefix
    - 검색에서 사용자 역할의 접두사.
    - ``1``
  * - role.search.group.prefix
    - 검색에서 그룹 역할의 접두사.
    - ``2``
  * - role.search.role.prefix
    - 검색에서 role 역할의 접두사.
    - ``R``
  * - role.search.denied.prefix
    - 검색에서 거부된 역할의 접두사.
    - ``D``
  * - cookie.default.path
    - 쿠키의 기본 경로(컨텍스트 경로가 없으면 기본적으로 '/')
    - ``/``
  * - cookie.default.expire
    - 쿠키의 기본 만료 시간(초) 예: 31556926: 1년, 86400: 1일
    - ``3600``
  * - session.tracking.modes
    - 세션 추적 모드
    - ``cookie``
  * - session.cookie.secure
    - 시작 시 세션 쿠키(JSESSIONID)에 Secure 속성을 추가할지 여부입니다. 비어 있으면(기본값) Tomcat의 자동 동작이 사용됩니다(Secure는 HTTPS 요청에만 추가됩니다). 운영 환경의 HTTPS 배포, 특히 리버스 프록시에서 TLS를 종료하는 경우에는 true로 설정하십시오. true이면 쿠키가 HTTP로 전송되지 않으므로 일반 HTTP에서는 세션이 수립되지 않습니다. localhost 개발 환경에서는 비워 두십시오. SameSite=none을 사용하는 경우에도 Secure 속성이 필요합니다. 이 값을 변경하려면 재시작이 필요합니다.
    - (empty)
  * - cookie.search.parameter.keys
    - SSO 로그인 전에 쿠키에 저장할 요청 파라미터 키의 쉼표 구분 목록.
    - ``q,num,sort``
  * - cookie.search.parameter.required_keys
    - 쿠키에 저장하기 위해 반드시 존재해야 하는 필수 파라미터 키의 쉼표 구분 목록.
    - ``q``
  * - cookie.search.parameter.max.length
    - 쿠키에 저장하는 인코딩된 검색 파라미터의 최대 길이.
    - ``1000``
  * - cookie.search.parameter.max.decompressed.length
    - 저장된 검색 파라미터를 압축 해제했을 때 허용되는 최대 크기(바이트)입니다. 위의 상한은 gzip으로 압축된 쿠키에 적용되는데, 이는 압축 해제 후의 크기에 대한 제한이 되지 않으며, 쿠키는 클라이언트에서 전달됩니다.
    - ``65536``
  * - cookie.search.parameter.max.restored.length
    - 로그인 후 저장된 검색 파라미터를 복원할 때 만들어지는 쿼리 문자열의 최대 길이입니다. 복원은 편의 기능일 뿐 로그인은 그렇지 않으므로, 이보다 긴 쿼리 문자열은 컨테이너가 거부할 Location 헤더에 쓰지 않고 버립니다. 퍼센트 인코딩은 CJK 쿼리를 9배로 늘리므로, 이 값은 쿼리 자체가 가질 수 있는 길이보다 훨씬 작습니다. 응답 헤더를 제한하는 tomcat_config.properties 의 tomcat.maxHttpHeaderSize 와 함께 올리십시오.
    - ``4096``
  * - cookie.search.parameter.name
    - SSO 로그인 전에 인코딩된 검색 파라미터를 저장하는 데 사용하는 쿠키 이름.
    - ``fsrp``
  * - cookie.search.parameter.http_only
    - 검색 파라미터 쿠키의 HttpOnly 속성 설정 여부.
    - ``true``
  * - cookie.search.parameter.secure
    - 검색 파라미터 쿠키에 Secure 속성을 설정할지 여부입니다. HTTPS를 사용하는 운영 환경에서는 true여야 합니다.
    - (empty)
  * - cookie.search.parameter.max_age
    - 검색 파라미터 쿠키의 Max-Age(초)입니다. 세션 전용 쿠키로 하려면 -1을 사용하십시오.
    - ``60``
  * - cookie.search.parameter.domain
    - 검색 파라미터 쿠키의 Domain 속성입니다. 쿠키를 사용할 수 있게 할 도메인 범위를 설정하십시오(예: example.com).
    - (empty)
  * - cookie.search.parameter.path
    - 검색 파라미터 쿠키의 Path 속성입니다. 일반적으로 "/" 또는 애플리케이션의 컨텍스트 경로로 설정합니다.
    - ``/``
  * - cookie.search.parameter.same_site
    - 검색 파라미터 쿠키의 SameSite 속성입니다. 유효한 값: Lax, Strict, None
    - ``Lax``
  * - paging.page.size
    - 페이징의 1페이지 크기
    - ``25``
  * - paging.page.range.size
    - 페이징의 페이지 범위 크기
    - ``5``
  * - paging.page.range.fill.limit
    - 페이징의 페이지 범위 옵션 'fillLimit'
    - ``true``

.. list-table:: 가져오기 페이지 크기
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - page.docboost.max.fetch.size
    - 페이지당 가져올 문서 부스트 레코드의 최대 수.
    - ``1000``
  * - page.keymatch.max.fetch.size
    - 페이지당 가져올 키 매치 레코드의 최대 수.
    - ``1000``
  * - page.labeltype.max.fetch.size
    - 페이지당 가져올 라벨 유형 레코드의 최대 수.
    - ``1000``
  * - page.tagtype.max.fetch.size
    - 페이지당 가져올 태그 유형 레코드의 최대 수.
    - ``1000``
  * - page.roletype.max.fetch.size
    - 페이지당 가져올 역할 유형 레코드의 최대 수.
    - ``1000``
  * - page.user.max.fetch.size
    - 페이지당 가져올 사용자 레코드의 최대 수.
    - ``1000``
  * - page.role.max.fetch.size
    - 페이지당 가져올 역할 레코드의 최대 수.
    - ``1000``
  * - page.group.max.fetch.size
    - 페이지당 가져올 그룹 레코드의 최대 수.
    - ``1000``
  * - page.crawling.info.param.max.fetch.size
    - 페이지당 가져올 크롤링 정보 파라미터의 최대 수.
    - ``100``
  * - page.crawling.info.max.fetch.size
    - 페이지당 가져올 크롤링 정보 레코드의 최대 수.
    - ``1000``
  * - page.data.config.max.fetch.size
    - 페이지당 가져올 데이터 스토어 설정 레코드의 최대 수.
    - ``100``
  * - page.web.config.max.fetch.size
    - 페이지당 가져올 웹 크롤링 설정 레코드의 최대 수.
    - ``100``
  * - page.file.config.max.fetch.size
    - 페이지당 가져올 파일 크롤링 설정 레코드의 최대 수.
    - ``100``
  * - page.duplicate.host.max.fetch.size
    - 페이지당 가져올 중복 호스트 레코드의 최대 수.
    - ``1000``
  * - page.failure.url.max.fetch.size
    - 페이지당 가져올 장애 URL 레코드의 최대 수.
    - ``1000``
  * - page.favorite.log.max.fetch.size
    - 페이지당 가져올 즐겨찾기 로그 레코드의 최대 수.
    - ``100``
  * - page.file.auth.max.fetch.size
    - 페이지당 가져올 파일 인증 레코드의 최대 수.
    - ``100``
  * - page.web.auth.max.fetch.size
    - 페이지당 가져올 웹 인증 레코드의 최대 수.
    - ``100``
  * - page.path.mapping.max.fetch.size
    - 페이지당 가져올 경로 매핑 레코드의 최대 수.
    - ``1000``
  * - page.request.header.max.fetch.size
    - 페이지당 가져올 요청 헤더 레코드의 최대 수.
    - ``1000``
  * - page.scheduled.job.max.fetch.size
    - 페이지당 가져올 스케줄 작업 레코드의 최대 수.
    - ``100``
  * - page.elevate.word.max.fetch.size
    - 페이지당 가져올 추가 단어 레코드의 최대 수.
    - ``1000``
  * - page.bad.word.max.fetch.size
    - 페이지당 가져올 제외 단어 레코드의 최대 수.
    - ``1000``
  * - page.dictionary.max.fetch.size
    - 페이지당 가져올 사전 레코드의 최대 수.
    - ``1000``
  * - page.relatedcontent.max.fetch.size
    - 페이지당 가져올 관련 콘텐츠 레코드의 최대 수.
    - ``5000``
  * - page.relatedquery.max.fetch.size
    - 페이지당 가져올 관련 쿼리 레코드의 최대 수.
    - ``5000``
  * - page.thumbnail.queue.max.fetch.size
    - 페이지당 가져올 썸네일 큐 레코드의 최대 수.
    - ``100``
  * - page.thumbnail.purge.max.fetch.size
    - 페이지당 가져올 썸네일 삭제 레코드의 최대 수.
    - ``100``
  * - page.score.booster.max.fetch.size
    - 페이지당 가져올 스코어 부스터 레코드의 최대 수.
    - ``1000``
  * - page.searchlog.max.fetch.size
    - 페이지당 가져올 검색 로그 레코드의 최대 수.
    - ``10000``
  * - page.searchlist.track.total.hits
    - 검색 목록 페이지의 총 히트 건수 추적 여부.
    - ``true``
  * - page.searchlist.content.max.length
    - 검색 목록 편집 페이지에 표시하는 콘텐츠의 최대 길이(문자 수).
    - ``100000``

.. list-table:: 검색 페이지
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - paging.search.page.start
    - 검색 결과의 기본 시작 페이지.
    - ``0``
  * - paging.search.page.size
    - 페이지당 검색 결과의 기본 크기.
    - ``10``
  * - paging.search.page.max.size
    - 페이지당 검색 결과의 최대 크기.
    - ``100``
  * - api.param.max.length
    - v2 API 문자열 쿼리 파라미터(q, sort, sdh)의 최대 길이. OWASP API4:2023.
    - ``1000``
  * - api.param.max.array.size
    - v2 API 반복 가능 쿼리 파라미터의 최대 값 수.
    - ``100``
  * - api.click.max.timestamp
    - v2 클릭 API가 받아들이는 클릭 로그 타임스탬프(rt, epoch ms)의 최대값. OWASP API4:2023.
    - ``9999999999999``
  * - searchlog.agg.shard.size
    - 검색 로그
    - ``-1``
  * - searchlog.request.headers
    - 검색 로그에 포함할 요청 헤더.
    - (empty)
  * - searchlog.process.batch_size
    - 검색 로그 처리의 배치 크기.
    - ``100``
  * - related_query.generate.days
    - 검색 로그에서 관련 쿼리를 생성할 때 읽는 검색 로그의 일수.
    - ``30``
  * - related_query.generate.term.size
    - 가상 호스트당 생성되는 단어의 최대 수.
    - ``100``
  * - related_query.generate.query.size
    - 단어당 생성되는 관련 쿼리의 최대 수.
    - ``5``
  * - related_query.generate.min.sessions
    - 단어와 그 관련 쿼리 각각에 필요한 서로 다른 사용자 세션의 최소 수.
    - ``3``
  * - related_query.generate.session.interval
    - 검색 후 같은 세션의 후속 검색이 리파인먼트로 간주되는 간격(분).
    - ``10``
  * - related_query.generate.seed.log.size
    - 단어를 검색한 세션을 찾기 위해 읽는 단어별 검색 로그의 최대 수.
    - ``1000``
  * - related_query.generate.seed.session.size
    - 후속 검색을 읽는 단어별 세션의 최대 수.
    - ``200``
  * - related_query.generate.log.fetch.size
    - 단어별로 읽는 후속 검색 로그의 최대 수.
    - ``2000``
  * - related_query.generate.query.min.length
    - 생성되는 단어 또는 관련 쿼리의 최소 길이(문자 수).
    - ``2``
  * - related_query.generate.query.max.length
    - 생성되는 단어 또는 관련 쿼리의 최대 길이(문자 수).
    - ``50``
  * - docreport.duplicate.group.size
    - docreport 문서 리포트 화면에 표시하는 중복 그룹의 최대 수(큰 그룹부터).
    - ``100``
  * - docreport.duplicate.docs.size
    - 문서 리포트 화면이 중복 그룹마다 나열하는 문서의 최대 수.
    - ``10``
  * - docreport.duplicate.export.page.size
    - 중복 리포트를 CSV로 다운로드할 때 요청 1회당 읽는 콘텐츠 서명 수.
    - ``10000``
  * - docreport.dormant.days
    - 마지막 수정 후 문서를 휴면으로 간주하는 기본 일수.
    - ``365``
  * - thumbnail.html.image.min.width
    - 썸네일의 HTML 이미지 최소 너비.
    - ``100``
  * - thumbnail.html.image.min.height
    - 썸네일의 HTML 이미지 최소 높이.
    - ``100``
  * - thumbnail.html.image.max.aspect.ratio
    - 썸네일의 HTML 이미지 최대 종횡비.
    - ``3.0``
  * - thumbnail.html.image.thumbnail.width
    - 생성되는 썸네일 이미지의 너비.
    - ``100``
  * - thumbnail.html.image.thumbnail.height
    - 생성되는 썸네일 이미지의 높이.
    - ``100``
  * - thumbnail.html.image.format
    - 생성되는 썸네일 이미지의 형식.
    - ``png``
  * - thumbnail.html.image.xpath
    - 썸네일용 이미지를 선택하는 XPath.
    - ``//IMG``
  * - thumbnail.html.image.exclude.extensions
    - 썸네일 생성에서 제외할 파일 확장자.
    - ``svg,html,css,js``
  * - thumbnail.generator.interval
    - 썸네일 생성기의 간격.
    - ``0``
  * - thumbnail.generator.targets
    - 썸네일 생성기의 대상(예: all).
    - ``all``
  * - thumbnail.crawler.enabled
    - 썸네일 크롤러 활성화 여부.
    - ``true``
  * - thumbnail.system.monitor.interval
    - 썸네일 처리의 시스템 모니터링 간격.
    - ``60``

.. list-table:: 사용자
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - user.code.request.parameter
    - 사용자 코드 설정
    - ``userCode``
  * - user.code.min.length
    - 사용자 코드의 최소 길이.
    - ``20``
  * - user.code.max.length
    - 사용자 코드의 최대 길이.
    - ``100``
  * - user.code.pattern
    - 검증용 사용자 코드 패턴.
    - ``[a-zA-Z0-9_]+``
  * - mail.from.name
    - 이메일의 From 필드에 표시할 이름.
    - ``Administrator``
  * - mail.from.address
    - From 필드에 사용할 이메일 주소.
    - ``root@localhost``
  * - mail.hostname
    - 메일 서버의 호스트명.
    - (empty)
  * - scheduler.target.name
    - 스케줄러의 대상 이름.
    - (empty)
  * - scheduler.job.class
    - 스케줄러의 작업 클래스.
    - ``org.codelibs.fess.app.job.ScriptExecutorJob``
  * - scheduler.concurrent.exec.mode
    - 스케줄러의 동시 실행 모드.
    - ``QUIT``
  * - scheduler.monitor.interval
    - 스케줄러 모니터링 간격.
    - ``30``
  * - coordinator.poll.interval
    - 하트비트와 이벤트를 폴링하는 간격(초).
    - ``60``
  * - coordinator.heartbeat.ttl
    - 인스턴스 하트비트 문서의 유효 기간(밀리초).
    - ``180000``
  * - coordinator.operation.ttl
    - 오퍼레이션 잠금 문서의 유효 기간(밀리초).
    - ``7200000``
  * - coordinator.operation.retry
    - 오퍼레이션 잠금 획득의 최대 재시도 횟수.
    - ``3``
  * - coordinator.event.ttl
    - 이벤트 통지 문서의 유효 기간(밀리초).
    - ``600000``
  * - online.help.base.link
    - 온라인 도움말의 기본 링크.
    - ``https://fess.codelibs.org/{lang}/{version}/admin/``
  * - online.help.installation
    - 온라인 도움말의 설치 가이드 링크.
    - ``https://fess.codelibs.org/{lang}/{version}/install/install.html``
  * - online.help.eol
    - 온라인 도움말의 수명 종료 정보 링크.
    - ``https://fess.codelibs.org/{lang}/eol.html``
  * - online.help.name.failureurl
    - 장애 URL의 온라인 도움말 키.
    - ``failureurl``
  * - online.help.name.elevateword
    - 추가 단어의 온라인 도움말 키.
    - ``elevateword``
  * - online.help.name.reqheader
    - 요청 헤더의 온라인 도움말 키.
    - ``reqheader``
  * - online.help.name.dict.synonym
    - 동의어 사전의 온라인 도움말 키.
    - ``synonym``
  * - online.help.name.dict
    - 사전의 온라인 도움말 키.
    - ``dict``
  * - online.help.name.dict.kuromoji
    - Kuromoji 사전의 온라인 도움말 키.
    - ``kuromoji``
  * - online.help.name.dict.protwords
    - 보호 단어 사전의 온라인 도움말 키.
    - ``protwords``
  * - online.help.name.dict.stopwords
    - 불용어 사전의 온라인 도움말 키.
    - ``stopwords``
  * - online.help.name.dict.stemmeroverride
    - Stemmer 재정의 사전의 온라인 도움말 키.
    - ``stemmeroverride``
  * - online.help.name.dict.mapping
    - 매핑 사전의 온라인 도움말 키.
    - ``mapping``
  * - online.help.name.webconfig
    - 웹 크롤링 설정의 온라인 도움말 키.
    - ``webconfig``
  * - online.help.name.searchlist
    - 검색 목록의 온라인 도움말 키.
    - ``searchlist``
  * - online.help.name.log
    - 로그의 온라인 도움말 키.
    - ``log``
  * - online.help.name.general
    - 일반 설정의 온라인 도움말 키.
    - ``general``
  * - online.help.name.role
    - 역할의 온라인 도움말 키.
    - ``role``
  * - online.help.name.joblog
    - 작업 로그의 온라인 도움말 키.
    - ``joblog``
  * - online.help.name.keymatch
    - 키 매치의 온라인 도움말 키.
    - ``keymatch``
  * - online.help.name.relatedquery
    - 관련 쿼리의 온라인 도움말 키.
    - ``relatedquery``
  * - online.help.name.relatedcontent
    - 관련 콘텐츠의 온라인 도움말 키.
    - ``relatedcontent``
  * - online.help.name.wizard
    - 구성 마법사의 온라인 도움말 키.
    - ``wizard``
  * - online.help.name.badword
    - 제외 단어의 온라인 도움말 키.
    - ``badword``
  * - online.help.name.pathmap
    - 경로 매핑의 온라인 도움말 키.
    - ``pathmap``
  * - online.help.name.boostdoc
    - 문서 부스트의 온라인 도움말 키.
    - ``boostdoc``
  * - online.help.name.dataconfig
    - 데이터 스토어 설정의 온라인 도움말 키.
    - ``dataconfig``
  * - online.help.name.systeminfo
    - 시스템 정보의 온라인 도움말 키.
    - ``systeminfo``
  * - online.help.name.user
    - 사용자의 온라인 도움말 키.
    - ``user``
  * - online.help.name.group
    - 그룹의 온라인 도움말 키.
    - ``group``
  * - online.help.name.dashboard
    - 대시보드의 온라인 도움말 키.
    - ``dashboard``
  * - online.help.name.webauth
    - 웹 인증의 온라인 도움말 키.
    - ``webauth``
  * - online.help.name.fileconfig
    - 파일 크롤링 설정의 온라인 도움말 키.
    - ``fileconfig``
  * - online.help.name.fileauth
    - 파일 인증의 온라인 도움말 키.
    - ``fileauth``
  * - online.help.name.labeltype
    - 라벨 유형의 온라인 도움말 키.
    - ``labeltype``
  * - online.help.name.tagtype
    - 태그 유형의 온라인 도움말 키.
    - ``tagtype``
  * - online.help.name.duplicatehost
    - 중복 호스트의 온라인 도움말 키.
    - ``duplicatehost``
  * - online.help.name.scheduler
    - 스케줄러의 온라인 도움말 키.
    - ``scheduler``
  * - online.help.name.crawlinginfo
    - 크롤링 정보의 온라인 도움말 키.
    - ``crawlinginfo``
  * - online.help.name.backup
    - 백업의 온라인 도움말 키.
    - ``backup``
  * - online.help.name.upgrade
    - 업그레이드의 온라인 도움말 키.
    - ``upgrade``
  * - online.help.name.sereq
    - 검색 요청의 온라인 도움말 키.
    - ``sereq``
  * - online.help.name.accesstoken
    - 액세스 토큰의 온라인 도움말 키.
    - ``accesstoken``
  * - online.help.name.suggest
    - 서제스트의 온라인 도움말 키.
    - ``suggest``
  * - online.help.name.searchlog
    - 검색 로그의 온라인 도움말 키.
    - ``searchlog``
  * - online.help.name.maintenance
    - 유지보수의 온라인 도움말 키.
    - ``maintenance``
  * - online.help.name.plugin
    - 플러그인의 온라인 도움말 키.
    - ``plugin``
  * - online.help.name.storage
    - 스토리지의 온라인 도움말 키.
    - ``storage``
  * - online.help.name.docreport
    - 문서 리포트의 온라인 도움말 키.
    - ``docreport``
  * - online.help.supported.langs
    - 온라인 도움말에서 지원하는 언어.
    - ``de,es,fr,ja,ko,zh-cn``
  * - forum.link
    - 사용자 지원용 포럼 링크.
    - ``https://discuss.codelibs.org/c/Fess{lang}/``
  * - forum.supported.langs
    - 포럼에서 지원하는 언어.
    - ``en,ja``
  * - suggest.popular.word.seed
    - 인기 단어 서제스트의 시드 값.
    - ``0``
  * - suggest.popular.word.tags
    - 인기 단어 서제스트의 태그.
    - (empty)
  * - suggest.popular.word.fields
    - 인기 단어 서제스트의 필드.
    - (empty)
  * - suggest.popular.word.excludes
    - 인기 단어 서제스트의 제외 단어.
    - (empty)
  * - suggest.popular.word.size
    - 서제스트할 인기 단어 수.
    - ``10``
  * - suggest.popular.word.window.size
    - 인기 단어 서제스트의 윈도우 크기.
    - ``30``
  * - suggest.popular.word.query.freq
    - 인기 단어 서제스트의 쿼리 빈도.
    - ``10``
  * - suggest.min.hit.count
    - 서제스트의 최소 히트 건수.
    - ``1``
  * - suggest.field.contents
    - 서제스트 콘텐츠용 필드.
    - ``_default``
  * - suggest.field.tags
    - 서제스트 태그용 필드.
    - ``label``
  * - suggest.field.roles
    - 서제스트 역할용 필드.
    - ``role``
  * - suggest.field.index.contents
    - 서제스트용 인덱스 콘텐츠.
    - ``content,title``
  * - suggest.update.request.interval
    - 서제스트 업데이트 요청 간격.
    - ``0``
  * - suggest.update.doc.per.request
    - 서제스트 업데이트 요청 1회당 문서 수.
    - ``2``
  * - suggest.update.contents.limit.num.percentage
    - 서제스트 업데이트 콘텐츠의 비율 제한(퍼센트).
    - ``50%``
  * - suggest.update.contents.limit.num
    - 서제스트 업데이트 콘텐츠의 최대 수.
    - ``10000``
  * - suggest.update.contents.limit.doc.size
    - 서제스트 업데이트의 최대 문서 크기.
    - ``50000``
  * - suggest.source.reader.scroll.size
    - 서제스트 소스 리더의 스크롤 크기.
    - ``1``
  * - suggest.popular.word.cache.size
    - 인기 단어 서제스트의 캐시 크기.
    - ``1000``
  * - suggest.popular.word.cache.expire
    - 인기 단어 서제스트의 캐시 만료 시간(초).
    - ``60``
  * - suggest.search.log.permissions
    - 서제스트 검색 로그의 권한.
    - ``{user}guest,{role}guest``
  * - suggest.system.monitor.interval
    - 서제스트의 시스템 모니터링 간격.
    - ``60``
  * - ldap.admin.enabled
    - LDAP 관리 활성화 여부.
    - ``false``
  * - ldap.admin.user.filter
    - LDAP 관리의 사용자 필터.
    - ``uid=%s``
  * - ldap.admin.user.base.dn
    - LDAP 관리 사용자의 베이스 DN.
    - ``ou=People,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.user.object.classes
    - LDAP 관리 사용자의 오브젝트 클래스.
    - ``organizationalPerson,top,person,inetOrgPerson``
  * - ldap.admin.role.filter
    - LDAP 관리의 역할 필터.
    - ``cn=%s``
  * - ldap.admin.role.base.dn
    - LDAP 관리 역할의 베이스 DN.
    - ``ou=Role,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.role.object.classes
    - LDAP 관리 역할의 오브젝트 클래스.
    - ``groupOfNames``
  * - ldap.admin.group.filter
    - LDAP 관리의 그룹 필터.
    - ``cn=%s``
  * - ldap.admin.group.base.dn
    - LDAP 관리 그룹의 베이스 DN.
    - ``ou=Group,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.group.object.classes
    - LDAP 관리 그룹의 오브젝트 클래스.
    - ``groupOfNames``
  * - ldap.admin.sync.password
    - LDAP 관리의 비밀번호 동기화 여부.
    - ``true``
  * - ldap.auth.validation
    - LDAP 인증 검증 여부.
    - ``true``
  * - ldap.connect.timeout
    - LDAP 연결을 수립하는 타임아웃(밀리초)입니다. TLS 핸드셰이크와 최초 바인드 응답에도 적용됩니다. 0 이하이면 JDK/OS 기본값에 맡깁니다.
    - ``10000``
  * - ldap.read.timeout
    - 연결이 바인드된 후 LDAP 응답을 기다리는 타임아웃(밀리초)입니다. 0 이하이면 무기한 기다립니다.
    - ``30000``
  * - ldap.search.time.limit
    - LDAP 검색의 서버 측 시간 제한(밀리초)입니다. 0 이하이면 제한이 없습니다.
    - ``60000``
  * - ldap.max.username.length
    - LDAP의 최대 사용자 이름 길이.
    - ``-1``
  * - ldap.ignore.netbios.name
    - LDAP에서 NetBIOS 이름 무시 여부.
    - ``true``
  * - ldap.group.name.with.underscores
    - LDAP 그룹 이름에 언더스코어 허용 여부.
    - ``false``
  * - ldap.lowercase.permission.name
    - LDAP 권한 이름에 소문자 사용 여부.
    - ``false``
  * - ldap.allow.empty.permission
    - LDAP에서 빈 권한 허용 여부.
    - ``true``
  * - ldap.samaccountname.group
    - LDAP 그룹에 samAccountName 사용 여부.
    - ``false``
  * - ldap.role.search.user.enabled
    - 사용자에 대한 LDAP 역할 검색 활성화 여부.
    - ``true``
  * - ldap.role.search.group.enabled
    - 그룹에 대한 LDAP 역할 검색 활성화 여부.
    - ``true``
  * - ldap.role.search.role.enabled
    - 역할에 대한 LDAP 역할 검색 활성화 여부.
    - ``true``
  * - ldap.attr.surname
    - 성에 대한 LDAP 속성.
    - ``sn``
  * - ldap.attr.givenName
    - 이름에 대한 LDAP 속성.
    - ``givenName``
  * - ldap.attr.employeeNumber
    - 사원 번호에 대한 LDAP 속성.
    - ``employeeNumber``
  * - ldap.attr.mail
    - 메일에 대한 LDAP 속성.
    - ``mail``
  * - ldap.attr.telephoneNumber
    - 전화번호에 대한 LDAP 속성.
    - ``telephoneNumber``
  * - ldap.attr.homePhone
    - 자택 전화에 대한 LDAP 속성.
    - ``homePhone``
  * - ldap.attr.homePostalAddress
    - 자택 우편 주소에 대한 LDAP 속성.
    - ``homePostalAddress``
  * - ldap.attr.labeledURI
    - 라벨이 붙은 URI에 대한 LDAP 속성.
    - ``labeledURI``
  * - ldap.attr.roomNumber
    - 방 번호에 대한 LDAP 속성.
    - ``roomNumber``
  * - ldap.attr.description
    - 설명에 대한 LDAP 속성.
    - ``description``
  * - ldap.attr.title
    - 직함에 대한 LDAP 속성.
    - ``title``
  * - ldap.attr.pager
    - 호출기에 대한 LDAP 속성.
    - ``pager``
  * - ldap.attr.street
    - 도로명에 대한 LDAP 속성.
    - ``street``
  * - ldap.attr.postalCode
    - 우편번호에 대한 LDAP 속성.
    - ``postalCode``
  * - ldap.attr.physicalDeliveryOfficeName
    - 우편물 배달 사무소 이름에 대한 LDAP 속성.
    - ``physicalDeliveryOfficeName``
  * - ldap.attr.destinationIndicator
    - 목적지 표시자에 대한 LDAP 속성.
    - ``destinationIndicator``
  * - ldap.attr.internationaliSDNNumber
    - 국제 ISDN 번호에 대한 LDAP 속성.
    - ``internationaliSDNNumber``
  * - ldap.attr.state
    - 주에 대한 LDAP 속성.
    - ``st``
  * - ldap.attr.employeeType
    - 직원 유형에 대한 LDAP 속성.
    - ``employeeType``
  * - ldap.attr.facsimileTelephoneNumber
    - 팩스 전화번호에 대한 LDAP 속성.
    - ``facsimileTelephoneNumber``
  * - ldap.attr.postOfficeBox
    - 사서함에 대한 LDAP 속성.
    - ``postOfficeBox``
  * - ldap.attr.initials
    - 이니셜에 대한 LDAP 속성.
    - ``initials``
  * - ldap.attr.carLicense
    - 자동차 면허에 대한 LDAP 속성.
    - ``carLicense``
  * - ldap.attr.mobile
    - 휴대전화에 대한 LDAP 속성.
    - ``mobile``
  * - ldap.attr.postalAddress
    - 우편 주소에 대한 LDAP 속성.
    - ``postalAddress``
  * - ldap.attr.city
    - 도시에 대한 LDAP 속성.
    - ``l``
  * - ldap.attr.teletexTerminalIdentifier
    - 텔레텍스 단말 식별자에 대한 LDAP 속성.
    - ``teletexTerminalIdentifier``
  * - ldap.attr.x121Address
    - X.121 주소에 대한 LDAP 속성.
    - ``x121Address``
  * - ldap.attr.businessCategory
    - 비즈니스 카테고리에 대한 LDAP 속성.
    - ``businessCategory``
  * - ldap.attr.registeredAddress
    - 등록 주소에 대한 LDAP 속성.
    - ``registeredAddress``
  * - ldap.attr.displayName
    - 표시 이름에 대한 LDAP 속성.
    - ``displayName``
  * - ldap.attr.preferredLanguage
    - 선호 언어에 대한 LDAP 속성.
    - ``preferredLanguage``
  * - ldap.attr.departmentNumber
    - 부서 번호에 대한 LDAP 속성.
    - ``departmentNumber``
  * - ldap.attr.uidNumber
    - UID 번호에 대한 LDAP 속성.
    - ``uidNumber``
  * - ldap.attr.gidNumber
    - GID 번호에 대한 LDAP 속성.
    - ``gidNumber``
  * - ldap.attr.homeDirectory
    - 홈 디렉터리에 대한 LDAP 속성.
    - ``homeDirectory``
  * - plugin.repositories
    - 플러그인 저장소 URL.
    - ``https://maven.codelibs.org/release/org/codelibs/fess/,https://repo.maven.apache.org/maven2/org/codelibs/fess/,https://fess.codelibs.org/plugin/artifacts.yaml``
  * - plugin.version.filter
    - 플러그인의 버전 필터.
    - (empty)
  * - storage.max.items.in.page
    - 스토리지의 페이지당 최대 항목 수.
    - ``1000``
  * - password.invalid.admin.passwords
    - 유효하지 않은 관리자 비밀번호 목록.
    - ``admin``
  * - password.min.length
    - 비밀번호의 최소 길이(0이면 비활성화).
    - ``8``
  * - password.max.length
    - 비밀번호 필드의 최대 길이.
    - ``100``
  * - password.require.uppercase
    - 비밀번호에 대문자를 요구합니다.
    - ``false``
  * - password.require.lowercase
    - 비밀번호에 소문자를 요구합니다.
    - ``false``
  * - password.require.digit
    - 비밀번호에 숫자를 요구합니다.
    - ``false``
  * - password.require.special.char
    - 비밀번호에 특수 문자를 요구합니다.
    - ``false``
  * - rag.chat.enabled
    - RAG 채팅 기능 활성화 여부.
    - ``false``
  * - rag.chat.log.enabled
    - RAG 채팅 요청마다의 사용 내역(사용자, 시간, LLM 호출 및 토큰)을 채팅 로그에 기록할지 여부입니다. 질문과 답변은 절대 기록되지 않습니다.
    - ``true``
  * - rag.chat.context.max.documents
    - 채팅 생성 설정.
    - ``5``
  * - rag.chat.query.regeneration.max.count
    - 검색에서 문서가 하나도 발견되지 않는 경우(스트리밍 채팅에서는 어떤 히트도 관련 있다고 판정되지 않는 경우), 하나의 채팅 요청이 검색 쿼리를 다시 생성하여 재검색하는 최대 횟수입니다. 재생성할 때마다 LLM 호출이 1회 발생하며, 새 검색에 히트가 있으면 관련성 평가 호출이 1회 추가됩니다(0이면 비활성화).
    - ``2``
  * - rag.chat.session.timeout.minutes
    - 세션 설정.
    - ``30``
  * - rag.chat.session.max.size
    - 캐시하는 채팅 세션의 최대 수이며, 이를 넘으면 가장 오래전에 접근한 세션부터 제거됩니다(0 이하는 100을 의미).
    - ``10000``
  * - rag.chat.history.max.messages
    - 하나의 채팅 세션에 유지하는 메시지의 최대 수이며, 새 메시지가 올 때마다 오래된 턴이 삭제됩니다.
    - ``30``
  * - rag.chat.content.fields
    - 강화된 RAG 플로우 설정입니다. 문서 전체 콘텐츠를 가져오는 필드입니다.
    - ``title,url,content,doc_id,content_title,content_description``
  * - rag.chat.highlight.fragment.size
    - RAG 검색의 하이라이트 설정.
    - ``500``
  * - rag.chat.highlight.number.of.fragments
    - RAG 채팅 컨텍스트 검색에서 문서당 하이라이트 프래그먼트 수.
    - ``3``
  * - rag.chat.content.fulltext.max.length
    - 답변 생성 시의 대용량 문서 처리입니다. content_length가 이 값을 초과하는 문서는 답변 컨텍스트에서 전체 콘텐츠 대신 하이라이트된 구절을 사용합니다.
    - ``3000``
  * - rag.chat.answer.highlight.fragment.size
    - 답변 컨텍스트를 위해 대용량 문서에서 구절을 추출할 때 사용하는 하이라이트 설정.
    - ``1000``
  * - rag.chat.answer.highlight.number.of.fragments
    - 답변 컨텍스트를 위해 크기가 큰 문서마다 가져오는 하이라이트 프래그먼트 수.
    - ``5``
  * - rag.chat.history.assistant.content
    - 어시스턴트 메시지의 이력 콘텐츠 모드입니다. smart_summary - 어시스턴트 본문은 제외하고 턴마다 과거 검색 쿼리와 참조한 제목만 유지(기본값, 권장) full - 어시스턴트 응답 전체를 전송 source_titles - 본문 + 참조한 제목 접미 source_titles_and_urls - "[References: title (url), ...]" 만 truncated - history.assistant.max.chars 에서 어시스턴트 응답을 잘라냄 none - 이력에서 어시스턴트 턴을 제외
    - ``smart_summary``
  * - rag.chat.history.titles.max.count
    - smart_summary 이력 모드에서 턴마다 포함하는 참조 문서 제목의 최대 수.
    - ``5``
  * - rag.chat.document.max.parts
    - LLM 컨텍스트 예산보다 긴 단일 문서에 대해 채팅할 때 문서를 분할하는 파트의 최대 수입니다. 각 파트는 개별적으로 요약되고 요약들이 답변으로 결합되며, 이 수를 넘는 파트는 사용되지 않습니다. 이러한 문서에 대한 요청은 매 턴마다 최대 이 수만큼의 LLM 호출에 답변용 호출 1회를 더해 수행합니다.
    - ``10``
  * - rag.chat.response.language
    - LLM에게 답변을 요청하는 언어입니다. browser - 사용자 브라우저 또는 UI 로캘의 언어. 영어에 대한 지시는 없음(기본값) none - 언어 지시 없음. LLM은 보통 질문의 언어로 답변함 en, ja.. - 항상 이 언어로 답변
    - ``browser``
  * - index.export.path
    - 인덱스 내보내기
    - ``/var/lib/fess/export``
  * - index.export.exclude.fields
    - 인덱스 내보내기 작업이 쓰는 파일에서 제외하는 문서 필드(쉼표 구분).
    - ``cache,tag``
  * - index.export.scroll.size
    - 인덱스 내보내기 작업의 스크롤 요청 1회당 가져오는 문서 수.
    - ``100``
  * - index.export.format
    - 내보낸 문서의 출력 형식이며, html과 json만 허용되고 그 외의 값은 작업을 실패시킵니다.
    - ``html``
  * - log.notification.flush.interval
    - 로그 통지 로그 통지 버퍼를 검색 엔진으로 플러시하는 간격(초).
    - ``30``
  * - log.notification.max.details.length
    - 통지 상세 텍스트의 최대 길이.
    - ``3000``
  * - log.notification.max.display.events
    - 통지에 표시할 이벤트의 최대 수.
    - ``50``
  * - log.notification.max.message.length
    - 통지 내 각 로그 메시지의 최대 길이.
    - ``200``
  * - log.notification.search.size
    - 통지 작업당 검색 엔진에서 가져오는 이벤트의 최대 수.
    - ``1000``
  * - log.notification.buffer.size
    - 메모리에 버퍼링하는 이벤트의 최대 수.
    - ``1000``
  * - log.notification.interval
    - 통지 작업 주기의 간격(초)이며, 통지 메시지에 사용됩니다.
    - ``300``
  * - theme.directory.path
    - 정적 테마 시스템(docs/superpowers/specs/2026-05-21-fess-static-theme-design.md 참조)
    - ``themes``
  * - theme.upload.max.size
    - 업로드한 테마 아카이브의 최대 크기(바이트).
    - ``52428800``
  * - theme.upload.max.extracted.size
    - 압축 해제 후 총 크기의 최대값(바이트)이며, 이를 초과하면 압축 해제가 중단됩니다.
    - ``209715200``
  * - theme.upload.max.entries
    - 업로드한 테마 아카이브에 허용되는 항목의 최대 수.
    - ``1000``
  * - theme.upload.max.compression.ratio
    - 테마 아카이브의 단일 항목에 대한 비압축/압축 비율의 최대값.
    - ``100``
  * - theme.upload.zip.ratio.max
    - 아카이브 전체에 대한 누적 비압축/압축 비율의 최대값(zip 폭탄 방어).
    - ``50``
  * - theme.upload.zip.ratio.check.threshold.bytes
    - 누적 zip 비율 검사가 적용되기 전에 읽는 압축 바이트 수이며, 이보다 작은 아카이브는 검사를 건너뜁니다.
    - ``65536``
  * - theme.upload.attic.retention.days
    - 교체된 테마 디렉터리를 클린업 스윕이 삭제하기 전까지의 보존 기간(일).
    - ``7``
  * - theme.repositories
    - 정적 테마를 다운로드하는 저장소 URL(쉼표 구분).
    - ``https://maven.codelibs.org/release/org/codelibs/fess/themes/``
  * - theme.index.frame.ancestors
    - 정적 테마의 HTML 페이지에 붙는 Content-Security-Policy의 frame-ancestors 디렉티브 값으로, 해당 페이지를 프레임에 포함할 수 있는 오리진입니다. 기본값 'none'은 어떤 페이지도 이를 포함할 수 없게 합니다. WebKit(Safari)은 테마의 파일 미리보기와 캐시 보기가 사용하는 blob: 프레임에도 frame-ancestors를 적용하므로, 값이 'none'인 동안은 이들이 빈 화면으로 표시됩니다. 디렉티브를 제거하려면 값을 비워 두십시오. X-Frame-Options: DENY는 어느 쪽이든 전송되며 모든 브라우저에서 해당 페이지가 프레임에 들어가지 않게 합니다(frame-ancestors를 따르는 브라우저는 그 헤더를 무시합니다).
    - ``'none'``
  * - theme.api.csrf.server.origins
    - 선택 사항: 이 Fess 인스턴스의 표준 외부 오리진(쉼표/줄바꿈 구분)입니다. 예: https://fess.example.com. 설정하면 전달된 헤더를 신뢰하지 않고 v2 CSRF Origin 검사에서 이들을 동일 오리진으로 취급합니다. rate.limit.trusted.proxies 에 등록되지 않은 리버스 프록시 뒤에서 사용하기를 권장합니다. 비어 있으면 신뢰하는 프록시의 X-Forwarded-\* 헤더에서, 그다음으로 서블릿 요청에서 대상 오리진을 재구성합니다.
    - (empty)
  * - theme.api.login.rate.limit.per.ip.per.minute
    - 클라이언트 IP당 1분에 허용되는 로그인 시도 횟수이며, 0 이하이면 이 제한(게이트)이 비활성화됩니다.
    - ``10``
  * - theme.api.login.rate.limit.per.user.per.minute
    - 클라이언트 IP 및 사용자 이름별로 1분에 허용되는 로그인 시도 횟수이며, 비밀번호 변경에도 이 제한이 적용됩니다.
    - ``5``
  * - theme.api.login.lockout.seconds
    - 로그인 속도 제한을 초과하면 적용되는 잠금 시간(초)이며, 0 이하이면 잠금이 비활성화됩니다.
    - ``900``
  * - theme.api.login.rate.limit.max.entries
    - 메모리에 보관하는 로그인 속도 제한 버킷의 최대 수이며, 상한에 도달하면 유휴 버킷부터 제거됩니다.
    - ``100000``
  * - api.chat.stream.keepalive.interval.ms
    - /api/v2/chat/stream 이 내보내는 SSE keep-alive ping의 간격입니다. ping은 주석만 있는 행(": keepalive\\n\\n")으로 이벤트 스트림에 영향을 주지 않으며, 긴 LLM 단계 동안 유휴 연결을 끊는 중간 장치(nginx의 기본 proxy_read_timeout은 60s)를 무력화합니다. 비활성화하려면 <=0으로 설정하십시오. 단위: 밀리초.
    - ``15000``
.. GENERATED-END: properties
