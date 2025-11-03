async function getUsername() {
    const username = await fetch('http://127.0.0.1:5000/getusername')
    return username.text();
}