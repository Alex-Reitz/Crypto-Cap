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

 
