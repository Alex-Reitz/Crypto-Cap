$('.fa-star').click(function() {
    $(this).toggleClass('fas far');
    id = this.id
    async function addFavorite() { 
      let response = await axios.post(`/api/add_favorite`, { 
        id
      });
      console.log("Got", response);
      return response
    } 
    addFavorite()
  })

   $('.btn-link').click(function(evt){
    console.log(this);
    id = this.id
    async function display_crypto_page(){
      let response = await axios.post(`/api/get_crypto_info`, {
        id
      })
      console.log("Got", response);
      return response
    }
    display_crypto_page()
  })
 
