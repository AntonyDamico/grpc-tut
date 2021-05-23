const grpc = require('grpc');
const protoLoader = require('@grpc/proto-loader')

const text = process.argv[2];
const packageDef = protoLoader.loadSync('todo.proto', {});
const grpcObject = grpc.loadPackageDefinition(packageDef);
const todoPackage = grpcObject.todoPackage;

const client = new todoPackage.Todo(
  'localhost:40000',
  grpc.credentials.createInsecure(),
);


client.createTodo({ text }, (err, response) => {
  console.log('creating')
  console.log(err, response);
});

client.readTodos({}, (err, response) => {
  console.log('reading')
  console.log(err, response)
})
