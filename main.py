from openai import OpenAI

# 创建 openai 客户端
client = OpenAI(api_key=你的api密钥)

# 创建对话历史列表
history=[]


first=True
# 检查状态并打印
while True:
    user_input=input(str("You: "))
    history.append({"role":"user","content":user_input})

    if first:
        thread = client.beta.threads.create(messages=history)

    # 创建Run
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id="asst_fSljScMEBYSZhjauv0n6ulJR"
    )

    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
            thread_id=thread.id
            )

            for message in reversed(messages.data):
                if message.role == 'assistant':
                    last_assistant_message = message
                    break

            if last_assistant_message is not None:
                output = str(f"Assistant: {last_assistant_message.content[0].text.value}")
                print(output)

            break
