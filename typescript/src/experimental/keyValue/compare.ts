import type {
  InstanceConfiguration,
  IPAllowListEntry,
  KeyValueDetail,
  KeyValuePatch,
  MaxmemoryPolicy,
  Plan,
} from "./types";

export function compareInstanceConfiguration(
  desired: InstanceConfiguration,
  current: KeyValueDetail,
): KeyValuePatch | null {
  let newPlan: Plan | undefined;
  if (desired.plan && desired.plan !== current.plan) {
    newPlan = desired.plan;
  }

  let newMaxmemoryPolicy: MaxmemoryPolicy | undefined;
  if (desired.maxmemoryPolicy && desired.maxmemoryPolicy !== current.options.maxmemoryPolicy) {
    newMaxmemoryPolicy = desired.maxmemoryPolicy;
  }

  let newIPAllowList: IPAllowListEntry[] | undefined;
  if (desired.ipAllowList) {
    newIPAllowList = compareIPAllowLists(desired.ipAllowList, current.ipAllowList ?? []);
  }

  if (newPlan || newMaxmemoryPolicy || newIPAllowList) {
    return {
      plan: newPlan,
      maxmemoryPolicy: newMaxmemoryPolicy,
      ipAllowList: newIPAllowList,
    };
  }

  return null;
}

function compareIPAllowLists(
  desired: IPAllowListEntry[],
  current: IPAllowListEntry[],
): IPAllowListEntry[] | undefined {
  if (desired.length !== current.length) {
    return desired;
  }

  const desiredSorted = [...desired].sort(compareIPAllowListEntries);
  const currentSorted = [...current].sort(compareIPAllowListEntries);

  const different = desiredSorted.some(
    (value, index) => compareIPAllowListEntries(value, currentSorted[index]) !== 0,
  );

  if (different) {
    return desiredSorted;
  }

  return undefined;
}

function compareIPAllowListEntries(entryA: IPAllowListEntry, entryB: IPAllowListEntry): number {
  if (entryA.cidrBlock < entryB.cidrBlock) {
    return -1;
  } else if (entryA.cidrBlock > entryB.cidrBlock) {
    return 1;
  } else {
    return 0;
  }
}
