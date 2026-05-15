export function renderUserList(users) {
  return users.map((user) => `${user.name} <${user.email}>`).join("\n");
}
