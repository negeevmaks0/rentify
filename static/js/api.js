async function api(url, options={})
{
    return fetch(
        "/api/" + url,
        {
            credentials: "include",
            ...options
        }
    );
}