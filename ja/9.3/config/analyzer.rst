====================
索引文字列抽出の設定
====================

索引文字列抽出について
======================

検索のためのインデックスを作成する際、索引として登録するために文書を切り分ける必要があります。
|Fess| では、文書を単語に分解する機能を Analyzer として登録します。
Analyzer は CharFilter、Tokenizer および TokenFilter により構成されます。

基本的に、Analyzer によって切り分けられた単位よりも小さいものは、検索を行ってもヒットしません。
たとえば、「東京都に住む」という文を考えます。
この文が「東京都」「に」「住む」というように Analyzer によって分割されたとします。
この場合、「東京都」という語で検索を行った場合はヒットします。
しかし、「京都」という語で検索を行った場合はヒットしません。

Analyzer の設定は solr/core1/conf/schema.xml で設定されています。
|Fess| のデフォルトでは、fieldType 要素で name 属性が text の Analyzer が利用されています。

::
    <fieldType name="text" class="solr.TextField" positionIncrementGap="100" autoGeneratePhraseQueries="true">
      <analyzer type="index">
        <tokenizer class="jp.sf.fess.solr.plugin.analysis.monitor.MonitoringTokenizerFactory"
            monitoringFile="synonyms.txt"
            baseClass="jp.sf.fess.solr.plugin.analysis.synonym.NGramSynonymTokenizerFactory"
            expand="true"
            n="2"
            synonyms="synonyms.txt"
            />
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
      <analyzer type="query">
        <tokenizer class="jp.sf.fess.solr.plugin.analysis.monitor.MonitoringTokenizerFactory"
            monitoringFile="synonyms.txt"
            baseClass="jp.sf.fess.solr.plugin.analysis.synonym.NGramSynonymTokenizerFactory"
            expand="false"
            n="2"
            synonyms="synonyms.txt"
            />
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
    </fieldType>

type 属性が index であるものがインデクシング時に利用される Analyzer で、query であるものが検索時に利用される Analyzer になります。
また、|Fess| では言語判定機能を実装しており、対象ドキュメントの言語が判定できた場合には各言語用のインデックスも追加で作成されます。
たとえば、日本語であれば以下の Analyzer が適用されます。

::

    <fieldType name="text_ja" class="solr.TextField" positionIncrementGap="100" autoGeneratePhraseQueries="true">
      <analyzer>
        <tokenizer class="jp.sf.fess.solr.plugin.analysis.monitor.MonitoringTokenizerFactory"
            monitoringFile="lang/userdict_ja.txt"
            baseClass="org.apache.lucene.analysis.ja.JapaneseTokenizerFactory"
            mode="search" userDictionary="lang/userdict_ja.txt"/>
        <filter class="solr.JapaneseBaseFormFilterFactory"/>
        <filter class="solr.JapanesePartOfSpeechStopFilterFactory" tags="lang/stoptags_ja.txt" />
        <filter class="solr.CJKWidthFilterFactory"/>
        <filter class="solr.StopFilterFactory" ignoreCase="true" words="lang/stopwords_ja.txt" />
        <filter class="solr.JapaneseKatakanaStemFilterFactory" minimumLength="4"/>
        <filter class="solr.LowerCaseFilterFactory"/>
      </analyzer>
    </fieldType>

Analyzer の設定は検索に大きな影響を与えます。
schema.xml で Analyzer の変更する場合は、Lucene の Analyzer の動きを理解した上で実施してください。

