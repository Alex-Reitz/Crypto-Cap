$('.fa-star').click(function() {
    $(this).toggleClass('fas far');
    id = this.id
    //selected = this.className;
    async function addFavorite() { 
      let response = await axios.post(`/api/toggle_favorite`, { 
        id,
        //selected
      });
      console.log("Got", response);
      return response
    } 
    addFavorite()
  })

 
