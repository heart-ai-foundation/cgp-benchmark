export function renderItemList(items) {
  return items.map((item) => item.name).join(", ");
}
