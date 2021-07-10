$('.fa-star').click(function() {
    $(this).toggleClass('fas far');
    id = this.id
    async function toggleFavorite() { 
      let response = await axios.post(`/api/toggle_favorite`, { 
        id,
      });
      return response
    }  
    toggleFavorite()
  })

  //Check for favorites, on page load, get favorites list, cmc_ids from backend
  //Iterate over list rendered onto page and change class to 'fas far' - dark 
 

 
