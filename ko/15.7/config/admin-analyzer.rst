=============
Analyzer 설정
=============

Analyzer에 대하여
==============

검색을 위한 인덱스를 생성할 때 색인으로 등록하기 위해 문서를 분할해야 합니다.
|Fess| 에서는 문서를 단어로 분해하는 기능을 Analyzer로 등록하고 있습니다.
Analyzer는 CharFilter, Tokenizer 및 TokenFilter로 구성됩니다.

기본적으로 Analyzer에 의해 분할된 단위보다 작은 것은 검색해도 검색되지 않습니다.
예를 들어 "서울특별시에 거주"라는 문장을 생각해 봅시다.
이 문장이 "서울특별시", "에", "거주"와 같이 Analyzer에 의해 분할되었다고 가정합니다.
이 경우 "서울특별시"라는 단어로 검색하면 검색됩니다.
그러나 "서울시"라는 단어로 검색하면 검색되지 않습니다.

Analyzer의 설정은 |Fess| 시작 시 fess 인덱스가 존재하지 않는 경우 app/WEB-INF/classes/fess_indices/fess.json에서 fess 인덱스를 생성하여 등록됩니다.
Analyzer의 구성 방법은 OpenSearch의 Analyzer 문서를 참조하십시오.

Analyzer의 설정은 검색에 큰 영향을 줍니다.
Analyzer를 변경하는 경우 Lucene의 Analyzer의 동작을 이해한 후 수행하거나 상용 지원에 문의하십시오.
