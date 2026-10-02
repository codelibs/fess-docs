=============================================
Amazon Bedrock-Konfiguration (AI-Suche / RAG)
=============================================

Übersicht
=========

Diese Seite erläutert, wie Sie das Plugin ``fess-llm-bedrock`` konfigurieren, damit |Fess| Amazon Bedrock für seinen **AI-Suchmodus (RAG: Retrieval-Augmented Generation)** und als Embedding-Anbieter für Inhalts-Chunks nutzen kann.

Amazon Bedrock ist der AWS-Dienst, der Foundation-Modelle von Amazon und weiteren Modellanbietern über eine einheitliche API bereitstellt.
Das Plugin ruft die Bedrock-Runtime-API in der von Ihnen gewählten AWS-Region auf:

- **AI-Suchmodus**: die Converse API (``ConverseStream`` für gestreamte Antworten)
- **Embedding von Inhalts-Chunks**: die InvokeModel API mit Amazon Titan Text Embeddings V2 oder Cohere Embed

Unterstützte Modelle
--------------------

Der AI-Suchmodus funktioniert mit jedem Modell, das die Converse API in Ihrer Region unterstützt.
Standard ist Amazon Nova 2 Lite über das regionsübergreifende Inferenzprofil für die USA, ``us.amazon.nova-2-lite-v1:0``.
``rag.llm.bedrock.model`` akzeptiert eine Modell-ID, eine Inferenzprofil-ID (zum Beispiel mit dem Präfix ``us.``, ``eu.`` oder ``global.``) oder einen ARN.

Das Embedding von Inhalts-Chunks unterstützt die folgenden Modelle.

.. list-table::
   :header-rows: 1
   :widths: 40 35 25

   * - Modell
     - ``content_chunker.embedding.dimension``
     - Texte pro Anfrage
   * - ``amazon.titan-embed-text-v2:0``
     - ``256``, ``512`` oder ``1024``
     - 1
   * - ``cohere.embed-english-v3`` / ``cohere.embed-multilingual-v3``
     - ``1024``
     - bis zu 96, jeweils höchstens 2048 Zeichen
   * - ``cohere.embed-v4:0`` (auch über ein Inferenzprofil)
     - ``256``, ``512``, ``1024`` oder ``1536``
     - bis zu 96

Das Embedding-Modell wird anhand des Basismodellnamens innerhalb der konfigurierten ID erkannt: einer Basismodell-ID, einer regionsübergreifenden Inferenzprofil-ID (``us.``, ``eu.``, ``global.`` ...) oder eines ARN, der eine davon enthält.
Anwendungs-Inferenzprofile haben undurchsichtige IDs und werden nicht erkannt.

.. note::
   Welche Modelle in welcher Region verfügbar sind, finden Sie unter `Supported foundation models in Amazon Bedrock <https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html>`__.

Voraussetzungen
===============

1. **AWS-Konto** mit verfügbarem Amazon Bedrock in der von Ihnen verwendeten Region
2. **Modellzugriff**: Die konfigurierten Modelle müssen von Ihrem Konto aus in dieser Region nutzbar sein
3. **Zugangsdaten**: entweder ein Bedrock-API-Schlüssel oder AWS-Zugangsdaten mit der Berechtigung, die Modelle aufzurufen (siehe :ref:`bedrock-authentication`)

Plugin-Installation
===================

Die Bedrock-Integration wird als Plugin ``fess-llm-bedrock`` bereitgestellt.
Installieren Sie es in der Administrationsoberfläche unter „System" > „Plugins" oder legen Sie die JAR-Datei manuell ab und starten Sie |Fess| neu.

::

    cp fess-llm-bedrock-15.9.0.jar /path/to/fess/app/WEB-INF/plugin/

.. note::
   Die Plugin-Version muss mit der Version von |Fess| übereinstimmen.

Grundeinstellungen
==================

Der LLM-Anbieter (``rag.llm.name``) wird über die Administrationsoberfläche (Administration > System > Allgemein) oder in ``system.properties`` ausgewählt.
Die Aktivierung des AI-Suchmodus und die Einstellungen ``rag.llm.bedrock.*`` werden in ``fess_config.properties`` vorgenommen.

``system.properties`` (auch über Administration > System > Allgemein konfigurierbar):

::

    rag.llm.name=bedrock

``app/WEB-INF/classes/fess_config.properties`` (``/etc/fess/fess_config.properties`` bei Paketinstallationen), mit AWS-Zugangsdaten:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.model=us.amazon.nova-2-lite-v1:0

Mit einem Bedrock-API-Schlüssel anstelle von AWS-Zugangsdaten:

::

    rag.chat.enabled=true
    rag.llm.bedrock.region=us-east-1
    rag.llm.bedrock.api.key=your-bedrock-api-key

Einstellungselemente
====================

Alle Einstellungselemente des Clients für den AI-Suchmodus. Sie werden in ``fess_config.properties`` (oder als JVM-Optionen ``-Dfess.config.<key>``) vorgenommen.

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rag.llm.bedrock.api.key``
     - Bedrock-API-Schlüssel. Wenn leer, werden Anfragen mit AWS-Zugangsdaten signiert (SigV4)
     - ``""``
   * - ``rag.llm.bedrock.region``
     - AWS-Region des Bedrock-Runtime-Endpunkts und der SigV4-Signatur
     - ``us-east-1``
   * - ``rag.llm.bedrock.endpoint``
     - Endpunkt-URL, zum Beispiel ein VPC-Schnittstellenendpunkt. Wenn leer, ``https://bedrock-runtime.<region>.amazonaws.com``
     - ``""``
   * - ``rag.llm.bedrock.model``
     - Modell-ID, Inferenzprofil-ID oder ARN
     - ``us.amazon.nova-2-lite-v1:0``
   * - ``rag.llm.bedrock.timeout``
     - Anfrage-Timeout (in Millisekunden)
     - ``120000``
   * - ``rag.llm.bedrock.availability.check.interval``
     - Intervall der Verfügbarkeitsprüfung (in Sekunden)
     - ``60``
   * - ``rag.llm.bedrock.temperature.enabled``
     - ``false`` verhindert das Senden von ``temperature``, für Modelle oder Modi, die es ablehnen
     - ``true``
   * - ``rag.llm.bedrock.additional.model.request.fields``
     - JSON-Objekt, das für modellspezifische Parameter als ``additionalModelRequestFields`` gesendet wird
     - ``""``
   * - ``rag.llm.bedrock.max.concurrent.requests``
     - Maximale Anzahl gleichzeitiger Anfragen
     - ``5``
   * - ``rag.llm.bedrock.concurrency.wait.timeout``
     - Wartezeit bei gleichzeitigen Anfragen (Millisekunden)
     - ``30000``
   * - ``rag.llm.bedrock.answer.context.max.chars``
     - Maximale Zeichenzahl des abgerufenen Kontexts für die Antwortgenerierung
     - ``16000``
   * - ``rag.llm.bedrock.summary.context.max.chars``
     - Maximale Zeichenzahl des Dokuments für die Zusammenfassungsgenerierung
     - ``16000``
   * - ``rag.llm.bedrock.faq.context.max.chars``
     - Maximale Zeichenzahl des abgerufenen Kontexts für die FAQ-Generierung
     - ``10000``
   * - ``rag.llm.bedrock.chat.evaluation.max.relevant.docs``
     - Maximale Anzahl relevanter Dokumente bei der Bewertung
     - ``3``
   * - ``rag.llm.bedrock.chat.evaluation.description.max.chars``
     - Maximale Zeichenzahl für Dokumentbeschreibung bei der Bewertung
     - ``500``
   * - ``rag.llm.bedrock.history.max.chars``
     - Maximale Zeichenzahl für Chat-Verlauf
     - ``8000``
   * - ``rag.llm.bedrock.intent.history.max.messages``
     - Maximale Anzahl von Verlaufsnachrichten für Absichtserkennung
     - ``8``
   * - ``rag.llm.bedrock.intent.history.max.chars``
     - Maximale Verlaufszeichenzahl für Absichtserkennung
     - ``4000``
   * - ``rag.llm.bedrock.history.assistant.max.chars``
     - Maximale Zeichenzahl für Assistenten-Verlauf
     - ``800``
   * - ``rag.llm.bedrock.history.assistant.summary.max.chars``
     - Maximale Zeichenzahl für Assistenten-Zusammenfassungsverlauf
     - ``800``
   * - ``rag.llm.bedrock.retry.max``
     - Maximale Anzahl von HTTP-Versuchen (bei ``429``, ``500``, ``502``, ``503`` und ``504``)
     - ``10``
   * - ``rag.llm.bedrock.retry.base.delay.ms``
     - Basisverzögerung des exponentiellen Backoffs (in Millisekunden)
     - ``2000``

.. _bedrock-authentication:

Authentifizierung
=================

API-Schlüssel
-------------

Wenn ``rag.llm.bedrock.api.key`` gesetzt ist, wird er als ``Authorization: Bearer <key>`` gesendet.
Kurzlebige Bedrock-API-Schlüssel laufen ab und sind nur in der Region gültig, in der sie erstellt wurden; langlebige Schlüssel sind an einen IAM-Benutzer gebunden.
Der Wert wird unter Administration > Systeminformationen maskiert angezeigt, wenn er in ``fess_config.properties`` gesetzt ist (bzw. bei ``content_chunker.embedding.bedrock.api.key`` in ``system.properties``).
Umgebungsvariablen und JVM-Systemeigenschaften, einschließlich der Optionen ``-Dfess.config.*`` und ``-Dfess.system.*``, werden dort unmaskiert aufgelistet; übergeben Sie den Schlüssel daher nicht auf diesem Weg.

AWS-Zugangsdaten (SigV4)
------------------------

Ist kein API-Schlüssel gesetzt, wird jede Anfrage mit AWS Signature Version 4 signiert.
Die Zugangsdaten stammen aus der ersten der folgenden Quellen, die sie bereitstellt:

1. die JVM-Systemeigenschaften ``aws.accessKeyId`` / ``aws.secretAccessKey`` / ``aws.sessionToken``
2. die Umgebungsvariablen ``AWS_ACCESS_KEY_ID`` / ``AWS_SECRET_ACCESS_KEY`` / ``AWS_SESSION_TOKEN``
3. Web Identity (``AWS_WEB_IDENTITY_TOKEN_FILE`` und ``AWS_ROLE_ARN``, wie unter Amazon EKS verwendet)
4. die gemeinsamen Dateien ``~/.aws/credentials`` und ``~/.aws/config`` (``AWS_PROFILE`` wählt das Profil aus)
5. der Container-Credentials-Endpunkt (Amazon ECS)
6. der EC2-Instance-Metadata-Service (Instanzprofil)

Die JVM-Systemeigenschaften (Quelle 1) erreichen nur den Webprozess von |Fess|.
Die Einbettung von Inhalts-Chunks (Dokumenten) läuft in einer separaten Kind-JVM; verwenden Sie dafür daher Umgebungsvariablen, ein gemeinsames Zugangsdatenprofil oder eine IAM-Rolle oder wiederholen Sie die Optionen ``-Daws.*`` in ``jvm.chunk.options``.

Die Region stammt immer aus ``rag.llm.bedrock.region``; ``AWS_REGION`` wird nicht gelesen.
Profile, die IAM Identity Center (SSO) verwenden, werden nicht unterstützt.

.. warning::
   Bevorzugen Sie eine IAM-Rolle (EC2-Instanzprofil, ECS-Task-Rolle, EKS-Web-Identity) oder die gemeinsame Zugangsdatendatei des Benutzers, unter dem |Fess| läuft.
   Umgebungsvariablen und JVM-Systemeigenschaften werden unter Administration > Systeminformationen unmaskiert aufgelistet; halten Sie langlebige Schlüssel daher aus ihnen heraus.

Der IAM-Principal benötigt ``bedrock:InvokeModel`` (Converse und InvokeModel) sowie ``bedrock:InvokeModelWithResponseStream`` (ConverseStream) für die Modelle, die er verwendet.
Handelt es sich bei dem Modell um ein Inferenzprofil, erlauben Sie sowohl das Inferenzprofil als auch die Foundation-Modelle, an die es weiterleitet.

Retry-Verhalten
===============

Anfragen werden bei ``429``, ``500``, ``502``, ``503`` und ``504`` sowie dann wiederholt, wenn die Verbindung zu Bedrock nicht hergestellt werden konnte.
Wiederholungsversuche warten mit exponentiellem Backoff (Basiswert ``rag.llm.bedrock.retry.base.delay.ms``, ±20% Jitter, maximal ``rag.llm.bedrock.retry.max`` Versuche); ein ``Retry-After``-Header hat Vorrang.
Bei Streaming-Anfragen wird nur die initiale Anfrage wiederholt; ein Fehler nach Beginn des Streamings der Antwort, einschließlich eines Exception-Events innerhalb des Streams, beendet die Anfrage.

Prompttypspezifische Einstellungen
==================================

``temperature`` und ``max.tokens`` können wie bei den anderen Anbietern pro Prompttyp festgelegt werden:

::

    rag.llm.bedrock.{promptType}.temperature
    rag.llm.bedrock.{promptType}.max.tokens
    rag.llm.bedrock.{promptType}.context.max.chars
    rag.llm.bedrock.{promptType}.additional.model.request.fields

``{promptType}`` ist einer von ``intent``, ``evaluation``, ``unclear``, ``noresults``, ``docnotfound``, ``direct``, ``faq``, ``answer``, ``summary`` und ``queryregeneration``.
Ein prompttypspezifisches ``additional.model.request.fields`` ersetzt für diesen Prompttyp den globalen Wert.

Standardwerte, die verwendet werden, wenn nichts konfiguriert ist:

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Prompttyp
     - temperature
     - max.tokens
   * - ``intent``, ``evaluation``
     - ``0.1``
     - ``256``
   * - ``unclear``, ``noresults``
     - ``0.7``
     - ``512``
   * - ``docnotfound``
     - ``0.7``
     - ``256``
   * - ``direct``, ``faq``
     - ``0.7``
     - ``1024``
   * - ``answer``
     - ``0.5``
     - ``2048``
   * - ``summary``
     - ``0.3``
     - ``2048``
   * - ``queryregeneration``
     - ``0.3``
     - ``256``

.. note::
   ``rag.llm.bedrock.{promptType}.thinking.budget`` wird nicht unterstützt: Die Reasoning-Einstellungen unterscheiden sich bei Bedrock von Modell zu Modell.
   Ein konfigurierter Wert wird nicht gesendet und es wird eine WARN-Meldung protokolliert. Verwenden Sie stattdessen ``additional.model.request.fields``.

Modellspezifische Parameter
===========================

``additional.model.request.fields`` übergibt ein JSON-Objekt unverändert an das Modell.
Ein Wert, der kein JSON-Objekt ist, wird nicht gesendet; stattdessen wird eine WARN-Meldung mit dem Namen der Eigenschaft protokolliert.

Zum Beispiel, um Extended Thinking eines Anthropic-Claude-Modells nur für die Antwortgenerierung zu verwenden:

::

    rag.llm.bedrock.model=<a Claude model ID or inference profile ID>
    rag.llm.bedrock.temperature.enabled=false
    rag.llm.bedrock.answer.additional.model.request.fields={"thinking":{"type":"enabled","budget_tokens":2048}}
    rag.llm.bedrock.answer.max.tokens=6144

Claude lehnt ``temperature`` ab, solange Thinking aktiviert ist, und ``max.tokens`` muss größer als ``budget_tokens`` sein.
Reasoning-Text wird Benutzern nie angezeigt; nur der Antworttext wird angezeigt.

Embedding von Inhalts-Chunks
============================

Um Bedrock für das Embedding von Inhalts-Chunks zu verwenden, setzen Sie Folgendes in ``app/WEB-INF/conf/system.properties`` (bei den RPM/DEB-Paketen ``/etc/fess/system.properties``, unter Docker ``/opt/fess/system.properties``) oder als Optionen ``-Dfess.system.<key>``.
Anders als ``rag.llm.bedrock.*`` werden diese Schlüssel nicht aus ``fess_config.properties`` gelesen.

::

    content_chunker.enabled=true
    content_chunker.embedding.name=bedrock
    content_chunker.embedding.dimension=1024
    content_chunker.embedding.bedrock.region=us-east-1
    content_chunker.embedding.bedrock.model=amazon.titan-embed-text-v2:0

.. list-table::
   :header-rows: 1
   :widths: 40 40 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``content_chunker.embedding.bedrock.api.key``
     - Bedrock-API-Schlüssel. Wenn leer, werden AWS-Zugangsdaten verwendet
     - ``""``
   * - ``content_chunker.embedding.bedrock.region``
     - AWS-Region
     - ``us-east-1``
   * - ``content_chunker.embedding.bedrock.endpoint``
     - Endpunkt-URL. Wenn leer, wird sie aus der Region abgeleitet
     - ``""``
   * - ``content_chunker.embedding.bedrock.model``
     - Embedding-Modell (siehe `Unterstützte Modelle`_)
     - ``amazon.titan-embed-text-v2:0``
   * - ``content_chunker.embedding.bedrock.normalize``
     - Nur Titan: ob Vektoren normalisiert werden
     - ``true``
   * - ``content_chunker.embedding.bedrock.truncate``
     - Nur Cohere: ``truncate`` (``NONE``/``START``/``END`` für v3, ``NONE``/``LEFT``/``RIGHT`` für v4). Wird nicht gesendet, wenn leer
     - ``""``
   * - ``content_chunker.embedding.bedrock.timeout``
     - Anfrage-Timeout (in Millisekunden)
     - ``120000``
   * - ``content_chunker.embedding.bedrock.connect.timeout``
     - Verbindungs-Timeout (in Millisekunden)
     - ``5000``
   * - ``content_chunker.embedding.bedrock.availability.check.interval``
     - Intervall der Verfügbarkeitsprüfung (in Sekunden)
     - ``60``
   * - ``content_chunker.embedding.bedrock.retry.max``
     - Maximale Anzahl von HTTP-Versuchen (bei ``429``, ``500``, ``502``, ``503`` und ``504``)
     - ``10``
   * - ``content_chunker.embedding.bedrock.retry.base.delay.ms``
     - Basisverzögerung des exponentiellen Backoffs (in Millisekunden)
     - ``2000``
   * - ``content_chunker.embedding.bedrock.retry.max.delay.ms``
     - Obergrenze einer einzelnen Backoff-Wartezeit, ``Retry-After`` eingeschlossen (in Millisekunden)
     - ``60000``

``content_chunker.embedding.dimension`` muss eine Größe sein, die das Modell erzeugt (siehe `Unterstützte Modelle`_); andernfalls wird der Embedding-Anbieter mit einem ERROR-Log als nicht verfügbar gemeldet.
Dokumente werden mit Coheres ``input_type=search_document`` und Anfragen mit ``search_query`` eingebettet.
Cohere Embed v3 akzeptiert höchstens 2048 Zeichen pro Text. Bedrock weist einen längeren Text mit ``400 ValidationException`` ab, unabhängig davon, was ``truncate`` festlegt; das Plugin kürzt oder teilt Texte nicht.
``truncate`` (``END``, wenn nicht gesetzt) gilt nur für einen Text innerhalb von 2048 Zeichen, der 512 Tokens überschreitet.

HTTP-Proxy verwenden
====================

Anfragen an Bedrock nutzen die globale HTTP-Proxy-Konfiguration von |Fess| (``http.proxy.host``, ``http.proxy.port``, ``http.proxy.username`` und ``http.proxy.password`` in ``fess_config.properties``).
Abfragen von Zugangsdaten, die AWS-Endpunkte aufrufen (STS für Web Identity, der Container-Credentials-Endpunkt, der Instance-Metadata-Service), verwenden diese Einstellungen nicht.
Um Bedrock über einen VPC-Schnittstellenendpunkt zu erreichen, setzen Sie ``rag.llm.bedrock.endpoint`` (und ``content_chunker.embedding.bedrock.endpoint``) auf dessen URL; die Regionseinstellung bestimmt weiterhin die Signaturregion.

Fehlerbehebung
==============

AI-Suchmodus ist nicht verfügbar
--------------------------------

Der Client meldet sich als verfügbar, wenn Modell und Region gesetzt sind, der Endpunkt eine gültige URL ist und entweder ein API-Schlüssel gesetzt ist oder AWS-Zugangsdaten aufgelöst werden können.
Eine ungültige Region oder ein ungültiger Endpunkt wird als ERROR protokolliert. Um herauszufinden, warum Zugangsdaten nicht aufgelöst werden konnten, aktivieren Sie DEBUG für ``org.codelibs.fess.llm.bedrock``.
Eine fehlgeschlagene Abfrage der Zugangsdaten wird 60 Sekunden lang gemerkt, sodass später verfügbar gemachte Zugangsdaten innerhalb einer Minute übernommen werden.

Zugriff verweigert
------------------

Ein ``403`` mit ``type=AccessDeniedException`` im WARN-Log bedeutet, dass der API-Schlüssel oder der IAM-Principal das Modell nicht aufrufen darf.
Prüfen Sie die oben genannten IAM-Berechtigungen sowie, ob das Modell von Ihrem Konto aus in der konfigurierten Region genutzt werden kann.

Validierungsfehler
------------------

Ein ``400`` mit ``type=ValidationException`` bedeutet in der Regel, dass die Modell-ID in der Region nicht verfügbar ist (bei manchen Modellen kann nur eine Inferenzprofil-ID verwendet werden) oder dass ``additional.model.request.fields`` Parameter enthält, die das Modell nicht akzeptiert.

Debug-Einstellungen
-------------------

Aktivieren Sie DEBUG für ``org.codelibs.fess.llm.bedrock``, um die Anfrage- und Antwortkörper des AI-Suchmodus sowie den Grund zu protokollieren, warum AWS-Zugangsdaten nicht aufgelöst werden konnten.
DEBUG für ``org.codelibs.fess.embedding.bedrock`` protokolliert, wie der Anfragetext normalisiert wurde, sowie denselben Grund für die Zugangsdaten; Embedding-Anfragen werden nicht protokolliert.
API-Schlüssel, AWS-Zugangsdaten und Signaturen werden von diesen Loggern nie geschrieben.

.. warning::
   Zwei andere Logger schreiben bei DEBUG Zugangsdaten: Das Wire-Logging des Apache HttpClient schreibt den ``Authorization``-Header, und der Signierer des AWS SDK (``software.amazon.awssdk.http.auth.aws.internal.signer``) schreibt die kanonische Anfrage, einschließlich des ``x-amz-security-token`` temporärer Zugangsdaten.
   Wird |Fess| mit dem Root-Log-Level DEBUG gestartet, sind beide aktiviert; belassen Sie ``org.apache.hc`` und ``software.amazon.awssdk`` bei INFO oder höher.

Weiterführende Informationen
============================

- :doc:`llm-overview` - Übersicht LLM-Integration
- :doc:`rag-chat` - Details zur AI-Suchmodus-Funktion
- :doc:`search-semantic` - Semantische Suche und Embedding von Inhalts-Chunks
- `Amazon Bedrock User Guide <https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html>`__
