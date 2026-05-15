export function submitLogin({ email, password }, authenticate) {
  if (!email) {
    return { ok: false, error: "Email is required" };
  }

  if (password.length < 1) {
    throw new Error("Password is required");
  }

  return authenticate({ email, password });
}
