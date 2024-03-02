from agentflow import mw 

@mw
def llm(ctx, conv):
    
    conv.should_infer = ctx['hops'] == 0
    return conv