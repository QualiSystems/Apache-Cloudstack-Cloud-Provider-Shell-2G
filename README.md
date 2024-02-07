[![Build status](https://github.com/QualiSystems/Apache-Cloudstack-Cloud-Provider-Shell-2G/workflows/CI/badge.svg?branch=master)](https://github.com/QualiSystems/Apache-Cloudstack-Cloud-Provider-Shell-2G/actions?query=branch%3Amaster)

# Apache Cloudstack Cloud Provider Shell 2G
A CloudShell 'Shell' that allows integrating Cloudstack as an App's deployment option in CloudShell
![Image][1]

Release date: July 2021

`Shell version: 1.0.0`

`Document version: 1.0`

# In This Guide

* [Overview](#overview)
* [Downloading the Shell](#downloading-the-shell)
* [Importing and Configuring the Shell](#importing-and-configuring-the-shell)
* [Updating Python Dependencies for Shells](#updating-python-dependencies-for-shells)
* [Typical Workflows](#typical-workflows)
* [References](#references)
* [Release Notes](#release-notes)


# Overview
A shell integrates a device model, application or other technology with CloudShell. A shell consists of a data model that defines how the device and its properties are modeled in CloudShell, along with automation that enables interaction with the device via CloudShell.

### Cloud Provider Shells
CloudShell Cloud Provider shells provide L2 or L3 connectivity between resources and/or Apps.

### Apache Cloudstack Cloud Provider Shell 2G
Apache Cloudstack Cloud Provider Shell 2G provides you with apps deployment and management capabilities. 

For more information on the device, see the vendor's official product documentation.

### Standard version
Apache Cloudstack Cloud Provider Shell 2G is based on the Cloud Provider Standard version **1.0.0**.

For detailed information about the shell’s structure and attributes, see the [Cloud Provider Standard](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md) in GitHub.

### Requirements

Release: Apache Cloudstack Cloud Provider Shell 2G

▪ CloudShell version **2022.2 and above**

**Note:** If your CloudShell version does not support this shell, you should consider upgrading to a later version of CloudShell or contact customer support. 

### Data Model

The shell's data model includes all shell metadata, families, and attributes.

#### **Apache Cloudstack Cloud Provider Shell 2G Attributes**

The attribute names and types are listed in the following section of the Cloud Provider Shell Standard:

[Common Cloud Provider Attributes](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md#attributes)

The following table describes attributes that are unique to this shell and are not documented in the Shell Standard: 


|Attribute Name|Data Type|Description|
|:---|:---|:---|
|API Key|String|Administrator account API Key.|
|Secret Key|String|Administrator account Secret Key.|
|Reserved Networks|String|Reserved networks separated by Semicolon(;), vNICs configured to those networks won't be used for VM connectivity.|
|Mgmt Network Id|String|UUID of the manually created CloudShell management network (for assistance identifying your management network, contact your Cloudstack admin). This network will be used to configure the communication between the Sandbox instances and the CloudShell components. For example: c14241d2-376c-4fb3-8d1e-61f5c1408448. *__Note__: The UUID can be found in the Horizon user interface.*|
|Execution Server Selector|String|(Optional) This attribute points to a pre-defined group of execution servers (grouped by a common __Execution Server Selector__ value). This attribute is typically used for different sites or domains. For additional information on managing App deployments per domains, see [Managing Private Cloud Apps in Domains](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/Mng-Prvt-Cld-Apps-in-Dmns.htm).|

### Automation
This section describes the automation (driver) associated with the data model. The shell’s driver is provided as part of the shell package. There are two types of automation processes, Autoload and Resource. Autoload is executed when creating the resource in the **Inventory** dashboard.

For detailed information on each available commands, see the following section of the Cloud Provider Standard:

[Common Cloud Provider Commands](https://github.com/QualiSystems/cloudshell-standards/blob/master/Documentation/cloud_provider_standard.md#commands)

# Cloudstack Integration Process
In order to integrate CloudShell with Cloudstack, you need to first prepare Cloudstack with the required user permissions, quotas, networks etc. Then, create an Cloudstack cloud provider resource and App templates which include the definition of the VMs, images and configuration management to be performed on the deployed VMs. For example, see CloudShell Help's for [Openstack Integration](https://help.quali.com/Online%20Help/0.0/portal/Content/Admn/OpenStack-Intgr) chapter.

# Downloading the Shell
The Apache Cloudstack Cloud Provider Shell 2G shell is available from the [Quali Community Integrations](https://community.quali.com/integrations) page. 

Download the files into a temporary location on your local machine. 

The shell comprises:

|File name|Description|
|:---|:---|
|Apache.Cloudstack.Cloud.Provider.Shell.2G.zip|Device shell package|
|cloudshell-Apache-Cloudstack-Cloud-Provider-Shell-2G-dependencies-linux-package-1.0.0.zip, cloudshell-Apache-Cloudstack-Cloud-Provider-Shell-2G-dependencies-win32-package-1.0.0.zip|Shell Python dependencies (for offline deployments only)|

# Importing and Configuring the Shell
This section describes how to import the Apache Cloudstack Cloud Provider Shell 2G shell and configure and modify the shell’s devices.

### Importing the shell into CloudShell

**To import the shell into CloudShell:**
  1. Make sure you have the shell’s zip package. If not, download the shell from the [Quali Community's Integrations](https://community.quali.com/integrations) page.
  
  2. In CloudShell Portal, as Global administrator, open the **Manage – Shells** page.
  
  3. Click **Import**.
  
  4. In the dialog box, navigate to the shell's zip package, select it and click **Open**. <br><br>The shell is displayed in the **Shells** page and can be used by domain administrators in all CloudShell domains to create new inventory resources, as explained in [Adding Inventory Resources](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Add-Rsrc-Tmplt.htm?Highlight=adding%20inventory%20resources). 

### Offline installation of a shell

**Note:** Offline installation instructions are relevant only if CloudShell Execution Server has no access to PyPi. You can skip this section if your execution server has access to PyPi. For additional information, see the online help topic on offline dependencies.

In offline mode, import the shell into CloudShell and place any dependencies in the appropriate dependencies folder. The dependencies folder may differ, depending on the CloudShell version you are using:

* For CloudShell version 8.3 and above, see [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository).

* For CloudShell version 8.2, perform the appropriate procedure: [Adding Shell and script packages to the local PyPi Server repository](#adding-shell-and-script-packages-to-the-local-pypi-server-repository) or [Setting the Python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

* For CloudShell versions prior to 8.2, see [Setting the Python pythonOfflineRepositoryPath configuration key](#setting-the-python-pythonofflinerepositorypath-configuration-key).

### Adding shell and script packages to the local PyPi Server repository
If your Quali Server and/or execution servers work offline, you will need to copy all required Python packages, including the out-of-the-box ones, to the PyPi Server's repository on the Quali Server computer (by default *C:\Program Files (x86)\QualiSystems\CloudShell\Server\Config\Pypi Server Repository*).

For more information, see [Configuring CloudShell to Execute Python Commands in Offline Mode](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=Configuring%20CloudShell%20to%20Execute%20Python%20Commands%20in%20Offline%20Mode).

**To add Python packages to the local PyPi Server repository:**
  1. If you haven't created and configured the local PyPi Server repository to work with the execution server, perform the steps in [Add Python packages to the local PyPi Server repository (offline mode)](http://help.quali.com/Online%20Help/9.0/Portal/Content/Admn/Cnfgr-Pyth-Env-Wrk-Offln.htm?Highlight=offline%20dependencies#Add). 
  
  2. For each shell or script you add into CloudShell, do one of the following (from an online computer):
      * Connect to the Internet and download each dependency specified in the *requirements.txt* file with the following command: 
`pip download -r requirements.txt`. 
     The shell or script's requirements are downloaded as zip files.

      * In the [Quali Community's Integrations](https://community.quali.com/integrations) page, locate the shell and click the shell's **Download** link. In the page that is displayed, from the Downloads area, extract the dependencies package zip file.

3. Place these zip files in the local PyPi Server repository.
 
### Configuring a new resource
This section explains how to create a new resource from the shell.

In CloudShell, the component that models the device is called a resource. It is based on the shell that models the device and allows the CloudShell user and API to remotely control the device from CloudShell.

You can also modify existing resources, see [Managing Resources in the Inventory](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/INVN/Mng-Rsrc-in-Invnt.htm?Highlight=managing%20resources).

**To create a resource for the device:**  
  1. In the CloudShell Portal, in the **Inventory** dashboard, click **Add New**.
     ![Image][2]
     
  3. From the list, select **Apache Cloudstack Cloud Provider Shell 2G**.
  
  4. Click **Create**.
  
  5. In the **Resource** dialog box, enter the following mandatory attributes with data from step 1:
        - **API Key** - An administrator account API Key.
        - **Secret Key** - An administrator account Secret Key.
        - **Mgmt Network Id** - UUID of the manually created CloudShell management network (for assistance identifying your management network, contact your Cloudstack admin). This network will be used to configure the communication between the Sandbox instances and the CloudShell components. For example: c14241d2-376c-4fb3-8d1e-61f5c1408448
<br>__Note__: The UUID can be found on the Cloudstack Portal.

        - **Execution Server Selector** - (Optional) This attribute points to a pre-defined group of execution servers (grouped by a common __Execution Server Selector__ value). 
This attribute is typically used for different sites or domains. For additional information on managing App deployments per domains, see [Managing Private Cloud Apps in Domains](https://help.quali.com/Online%20Help/0.0/Portal/Content/Admn/Mng-Prvt-Cld-Apps-in-Dmns.htm).
  1. Click **Continue**.

CloudShell validates provided settings and creates the new resource.

_**Apache Cloudstack Cloud Provider Shell 2G requires you to set up an Cloudstack cloud provider resource and also create an appropriate App template, which would be deployed as part of the sandbox reservation. For example, see [OpenStack Integration](https://help.quali.com/Online%20Help/0.0/cloudshell/Content/Admn/OpenStack-Intgr.htm)**_

# Updating Python Dependencies for Shells
This section explains how to update your Python dependencies folder. This is required when you upgrade a shell that uses new/updated dependencies. It applies to both online and offline dependencies.
### Updating offline Python dependencies
**To update offline Python dependencies:**
1. Download the latest Python dependencies package zip file locally.

2. Extract the zip file to the suitable offline package folder(s). 

3. Terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat). 

### Updating online Python dependencies
In online mode, the execution server automatically downloads and extracts the appropriate dependencies file to the online Python dependencies repository every time a new instance of the driver or script is created.

**To update online Python dependencies:**
* If there is a live instance of the shell's driver or script, terminate the shell’s instance, as explained [here](http://help.quali.com/Online%20Help/9.0/Portal/Content/CSP/MNG/Mng-Exctn-Srv-Exct.htm#Terminat). If an instance does not exist, the execution server will download the Python dependencies the next time a command of the driver or script runs.


# Typical Workflows

## Connecting Cloudstack App to an existing network
This section explains how to enable CloudShell to connect an Cloudstack App to an existing network. This capability requires editing the VLAN Auto / VLAN Manual service models in Resource Manager Client.

__To allow connecting to an existing VLAN network:__
1. In Resource Manager Client, open the __Attributes__ explorer.
2. Add the __Existing Network__ attribute.
3. Press __Rules__ button and check:
   1. __Configuration__
   2. __Setting__
4. Save
5. Open the __Resource Families__ explorer and expand the __Virtual Network__ family.
6. Click the appropriate service model (__VLAN Auto / VLAN Manual__).
7. From the model's __Attributes__ tab, select __Add/Remove From Bank__ find __Existing Network__ on the left pane and press '>' sign to attach attibute to the __Vlan Service__.
8. Select __Virtual Network__ and click __Edit Rules__.
9. Check __User input__ and click __OK__ and save.
10. In the blueprint, add the VLAN service and specify a network name or ID in the __Existing Network__ field. Make sure to specify a value in the __VLAN ID__ field - this will be ignored but it must have a value as it's a system mandatory attribute.
11. Click __Add__.

## Specify Subnet CIDR for Cloudstack VLAN service
This capability requires editing the VLAN Auto / VLAN Manual service models in Resource Manager Client.

__To allow connecting to an existing VLAN network:__
1. In Resource Manager Client, open the __Attributes__ explorer.
2. Add a new attribute with the following settings:
   * Name: Subnet CIDR
   * Attribute Type: String
   * Value: CIDR string in the format __CIDR;Gateway;First_IP-Last_IP__
     For example: "192.168.10.0/24;192.168.10.1;192.168.10.30-192.168.10.50"
3. Press __Rules__ button and check:
   1. __Configuration__
   2. __Setting__
4. Save
5. Open the __Resource Families__ explorer and expand the __Virtual Network__ family.
6. Click the appropriate service model (__VLAN Auto / VLAN Manual__).
7. From the model's __Attributes__ tab, select __Add/Remove From Bank__ find __Subnet CIDR__ on the left pane and press '>' sign to attach attibute to the __Vlan Service__.
6. To allow the user to set the subnet CIDR, in the service model, select the attribute, click __Edit Rules__, and make sure __User input__ is selected.
7. Save your changes in the __Resource Families__ explorer.

## Specify Network Isolation for Cloudstack VLAN service
This capability requires editing the VLAN Auto / VLAN Manual service models in the Resource Manager Client.

__To allow connecting to an existing VLAN network:__
1. In Resource Manager Client, open the __Attributes__ explorer.
2. Add a new attribute with the following settings:
   * Name: Network Isolation
   * Attribute Type: String
   * Value: Possible values are: L2, Isolated, Shared
3. Press __Rules__ button and check:
   1. __Configuration__
   2. __Setting__
4. Save
5. Open the __Resource Families__ explorer and expand the __Virtual Network__ family.
6. Click the appropriate service model (__VLAN Auto / VLAN Manual__).
7. From the model's __Attributes__ tab, select __Add/Remove From Bank__ find __Network Isolation__ on the left pane and press '>' sign to attach attibute to the __Vlan Service__.
6. To allow the user to set the network isolation, in the service model, select the attribute, click __Edit Rules__, and make sure __User input__ is selected.
7. Save your changes in the __Resource Families__ explorer.

# References
To download and share integrations, see [Quali Community's Integrations](https://community.quali.com/integrations). 

For instructional training and documentation, see [Quali University](https://www.quali.com/university/).

To suggest an idea for the product, see [Quali's Idea box](https://community.quali.com/ideabox). 

To connect with Quali users and experts from around the world, ask questions and discuss issues, see [Quali's Community forums](https://community.quali.com/forums). 

# Release Notes 

### What's New

For release updates, see the shell's [GitHub releases page](https://github.com/QualiSystems/Apache-Cloudstack-Cloud-Provider-Shell-2G/releases).


[1]: https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/cloudshell_logo.png
[2]: https://github.com/QualiSystems/cloudshell-shells-documentaion-templates/blob/master/create_a_resource_device.png
