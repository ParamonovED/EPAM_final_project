 new Vue({
      el: '#table',
      data: {
          targets: null
      },
      mounted () {
        axios
          .get('http://127.0.0.1:8000/avito_spy/target/')
          .then(response => (this.targets = response.data))
      }
    })
