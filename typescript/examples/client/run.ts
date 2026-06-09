import { randomInt } from "node:crypto";
import { Render, ServerError } from "@renderinc/sdk";

async function main() {
  const render = new Render({
    // rnd_ExSecpu1fN8LqpWSVPgSU8728Uoi
    token: "rnd_08YxwXgzPYNwucwTTtUUFNEtdXyz",
    baseUrl: "https://api.staging.render.com",
  });

  setInterval(async () => {
    try {
      // pyworkflows/add_squares
      const result = await render.workflows.runTask("render-workflows-examples/process_numbers", [
        randomInt(100),
        randomInt(100),
      ]);
      console.log("Task completed:", result.status, result.results);
    } catch (error) {
      if (error instanceof ServerError) {
        console.error("server error", error.name, error.message);
      }
      console.error("Error:", error);
      process.exit(1);
    }
  }, 5000);
}

main();
