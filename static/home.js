$('.fa-star').click(function() {
    $(this).toggleClass('fas far');
    id = this.id
    async function addFavorite() { 
      let response = await axios.post(`/api/toggle_favorite`, { 
        id,
      });
      console.log("Got", response);
      return response
    }  
    addFavorite()
  })

  //Check for favorites, on page load, get favorites list, cmc_ids from backend
  //Iterate over list rendered onto page and change class to 'fas far' - dark 
 

 
