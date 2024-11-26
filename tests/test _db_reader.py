import tkinter as tk

def show_entry_value():
    # 获取 Entry 的值
    user_input = entry.get()
    # 更新 Label 显示内容
    label.config(text=f"输入的内容是: {user_input}")

# 创建主窗口
root = tk.Tk()
root.title("读取 Entry 值示例")

# 创建 Entry
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# 创建按钮，点击后读取 Entry 的值
button = tk.Button(root, text="读取值", command=show_entry_value)
button.pack(pady=10)

# 创建 Label 用于显示读取的值
label = tk.Label(root, text="输入的内容是: ", font=("Arial", 12))
label.pack(pady=10)

# 运行主循环
root.mainloop()