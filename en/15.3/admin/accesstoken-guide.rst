============
Access Token
============

Overview
========

The access token settings page manages access tokens.

Management Operations
=====================

Display Method
--------------

To open the access token configuration list page shown below, click [System > Access Token] in the left menu.

|image0|

Click the configuration name to edit it.

Creating Configuration
----------------------

To open the access token configuration page, click the New button.

|image1|

Configuration Items
-------------------

Name
::::

Specifies the name to describe this access token.

Permission
::::::::::

Sets the permission for the access token.
Described in "{user|group|role}name" format.
For example, to allow users belonging to the developer group to view search results, set the permission to "{group}developer".

Parameter Name
::::::::::::::

Specifies the request parameter name when specifying permission as a search query.

.. warning::

   The parameter name feature is designed for use in trusted internal environments only.
   When this feature is enabled, additional permissions can be specified through URL parameters.
   However, in externally accessible environments or when exposed as a public API,
   malicious users may manipulate URL parameters to escalate to privileges they should not have.

   Please note the following:

   * Use this feature only when Fess is embedded within another application or service that fully controls inbound requests.
   * Do not configure a parameter name when Fess is exposed to untrusted networks.
   * Ensure that URL parameters cannot be manipulated by external users when using access tokens.

Expiration Date
:::::::::::::::

Specifies the expiration date for the access token.

Deleting Configuration
----------------------

Click the configuration name on the list page, then click the Delete button to display a confirmation screen.
Click the Delete button to remove the configuration.

.. |image0| image:: ../../../resources/images/en/15.3/admin/accesstoken-1.png
.. |image1| image:: ../../../resources/images/en/15.3/admin/accesstoken-2.png

