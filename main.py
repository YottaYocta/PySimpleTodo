import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime as dt


class Todo:
    def __init__(self, text: str, date_due: dt.date = None):
        self.todo_name: str = text
        self.date_added: dt.date = dt.now()
        self.date_due: dt.date = date_due
        self.date_completed: dt.date = None
        self.completed: bool = False

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed: bool):
        self._completed = completed
        if self._completed:
            self.date_completed = dt.now()
        else:
            self.date_completed = None

    def __str__(self) -> str:
        return f"\n*******\nName: {self.todo_name}\nCompleted: {str(self.completed)}"


class TodoApp:
    def __init__(self):
        self.root: tk.Tk = tk.Tk()
        self.root.title("PySimpleTodo")
        self.root.geometry("800x400")
        self.todos: List[Todo] = []

        # entry

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.grid(row=0, column=0, rowspan=2, sticky=tk.NW, padx=40)

        self.entry_field_label = tk.Label(self.entry_frame, text="Todo Name: ")
        self.entry_field_label.grid(row=0, column=0, sticky=tk.NW, pady=20)

        self.entry_field = tk.Entry(self.entry_frame)
        self.entry_field.bind("<Return>", lambda x: self.add_todo())
        self.entry_field.grid(row=0, column=1, sticky=tk.NSEW, pady=20)

        self.calendar_label_frame = tk.Frame(self.entry_frame)
        self.calendar_label_frame.grid(row=1, column=0, sticky=tk.NW, pady=20)

        self.show_calendar_label = tk.Label(self.calendar_label_frame, text="Due Date:")
        self.show_calendar_label.pack(side="right", anchor=tk.N)
        self.show_calendar = tk.BooleanVar(value=False)
        self.calendar_activate = tk.Checkbutton(
            self.calendar_label_frame,
            variable=self.show_calendar,
            command=self.update_calendar,
            cursor="hand2",
        )
        self.calendar_activate.pack(side="left", anchor=tk.N)
        self.calendar = Calendar(self.entry_frame, selectmode="day")
        self.calendar.grid(row=1, column=1, sticky=tk.NW, pady=20)

        self.submit_button = tk.Button(
            self.entry_frame, text=">>", command=self.add_todo, cursor="plus"
        )
        self.submit_button.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=20)

        # todo list

        self.todo_frame: tk.Frame = tk.Frame(self.root)
        self.todo_frame.grid(row=0, column=1, padx=40, sticky=tk.N)

        # page controls

        self.total_page_count = 0
        self._current_page = 0
        self.todos_per_page = 6
        self.page_control_frame = tk.Frame(self.root)
        self.page_control_frame.grid(row=2, column=1, padx=40, pady=40, sticky=tk.W)

        def increment_page():
            self.current_page += 1

        def decrement_page():
            self.current_page -= 1

        self.previous_page_button = tk.Button(
            self.page_control_frame, command=decrement_page, text="<"
        )
        self.previous_page_button.pack(side="left")
        self.page_label = tk.Label(
            self.page_control_frame,
            text=f"Page {self.current_page + 1}/{self.total_page_count + 1}",
        )
        self.page_label.pack(side="left")
        self.next_page_button = tk.Button(
            self.page_control_frame, command=increment_page, text=">"
        )
        self.next_page_button.pack(side="right")

        self.update_calendar()
        self.update_view()
        self.root.mainloop()

    @property
    def current_page(self):
        return self._current_page

    @current_page.setter
    def current_page(self, page):
        if page >= 0 and page <= self.total_page_count and page != self._current_page:
            self._current_page = page
            self.update_view()

    def update_calendar(self):
        if self.show_calendar.get() == tk.TRUE:
            self.calendar.config(state="normal")
            self.show_calendar_label.config(fg="white")
        else:
            self.calendar.config(state="disabled")
            self.show_calendar_label.config(fg="gray")

    def add_todo(self):
        text = self.entry_field.get()
        date_str = self.calendar.get_date()
        date_obj = dt.strptime(date_str, "%m/%d/%y")
        if text != "":
            self.entry_field.delete(0, tk.END)
            if self.show_calendar.get() == tk.TRUE:
                self.todos.append(Todo(text=text, date_due=date_obj))
            else:
                self.todos.append(Todo(text=text))
            self.update_view()

    def remove_todo(self, todo: Todo):
        self.todos.remove(todo)
        self.update_view()

    def update_view(self):
        children = self.todo_frame.winfo_children()

        for child in children:
            child.destroy()

        complete = [todo for todo in self.todos if todo.completed]
        incomplete = [todo for todo in self.todos if not todo.completed]

        complete.sort(
            key=lambda x: x.date_due if x.date_due is not None else x.date_added
        )
        incomplete.sort(
            key=lambda x: x.date_due if x.date_due is not None else x.date_added
        )

        self.todos = incomplete + complete
        self.total_page_count = max(0, (len(self.todos) - 1)) // self.todos_per_page
        self.current_page = max(0, min(self.total_page_count, self.current_page))

        self.page_label.config(
            text=f"Page {self.current_page + 1}/{self.total_page_count + 1}"
        )

        for todo in self.todos[
            self.todos_per_page
            * self.current_page : min(
                self.todos_per_page * (self.current_page + 1),
                len(self.todos),
            )
        ]:
            TodoElement(todo, self)

        if self.total_page_count > 0:
            self.page_control_frame.grid(row=2, column=1, padx=40, sticky=tk.W)
        else:
            self.page_control_frame.grid_remove()


class TodoElement:
    def __init__(self, todo: Todo, parent: TodoApp):
        self.parent = parent

        self.todo = todo

        self.frame = tk.Frame(parent.todo_frame)
        self.frame.pack(pady=10, side="top", anchor=tk.W)

        self.text_frame = tk.Frame(self.frame)
        self.text_frame.pack(side="left", anchor=tk.W)

        self.todo_name = tk.Label(
            self.text_frame, text=self.todo.todo_name, font=("Helvetica", 24, "bold")
        )
        self.todo_name.pack(anchor=tk.W)

        if self.todo.date_due is not None:
            self.todo_date_due = tk.Label(
                self.text_frame,
                text="Due " + self.todo.date_due.strftime("%a %d %b %Y, %I:%M%p"),
            )
            self.todo_date_due.pack(anchor=tk.W)

        self.todo_date_created = tk.Label(
            self.text_frame,
            text="Added " + self.todo.date_added.strftime("%a %d %b %Y, %I:%M%p"),
        )
        self.todo_date_created.pack(anchor=tk.W)

        if self.todo.date_due is not None:
            self.due_text = tk.Label(
                self.text_frame,
                text="Due: " + self.todo.date_due.strftime("%a %d %b %Y"),
            )

        """
        self.todo_date_completed = tk.Label(self.text_frame, text="Completed ")
        self.todo_date_completed.pack_forget()
        """

        self.delete_button: tk.Button = tk.Button(
            self.frame, text="x", command=self.on_delete, cursor="hand2"
        )
        self.delete_button.pack(side="right", anchor=tk.E)

        self.check_variable = tk.BooleanVar(value=self.todo.completed)
        self.checkbox = tk.Checkbutton(
            self.frame,
            variable=self.check_variable,
            command=self.on_toggle,
            cursor="hand2",
        )
        self.checkbox.pack(side="right", anchor=tk.E)

        self.update_view()

    def on_delete(self):
        self.parent.remove_todo(self.todo)

    def on_toggle(self):
        if self.check_variable.get() == tk.TRUE:
            self.todo.completed = True
        else:
            self.todo.completed = False

        self.parent.update_view()

    def update_view(self):
        if self.todo.completed:
            self.todo.date_completed = dt.now()
            self.todo_name.config(fg="gray")
            self.todo_date_created.config(fg="gray")

            if self.todo.date_due is not None:
                self.todo_date_due.config(fg="gray")

            """
            self.todo_date_completed.config(
                text="Completed: "
                + self.todo.date_completed.strftime("%a %d %b %Y, %I:%M%p"),
                fg="gray",
            )
            self.todo_date_completed.pack()
            """

        else:
            self.todo.date_completed = None
            self.todo_name.config(text=self.todo.todo_name, fg="white")
            self.todo_date_created.config(fg="white")
            if self.todo.date_due is not None:
                self.todo_date_due.config(fg="white")

            """
            self.todo_date_completed.pack_forget()
            """


if __name__ == "__main__":
    TodoApp()
