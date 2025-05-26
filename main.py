import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = "Todo App"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_maximized = True

    task_list = ft.Column(spacing=10)
    filter_type = 'all'
    sort_by_date_desc = True
    sort_by_completed = None

    def load_tasks():
        task_list.controls.clear()
        tasks = main_db.get_tasks()

        # фильтрация
        if filter_type == 'completed':
            tasks = [t for t in tasks if t[2]]
        elif filter_type == 'uncompleted':
            tasks = [t for t in tasks if not t[2]]

        # сортировка по дате
        tasks.sort(key=lambda x: x[3], reverse=sort_by_date_desc)

        # сортировка по статусу
        if sort_by_completed is not None:
            tasks.sort(key=lambda x: x[2], reverse=sort_by_completed)

        for task_id, task_text, completed, created_at in tasks:
            task_list.controls.append(create_task_row(task_id, task_text, completed, created_at))

        page.update()

    def clear_history(e):
        main_db.clear_history()
        load_tasks()

    def create_task_row(task_id, task_text, completed, created_at):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e: toggle_task(task_id, e.control.value)
        )

        def enable_edit(e):
            task_field.read_only = False
            task_field.update()

        def save_task(e):
            main_db.update_task_db(task_id, task_field.value)
            task_field.read_only = True
            page.update()

        date_label = ft.Text(f"📅 {created_at.split('T')[0]}", size=12, color=ft.Colors.GREY)


        return ft.Row([
            task_checkbox,
            task_field,
            date_label,
            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.YELLOW_400, on_click=enable_edit),
            ft.IconButton(ft.Icons.SAVE, icon_color=ft.Colors.GREEN_400, on_click=save_task),
            ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e: delete_task(task_id))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def add_task(e):
        if task_input.value:
            task_id = main_db.add_task_db(task_input.value)
            load_tasks()
            task_input.value = ""
            page.update()

    def toggle_task(task_id, is_completed):
        main_db.update_task_db(task_id, completed=int(is_completed))
        load_tasks()

    def delete_task(task_id):
        main_db.delete_task_db(task_id)
        load_tasks()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    def toggle_sort_date(desc):
        nonlocal sort_by_date_desc
        sort_by_date_desc = desc
        load_tasks()

    def toggle_sort_completed(top):
        nonlocal sort_by_completed
        sort_by_completed = top
        load_tasks()

    task_input = ft.TextField(hint_text="Добавьте задачу: ", expand=True, dense=True, on_submit=add_task)
    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN_400)

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton("Завершенные", on_click=lambda e: set_filter('completed')),
        ft.ElevatedButton("Незавершенные", on_click=lambda e: set_filter('uncompleted')),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    sort_buttons = ft.Row([
        ft.ElevatedButton("📅 Новые выше", on_click=lambda e: toggle_sort_date(True)),
        ft.ElevatedButton("📅 Старые выше", on_click=lambda e: toggle_sort_date(False)),
        ft.ElevatedButton("✅ Выполненные вверх", on_click=lambda e: toggle_sort_completed(True)),
        ft.ElevatedButton("✅ Выполненные вниз", on_click=lambda e: toggle_sort_completed(False)),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    clear_button = ft.IconButton(icon=ft.Icons.DELETE_FOREVER, tooltip="Очистить все задачи", on_click=clear_history)

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([task_input, add_button]),
                filter_buttons,
                sort_buttons,
                clear_button,
                task_list
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=20,
        alignment=ft.alignment.center
    )

    page.add(content)
    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
