import os
from time import sleep

from yowsuplayer import EchoLayer
from yowsup.layers.auth                        import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS
from yowsup import env

#
# The azure library provides access to services made available by the
# Microsoft Azure platform, such as storage and messaging. 
#
# See http://go.microsoft.com/fwlink/?linkid=254360 for documentation and
# example code.
#
from azure.servicebus import ServiceBusService
from azure.storage import CloudStorageAccount

#
# The CloudStorageAccount provides factory methods for the queue, table, and
# blob services.
#
# See http://go.microsoft.com/fwlink/?linkid=246933 for Storage documentation.
#
STORAGE_ACCOUNT_NAME = 'trinitystci'
STORAGE_ACCOUNT_KEY = 'Fr/bAey/Mk0ei+BvhQ11ZNGdrS0OtLURmOvvGsKtqcOMUjyIBEPY56s46+l3tnSIM2MPsa7TY+UXoA7MyZOWuQ=='

if os.environ.get('EMULATED', '').lower() == 'true':
    # Running in the emulator, so use the development storage account
    storage_account = CloudStorageAccount(None, None)
else:
    storage_account = CloudStorageAccount(STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY)

blob_service = storage_account.create_blob_service()
table_service = storage_account.create_table_service()
queue_service = storage_account.create_queue_service()

#
# Service Bus is a messaging solution for applications. It sits between
# components of your applications and enables them to exchange messages in a
# loosely coupled way for improved scale and resiliency.
#
# See http://go.microsoft.com/fwlink/?linkid=246934 for Service Bus documentation.
#
SERVICE_BUS_NAMESPACE = '__paste_your_service_bus_namespace_here__'
SERVICE_BUS_KEY = '__paste_your_service_bus_key_here__'
bus_service = ServiceBusService(SERVICE_BUS_NAMESPACE, SERVICE_BUS_KEY, issuer='owner')


"""if __name__ == '__main__':
    while True:
        #
        # Write your worker process here.
        #
        # You will probably want to call a blocking function such as
        #    bus_service.receive_queue_message('queue name', timeout=seconds)
        # to avoid consuming 100% CPU time while your worker has no work.
        #
        sleep(1.0)
        """


CREDENTIALS = ('919930090096', 'xp2iXCs/0SQU4KIqTAnG3rw1i+4=') # replace with your phone and password

if __name__==  "__main__":
    layers = (
        EchoLayer,
        (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer)
    ) + YOWSUP_CORE_LAYERS

    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)         #setting credentials
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])             #whatsapp server address
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)              
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())           #info about us as WhatsApp client

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))            #sending the connect signal

    stack.loop() #this is the program mainloop