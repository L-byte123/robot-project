print("机器人启动成功！")
while True:
    user_input=input("你：")
    if user_input=="退出":
        print("机器人：再见！")
        break
    if "你好" in user_input:
        print("机器人：你好！")
    elif "名字" in user_input:
        print("机器人：我叫robot")
    else:
        print("机器人：我还不会回答这个问题。")
