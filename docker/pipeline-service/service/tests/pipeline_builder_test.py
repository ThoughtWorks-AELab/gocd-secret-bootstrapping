# from pipelineservice.pipeline_builder import PipelineBuilder
#
#
# class MockPolicyBuilder:
#     def __init__(self):
#         self.built_policies = []
#
#     def build_pipeline_policy(self, name):
#         self.built_policies.append(name)
#
#
# class MockVaultClient:
#     def __init__(self, read_values=None):
#         self.writes = []
#         if read_values is None:
#             read_values = {}
#         self.read_values = read_values
#
#     def write(self, path, **args):
#         self.writes.append((path, args))
#
#     def read(self, path):
#         return self.read_values[path]
#
#
# def test_build_pipeline():
#     config = {
#         'registry_username': 'ru',
#         'registry_password': 'rp'
#     }
#     policy_builder = MockPolicyBuilder()
#     vault_client = MockVaultClient(read_values={'auth/approle/role/my-app-pipeline/role-id', {
#         'data': {
#             'role_id': 'my-app-pipeline-role-id'
#         }
#     }})
#
#     PipelineBuilder(policy_builder, vault_client, config).build_pipeline("my-app", "repo")
#     # assert policy_builder.built_policies[0] == "my-app-pipeline-policy"
#     # assert ("secret/app/pipeline/my-app-pipeline/registry", {'username': 'ru', 'password': 'rp'}) in vault_client.writes
#     # assert ("auth/approle/role/my-app-pipeline", {'policies': 'my-app-pipeline-policy'}) in vault_client.writes
