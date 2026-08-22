================
Analyzer 설정
================

Analyzer에 대하여
=================

검색을 위한 인덱스를 생성할 때 색인으로 등록하기 위해 문서를 분할해야 합니다.
|Fess| 에서는 문서를 단어로 분해하는 기능을 Analyzer로 등록하고 있습니다.
Analyzer는 CharFilter, Tokenizer 및 TokenFilter로 구성됩니다.

기본적으로 Analyzer에 의해 분할된 단위보다 작은 것은 검색해도 검색되지 않습니다.
예를 들어 "서울특별시에 거주"라는 문장을 생각해 봅시다.
이 문장이 "서울특별시", "에", "거주"와 같이 Analyzer에 의해 분할되었다고 가정합니다.
이 경우 "서울특별시"라는 단어로 검색하면 검색됩니다.
그러나 "서울시"라는 단어로 검색하면 검색되지 않습니다.

|Fess| 에서는 언어별로 전용 Analyzer를 제공합니다.
인덱스 내 필드명의 접미사(예: ``content_ja``, ``content_en``)에 따라 적용되는 언어별 Analyzer가 자동으로 전환됩니다.

Analyzer 정의 파일
==================

Analyzer는 전용 관리 화면을 갖지 않으며, 설정 파일을 직접 편집하여 변경합니다.
관련 파일은 ``app/WEB-INF/classes/fess_indices/`` 하위에 배치되어 있습니다.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 파일
     - 내용
   * - ``fess_indices/fess.json``
     - 문서 인덱스 설정. CharFilter, Tokenizer, TokenFilter 및 Analyzer의 정의를 포함합니다.
   * - ``fess_indices/fess/doc.json``
     - 문서 인덱스의 매핑. ``*_ja`` 나 ``*_en`` 과 같은 필드명 패턴별로 적용할 Analyzer를 지정합니다.
   * - ``fess_indices/fess/<언어>/``
     - 언어별 사전 파일(예: ``ja/kuromoji.txt``, ``ko/nori.txt``, ``en/protwords.txt``, ``en/stemmer_override.txt``, 각 언어의 ``stopwords.txt``).
   * - ``fess_indices/fess/mapping.txt``, ``fess_indices/fess/synonym.txt``
     - 모든 언어에서 공유되는 문자 매핑 사전 및 동의어 사전.

Analyzer 자체의 정의(Tokenizer나 TokenFilter의 조합)는 ``fess.json`` 에서 수행하고, 어떤 필드에 어떤 Analyzer를 적용할지는 ``fess/doc.json`` 에서 지정합니다.

.. note::
   Amazon OpenSearch Service 등의 매니지드 서비스를 이용하는 경우, ``fess_indices/_aws/fess.json`` 이나 ``fess_indices/_cloud/fess.json`` 과 같이 검색 엔진 종류에 대응하는 설정 파일이 우선적으로 사용됩니다.

Analyzer 등록
=============

Analyzer 설정은 |Fess| 시작 시 검색용 인덱스가 존재하지 않는 경우, 위의 설정 파일을 기반으로 인덱스를 생성하여 등록됩니다.
인덱스는 타임스탬프가 포함된 이름(예: ``fess.20240101120000000``)으로 생성되며, ``fess.search`` 및 ``fess.update`` 앨리어스가 할당됩니다.

설정 파일 내의 ``${fess.dictionary.path}`` 등의 플레이스홀더는 인덱스 생성 시 실제 값으로 치환됩니다.
사전 파일의 배치 경로는 시스템 프로퍼티 ``fess.dictionary.path`` 로 변경할 수 있습니다.

기존 인덱스가 있는 경우, 정의된 설정이 재사용됩니다.
따라서 Analyzer 정의를 변경한 경우, 변경 사항을 반영하려면 인덱스를 다시 생성해야 합니다.

사전에 의한 조정
================

Analyzer가 참조하는 사전은 관리 화면에서 편집할 수 있습니다.

* :doc:`../admin/kuromoji-guide` - 일본어 형태소 분석의 사용자 사전
* :doc:`../admin/synonym-guide` - 동의어 사전
* :doc:`../admin/mapping-guide` - 문자 매핑
* :doc:`../admin/stopwords-guide` - 불용어
* :doc:`../admin/protwords-guide` - 보호어
* :doc:`../admin/stemmeroverride-guide` - 스테밍 재정의

Analyzer의 구성 방법은 OpenSearch의 Analyzer 문서를 참조하십시오.

주의사항
========

Analyzer의 설정은 검색에 큰 영향을 줍니다.
Analyzer를 변경하는 경우 Lucene의 Analyzer의 동작을 이해한 후 수행하거나, 상용 지원에 문의하십시오.
