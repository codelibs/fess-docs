===========
Role Search
===========

|Fess| provides user management functionality, and users who have logged in can search based on the roles they belong to. Users managed by |Fess| can use role search and change their own password after logging in.

Role search compares the permissions (roles, groups, and users) set on content with the permissions held by the searching user, and displays only the content for which access is permitted in the search results. For information on how to create roles and users, and how to assign permissions to content, and other role-based search configuration, see :doc:`../config/security-role`.


Search Method
-------------

If roles are configured and the content has been crawled and indexed with those roles, the search results can be displayed only to users who hold that role.
When a user is logged in, searches are performed based on the roles and groups that user belongs to.
When not logged in, searches are performed as the guest user, and only content published for guest is displayed.

Login
-----

Clicking the Login link displayed at the top of the search screen displays the login screen. After entering your username and password and logging in, you are returned to the search screen, and subsequent searches are performed based on the roles the user belongs to.

.. note::
    If integrated with single sign-on or LDAP, log in using the respective authentication method. Also, whether the Login link is displayed can be changed via configuration.

Changing Password
------------------

After logging in, click the username displayed at the top of the search screen to display the menu.

|image0|

Clicking "Change Password" in the menu displays the password change screen.

|image1|

Enter your Current Password, New Password, and Confirm New Password (re-enter), then click the Update button to update your password.
After changing your password, click the Back button to return to the search screen.

.. note::
    The "Change Password" menu item is displayed only for users managed by |Fess| (and LDAP users permitted to edit their password). It is not displayed for users authenticated via single sign-on.
    A password policy, such as length and allowed character types, may apply to the new password.

Logging Out
-----------

While logged in, click the username displayed at the top of the search screen and select "Logout" from the menu to log out.
Users with administrator privileges can also select "Administration" from the same menu to go to the administration screen.



.. |image0| image:: ../../../resources/images/en/15.8/user/role-search-1.png
.. pdf   :width: 200 px
.. |image1| image:: ../../../resources/images/en/15.8/user/role-search-2.png
.. pdf   :width: 300 px
