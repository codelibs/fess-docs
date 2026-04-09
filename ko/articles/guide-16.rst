============================================================
제16회: 검색 인프라 자동화 -- CI/CD 파이프라인과 Infrastructure as Code를 활용한 관리
============================================================

들어가며
========

검색 시스템의 설정을 수동으로 관리하면 환경 재현이 어려워지고 설정 오류의 위험도 높아집니다.
모던 DevOps 사고방식을 도입하여 검색 인프라도 코드로 관리하고 자동화합시다.

이 글에서는 Fess의 설정을 코드로 관리하고 배포를 자동화하는 접근 방식을 소개합니다.

대상 독자
=========

- 검색 시스템 운영을 자동화하고 싶은 분
- DevOps/IaC 방법론을 검색 인프라에 적용하고 싶은 분
- Docker와 CI/CD에 대한 기본 지식이 있는 분

Infrastructure as Code 적용
==============================

Fess 환경을 "코드"로 관리하는 대상은 다음과 같습니다.

.. list-table:: IaC 관리 대상
   :header-rows: 1
   :widths: 25 35 40

   * - 대상
     - 관리 방법
     - 버전 관리
   * - Docker 구성
     - compose.yaml
     - Git
   * - Fess 설정
     - 백업 파일 / 관리 API
     - Git
   * - 사전 데이터
     - 관리 API로 내보내기
     - Git
   * - OpenSearch 설정
     - 설정 파일
     - Git

Docker Compose를 이용한 환경 정의
====================================

프로덕션 환경용 Docker Compose 파일
--------------------------------------

제2회에서 사용한 기본 구성을 확장하여 프로덕션 환경에 적합한 구성을 정의합니다.

.. code-block:: yaml

    services:
      fess:
        image: ghcr.io/codelibs/fess:15.5.1
        environment:
          - SEARCH_ENGINE_HTTP_URL=http://opensearch:9200
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        ports:
          - "8080:8080"
        depends_on:
          opensearch:
            condition: service_healthy
        restart: unless-stopped

      opensearch:
        image: ghcr.io/codelibs/fess-opensearch:3.6.0
        environment:
          - discovery.type=single-node
          - OPENSEARCH_JAVA_OPTS=-Xmx4g -Xms4g
          - DISABLE_INSTALL_DEMO_CONFIG=true
          - DISABLE_SECURITY_PLUGIN=true
          - FESS_DICTIONARY_PATH=/usr/share/opensearch/config/dictionary/
        volumes:
          - opensearch-data:/usr/share/opensearch/data
          - opensearch-dictionary:/usr/share/opensearch/config/dictionary
        healthcheck:
          test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 90s
        restart: unless-stopped

    volumes:
      opensearch-data:
      opensearch-dictionary:

주요 포인트는 다음과 같습니다.

- 헬스 체크 정의: OpenSearch가 준비된 후 Fess를 시작
- 볼륨 영속화: 데이터 영속화
- 재시작 정책: 장애 시 자동 복구
- JVM 힙의 명시적 설정

관리 API를 이용한 설정 자동화
===============================

Fess의 관리 API를 사용하면 GUI를 거치지 않고 프로그래밍 방식으로 설정을 조작할 수 있습니다.

설정 내보내기
--------------

현재 Fess 설정을 내보내어 코드로 저장합니다.

관리 화면의 [시스템 정보] > [백업]에서 내보낼 수 있습니다.
또한 관리 API를 사용하여 스크립트에서 내보내기도 가능합니다.

설정 가져오기
--------------

저장한 설정 파일을 사용하여 새로운 Fess 환경에 설정을 적용합니다.
이를 통해 환경의 재구축이나 복제가 용이해집니다.

fessctl CLI 활용
===================

fessctl은 Fess의 커맨드라인 도구입니다.
관리 화면에서 수행하는 대부분의 작업을 커맨드라인에서 실행할 수 있습니다.

주요 작업
----------

- 크롤 설정의 생성, 업데이트, 삭제(웹, 파일 시스템, 데이터 스토어)
- 스케줄러 작업 실행
- 사용자, 역할, 그룹 관리
- 키 매치, 라벨, 부스트 등의 검색 설정 관리

CLI를 사용하면 설정 변경을 스크립트화하여 CI/CD 파이프라인에 통합할 수 있습니다.

CI/CD 파이프라인 구축
=======================

설정 변경 워크플로
--------------------

검색 시스템의 설정 변경을 다음 워크플로로 관리합니다.

1. **변경**: 설정 파일을 수정하고 Git 브랜치에서 관리
2. **리뷰**: 풀 리퀘스트로 변경 내용을 리뷰
3. **테스트**: 스테이징 환경에서 동작 확인
4. **배포**: 프로덕션 환경에 설정 적용

GitHub Actions 자동화 예시
----------------------------

설정 파일의 변경이 머지되면 자동으로 프로덕션 환경에 반영하는 예시입니다.

.. code-block:: yaml

    name: Deploy Fess Config
    on:
      push:
        branches: [main]
        paths:
          - 'fess-config/**'
          - 'dictionary/**'

    jobs:
      deploy:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4

          - name: Apply dictionary updates
            run: |
              # 사전 파일을 Fess 서버로 전송
              scp dictionary/* fess-server:/opt/fess/dictionary/

          - name: Verify Fess health
            run: |
              # 헬스 API로 Fess 가동 상태 확인
              curl -s https://fess.example.com/api/v1/health

백업 자동화
============

정기적인 백업도 자동화합시다.

백업 스크립트
--------------

cron이나 CI/CD의 스케줄 기능을 사용하여 정기적으로 백업을 수행합니다.

.. code-block:: bash

    #!/bin/bash
    set -euo pipefail

    BACKUP_DIR="/backup/fess/$(date +%Y%m%d)"
    mkdir -p "${BACKUP_DIR}"

    # Fess 백업 파일 목록 가져오기
    curl -s -o "${BACKUP_DIR}/fess-backup-files.json" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/files"

    # 설정 데이터 다운로드(예: fess_config.bulk)
    curl -s -o "${BACKUP_DIR}/fess_config.bulk" \
      -H "Authorization: Bearer ${FESS_TOKEN}" \
      "https://fess.example.com/api/admin/backup/file/fess_config.bulk"

    # 오래된 백업 삭제(30일 이상)
    find /backup/fess -type d -mtime +30 -exec rm -rf {} +

    echo "Backup completed: ${BACKUP_DIR}"

환경 재구축 절차
=================

재해 복구나 테스트 환경 구축을 위해 환경을 완전히 재구축하는 절차를 문서화해 둡니다.

1. Docker Compose로 컨테이너 시작
2. OpenSearch의 헬스 체크가 green/yellow가 될 때까지 대기
3. Fess 설정 가져오기(관리 API 또는 복원 기능)
4. 사전 파일 배치
5. 크롤 작업 실행
6. 동작 확인(검색 테스트)

이 절차를 스크립트화해 두면 환경 재구축을 신속하게 수행할 수 있습니다.

정리
====

이 글에서는 Fess의 검색 인프라를 DevOps 방법론으로 관리하는 접근 방식을 소개했습니다.

- Docker Compose를 이용한 환경 정의의 코드화
- 관리 API와 fessctl을 이용한 설정 자동화
- CI/CD 파이프라인을 이용한 설정 변경 배포 자동화
- 백업 자동화와 환경 재구축 절차

"절차서를 읽고 수작업으로 설정"에서 "코드를 실행하여 자동 배포"로, 검색 인프라 운영을 발전시킵시다.

다음 회에서는 플러그인 개발을 통한 Fess 확장에 대해 다룹니다.

참고 자료
=========

- `Fess 관리 API <https://fess.codelibs.org/ja/15.5/api/api-admin.html>`__

- `Docker Fess <https://github.com/codelibs/docker-fess>`__
