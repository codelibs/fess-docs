========
정렬 검색
========

검색 일시 등의 필드를 지정하여 검색 결과를 정렬할 수 있습니다.

정렬 대상 필드
---------------

기본적으로 다음 필드를 지정하여 정렬할 수 있습니다.

.. list-table::
   :header-rows: 1

   * - 필드명
     - 설명
   * - created
     - 크롤링한 일시
   * - content_length
     - 크롤링한 문서 크기
   * - last_modified
     - 크롤링한 문서의 최종 수정 일시
   * - filename
     - 파일명
   * - score
     - 점수 값
   * - timestamp
     - 문서를 인덱싱한 일시
   * - click_count
     - 문서를 클릭한 횟수
   * - favorite_count
     - 문서를 즐겨찾기한 횟수

표: 정렬 대상 필드 목록


커스터마이징을 통해 독자적인 필드를 정렬 대상으로 추가할 수도 있습니다.

사용 방법
------

검색 시 정렬 조건을 선택할 수 있습니다. 정렬 조건은 옵션 버튼을 클릭하여 표시되는 검색 옵션 대화상자에서 선택할 수 있습니다.

|image0|

또한 검색 필드에서 정렬하는 경우 "sort:필드명"과 같이 sort와 필드명을 콜론(:)으로 구분하여 검색 양식에 입력하여 검색합니다.

다음은 fess를 검색어로 하여 문서 크기를 오름차순으로 정렬합니다.

::

    fess sort:content_length

내림차순으로 정렬하는 경우 다음과 같이 합니다.

::

    fess sort:content_length.desc

여러 필드로 정렬하는 경우 다음과 같이 쉼표(,)로 구분하여 지정합니다.

::

    fess sort:content_length.desc,last_modified

.. |image0| image:: ../../../resources/images/en/15.4/user/search-sort-1.png
.. pdf            :width: 300 px
