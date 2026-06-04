// TS 端 Vercel AI SDK 集成 demo
// 运行：npx tsx ts/web_integration.ts
import { openai } from "@ai-sdk/openai";
import { streamText } from "ai";

async function main() {
  const result = await streamText({
    model: openai("gpt-4o-mini"),
    prompt: "用 3 句话介绍 RAG",
  });

  for await (const chunk of result.textStream) {
    process.stdout.write(chunk);
  }
  console.log();
}

main();
