$(document).ready(function() {
    test = $(location).attr('pathname');
    id = test.substring(test.lastIndexOf('/') + 1);
    async function load_crypto_information() { 
      let response = await axios.post(`/api/load_info`, { 
        id
      });
      console.log("Got", response);
      $("#logo").attr({ "src": response.data.logo });
      $('#description').append(response.data.description)
      $('#date_added').append(response.data.date_added)
      $('#cmc_id').append(response.data.id)
      $('#slug').append(response.data.slug)
      $('#symbol').append(response.data.symbol)
      $('#twitter_username').append(response.data.twitter_username)
      $('#reddit_username').append(response.data.subreddit)
      return response
    } 

    load_crypto_information()
});

