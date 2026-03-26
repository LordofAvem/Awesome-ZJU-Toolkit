import ollama

# 构造你的系统指令和例子
system_prompt = "You are a task extractor. Only output JSON. Text content should be in Chinese."

# 测试你的“乱糟糟”消息
user_input = "[烟花]各位同学好！为了帮助大家更好地了解自己进入大学以来的的学习适应情况，学校组织了“心晴航标”2026年度“心理体验”活动，每位同学均须参加~[奶茶]测试较个性化，填写时长10-20min不等，测完后可以查看自己的测试结果，更好地掌握自我状态变化，积累专属的私人心理档案。[火箭]操作方式：浙大钉→工作台→全部→浙大生活→“心晴航标Beacon of Mind”→一键跳转，跟随考拉老师完成“心灵体检”（选择“复测”）。请大家3月27日（周五）17:30前完成测评。操作指南和常见问题详见推文。https://mp.weixin.qq.com/s/MQ62IxS4w7CQzOXGUpxgXw[对勾]如果同学们对于测试安排和测试结果有疑问，随时联系自己的辅导员"

response = ollama.chat(model='gemma3:1b', messages=[
    {'role': 'system', 'content': system_prompt},
    {'role': 'user', 'content': user_input},
])
print(response['message']['content'])
