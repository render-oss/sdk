import { randomUUID } from "node:crypto";
import { flow, StepError } from "@renderinc/sdk/workflows";

interface Order {
  id: string;
  email: string;
  total: number;
}

// Plain functions. A workflow runs them as inline steps, in its own process.
function generateInvoice(orderId: string) {
  console.log(`Generating invoice for ${orderId}`);
  return { id: `inv-${orderId}` };
}

function chargeCard(orderId: string, total: number) {
  console.log(`Charging ${total} for ${orderId}`);
  if (Math.random() < 0.3) {
    throw new Error("card network timeout");
  }
  return { id: `ch-${orderId}` };
}

function sendReceipt(email: string, invoiceId: string) {
  console.log(`Sending receipt for ${invoiceId} to ${email}`);
}

function notifySupport(orderId: string) {
  console.log(`Receipt failed for ${orderId}`);
}

flow({ name: "fulfillOrder" }, async (ctx, order: Order) => {
  // Inline step: retries in-process, and is memoized on replay.
  const charge = await ctx.step("chargeCard", chargeCard, [order.id, order.total], {
    retry: { maxRetries: 3, waitDurationMs: 500 },
  });

  const invoice = await ctx.step("generateInvoice", generateInvoice, [order.id]);

  // Non-deterministic values belong in a step, so a replay sees the same one.
  const receiptId = await ctx.step("receiptId", () => randomUUID());

  try {
    await ctx.step("sendReceipt", sendReceipt, [order.email, invoice.id]);
  } catch (error) {
    // sendReceipt failed, so fall back to notifying support.
    // If the workflow later replays, this step isn't run again: its recorded
    // error is thrown again instead, so the workflow takes this same branch.
    if (!(error instanceof StepError)) throw error;
    await ctx.step("notifySupport", notifySupport, [order.id]);
  }

  return {
    charge: charge.id,
    invoice: invoice.id,
    receiptId,
  };
});

function square(a: number) {
  console.log(`running square for ${a}`);
  return a * a;
}

flow({ name: "sumSquares" }, async (ctx, a: number, b: number) => {
  console.log(`sum the square of ${a} and ${b}`);
  const aa = await ctx.step("square", square, [a]);
  const bb = await ctx.step("square", square, [b]);
  return aa + bb;
});
