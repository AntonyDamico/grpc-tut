import sys
import logging
import grpc

from todo_pb2 import voidMsg, TodoText

import todo_pb2_grpc


def create_todo(stub):
    todo = TodoText(text=sys.argv[1])
    res = stub.createTodo(todo)
    print(res)


def get_todos(stub):
    todos = stub.readTodos(voidMsg())
    print(todos)


def get_todos_stream(stub):
    todos = stub.readTodosStream(voidMsg())
    for todo in todos:
        print(todo)


def run():
    with grpc.insecure_channel('localhost:40000') as channel:
        stub = todo_pb2_grpc.TodoStub(channel)
        create_todo(stub)
        # get_todos(stub)
        get_todos_stream(stub)

if __name__ == '__main__':
    logging.basicConfig()
    run()
