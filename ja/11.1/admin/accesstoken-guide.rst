============
アクセストークン
============

概要
========

アクセストークン設定ページではアクセストークンを管理します。

管理方法
========

表示方法
--------

下図のアクセストークンの設定一覧ページを開くには、左メニューの[システム>アクセストークン] をクリックします。

|image0|

編集するには設定名をクリックします。

設定の作成
----------

アクセストークンの設定ページを開くには新規作成ボタンをクリックします。

|image1|

設定項目
--------

名前
::::

このアクセストークンを説明するための名前。

パーミッション
::::

Permissions for this access token.
This format is "{user/group/role}name".
For example, to display search results on users who belong to developer group, the permission is {group}developer.

Parameter Name
:::::

Request parameter name to specify permissions as a query.

Expired Time
::::::

Expired time for this access token.

Delete Configuration
--------------------

Click a configuration on a list page, and click Delete button to display a confirmation dialog.
Click Delete button to delete the configuration.



.. |image0| image:: ../../../resources/images/ja/11.1/admin/accesstoken-1.png
.. |image1| image:: ../../../resources/images/ja/11.1/admin/accesstoken-2.png
