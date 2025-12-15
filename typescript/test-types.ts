import { Client } from './src/client/index.js';

async function test() {
  const client = Client.create({
    baseUrl: "https://api.localhost.render.com:8443",
    token: "test"
  });
  
  const taskRun = await client.workflows.runTask('workflow-sdk/greet', ["Ruben"]);
  
  // This should show the type
  type TaskRunType = typeof taskRun;
}
