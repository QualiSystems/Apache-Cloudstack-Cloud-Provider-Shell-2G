from cloudshell.cp.core.cancellation_manager import CancellationContextManager
from cloudshell.cp.core.request_actions import GetVMDetailsRequestActions, \
    DriverResponse
from cloudshell.cp.core.reservation_info import ReservationInfo
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from cloudshell.shell.core.driver_context import AutoLoadCommandContext, \
    ResourceCommandContext, \
    AutoLoadDetails, CancellationContext, ResourceRemoteCommandContext

from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext
from cloudshell.shell.core.session.logging_session import LoggingSessionContext
from cloudshell.shell.flows.connectivity.parse_request_service import \
    ParseConnectivityRequestService

from cloudshell.cp.cloudstack.flows.connectivity import ConnectivityFlow
from cloudshell.cp.cloudstack.flows.deploy import DeployFlow
from cloudshell.cp.cloudstack.flows.refresh_vm_ip import refresh_ip
from cloudshell.cp.cloudstack.flows.vm_details import \
    CloudstackGetVMDetailsFlow
from cloudshell.cp.cloudstack.models.connectivity_action_model import \
    CloudstackConnectivityActionModel
from cloudshell.cp.cloudstack.models.deploy_app import VMFromTemplateDeployApp, \
    CloudStackDeployVMRequestActions
from cloudshell.cp.cloudstack.models.deployed_app import VMFromTemplateDeployedApp, \
    CloudstackDeployedVMActions
from cloudshell.cp.cloudstack.models.resource_config import CloudstackResourceConfig
from cloudshell.cp.cloudstack.services.cloudstack_api_service import \
    CloudStackAPIService


class Cloudstack2GDriver(ResourceDriverInterface):
    def __init__(self):
        for deploy_app_cls in (
                VMFromTemplateDeployApp,
        ):
            CloudStackDeployVMRequestActions.register_deployment_path(deploy_app_cls)
        for deployed_app_cls in (
                VMFromTemplateDeployedApp,
        ):
            CloudstackDeployedVMActions.register_deployment_path(deployed_app_cls)

    def initialize(self, context):
        pass

    def get_inventory(self, context):
        """
        Called when the cloud provider resource is created
        in the inventory.

        Method validates the values of the cloud provider attributes, entered by the user as part of the cloud provider resource creation.
        In addition, this would be the place to assign values programmatically to optional attributes that were not given a value by the user.

        If one of the validations failed, the method should raise an exception

        :param AutoLoadCommandContext context: the context the command runs on
        :return Attribute and sub-resource information for the Shell resource you can return an AutoLoadDetails object
        :rtype: AutoLoadDetails
        """

        with LoggingSessionContext(context) as logger:
            api = CloudShellSessionContext(context).get_api()
            resource_config = CloudstackResourceConfig.from_context(context, api=api)

            CloudStackAPIService.from_config(resource_config, logger)

        return AutoLoadDetails([], [])

    def Deploy(self, context, request, cancellation_context=None):
        """
        Called when reserving a sandbox during setup, a call for each app in the sandbox.

        Method creates the compute resource in the cloud provider - CloudstackVirtualMachine instance or container.

        If App deployment fails, return a "success false" action result.

        :param ResourceCommandContext context:
        :param str request: A JSON string with the list of requested deployment actions
        :param CancellationContext cancellation_context:
        :return:
        :rtype: str
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Deploy command")
            logger.debug(f"Request: {request}")
            api = CloudShellSessionContext(context).get_api()
            resource_config = CloudstackResourceConfig.from_context(context, api=api)

            request_actions = CloudStackDeployVMRequestActions.from_request(
                request, api
            )
            deploy_flow = DeployFlow(
                resource_config=resource_config,
                logger=logger
            )
            deploy_app_result = deploy_flow.deploy_from_template(
                deploy_action=request_actions.deploy_app
            )
            return DriverResponse([deploy_app_result]).to_driver_response_json()

    def ApplyConnectivityChanges(
        self, context: ResourceCommandContext, request: str
    ) -> str:
        """Connects/disconnect VMs to VLANs based on requested actions."""
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Connectivity command")
            api = CloudShellSessionContext(context).get_api()
            resource_conf = CloudstackResourceConfig.from_context(context, api)
            parse_connectivity_req_service = ParseConnectivityRequestService(
                is_vlan_range_supported=False,
                is_multi_vlan_supported=False,
                connectivity_model_cls=CloudstackConnectivityActionModel,
            )
            reservation_info = ReservationInfo.from_resource_context(context)
            cloudstack_api = CloudStackAPIService.from_config(resource_conf, logger)
            return ConnectivityFlow(
                parse_connectivity_req_service,
                cloudstack_api,
                resource_conf,
                reservation_info,
            ).apply_connectivity(request)

    def PowerOn(self, context, ports):
        """
        Called when reserving a sandbox during setup, a call for each app in the sandbox can also be run manually by the sandbox end-user from the deployed App's commands pane

        Method spins up the CloudstackVirtualMachine

        If the operation fails, method should raise an exception.

        :param ResourceRemoteCommandContext context:
        :param ports:
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Get CloudstackVirtualMachine Details command...")
            api = CloudShellSessionContext(context).get_api()
            resource_config = CloudstackResourceConfig.from_context(context, api=api)
            resource = context.remote_endpoints[0]
            request_actions = GetVMDetailsRequestActions.from_remote_resource(
                resource, cs_api=api)
            vm = CloudStackAPIService.from_config(
                resource_config,
                logger
            ).VM.get(
                request_actions.deployed_app.vmdetails.uid
            )
            vm.power_on_vm()

    def remote_refresh_ip(self, context, ports, cancellation_context):
        """

        Called when reserving a sandbox during setup, a call for each app in the sandbox can also be run manually by the sandbox end-user from the deployed App's commands pane

        Method retrieves the CloudstackVirtualMachine's updated IP address from the cloud provider and sets it on the deployed App resource
        Both private and public IPs are retrieved, as appropriate.

        If the operation fails, method should raise an exception.

        :param ResourceRemoteCommandContext context:
        :param ports:
        :param CancellationContext cancellation_context:
        :return:
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Get CloudstackVirtualMachine Details command...")
            api = CloudShellSessionContext(context).get_api()
            resource_config = CloudstackResourceConfig.from_context(context, api=api)
            resource = context.remote_endpoints[0]
            request_actions = GetVMDetailsRequestActions.from_remote_resource(
                resource, cs_api=api)
            return refresh_ip(request_actions.deployed_app, resource_config, logger)

    def GetVmDetails(self, context, requests, cancellation_context):
        """
        Called when reserving a sandbox during setup, a call for each app in the sandbox can also be run manually by the sandbox
        end-user from the deployed App's CloudstackVirtualMachine Details pane

        Method queries cloud provider for instance operating system, specifications and networking information and
        returns that as a json serialized driver response containing a list of VmDetailsData.

        If the operation fails, method should raise an exception.

        :param ResourceCommandContext context:
        :param str requests:
        :param CancellationContext cancellation_context:
        :return:
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Get CloudstackVirtualMachine Details command...")
            logger.debug(f"Requests: {requests}")
            api = CloudShellSessionContext(context).get_api()
            resource_config = CloudstackResourceConfig.from_context(context, api=api)
            GetVMDetailsRequestActions.register_deployment_path(VMFromTemplateDeployedApp)
            request_actions = GetVMDetailsRequestActions.from_request(requests, api)
            return CloudstackGetVMDetailsFlow(
                resource_config, logger).get_vm_details(request_actions)

    def PowerCycle(self, context, ports, delay):
        """ please leave it as is """
        pass

    def PowerOff(self, context, ports):
        """
        Called during sandbox's teardown can also be run manually by the sandbox end-user from the deployed App's commands pane

        Method shuts down (or powers off) the CloudstackVirtualMachine instance.

        If the operation fails, method should raise an exception.

        :param ResourceRemoteCommandContext context:
        :param ports:
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Get CloudstackVirtualMachine Details command...")
            api = CloudShellSessionContext(context).get_api()
            resource_config = CloudstackResourceConfig.from_context(context, api=api)
            resource = context.remote_endpoints[0]
            request_actions = GetVMDetailsRequestActions.from_remote_resource(
                resource, cs_api=api)
            vm = CloudStackAPIService.from_config(
                resource_config,
                logger
            ).VM.get(
                request_actions.deployed_app.vmdetails.uid
            )
            vm.power_off_vm()

    def DeleteInstance(self, context, ports):
        """
        Called during sandbox's teardown or when removing a deployed App from the sandbox

        Method deletes the CloudstackVirtualMachine from the cloud provider.

        If the operation fails, method should raise an exception.

        :param ResourceRemoteCommandContext context:
        :param ports:
        """
        with LoggingSessionContext(context) as logger:
            logger.info("Starting Get CloudstackVirtualMachine Details command...")
            api = CloudShellSessionContext(context).get_api()
            resource_config = CloudstackResourceConfig.from_context(context, api=api)
            resource = context.remote_endpoints[0]
            request_actions = GetVMDetailsRequestActions.from_remote_resource(
                resource, cs_api=api)
            vm = CloudStackAPIService.from_config(
                resource_config,
                logger
            ).VM.get(
                request_actions.deployed_app.vmdetails.uid
            )
            vm.delete_vm()

    def cleanup(self):
        """
        Destroy the driver session, this function is called every time a driver instance is destroyed
        This is a good place to close any open sessions, finish writing to log files, etc.
        """
        pass
