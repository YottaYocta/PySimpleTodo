import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime as dt


class Todo:
    def __init__(self, text: str, date_due: dt.date = None):
        self.todo_name: str = text
        self.date_added: dt.date = dt.now().date()
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
            self.date_completed = dt.now().date()
        else:
            self.date_completed = None

    def __str__(self) -> str:
        return f"\n*******\nName: {self.todo_name}\nCompleted: {str(self.completed)}"


class TodoApp:
    def __init__(self):
        self.root: tk.Tk = tk.Tk()
        self.root.title("SimpleTodo")
        self.root.geometry("600x600")
        self.todos: List[Todo] = []

        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack()

        self.entry_field = tk.Entry(self.entry_frame)
        self.entry_field.bind("<Return>", lambda x: self.add_todo())
        self.entry_field.pack(side="left")

        self.calendar = Calendar(self.entry_frame, selectmode="day")
        self.calendar.pack()

        self.submit_button = tk.Button(
            self.entry_frame, text=">>", command=self.add_todo
        )
        self.submit_button.pack(side="right")

        self.todo_frame: tk.Frame = tk.Frame(self.root)
        self.todo_frame.pack()

        self.root.mainloop()

    def add_todo(self):
        text = self.entry_field.get()
        date_str = self.calendar.get_date()
        date_obj = dt.strptime(date_str, "%m/%d/%y")
        if text != "":
            self.entry_field.delete(0, tk.END)
            self.todos.append(Todo(text=text, date_due=date_obj))
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

        complete.sort(key=lambda x: x.date_due)
        incomplete.sort(key=lambda x: x.date_due)

        self.todos = incomplete + complete

        for todo in self.todos:
            TodoElement(todo, self)


class TodoElement:
    def __init__(self, todo: Todo, parent: TodoApp):
        self.parent = parent

        self.todo = todo

        self.frame = tk.Frame(parent.todo_frame)
        self.frame.pack()

        self.text_frame = tk.Frame(self.frame)
        self.text_frame.pack(side="left")

        self.todo_name = tk.Label(self.text_frame, text=self.todo.todo_name)
        self.todo_name.pack()

        self.todo_date_due = tk.Label(
            self.text_frame,
            text="Due " + self.todo.date_due.strftime("%a %d %b %Y, %I:%M%p"),
        )
        self.todo_date_due.pack()

        self.todo_date_created = tk.Label(
            self.text_frame,
            text="Added " + self.todo.date_added.strftime("%a %d %b %Y, %I:%M%p"),
        )
        self.todo_date_created.pack()

        if self.todo.date_due is not None:
            self.due_text = tk.Label(
                self.text_frame,
                text="Due: " + self.todo.date_due.strftime("%a %d %b %Y, %I:%M%p"),
            )

        self.todo_date_completed = tk.Label(self.text_frame, text="Completed ")
        self.todo_date_completed.pack_forget()

        self.delete_button: tk.Button = tk.Button(
            self.frame, text="x", command=self.on_delete
        )
        self.delete_button.pack(side="right")

        self.check_variable = tk.BooleanVar(value=self.todo.completed)
        self.checkbox = tk.Checkbutton(
            self.frame, variable=self.check_variable, command=self.on_toggle
        )
        self.checkbox.pack(side="right")

        self.update_view()

    def on_delete(self):
        self.parent.remove_todo(self.todo)

    def on_toggle(self):
        if self.check_variable.get() == 1:
            self.todo.completed = True
        else:
            self.todo.completed = False

        self.parent.update_view()

    def update_view(self):
        if self.todo.completed:
            self.todo.date_completed = dt.now().date()
            self.todo_name.config(fg="gray")
            self.todo_date_created.config(fg="gray")
            self.todo_date_due.config(fg="gray")
            self.todo_date_completed.config(
                text="Completed: "
                + self.todo.date_completed.strftime("%a %d %b %Y, %I:%M%p"),
                fg="gray",
            )
            self.todo_date_completed.pack()

        else:
            self.todo.date_completed = None
            self.todo_name.config(text=self.todo.todo_name, fg="white")
            self.todo_date_created.config(fg="white")
            self.todo_date_due.config(fg="white")

            self.todo_date_completed.pack_forget()


if __name__ == "__main__":
    TodoApp()
