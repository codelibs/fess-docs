============================
Register for Windows Service
============================

Registering as a Windows Service
================================

You can register |Fess| as a Windows service, which allows it to run seamlessly in the background on your Windows system. To successfully run |Fess| as a service, you must ensure that OpenSearch is running as a prerequisite. In this guide, we assume that |Fess| is installed in "c:\opt\fess" and OpenSearch is installed in "c:\opt\opensearch."

**Prerequisites**

Before proceeding with the registration process, please make sure that you have set the JAVA_HOME environment variable as a system-wide setting.

**Registering OpenSearch as a Service**

To register OpenSearch as a Windows service, follow these steps:

1. Open a Command Prompt with administrative privileges.

2. Navigate to the "c:\opt\opensearch\bin" directory.

3. Run the following command:

   ```
   > opensearch-service.bat install
   ```

   This command will install OpenSearch as a service. You should see a confirmation message like:

   ```
   The service 'opensearch-service-x64' has been installed.
   ```

   For more detailed information, please refer to the `OpenSearch documentation <https://opensearch.org/docs/2.4/install-and-configure/install-opensearch/windows/>`_.

**Configuration**

To configure |Fess| to work with OpenSearch, you'll need to make some adjustments. Follow these steps:

1. Edit the "c:\opt\fess\bin\fess.in.bat" file.

2. Set the SEARCH_ENGINE_HOME variable to the directory where OpenSearch is installed:

   ```
   set SEARCH_ENGINE_HOME=c:/opt/opensearch
   ```

   By doing this, you specify the location of OpenSearch for |Fess| to use.

3. By default, |Fess| uses port 8080 for its search and administration interfaces. If you want to change the port to 80, modify the "c:\opt\fess\bin\fess.in.bat" file by setting the fess.port variable:

   ```
   set FESS_JAVA_OPTS=%FESS_JAVA_OPTS% -Dfess.port=80
   ```

   This will change the port to 80.

**Service Registration**

To register |Fess| as a Windows service, follow these steps:

1. Open a Command Prompt with administrative privileges.

2. Navigate to the "c:\opt\fess\bin" directory.

3. Run the following command to install the |Fess| service:

   ```
   > service.bat install
   ```

   You will receive a confirmation message like:

   ```
   The service 'fess-service-x64' has been installed.
   ```

**Service Configuration**

If you prefer to start the services manually, ensure that you start the OpenSearch service before starting the |Fess| service. For automatic startup, you can set up a service dependency as follows:

1. In the general settings of the |Fess| service, set the startup type to "Automatic (Delayed Start)."

2. Configure the service dependency in the Windows Registry.

   Using the Registry Editor (regedit), add the following key and value:

   **Key**: `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\fess-service-x64\DependOnService`

   **Value**: `opensearch-service-x64`

   After adding this dependency, you will see "opensearch-service-x64" listed as a prerequisite in the properties of the |Fess| service.
   
This revised version maintains accuracy while improving readability and comprehension.