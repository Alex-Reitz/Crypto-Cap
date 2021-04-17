$( document ).ready(function() {
    async function pingAPI(){
        let response = await axios.get("/api/get-data")
    }
    console.log(response);
    return response
});