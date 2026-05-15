export async function getJson(fetcher, url) {
  const response = await fetcher(url);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}
