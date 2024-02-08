from openai import OpenAI

# 导入 OpenAI 库并创建一个 OpenAI 客户端
client = OpenAI()

# 创建一个空的对话历史列表，用于存储用户和助手的对话历史
history=[]

# 创建一个标志变量，用于判断是否是第一次创建对话线程
first=True

# 主循环，用于接收用户输入并处理
while True:
    # 获取用户输入
    user_input=input(str("You: "))
    # 将用户输入添加到对话历史列表中
    history.append({"role":"user","content":user_input})

    # 如果是第一次创建对话线程，则创建一个新的对话线程
    if first:
        thread = client.beta.threads.create(messages=history)

    # 创建一个运行实例，用于处理对话线程
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id="asst_fSljScMEBYSZhjauv0n6ulJR"
    )

    # 循环检查运行实例的状态，直到运行完成
    while True:
        # 获取运行实例的最新状态
        run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )

        # 如果运行实例的状态为完成，则获取对话线程的所有消息
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
            thread_id=thread.id
            )

            # 从最新的消息开始，找到最新的助手消息
            for message in reversed(messages.data):
                if message.role == 'assistant':
                    last_assistant_message = message
                    break

            # 如果找到了最新的助手消息，则打印出来
            if last_assistant_message is not None:
                output = str(f"Assistant: {last_assistant_message.content[0].text.value}")
                print(output)

            # 退出内部循环，等待下一次用户输入
            break
