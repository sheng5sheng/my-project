import json
import os
from datetime import datetime

# 存储待办事项的文件
STORAGE_FILE = "todo_data.json"


class TodoSystem:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """从文件加载任务"""
        if os.path.exists(STORAGE_FILE):
            try:
                with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        """保存任务到文件"""
        with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def show_message(self, message, is_error=True):
        """显示消息"""
        if is_error:
            print(f"\033[91m{message}\033[0m")  # 红色
        else:
            print(f"\033[92m{message}\033[0m")  # 绿色

    def add_task(self):
        """添加待办事项"""
        print("\n===== 添加待办事项 =====")
        while True:
            try:
                num = input("任务序号（数字）：").strip()
                if not num:
                    self.show_message("任务序号不能为空！")
                    continue
                num = int(num)

                # 检查序号是否已存在
                exists = any(task['num'] == num for task in self.tasks)
                if exists:
                    self.show_message("该任务序号已存在！")
                    continue

                things = input("待办事项内容：").strip()
                if not things:
                    self.show_message("待办事项内容不能为空！")
                    continue

                deadline = input("截止日期（YYYY-MM-DD，可选）：").strip()
                if deadline:
                    # 验证日期格式
                    try:
                        datetime.strptime(deadline, '%Y-%m-%d')
                    except ValueError:
                        self.show_message("日期格式不正确，请输入YYYY-MM-DD格式！")
                        continue

                finish = input("完成情况（未完成/已完成，默认未完成）：").strip() or "未完成"
                if finish not in ["未完成", "已完成"]:
                    finish = "未完成"

                # 添加任务
                self.tasks.append({
                    "num": num,
                    "things": things,
                    "deadline": deadline,
                    "finish": finish,
                    "create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })

                self.save_tasks()
                self.show_message(f"任务添加成功！", False)
                break

            except ValueError:
                self.show_message("任务序号必须是数字！")

    def show_tasks(self, filter_type="all"):
        """显示待办事项"""
        print("\n===== 待办事项列表 =====")

        if not self.tasks:
            self.show_message("暂无待办事项")
            return

        # 筛选任务
        filtered_tasks = []
        if filter_type == "all":
            filtered_tasks = self.tasks
        elif filter_type == "active":
            filtered_tasks = [t for t in self.tasks if t['finish'] == "未完成"]
        elif filter_type == "completed":
            filtered_tasks = [t for t in self.tasks if t['finish'] == "已完成"]

        if not filtered_tasks:
            self.show_message(f"暂无{filter_type}任务")
            return

        # 按序号排序
        filtered_tasks.sort(key=lambda x: x['num'])

        for task in filtered_tasks:
            status_color = "\033[91m未完成\033[0m" if task['finish'] == "未完成" else "\033[92m已完成\033[0m"
            overdue = ""
            if task['deadline'] and task['finish'] == "未完成":
                try:
                    deadline_date = datetime.strptime(task['deadline'], '%Y-%m-%d')
                    if deadline_date < datetime.now():
                        overdue = " \033[91m[已逾期]\033[0m"
                except:
                    pass

            print(f"\n序号：{task['num']}")
            print(f"内容：{task['things']}")
            if task['deadline']:
                print(f"截止：{task['deadline']}{overdue}")
            print(f"状态：{status_color}")
            print("-" * 30)

    def delete_task(self):
        """删除待办事项"""
        print("\n===== 删除待办事项 =====")
        if not self.tasks:
            self.show_message("暂无待办事项可删除")
            return

        try:
            num = int(input("请输入要删除的任务序号：").strip())
            index = next((i for i, t in enumerate(self.tasks) if t['num'] == num), -1)

            if index == -1:
                self.show_message("未找到该序号的任务！")
                return

            confirm = input(f"确定要删除序号为{num}的任务吗？(y/n)：").strip().lower()
            if confirm == 'y':
                self.tasks.pop(index)
                self.save_tasks()
                self.show_message("任务删除成功！", False)

        except ValueError:
            self.show_message("请输入有效的数字序号！")

    def edit_task(self):
        """修改待办事项"""
        print("\n===== 修改待办事项 =====")
        if not self.tasks:
            self.show_message("暂无待办事项可修改")
            return

        try:
            num = int(input("请输入要修改的任务序号：").strip())
            task = next((t for t in self.tasks if t['num'] == num), None)

            if not task:
                self.show_message("未找到该序号的任务！")
                return

            print(f"\n当前任务信息：")
            print(f"内容：{task['things']}")
            print(f"截止：{task['deadline'] or '无'}")
            print(f"状态：{task['finish']}")

            # 获取新内容
            new_things = input("\n新的任务内容（回车保持不变）：").strip() or task['things']
            new_deadline = input("新的截止日期（YYYY-MM-DD，回车保持不变）：").strip() or task['deadline']

            if new_deadline:
                try:
                    datetime.strptime(new_deadline, '%Y-%m-%d')
                except ValueError:
                    self.show_message("日期格式不正确，保持原日期！")
                    new_deadline = task['deadline']

            new_finish = input("新的完成情况（未完成/已完成，回车保持不变）：").strip() or task['finish']
            if new_finish not in ["未完成", "已完成"]:
                new_finish = task['finish']

            # 更新任务
            task['things'] = new_things
            task['deadline'] = new_deadline
            task['finish'] = new_finish

            self.save_tasks()
            self.show_message("任务修改成功！", False)

        except ValueError:
            self.show_message("请输入有效的数字序号！")

    def clear_completed(self):
        """清空已完成任务"""
        print("\n===== 清空已完成任务 =====")
        completed_tasks = [t for t in self.tasks if t['finish'] == "已完成"]

        if not completed_tasks:
            self.show_message("暂无已完成任务！")
            return

        confirm = input(f"确定要删除{len(completed_tasks)}个已完成任务吗？(y/n)：").strip().lower()
        if confirm == 'y':
            self.tasks = [t for t in self.tasks if t['finish'] == "未完成"]
            self.save_tasks()
            self.show_message(f"已清空{len(completed_tasks)}个已完成任务！", False)

    def filter_tasks(self):
        """筛选任务"""
        print("\n===== 筛选任务 =====")
        print("1. 查看所有任务")
        print("2. 查看未完成任务")
        print("3. 查看已完成任务")

        choice = input("请选择（1-3）：").strip()
        if choice == "1":
            self.show_tasks("all")
        elif choice == "2":
            self.show_tasks("active")
        elif choice == "3":
            self.show_tasks("completed")
        else:
            self.show_message("无效选择！")

    def main_menu(self):
        """主菜单"""
        while True:
            print("\n" + "=" * 40)
            print("          待办事项管理系统")
            print("=" * 40)
            print("1. 添加待办事项")
            print("2. 查看待办事项")
            print("3. 删除待办事项")
            print("4. 修改待办事项")
            print("5. 筛选任务")
            print("6. 清空已完成任务")
            print("7. 退出系统")
            print("=" * 40)

            choice = input("请选择功能（1-7）：").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.show_tasks()
            elif choice == "3":
                self.delete_task()
            elif choice == "4":
                self.edit_task()
            elif choice == "5":
                self.filter_tasks()
            elif choice == "6":
                self.clear_completed()
            elif choice == "7":
                print("\n感谢使用待办事项管理系统，再见！")
                break
            else:
                self.show_message("无效的选择，请输入1-7之间的数字！")


if __name__ == "__main__":
    todo_system = TodoSystem()
    todo_system.main_menu()