import tkinter as tk
from datetime import datetime as dt


class Todo:

    def __init__(self, text: str, date_due=None):
        self.text: str = text
        self.date_added: dt.date = dt.now().date()
        self.date_due: dt.date = date_due
        self.date_completed: dt.date = None
        completed: bool = False

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, completed: bool):
        self._completed = completed
        if self._completed:
            date_completed = dt.now().date()
        else:
            date_completed = None


class TodoApp:
    def __init__(self):
        self.root: tk.Tk = tk.Tk()
        self.root.title("SimpleTodo")
        self.root.geometry("400x300")
        self.todos: List[Todo] = []

        self.entry_field = tk.Entry(self.root)
        self.entry_field.pack(side="top")

        self.submit_button = tk.Button(self.root, text=">>", command=self.add_todo)
        self.submit_button.pack(side="top")

        self.todo_frame: tk.Frame = tk.Frame(self.root)
        self.todo_frame.pack(side="bottom")

        self.root.mainloop()

    def add_todo(self):
        text = self.entry_field.get()
        if text != "":
            self.entry_field.delete(0, tk.END)
            self.todos.append(Todo(text=text))
            self.update_view()

    def remove_todo(self, todo: Todo):
        self.todos.remove(todo)
        self.update_view()

    def update_view(self):
        # Get a list of all children widgets
        children = self.todo_frame.winfo_children()

        # Loop through the list and destroy each child widget
        for child in children:
            child.destroy()

        for todo in self.todos:
            new_todo_element = TodoElement(todo, self)


class TodoElement:
    def __init__(self, todo: Todo, parent: TodoApp):
        self.parent = parent

        self.todo = todo

        self.frame = tk.Frame(parent.todo_frame)
        self.frame.pack()

        self.text = tk.Label(self.frame, text=self.todo.text)
        self.text.pack(side="left")

        if self.todo.date_due is not None:
            self.due_text = tk.Label(
                self.frame, text="Due: " + self.todo.date_due.strftime("%M / %D / %Y")
            )

        self.check_variable = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(
            self.frame, variable=self.check_variable, command=self.toggle_todo
        )
        self.checkbox.pack(side="left")

        self.delete_button: tk.Button = tk.Button(
            self.frame, text="x", command=self.on_delete
        )
        self.delete_button.pack()

    def on_delete(self):
        self.parent.remove_todo(self.todo)

    def toggle_todo(self):
        if self.check_variable.get() == 1:
            self.todo.date_completed = dt.now().date()
            self.todo.completed = True
            self.text.config(text="\u0336".join(self.todo.text) + "\u0336", fg="gray")
        else:
            self.todo.date_completed = None
            self.todo.completed = False
            self.text.config(text=self.todo.text, fg="white")


if __name__ == "__main__":
    TodoApp()
