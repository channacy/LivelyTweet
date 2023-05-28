from app import app, db, Todo

with app.app_context():
    first_todo = Todo(todo_text="Learn Flask")
    db.session.add(first_todo)
    db.session.commit()
    all_todos = Todo.query.all()
    print(all_todos)
    print(all_todos[0].todo_text)