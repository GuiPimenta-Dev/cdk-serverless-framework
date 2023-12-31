import aws_cdk as cdk

from infra.stacks.dev_pipeline_stack import DevPipelineStack
from infra.stacks.playground_pipeline_stack import PlaygroundPipelineStack
from infra.stacks.prod_pipeline_stack import ProdPipelineStack

app = cdk.App()


DevStack = DevPipelineStack(app)
ProdStack = ProdPipelineStack(app)
PlaygroundStack = PlaygroundPipelineStack(app)

cdk.Tags.of(DevStack).add("VantaOwner", "gui@goentri.com")
cdk.Tags.of(DevStack).add("VantaNoAlert", "This is our Dev stack")
cdk.Tags.of(ProdStack).add("VantaOwner", "gui@goentri.com")
app.synth()
