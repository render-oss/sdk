import { Render } from "./src";

export async function test() {
  const render = new Render({
    baseUrl: "https://api.localhost.render.com:8443",
    token: "test",
  });

  const taskRun = await render.workflows.runTask("workflow-sdk/greet", ["Ruben"]);

  // This should show the type
  const taskRunType = typeof taskRun;
  console.log(taskRunType);
}
