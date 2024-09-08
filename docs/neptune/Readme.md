# Create
* Create notebook while creating db


# Query
```python
from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.process.traversal import T
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver.aiohttp.transport import AiohttpTransport


graph = Graph()


remoteConn = DriverRemoteConnection('wss://<your-neptune-endpoint>:8182/gremlin','g',
transport_factory=lambda:AiohttpTransport(call_from_event_loop=True))


g = graph.traversal().withRemote(remoteConn)


nusr =
g.V(‘1000’).fold().coalesce(__.unfold(),__.addV('User').property(T.id, ’1000’)).id_().next()


print(nusr)


remoteConn.close()
```