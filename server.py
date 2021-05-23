import logging
from concurrent import futures
import time

import grpc

import todo_pb2_grpc
from todo_pb2 import TodoItems, TodoItem

local_db = [
    {'id': 1, 'text': 'this is a test'},
    {'id': 2, 'text': 'this is another test'},
]


class TodoServicer(todo_pb2_grpc.TodoServicer):

    def __init__(self) -> None:
        self.db = local_db

    def readTodos(self, request, context):
        todos = TodoItems()
        for todo in self.db:
            todos.items.append(TodoItem(**todo))
        return todos

    def readTodosStream(self, request, context):
        for todo in self.db:
            time.sleep(0.75)
            yield TodoItem(**todo)

    def createTodo(self, request, context):
        new_todo = {'id': len(self.db) + 1, 'text': request.text}
        self.db.append(new_todo)
        return TodoItem(**new_todo)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServicer_to_server(TodoServicer(), server)
    server.add_insecure_port('[::]:40000')
    server.start()
    print('server started')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
