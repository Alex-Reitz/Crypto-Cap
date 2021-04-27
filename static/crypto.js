$(document).ready(function() {
    test = $(location).attr('pathname');
    id = test.substring(test.lastIndexOf('/') + 1);
    async function load_crypto_information() { 
      let response = await axios.post(`/api/load_info`, { 
        id
      });
      console.log("Got", response);
      $('#description').append(response.data.description)
      $('#date_added').append(response.data.date_added)
      return response
    } 

    load_crypto_information()
});

