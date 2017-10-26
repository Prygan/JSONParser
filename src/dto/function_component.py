from dto.component import Component

class FunctionComponent(Component):
    types = ['compute_api', 'neutron_api', 'nova_image', 'rpc', 'l3', 'vif_driver'] # potentiellement l3-agent

    def __init__(self, function_call, name, service, duration, parent_id, trace_id):
        super(FunctionComponent, self).__init__(name, service, duration, parent_id, trace_id)
        self.function_call = function_call

    def __str__(self):
        result = 'FUNCTION_COMPONENT\n'
        result += self.function_call + '\n'
        return result
