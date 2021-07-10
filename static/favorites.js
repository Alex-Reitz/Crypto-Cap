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