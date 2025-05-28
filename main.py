import flet as ft
from db import main_db  

def main(page: ft.Page):
    page.title = "Список покупок"

    filter_type = "all"

    task_list = ft.Column(spacing=10)
   
    task_input = ft.TextField(hint_text="Название товара", expand=True, dense=True)
    quantity_input = ft.TextField(hint_text="Количество", width=100, value="1", dense=True, keyboard_type=ft.KeyboardType.NUMBER)

    def load_tasks():
        task_list.controls.clear()
        tasks = main_db.get_tasks()

        if filter_type == 'completed':
            tasks = [t for t in tasks if t[2]]
        elif filter_type == 'uncompleted':
            tasks = [t for t in tasks if not t[2]]

        for task_id, task_text, completed, quantity in tasks:
            task_list.controls.append(create_task_row(task_id, task_text, completed, quantity))


        page.update()

    def create_task_row(task_id, task_text, completed, quantity):
        task_checkbox = ft.Checkbox(
            value=bool(completed),
            on_change=lambda e, tid=task_id: toggle_task(tid, e.control.value)
        )
        task_label = ft.Text(f"{task_text} (x{quantity})", expand=True)
        delete_button = ft.IconButton(ft.Icons.DELETE, icon_color=ft.Colors.RED_400, on_click=lambda e, tid=task_id: delete_task(tid))

        return ft.Row([
            task_checkbox,
            task_label,
            delete_button
        ], alignment=ft.MainAxisAlignment.START)

    def add_task(e):
        text = task_input.value.strip()
        qty_text = quantity_input.value.strip()

        if not text:
            return  

        try:
            qty = int(qty_text)
            if qty < 1:
                qty = 1
        except:
            qty = 1  

        main_db.add_task_db(text, quantity=qty)
        task_input.value = ""
        quantity_input.value = "1"
        load_tasks()

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

    filter_buttons = ft.Row([
        ft.ElevatedButton("Все", on_click=lambda e: set_filter('all')),
        ft.ElevatedButton("Купленные", on_click=lambda e: set_filter('completed')),
        ft.ElevatedButton("Некупленные", on_click=lambda e: set_filter('uncompleted')),
    ], alignment=ft.MainAxisAlignment.CENTER)

    add_button = ft.ElevatedButton("Добавить", on_click=add_task, icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN_400)

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row([task_input, quantity_input, add_button]),
                filter_buttons,
                task_list
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
        ),
        padding=20,
        alignment=ft.alignment.center
    )

    page.add(content)
    load_tasks()

if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main)
